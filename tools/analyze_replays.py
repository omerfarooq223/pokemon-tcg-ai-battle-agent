import argparse
import json
from collections import Counter
from pathlib import Path


def deck_from_step(replay, player):
    try:
        deck = replay["steps"][1][player]["action"]
    except (KeyError, IndexError, TypeError):
        return []
    return deck if isinstance(deck, list) else []


def option_type_counts(replay):
    counts = Counter()
    decisions = 0
    for step in replay.get("steps", []):
        for player in step:
            obs = player.get("observation") or {}
            select = obs.get("select") or {}
            options = select.get("option") or []
            if options:
                decisions += 1
            for option in options:
                counts[option.get("type")] += 1
    return decisions, counts


def main():
    parser = argparse.ArgumentParser(description="Inspect one or more Kaggle replay JSON files.")
    parser.add_argument("replays", nargs="+", type=Path)
    args = parser.parse_args()

    for path in args.replays:
        replay = json.loads(path.read_text())
        print(f"\n{path.name}")
        print(f"  rewards: {replay.get('rewards')}")
        print(f"  steps: {len(replay.get('steps', []))}")
        for player in (0, 1):
            deck = deck_from_step(replay, player)
            print(f"  player {player} deck cards: {len(deck)} unique: {len(set(deck))}")
            print(f"  player {player} deck: {deck}")
        decisions, counts = option_type_counts(replay)
        print(f"  decision menus: {decisions}")
        print(f"  option types: {dict(sorted(counts.items(), key=lambda x: str(x[0])))}")


if __name__ == "__main__":
    main()
