#!/usr/bin/env python3
"""Train a compact action-ranking policy from public replay decisions."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from analyze_replay_corpus import DEFAULT_CORPUS, load_unique_replays


ROOT = Path(__file__).resolve().parents[1]


def card_at(state: dict, player: int, area: int, index: int, select: dict) -> int | None:
    if area == 1:
        cards = select.get("deck") or []
    elif area == 2:
        players = state.get("players") or []
        cards = (players[player].get("hand") or []) if player < len(players) else []
    elif area == 3:
        players = state.get("players") or []
        cards = (players[player].get("discard") or []) if player < len(players) else []
    elif area == 4:
        players = state.get("players") or []
        cards = (players[player].get("active") or []) if player < len(players) else []
    elif area == 5:
        players = state.get("players") or []
        cards = (players[player].get("bench") or []) if player < len(players) else []
    elif area == 12:
        cards = state.get("looking") or []
    else:
        cards = []
    if not isinstance(index, int) or not 0 <= index < len(cards):
        return None
    card = cards[index]
    return card.get("id") if isinstance(card, dict) else None


def option_features(obs: dict, option: dict) -> list[str]:
    select = obs.get("select") or {}
    state = obs.get("current") or {}
    context = select.get("context")
    option_type = option.get("type")
    your_index = state.get("yourIndex", 0)
    owner = option.get("playerIndex", your_index)
    features = [
        f"type:{option_type}",
        f"context:{context}:type:{option_type}",
    ]

    area = option.get("area")
    index = option.get("index")
    if area is None and option_type == 7:
        area = 2
    if isinstance(area, int) and isinstance(index, int):
        card_id = card_at(state, owner, area, index, select)
        if card_id is not None:
            features.append(f"card:{card_id}")
            features.append(f"context:{context}:card:{card_id}")

    in_play_area = option.get("inPlayArea")
    in_play_index = option.get("inPlayIndex")
    if isinstance(in_play_area, int) and isinstance(in_play_index, int):
        target_owner = option.get("playerIndex", your_index)
        target_id = card_at(state, target_owner, in_play_area, in_play_index, select)
        if target_id is not None:
            features.append(f"target:{target_id}")
            features.append(f"context:{context}:target:{target_id}")

    attack_id = option.get("attackId")
    if attack_id is not None:
        features.append(f"attack:{attack_id}")
    card_id = option.get("cardId")
    if card_id is not None:
        features.append(f"skill-card:{card_id}")
    if owner == your_index:
        features.append("owner:self")
    elif option.get("playerIndex") is not None:
        features.append("owner:opponent")
    return features


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("agent_name")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    unique, _ = load_unique_replays(args.corpus)
    available = Counter()
    expected = Counter()
    selected = Counter()
    deck_counts = Counter()
    decisions = 0

    for _, (_, replay) in unique.items():
        agents = replay.get("info", {}).get("Agents") or []
        names = [agent.get("Name") for agent in agents]
        for player, name in enumerate(names):
            if name != args.agent_name:
                continue
            steps = replay.get("steps") or []
            if len(steps) > 1:
                deck = steps[1][player].get("action")
                if isinstance(deck, list) and len(deck) == 60:
                    deck_counts[tuple(deck)] += 1
            for step_index in range(1, len(steps)):
                action = steps[step_index][player].get("action")
                obs = steps[step_index - 1][player].get("observation") or {}
                options = (obs.get("select") or {}).get("option") or []
                if not isinstance(action, list) or not action or not options:
                    continue
                chosen = {index for index in action if isinstance(index, int)}
                chosen = {index for index in chosen if 0 <= index < len(options)}
                if not chosen:
                    continue
                decisions += 1
                expected_rate = len(chosen) / len(options)
                for option_index, option in enumerate(options):
                    features = option_features(obs, option)
                    for feature in features:
                        available[feature] += 1
                        expected[feature] += expected_rate
                        if option_index in chosen:
                            selected[feature] += 1

    if not deck_counts:
        raise SystemExit(f"No 60-card deck found for {args.agent_name}")

    weights = {}
    for feature, total in available.items():
        picked = selected[feature]
        support = min(1.0, total / 12.0)
        weights[feature] = round(
            math.log((picked + 1.0) / (expected[feature] + 1.0)) * support,
            5,
        )

    deck = list(deck_counts.most_common(1)[0][0])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "policy.json").write_text(
        json.dumps(
            {
                "source_agent": args.agent_name,
                "decisions": decisions,
                "episodes": sum(deck_counts.values()),
                "weights": weights,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    (args.output_dir / "deck.csv").write_text("\n".join(map(str, deck)) + "\n")
    print(f"episodes: {sum(deck_counts.values())}")
    print(f"decisions: {decisions}")
    print(f"features: {len(weights)}")
    print(f"output: {args.output_dir}")


if __name__ == "__main__":
    main()
