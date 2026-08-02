#!/usr/bin/env python3
"""Run the submitted agent in the official local battle simulator."""

from __future__ import annotations

import argparse
import importlib.util
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start  # noqa: E402


def load_agent(agent_dir: Path, module_name: str):
    source = agent_dir / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def read_deck(path: Path) -> list[int]:
    deck = [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(deck) != 60:
        raise ValueError(f"{path} contains {len(deck)} cards; expected 60")
    return deck


def random_agent(obs: dict) -> list[int]:
    select = obs["select"]
    return random.sample(range(len(select["option"])), select["maxCount"])


def run_match(agents, decks, max_decisions: int) -> tuple[int, int, int]:
    obs, start = battle_start(decks[0], decks[1])
    if obs is None:
        raise RuntimeError(
            f"Battle failed to start: player={start.errorPlayer}, error={start.errorType}"
        )

    try:
        for decisions in range(1, max_decisions + 1):
            select = obs.get("select")
            if select is None:
                raise RuntimeError("Simulator requested a deck after battle start")
            player_index = (obs.get("current") or {}).get("yourIndex")
            if player_index not in (0, 1):
                raise RuntimeError(f"Invalid selecting player: {player_index}")
            selection = agents[player_index](obs)
            if not isinstance(selection, list):
                raise TypeError(f"Agent returned {type(selection).__name__}, expected list")
            if len(selection) < select["minCount"] or len(selection) > select["maxCount"]:
                raise ValueError(
                    f"Invalid selection length {len(selection)}; expected "
                    f"{select['minCount']}..{select['maxCount']}"
                )
            if len(selection) != len(set(selection)):
                raise ValueError("Agent returned duplicate option indexes")
            if any(index < 0 or index >= len(select["option"]) for index in selection):
                raise IndexError("Agent returned an out-of-range option index")

            obs = battle_select(selection)
            current = obs.get("current") or {}
            if current.get("result", -1) != -1:
                return current["result"], current.get("turn", 0), decisions
    finally:
        battle_finish()

    raise TimeoutError(f"Battle exceeded {max_decisions} decisions")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=int, default=10)
    parser.add_argument("--max-decisions", type=int, default=5000)
    parser.add_argument("--agent-dir", type=Path, default=ROOT)
    parser.add_argument("--agent-deck", type=Path)
    parser.add_argument("--opponent-dir", type=Path)
    parser.add_argument("--opponent-deck", type=Path)
    parser.add_argument("--opponent", choices=("agent", "self", "random"), default="self")
    parser.add_argument(
        "--swap-seats",
        action="store_true",
        help="Alternate which seat uses the primary agent.",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.matches < 1:
        parser.error("--matches must be positive")
    if args.max_decisions < 1:
        parser.error("--max-decisions must be positive")

    agent_dir = args.agent_dir.resolve()
    agent = load_agent(agent_dir, "primary_agent")
    deck = read_deck((args.agent_deck or agent_dir / "deck.csv").resolve())
    if args.opponent == "random":
        opponent = random_agent
        opponent_deck = read_deck(
            (args.opponent_deck or SAMPLE_DIR / "deck.csv").resolve()
        )
    elif args.opponent == "agent":
        if args.opponent_dir is None:
            parser.error("--opponent agent requires --opponent-dir")
        opponent_dir = args.opponent_dir.resolve()
        opponent = load_agent(opponent_dir, "opponent_agent")
        opponent_deck = read_deck(
            (args.opponent_deck or opponent_dir / "deck.csv").resolve()
        )
    else:
        # Load an independent module instance. Several policies keep bounded
        # per-game memory; sharing one module between both seats corrupts a
        # nominal self-play comparison.
        opponent = load_agent(agent_dir, "self_opponent_agent")
        opponent_deck = deck
    primary_wins = 0
    opponent_wins = 0
    draws = 0
    seat_records = {
        0: {"wins": 0, "losses": 0, "draws": 0},
        1: {"wins": 0, "losses": 0, "draws": 0},
    }

    for match_number in range(1, args.matches + 1):
        primary_seat = 1 if args.swap_seats and match_number % 2 == 0 else 0
        if primary_seat == 0:
            match_agents = (agent, opponent)
            match_decks = (deck, opponent_deck)
        else:
            match_agents = (opponent, agent)
            match_decks = (opponent_deck, deck)
        result, turns, decisions = run_match(
            match_agents, match_decks, args.max_decisions
        )
        if result == primary_seat:
            primary_wins += 1
            seat_records[primary_seat]["wins"] += 1
        elif result in (0, 1):
            opponent_wins += 1
            seat_records[primary_seat]["losses"] += 1
        else:
            draws += 1
            seat_records[primary_seat]["draws"] += 1
        if not args.quiet:
            print(
                f"match={match_number} primary_seat={primary_seat} winner={result} "
                f"turns={turns} decisions={decisions}",
                flush=True,
            )

    print(
        f"summary primary={primary_wins} opponent={opponent_wins} draws={draws} "
        f"seat0={seat_records[0]['wins']}-{seat_records[0]['losses']}"
        f"-{seat_records[0]['draws']} "
        f"seat1={seat_records[1]['wins']}-{seat_records[1]['losses']}"
        f"-{seat_records[1]['draws']}"
    )


if __name__ == "__main__":
    main()
