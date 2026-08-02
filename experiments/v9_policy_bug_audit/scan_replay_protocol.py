#!/usr/bin/env python3
"""Summarize count and Energy-choice protocol menus in saved raw replays."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DECK = [int(line) for line in (ROOT / "experiments/v9_discard_only/deck.csv").read_text().splitlines() if line]


def submitted_deck(steps: list, player: int) -> list[int] | None:
    for step in steps[:4]:
        action = step[player].get("action")
        if isinstance(action, list) and len(action) == 60 and all(isinstance(card, int) for card in action):
            return action
    return None


def selected_options(steps: list, step_index: int, player: int, options: list[dict]) -> list[dict]:
    if step_index + 1 >= len(steps):
        return []
    action = steps[step_index + 1][player].get("action") or []
    return [options[index] for index in action if isinstance(index, int) and 0 <= index < len(options)]


def main() -> None:
    paths: dict[int, Path] = {}
    for path in sorted((ROOT / "scouting_replays").rglob("*.json")):
        if not path.stem.isdigit():
            continue
        with path.open(encoding="utf-8") as handle:
            replay = json.load(handle)
        episode = int((replay.get("info") or {}).get("EpisodeId", path.stem))
        paths.setdefault(episode, path)

    draw_menus = 0
    draw_order: Counter[tuple[int, ...]] = Counter()
    draw_chosen: Counter[int] = Counter()
    draw_max_chosen = 0
    exact_deck_draw_menus = 0
    exact_deck_draw_chosen: Counter[int] = Counter()
    exact_deck_draw_max_chosen = 0
    retreat_menus = 0
    retreat_first_index = 0
    retreat_multi = 0
    context_card_presence: Counter[tuple[int, bool]] = Counter()

    for episode, path in paths.items():
        del episode
        with path.open(encoding="utf-8") as handle:
            replay = json.load(handle)
        steps = replay.get("steps") or []
        decks = [submitted_deck(steps, player) for player in (0, 1)]
        for step_index, step in enumerate(steps[:-1]):
            for player in (0, 1):
                observation = step[player].get("observation") or {}
                select = observation.get("select") or {}
                context = select.get("context")
                options = select.get("option") or []
                if context in (21, 22):
                    context_card_presence[(context, isinstance(select.get("contextCard"), dict))] += 1
                if context == 38:
                    numbers = tuple(int(option.get("number", 0)) for option in options)
                    chosen = selected_options(steps, step_index, player, options)
                    chosen_number = int(chosen[0].get("number", 0)) if chosen else -1
                    draw_menus += 1
                    draw_order[numbers] += 1
                    draw_chosen[chosen_number] += 1
                    draw_max_chosen += int(bool(numbers) and chosen_number == max(numbers))
                    if decks[player] == DECK:
                        exact_deck_draw_menus += 1
                        exact_deck_draw_chosen[chosen_number] += 1
                        exact_deck_draw_max_chosen += int(bool(numbers) and chosen_number == max(numbers))
                elif context == 30:
                    chosen = selected_options(steps, step_index, player, options)
                    retreat_menus += 1
                    retreat_multi += int(len(options) > 1)
                    retreat_first_index += int(
                        bool(chosen) and chosen[0].get("energyIndex") == options[0].get("energyIndex")
                    )

    print(
        json.dumps(
            {
                "unique_replays": len(paths),
                "draw_count": {
                    "menus": draw_menus,
                    "option_order": {str(key): value for key, value in draw_order.items()},
                    "chosen_numbers": dict(draw_chosen),
                    "maximum_chosen": draw_max_chosen,
                    "exact_deck_menus": exact_deck_draw_menus,
                    "exact_deck_chosen_numbers": dict(exact_deck_draw_chosen),
                    "exact_deck_maximum_chosen": exact_deck_draw_max_chosen,
                },
                "retreat_energy": {
                    "menus": retreat_menus,
                    "multi_option_menus": retreat_multi,
                    "first_energy_index_chosen": retreat_first_index,
                },
                "context_card_presence": {
                    str(key): value for key, value in context_card_presence.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
