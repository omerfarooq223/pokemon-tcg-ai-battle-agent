#!/usr/bin/env python3
"""Summarize a directory of Kaggle PTCG replay JSON files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "scouting_replays"
CARD_CSV = ROOT / "competition_data" / "EN_Card_Data.csv"


def load_card_names() -> dict[int, str]:
    with CARD_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return {
            int(row["Card ID"]): row["Card Name"]
            for row in csv.DictReader(handle)
        }


def replay_files(corpus: Path) -> list[Path]:
    return sorted(
        path
        for path in corpus.rglob("*.json")
        if path.name not in {"corpus_summary.json"}
    )


def load_unique_replays(corpus: Path) -> tuple[dict[int, tuple[Path, dict]], int]:
    unique: dict[int, tuple[Path, dict]] = {}
    duplicates = 0
    for path in replay_files(corpus):
        replay = json.loads(path.read_text())
        episode_id = int(replay.get("info", {}).get("EpisodeId") or path.stem)
        if episode_id in unique:
            duplicates += 1
            continue
        unique[episode_id] = (path, replay)
    return unique, duplicates


def deck_from_replay(replay: dict, player: int) -> list[int]:
    steps = replay.get("steps") or []
    if len(steps) < 2:
        return []
    action = steps[1][player].get("action")
    return action if isinstance(action, list) and len(action) == 60 else []


def selected_option_stats(replay: dict, player: int) -> Counter:
    stats = Counter()
    steps = replay.get("steps") or []
    for step_index in range(1, len(steps)):
        action = steps[step_index][player].get("action")
        previous_obs = steps[step_index - 1][player].get("observation") or {}
        select = previous_obs.get("select") or {}
        options = select.get("option") or []
        if not isinstance(action, list) or not options:
            continue
        context = select.get("context")
        for option_index in action:
            if not isinstance(option_index, int) or not 0 <= option_index < len(options):
                continue
            option = options[option_index]
            stats[(context, option.get("type"))] += 1
    return stats


def deck_label(deck: list[int], names: dict[int, str]) -> str:
    pokemon = []
    for card_id, count in Counter(deck).most_common():
        name = names.get(card_id, str(card_id))
        if "Energy" in name:
            continue
        pokemon.append(f"{count}x {name}")
        if len(pokemon) == 5:
            break
    return ", ".join(pokemon)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", nargs="?", type=Path, default=DEFAULT_CORPUS)
    args = parser.parse_args()

    names = load_card_names()
    unique, duplicates = load_unique_replays(args.corpus)
    agent_records = defaultdict(lambda: {"wins": 0, "losses": 0, "decks": Counter()})
    episode_rows = []

    for episode_id, (path, replay) in sorted(unique.items()):
        agents = replay.get("info", {}).get("Agents") or []
        agent_names = [agent.get("Name", f"Player {i}") for i, agent in enumerate(agents)]
        rewards = replay.get("rewards") or [None, None]
        decks = [deck_from_replay(replay, player) for player in (0, 1)]
        for player in (0, 1):
            name = agent_names[player] if player < len(agent_names) else f"Player {player}"
            if rewards[player] == 1:
                agent_records[name]["wins"] += 1
            elif rewards[player] == -1:
                agent_records[name]["losses"] += 1
            if decks[player]:
                agent_records[name]["decks"][tuple(decks[player])] += 1

        episode_rows.append(
            {
                "episode_id": episode_id,
                "path": str(path.relative_to(ROOT)),
                "agents": agent_names,
                "rewards": rewards,
                "steps": len(replay.get("steps") or []),
                "deck_labels": [deck_label(deck, names) for deck in decks],
                "chosen_context_types": [
                    {f"{context}:{option_type}": count for (context, option_type), count in selected_option_stats(replay, player).most_common()}
                    for player in (0, 1)
                ],
            }
        )

    summary_agents = {}
    for name, record in sorted(
        agent_records.items(), key=lambda item: (-item[1]["wins"], item[0])
    ):
        top_decks = []
        for deck, count in record["decks"].most_common(3):
            top_decks.append(
                {
                    "count": count,
                    "cards": list(deck),
                    "label": deck_label(list(deck), names),
                }
            )
        summary_agents[name] = {
            "wins": record["wins"],
            "losses": record["losses"],
            "top_decks": top_decks,
        }

    summary = {
        "unique_episodes": len(unique),
        "duplicate_files": duplicates,
        "agents": summary_agents,
        "episodes": episode_rows,
    }
    output = args.corpus / "corpus_summary.json"
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    print(f"unique episodes: {len(unique)}")
    print(f"duplicate files: {duplicates}")
    print(f"summary: {output}")
    for name, record in list(summary_agents.items())[:20]:
        deck = record["top_decks"][0]["label"] if record["top_decks"] else "unknown deck"
        print(f"{name}: {record['wins']}W {record['losses']}L | {deck}")


if __name__ == "__main__":
    main()
