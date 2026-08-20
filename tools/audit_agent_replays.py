#!/usr/bin/env python3
"""Re-run an agent against recorded active observations from Kaggle replays.

This is an exact policy audit, not a counterfactual battle simulation. Kaggle
stores an active observation on one global row and the corresponding action on
the following row for that same player. The audit preserves that pairing,
loads a fresh module for every episode, validates every returned selection,
and reports exact action reproduction plus attack-turn conversion.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_module(source: Path, tag: str):
    spec = importlib.util.spec_from_file_location(tag, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_deck(path: Path) -> list[int]:
    cards = [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(cards) != 60:
        raise ValueError(f"{path} contains {len(cards)} cards; expected 60")
    return cards


def replay_paths(inputs: list[Path]) -> list[Path]:
    paths: set[Path] = set()
    for item in inputs:
        if item.is_dir():
            paths.update(
                path.resolve()
                for path in item.rglob("*.json")
                if path.name != "corpus_summary.json"
            )
        else:
            paths.add(item.resolve())
    return sorted(paths)


def replay_deck(replay: dict[str, Any], player: int) -> list[int]:
    steps = replay.get("steps") or []
    if len(steps) < 2:
        return []
    action = steps[1][player].get("action")
    return action if isinstance(action, list) and len(action) == 60 else []


def player_for_agent(
    replay: dict[str, Any], expected_deck: list[int], aliases: set[str]
) -> int:
    names = replay.get("info", {}).get("TeamNames") or []
    alias_seats = [index for index, name in enumerate(names) if name in aliases]
    deck_seats = [
        player for player in (0, 1) if replay_deck(replay, player) == expected_deck
    ]
    candidates = [seat for seat in alias_seats if seat in deck_seats]
    if candidates:
        # Self-play replays can legitimately have the same alias and exact
        # deck in both seats. Auditing either seat is sufficient to validate
        # the submitted policy, so use the first deterministically.
        return candidates[0]
    if deck_seats:
        return deck_seats[0]
    if alias_seats:
        return alias_seats[0]
    raise ValueError(
        f"unable to identify agent seat; aliases={alias_seats}, decks={deck_seats}"
    )


def validate_action(obs: dict[str, Any], action: Any) -> str | None:
    if not isinstance(action, list):
        return f"returned {type(action).__name__}, expected list"
    select = obs.get("select")
    if select is None:
        if len(action) != 60:
            return f"startup returned {len(action)} cards"
        return None
    options = select.get("option") or []
    minimum = int(select.get("minCount") or 0)
    maximum = int(select.get("maxCount") or 0)
    if not minimum <= len(action) <= maximum:
        return f"selected {len(action)} options; expected {minimum}..{maximum}"
    if len(action) != len(set(action)):
        return "returned duplicate option indexes"
    if any(not isinstance(index, int) or not 0 <= index < len(options) for index in action):
        return "returned an out-of-range option index"
    return None


def active_decisions(replay: dict[str, Any], player: int):
    steps = replay.get("steps") or []
    for step_index in range(len(steps) - 1):
        if player >= len(steps[step_index]) or player >= len(steps[step_index + 1]):
            continue
        row = steps[step_index][player]
        if row.get("status") != "ACTIVE":
            continue
        obs = row.get("observation") or {}
        recorded = steps[step_index + 1][player].get("action")
        if isinstance(recorded, list):
            yield step_index, obs, recorded


def audit_replay(
    path: Path,
    source: Path,
    expected_deck: list[int],
    aliases: set[str],
) -> dict[str, Any]:
    replay = json.loads(path.read_text(encoding="utf-8"))
    episode = int(replay.get("info", {}).get("EpisodeId") or path.stem)
    player = player_for_agent(replay, expected_deck, aliases)
    module = load_module(source, f"audit_agent_{episode}")
    decision_module = load_module(source, f"audit_choose_{episode}")
    exact = invalid = exceptions = 0
    mismatches: list[dict[str, Any]] = []
    offered_attack_turns: set[int] = set()
    attacked_turns: set[int] = set()
    decisions = 0

    for step_index, obs, recorded in active_decisions(replay, player):
        decisions += 1
        turn = int((obs.get("current") or {}).get("turn") or 0)
        select = obs.get("select") or {}
        options = select.get("option") or []
        if any(option.get("type") == 13 for option in options):
            offered_attack_turns.add(turn)
        if any(
            isinstance(index, int)
            and 0 <= index < len(options)
            and options[index].get("type") == 13
            for index in recorded
        ):
            attacked_turns.add(turn)

        try:
            action = module.agent(obs)
        except Exception as exc:  # pragma: no cover - diagnostic path
            exceptions += 1
            action = None
            mismatches.append(
                {"step": step_index, "turn": turn, "exception": repr(exc)}
            )
        issue = validate_action(obs, action)
        if issue:
            invalid += 1
        if action == recorded:
            exact += 1
        elif len(mismatches) < 20:
            mismatches.append(
                {
                    "step": step_index,
                    "turn": turn,
                    "recorded": recorded,
                    "predicted": action,
                    "invalid": issue,
                }
            )

        choose = getattr(decision_module, "choose_action", None)
        if choose is not None:
            try:
                choose(obs)
            except Exception as exc:  # pragma: no cover - diagnostic path
                exceptions += 1
                if len(mismatches) < 20:
                    mismatches.append(
                        {
                            "step": step_index,
                            "turn": turn,
                            "choose_exception": repr(exc),
                        }
                    )

    rewards = replay.get("rewards") or [None, None]
    return {
        "episode": episode,
        "path": str(path),
        "player": player,
        "reward": rewards[player] if player < len(rewards) else None,
        "decisions": decisions,
        "exact": exact,
        "mismatches": decisions - exact,
        "invalid": invalid,
        "exceptions": exceptions,
        "attack_turns": len(offered_attack_turns),
        "attacked_turns": len(attacked_turns),
        "abandoned_attack_turns": len(offered_attack_turns - attacked_turns),
        "details": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-dir", type=Path, required=True)
    parser.add_argument("--replays", type=Path, nargs="+", required=True)
    parser.add_argument(
        "--alias", action="append", default=["ROASTERS", "MUHAMMAD UMER FAROOQ"]
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    agent_dir = args.agent_dir.resolve()
    source = agent_dir / "main.py"
    expected_deck = read_deck(agent_dir / "deck.csv")
    rows = [
        audit_replay(path, source, expected_deck, set(args.alias))
        for path in replay_paths(args.replays)
    ]
    totals = Counter()
    for row in rows:
        for key in (
            "decisions",
            "exact",
            "mismatches",
            "invalid",
            "exceptions",
            "attack_turns",
            "attacked_turns",
            "abandoned_attack_turns",
        ):
            totals[key] += int(row[key])
    totals["wins"] = sum(row["reward"] == 1 for row in rows)
    totals["losses"] = sum(row["reward"] == -1 for row in rows)
    report = {"agent": str(agent_dir), "episodes": len(rows), "totals": dict(totals), "rows": rows}
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"episodes": len(rows), **dict(totals)}, indent=2))
    for row in rows:
        if row["mismatches"] or row["invalid"] or row["exceptions"]:
            print(
                f"{row['episode']}: exact {row['exact']}/{row['decisions']}, "
                f"invalid={row['invalid']}, exceptions={row['exceptions']}"
            )
    return 1 if totals["invalid"] or totals["exceptions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
