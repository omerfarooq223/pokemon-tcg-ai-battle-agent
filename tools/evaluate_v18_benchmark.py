import argparse
import gc
import importlib.util
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start


def load_agent_from_dir(agent_dir: Path, module_tag: str):
    source_path = agent_dir / "main.py"
    spec = importlib.util.spec_from_file_location(f"eval_agent_{module_tag}", source_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def read_deck_csv(path: Path) -> list[int]:
    return [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def run_single_match(agent1, deck1, agent2, deck2, max_decisions=2500):
    obs, start_res = battle_start(deck1, deck2)
    if obs is None:
        return -1
    try:
        for _ in range(max_decisions):
            cur = (obs or {}).get("current") or {}
            player_idx = cur.get("yourIndex", 0)
            if player_idx == 0:
                act = agent1(obs)
            else:
                act = agent2(obs)
            obs = battle_select(act)
            res = ((obs or {}).get("current") or {}).get("result", -1)
            if res != -1:
                return res
    finally:
        battle_finish()
    return -1


def evaluate_head_to_head(agent1_name, agent1, deck1, agent2_name, agent2, deck2, total_matches=20, batch_size=10):
    wins = 0
    losses = 0
    draws = 0

    print(f"\n==========================================")
    print(f"  Evaluating {agent1_name} vs {agent2_name} ({total_matches} matches, batch_size={batch_size})")
    print(f"==========================================")

    for i in range(total_matches):
        seat = i % 2
        if seat == 0:
            res = run_single_match(agent1, deck1, agent2, deck2)
            if res == 0:
                wins += 1
            elif res == 1:
                losses += 1
            else:
                draws += 1
        else:
            res = run_single_match(agent2, deck2, agent1, deck1)
            if res == 1:
                wins += 1
            elif res == 0:
                losses += 1
            else:
                draws += 1

        if (i + 1) % batch_size == 0 or (i + 1) == total_matches:
            played = i + 1
            pct = (wins / played) * 100 if played > 0 else 0
            print(f"  Progress {played}/{total_matches} | Wins: {wins}, Losses: {losses}, Draws: {draws} ({pct:.1f}%)")
            gc.collect()

    final_pct = (wins / total_matches) * 100 if total_matches > 0 else 0
    print(f"--> Final vs {agent2_name}: {wins}-{losses}-{draws} ({final_pct:.2f}% Win Rate)\n")
    return wins, losses, draws


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    v18_dir = ROOT / "agents" / "v18_candidate"
    v18_agent = load_agent_from_dir(v18_dir, "v18")
    v18_deck = read_deck_csv(v18_dir / "deck.csv")

    baselines = [
        ("V17", ROOT / "agents" / "v17_candidate"),
        ("V16", ROOT / "agents" / "v16_candidate"),
        ("V15", ROOT / "agents" / "v15_candidate"),
        ("V14", ROOT / "agents" / "v14_candidate"),
        ("V13", ROOT / "agents" / "v13_candidate"),
        ("V12", ROOT / "agents" / "v12_candidate"),
        ("V10_FINAL", ROOT / "agents" / "v10_final_candidate"),
        ("V10", ROOT / "agents" / "v10_candidate"),
        ("V5", ROOT / "agents" / "v5_candidate"),
        ("V4", ROOT / "agents" / "v4_candidate"),
        ("V1", ROOT / "agents" / "v1_active"),
    ]

    results = {}
    total_w = 0
    total_l = 0
    total_d = 0

    for name, base_dir in baselines:
        if not base_dir.exists():
            continue
        try:
            b_agent = load_agent_from_dir(base_dir, name.lower())
            b_deck = read_deck_csv(base_dir / "deck.csv")
            w, l, d = evaluate_head_to_head("V18", v18_agent, v18_deck, name, b_agent, b_deck, args.matches, args.batch_size)
            results[name] = (w, l, d)
            total_w += w
            total_l += l
            total_d += d
        except Exception as e:
            print(f"Error testing vs {name}: {e}")

    print("\n" + "=" * 56)
    print("                V18 BENCHMARK SUMMARY                   ")
    print("=" * 56)
    for name, (w, l, d) in results.items():
        tot = w + l + d
        pct = (w / tot) * 100 if tot > 0 else 0
        print(f"  V18 vs {name:12s}:  {w:3d} W |  {l:3d} L |  {d:3d} D ({pct:6.2f}%)")
    print("-" * 56)
    overall_tot = total_w + total_l + total_d
    overall_pct = (total_w / overall_tot) * 100 if overall_tot > 0 else 0
    print(f"  OVERALL RECORD      : {total_w:4d} W | {total_l:4d} L | {total_d:4d} D ({overall_pct:6.2f}%)")
    print("=" * 56)


if __name__ == "__main__":
    main()
