#!/usr/bin/env python3
"""Inspect selection-menu shapes reached by the candidate in local games."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start  # noqa: E402


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_deck(path: Path) -> list[int]:
    return [int(line.strip().split(",")[0]) for line in path.read_text().splitlines() if line.strip()]


def card_id(card):
    return card.get("id") if isinstance(card, dict) else None


def summarize(obs: dict, action: list[int], previous: dict | None) -> dict:
    select = obs.get("select") or {}
    current = obs.get("current") or {}
    options = select.get("option") or []
    summary = {
        "turn": current.get("turn"),
        "your_index": current.get("yourIndex"),
        "context": select.get("context"),
        "select_type": select.get("type"),
        "min_count": select.get("minCount"),
        "max_count": select.get("maxCount"),
        "effect_id": card_id(select.get("effect")),
        "context_card": select.get("contextCard"),
        "chosen": action,
        "options": options,
        "players": current.get("players"),
        "looking": current.get("looking"),
        "logs": obs.get("logs"),
    }
    if previous is not None:
        pselect = previous["obs"].get("select") or {}
        summary["previous"] = {
            "context": pselect.get("context"),
            "effect_id": card_id(pselect.get("effect")),
            "chosen": previous["action"],
            "chosen_options": [
                (pselect.get("option") or [])[index]
                for index in previous["action"]
                if 0 <= index < len(pselect.get("option") or [])
            ],
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=int, default=100)
    parser.add_argument("--max-examples", type=int, default=20)
    args = parser.parse_args()

    candidate_dir = Path(__file__).resolve().parent
    opponent_dir = ROOT / "agents" / "v7_candidate"
    modules = [
        load_module(candidate_dir / "main.py", "audit_candidate"),
        load_module(opponent_dir / "main.py", "audit_opponent"),
    ]
    decks = [read_deck(candidate_dir / "deck.csv"), read_deck(opponent_dir / "deck.csv")]
    context_counts: Counter[tuple] = Counter()
    option_shapes: dict[tuple, Counter] = defaultdict(Counter)
    examples: list[dict] = []

    for match in range(args.matches):
        obs, start = battle_start(decks[0], decks[1])
        if obs is None:
            raise RuntimeError((start.errorPlayer, start.errorType))
        previous_by_player: dict[int, dict] = {}
        try:
            for _ in range(5000):
                current = obs.get("current") or {}
                player = current.get("yourIndex")
                select = obs.get("select") or {}
                action = modules[player].agent(obs)
                effect = card_id(select.get("effect"))
                key = (player, select.get("context"), select.get("type"), effect)
                context_counts[key] += 1
                for option in select.get("option") or []:
                    option_shapes[key][tuple(sorted(option))] += 1
                if player == 0 and select.get("context") in {21, 22, 26, 27, 28, 29, 30, 31, 32, 33, 34, 38, 39, 40, 41, 43}:
                    if len(examples) < args.max_examples:
                        examples.append(summarize(obs, action, previous_by_player.get(player)))
                previous_by_player[player] = {"obs": obs, "action": action}
                obs = battle_select(action)
                if (obs.get("current") or {}).get("result", -1) != -1:
                    break
            else:
                raise TimeoutError("local game exceeded 5000 decisions")
        finally:
            battle_finish()

    payload = {
        "matches": args.matches,
        "contexts": [
            {
                "player": key[0],
                "context": key[1],
                "select_type": key[2],
                "effect_id": key[3],
                "count": count,
                "option_shapes": [
                    {"fields": list(fields), "count": shape_count}
                    for fields, shape_count in option_shapes[key].most_common()
                ],
            }
            for key, count in sorted(context_counts.items(), key=lambda item: str(item[0]))
        ],
        "examples": examples,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
