#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start  # noqa: E402


def load_agent(agent_dir: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, agent_dir / "main.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(agent_dir)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def read_deck(path: Path) -> list[int]:
    cards = [int(line.strip().split(",")[0]) for line in path.read_text().splitlines() if line.strip()]
    if len(cards) != 60:
        raise ValueError(f"{path} has {len(cards)} cards")
    return cards


def write_deck(path: Path, deck: tuple[int, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(str(card) for card in deck) + "\n")


def safe_name(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")
    return text[:80] or "deck"


def extract_decks(limit: int | None = None) -> list[dict]:
    seen: dict[tuple[int, ...], dict] = {}
    for path in sorted((ROOT / "scouting_replays").glob("**/*.json")):
        if path.name == "corpus_summary.json":
            continue
        try:
            replay = json.loads(path.read_text())
        except Exception:
            continue
        teams = (replay.get("info") or {}).get("TeamNames") or []
        for player in (0, 1):
            deck = None
            for step in replay.get("steps") or []:
                if player >= len(step):
                    continue
                action = step[player].get("action")
                if isinstance(action, list) and len(action) == 60:
                    deck = tuple(int(card) for card in action)
                    break
            if deck is None:
                continue
            rec = seen.setdefault(
                deck,
                {
                    "deck": deck,
                    "count": 0,
                    "teams": Counter(),
                    "examples": [],
                },
            )
            rec["count"] += 1
            if player < len(teams):
                rec["teams"][teams[player]] += 1
            if len(rec["examples"]) < 5:
                rec["examples"].append(path.stem)
    decks = sorted(seen.values(), key=lambda rec: (-rec["count"], rec["teams"].most_common(1)[0][0] if rec["teams"] else ""))
    return decks[:limit] if limit else decks


def random_agent(obs: dict) -> list[int]:
    select = obs["select"]
    return random.sample(range(len(select["option"])), select["maxCount"])


def run_one(primary_agent, opponent_agent, primary_deck, opponent_deck, primary_seat: int, max_decisions: int):
    agents = (primary_agent, opponent_agent) if primary_seat == 0 else (opponent_agent, primary_agent)
    decks = (primary_deck, opponent_deck) if primary_seat == 0 else (opponent_deck, primary_deck)
    obs, start = battle_start(decks[0], decks[1])
    if obs is None:
        raise RuntimeError(f"Battle failed: player={start.errorPlayer} error={start.errorType}")
    stats = {
        "attacks": 0,
        "attack_menus": 0,
        "missed_attack_menus": 0,
        "first_attack_turn": None,
        "decisions": 0,
        "attack_turns": 0,
        "attacked_turns": 0,
        "abandoned_attack_turns": 0,
        "timed_out": 0,
    }
    offered_attack_turns = set()
    attacked_turns = set()

    def finalized_stats():
        stats["attack_turns"] = len(offered_attack_turns)
        stats["attacked_turns"] = len(attacked_turns)
        stats["abandoned_attack_turns"] = len(offered_attack_turns - attacked_turns)
        return stats
    try:
        for _ in range(max_decisions):
            current = obs.get("current") or {}
            select = obs.get("select") or {}
            options = select.get("option") or []
            player_index = current.get("yourIndex")
            action = agents[player_index](obs)
            if player_index == primary_seat and options:
                stats["decisions"] += 1
                attack_indexes = [i for i, option in enumerate(options) if option.get("type") == 13]
                if attack_indexes:
                    stats["attack_menus"] += 1
                    offered_attack_turns.add(current.get("turn"))
                    if any(i in attack_indexes for i in action):
                        stats["attacks"] += 1
                        attacked_turns.add(current.get("turn"))
                        if stats["first_attack_turn"] is None:
                            stats["first_attack_turn"] = current.get("turn")
                    else:
                        stats["missed_attack_menus"] += 1
            obs = battle_select(action)
            current = obs.get("current") or {}
            if current.get("result", -1) != -1:
                return current["result"], current.get("turn", 0), finalized_stats()
    finally:
        battle_finish()
    stats["timed_out"] = 1
    return None, 0, finalized_stats()


def evaluate(
    name: str,
    opponent_deck: list[int],
    matches: int,
    max_decisions: int,
    opponent_agent_name: str,
    primary_agent_dir: Path,
    primary_deck_path: Path,
):
    primary_agent = load_agent(primary_agent_dir, "primary_eval")
    primary_deck = read_deck(primary_deck_path)
    if opponent_agent_name == "generic":
        opponent_agent = load_agent(ROOT / "agents" / "generic_attack_first", f"generic_{safe_name(name)}")
    elif opponent_agent_name == "random":
        opponent_agent = random_agent
    else:
        opponent_agent = load_agent(ROOT / "agents" / opponent_agent_name, f"opp_{safe_name(name)}")

    wins = losses = draws = 0
    attack_menus = attacks = missed = decisions = 0
    attack_turns = attacked_turns = abandoned_attack_turns = timeouts = 0
    first_turns = []
    for match in range(matches):
        seat = 1 if match % 2 else 0
        winner, turns, stats = run_one(primary_agent, opponent_agent, primary_deck, opponent_deck, seat, max_decisions)
        if winner == seat:
            wins += 1
        elif winner in (0, 1):
            losses += 1
        else:
            draws += 1
        attack_menus += stats["attack_menus"]
        attacks += stats["attacks"]
        missed += stats["missed_attack_menus"]
        decisions += stats["decisions"]
        attack_turns += stats["attack_turns"]
        attacked_turns += stats["attacked_turns"]
        abandoned_attack_turns += stats["abandoned_attack_turns"]
        timeouts += stats["timed_out"]
        if stats["first_attack_turn"] is not None:
            first_turns.append(stats["first_attack_turn"])
    avg_first = round(sum(first_turns) / len(first_turns), 2) if first_turns else None
    return {
        "name": name,
        "matches": matches,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": round(wins / matches, 3),
        "decisions": decisions,
        "attack_menus": attack_menus,
        "attacks": attacks,
        "missed_attack_menus": missed,
        "attack_turns": attack_turns,
        "attacked_turns": attacked_turns,
        "abandoned_attack_turns": abandoned_attack_turns,
        "timeouts": timeouts,
        "avg_first_attack_turn": avg_first,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=int, default=20)
    parser.add_argument("--max-decisions", type=int, default=5000)
    parser.add_argument("--limit-decks", type=int)
    parser.add_argument("--opponent-agent", default="generic", choices=["generic", "random", "v1_active", "v2_challenger", "v3_planner", "v4_attackfix"])
    parser.add_argument("--primary-agent-dir", type=Path, default=ROOT / "agents" / "v4_attackfix")
    parser.add_argument("--primary-deck", type=Path, default=ROOT / "agents" / "v4_attackfix" / "deck.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "v4_matrix_results.csv")
    args = parser.parse_args()

    rows = []
    deck_dir = ROOT / "tools" / "evaluation_decks"
    for index, rec in enumerate(extract_decks(args.limit_decks), 1):
        team = rec["teams"].most_common(1)[0][0] if rec["teams"] else "unknown"
        label = f"{index:02d}_{safe_name(team)}_{rec['examples'][0]}"
        deck_path = deck_dir / f"{label}.csv"
        write_deck(deck_path, rec["deck"])
        row = evaluate(
            label,
            list(rec["deck"]),
            args.matches,
            args.max_decisions,
            args.opponent_agent,
            args.primary_agent_dir.resolve(),
            args.primary_deck.resolve(),
        )
        row["deck_count"] = rec["count"]
        row["top_team"] = team
        row["examples"] = " ".join(rec["examples"])
        rows.append(row)
        print(row, flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)


if __name__ == "__main__":
    main()
