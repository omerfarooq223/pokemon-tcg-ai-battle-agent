#!/usr/bin/env python3
"""
V5 vs V6 and V5 vs V7 comparison + V7 loss analysis via replay suite.
Runs:
  1. V6 vs V5 direct 1000-game swapped-seat comparison
  2. V7 vs V5 direct 1000-game swapped-seat comparison
  3. V7 vs V6 direct 500-game swapped-seat comparison
  4. Full replay suite for V7 (all 315 saved replays)
  5. Replay-suite comparison: V5 vs V6 (already have data, but rerun for consistency)
"""

from __future__ import annotations

import csv
import importlib.util
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start  # noqa: E402
from tools.evaluate_replay_suite import load_unique_replays, evaluate_replay, load_module  # noqa: E402


def load_agent(agent_dir: Path, module_name: str):
    source = agent_dir / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def read_deck(path: Path) -> list[int]:
    cards = [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(cards) != 60:
        raise ValueError(f"{path} has {len(cards)} cards; expected 60")
    return cards


def run_match(primary_agent, opponent_agent, primary_deck, opponent_deck, primary_seat: int, max_decisions: int = 5000):
    agents = (primary_agent, opponent_agent) if primary_seat == 0 else (opponent_agent, primary_agent)
    decks = (primary_deck, opponent_deck) if primary_seat == 0 else (opponent_deck, primary_deck)
    obs, start = battle_start(decks[0], decks[1])
    if obs is None:
        raise RuntimeError(f"Battle failed: player={start.errorPlayer}, error={start.errorType}")

    stats = {
        "decisions": 0,
        "attack_menus": 0,
        "attacks": 0,
        "missed_attack_menus": 0,
        "first_attack_turn": None,
        "abandoned_attack_turns": 0,
    }
    offered_attack_turns: set[int] = set()
    attacked_turns: set[int] = set()

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
                    turn = current.get("turn", 0)
                    offered_attack_turns.add(turn)
                    if any(i in attack_indexes for i in action):
                        stats["attacks"] += 1
                        attacked_turns.add(turn)
                        if stats["first_attack_turn"] is None:
                            stats["first_attack_turn"] = turn
                    else:
                        stats["missed_attack_menus"] += 1

            obs = battle_select(action)
            current = obs.get("current") or {}
            result = current.get("result", -1)
            if result != -1:
                stats["abandoned_attack_turns"] = len(offered_attack_turns - attacked_turns)
                return result, current.get("turn", 0), stats
    finally:
        battle_finish()

    stats["abandoned_attack_turns"] = len(offered_attack_turns - attacked_turns)
    return None, 0, stats


def head_to_head(p_dir: Path, o_dir: Path, matches: int) -> dict:
    p_name = p_dir.name
    o_name = o_dir.name
    uid = f"{p_name}_vs_{o_name}"
    p_agent = load_agent(p_dir, f"p_{uid}")
    o_agent = load_agent(o_dir, f"o_{uid}")
    p_deck = read_deck(p_dir / "deck.csv")
    o_deck = read_deck(o_dir / "deck.csv")

    p_wins = o_wins = draws = timeouts = 0
    p_attacks = p_menus = p_missed = p_abandoned = 0
    seat_rec = {0: {"w": 0, "l": 0}, 1: {"w": 0, "l": 0}}

    for m in range(1, matches + 1):
        seat = 1 if m % 2 == 0 else 0
        winner, turns, stats = run_match(p_agent, o_agent, p_deck, o_deck, seat)
        p_attacks += stats["attacks"]
        p_menus += stats["attack_menus"]
        p_missed += stats["missed_attack_menus"]
        p_abandoned += stats["abandoned_attack_turns"]

        if winner == seat:
            p_wins += 1
            seat_rec[seat]["w"] += 1
        elif winner in (0, 1):
            o_wins += 1
            seat_rec[seat]["l"] += 1
        elif winner == 2:
            draws += 1
        else:
            timeouts += 1

        if m % 100 == 0:
            print(f"  [{uid}] {m}/{matches}: {p_wins}W-{o_wins}L-{draws}D", flush=True)

    decisive = p_wins + o_wins
    return {
        "primary": p_name,
        "opponent": o_name,
        "matches": matches,
        "primary_wins": p_wins,
        "opponent_wins": o_wins,
        "draws": draws,
        "timeouts": timeouts,
        "win_rate": round(p_wins / matches, 4),
        "decisive_win_rate": round(p_wins / decisive, 4) if decisive > 0 else 0.0,
        "seat0": f"{seat_rec[0]['w']}-{seat_rec[0]['l']}",
        "seat1": f"{seat_rec[1]['w']}-{seat_rec[1]['l']}",
        "attack_rate": round(p_attacks / p_menus, 4) if p_menus > 0 else 1.0,
        "abandoned_attack_turns": p_abandoned,
        "missed_attack_menus": p_missed,
    }


def replay_suite_eval(agent_dir: Path, trials: int = 3) -> tuple[dict, list[dict]]:
    """Run replay suite and return aggregate + per-replay rows."""
    name = agent_dir.name
    agent = load_agent(agent_dir, f"rs_{name}")
    deck = read_deck(agent_dir / "deck.csv")
    fallback = load_module(ROOT / "agents" / "generic_attack_first" / "main.py", f"fb_{name}")
    corpus = ROOT / "scouting_replays"
    replays = load_unique_replays(corpus)

    tot_wins = tot_losses = tot_draws = 0
    tot_attacks = tot_attack_turns = 0
    per_replay = []

    for episode_id, path, replay in replays:
        row, _ = evaluate_replay(
            episode_id,
            path,
            replay,
            agent,
            deck,
            fallback,
            trials,
            5000,
            "scripted",
            None,
            force_first_player=True,
        )
        tot_wins += row["wins"]
        tot_losses += row["losses"]
        tot_draws += row["draws"]
        tot_attacks += row["primary_attacked_turns"]
        tot_attack_turns += row["primary_attack_turns"]
        per_replay.append(row)

    total = tot_wins + tot_losses + tot_draws
    summary = {
        "agent": name,
        "replays": len(replays),
        "trials_per_replay": trials,
        "total_matches": total,
        "wins": tot_wins,
        "losses": tot_losses,
        "draws": tot_draws,
        "win_rate": round(tot_wins / total, 4) if total > 0 else 0.0,
        "attack_frequency": round(tot_attacks / tot_attack_turns, 4) if tot_attack_turns > 0 else 1.0,
    }
    return summary, per_replay


def main():
    print("=" * 60)
    print("V5/V6/V7 COMPARISON + V7 REPLAY ANALYSIS")
    print("=" * 60)
    t0 = time.time()

    v5_dir = ROOT / "agents" / "v5_candidate"
    v6_dir = ROOT / "agents" / "v6_candidate"
    v7_dir = ROOT / "agents" / "v7_candidate"

    # 1. Head-to-head comparisons
    print("\n--- HEAD-TO-HEAD COMPARISONS ---")
    pairs = [
        (v6_dir, v5_dir, 1000),
        (v7_dir, v5_dir, 1000),
        (v7_dir, v6_dir, 500),
    ]
    h2h_results = []
    for p_dir, o_dir, n in pairs:
        print(f"\n[{p_dir.name} vs {o_dir.name}] {n} games...")
        res = head_to_head(p_dir, o_dir, n)
        h2h_results.append(res)
        print(f"  RESULT: {res['primary_wins']}W-{res['opponent_wins']}L-{res['draws']}D "
              f"({res['win_rate']:.1%}) decisive={res['decisive_win_rate']:.1%} "
              f"timeouts={res['timeouts']} abandoned={res['abandoned_attack_turns']}")

    # 2. V7 full replay suite (3 trials per replay)
    print("\n--- V7 REPLAY SUITE (3 trials per replay) ---")
    v7_summary, v7_per_replay = replay_suite_eval(v7_dir, trials=3)
    print(f"  V7: {v7_summary['wins']}W-{v7_summary['losses']}L-{v7_summary['draws']}D "
          f"win_rate={v7_summary['win_rate']:.1%} attack_freq={v7_summary['attack_frequency']:.3f}")

    # Identify V7 losses (majority losses in multi-trial replays)
    v7_losses = [r for r in v7_per_replay if r["losses"] > r["wins"]]
    v7_mixed = [r for r in v7_per_replay if r["losses"] > 0 and r["wins"] > 0 and r["losses"] >= r["wins"]]
    print(f"\n  V7 replay rows with majority LOSSES: {len(v7_losses)}")
    print(f"  V7 replay rows with mixed/contested results: {len(v7_mixed)}")

    if v7_losses:
        print("\n  V7 LOSS ROWS (majority losses):")
        for row in sorted(v7_losses, key=lambda r: r["losses"] - r["wins"], reverse=True):
            print(f"    episode={row['episode_id']} {row['wins']}W-{row['losses']}L "
                  f"attacked={row['primary_attacked_turns']}/{row['primary_attack_turns']} "
                  f"scripted={row.get('scripted_fraction', 0):.0%}")

    # 3. V5 and V6 replay suite comparison
    print("\n--- V5 REPLAY SUITE (1 trial per replay for speed) ---")
    v5_summary, v5_per_replay = replay_suite_eval(v5_dir, trials=1)
    print(f"  V5: {v5_summary['wins']}W-{v5_summary['losses']}L-{v5_summary['draws']}D "
          f"win_rate={v5_summary['win_rate']:.1%}")

    print("\n--- V6 REPLAY SUITE (1 trial per replay for speed) ---")
    v6_summary, v6_per_replay = replay_suite_eval(v6_dir, trials=1)
    print(f"  V6: {v6_summary['wins']}W-{v6_summary['losses']}L-{v6_summary['draws']}D "
          f"win_rate={v6_summary['win_rate']:.1%}")

    # Save results
    out_dir = ROOT / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    with (out_dir / "v5_v6_v7_h2h_results.json").open("w") as f:
        json.dump(h2h_results, f, indent=2)

    with (out_dir / "v7_replay_suite_per_replay.json").open("w") as f:
        json.dump(v7_per_replay, f, indent=2)

    with (out_dir / "v5_v6_v7_replay_suite_summary.json").open("w") as f:
        json.dump([v7_summary, v6_summary, v5_summary], f, indent=2)

    # Save V7 loss analysis
    v7_loss_data = {
        "summary": v7_summary,
        "loss_rows": v7_losses,
        "mixed_rows": v7_mixed,
    }
    with (out_dir / "v7_loss_analysis.json").open("w") as f:
        json.dump(v7_loss_data, f, indent=2)

    dt = time.time() - t0
    print(f"\n=== DONE in {dt:.1f}s ===")
    print(f"Results saved to {out_dir}")


if __name__ == "__main__":
    main()
