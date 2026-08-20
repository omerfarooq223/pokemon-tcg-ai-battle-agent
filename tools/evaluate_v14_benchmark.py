#!/usr/bin/env python3
"""Memory-safe benchmark evaluation runner for V14 agent on 8GB RAM Mac.

Executes head-to-head match batches in isolated subprocesses to ensure memory
freed by OS keeps RAM footprint under 500 MB.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OPPONENTS = {
    "v13": ROOT / "agents" / "v13_candidate",
    "v12": ROOT / "agents" / "v12_candidate",
    "v11": ROOT / "agents" / "v11_candidate",
    "v10": ROOT / "agents" / "v10_candidate",
    "v5": ROOT / "agents" / "v5_candidate",
    "v4": ROOT / "agents" / "v4_attackfix",
    "v1": ROOT / "agents" / "v1_active",
}


def run_batch(v14_dir: Path, opp_dir: Path, matches: int, swap_seats: bool) -> tuple[int, int, int]:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "run_local_matches.py"),
        "--agent-dir", str(v14_dir),
        "--agent-deck", str(v14_dir / "deck.csv"),
        "--opponent", "agent",
        "--opponent-dir", str(opp_dir),
        "--opponent-deck", str(opp_dir / "deck.csv"),
        "--matches", str(matches),
        "--quiet",
    ]
    if swap_seats:
        cmd.append("--swap-seats")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error running match batch: {proc.stderr}", file=sys.stderr)
        return 0, 0, 0

    wins = 0
    losses = 0
    draws = 0

    for line in proc.stdout.splitlines():
        if line.startswith("summary "):
            # Format: summary primary=X opponent=Y draws=Z seat0=... seat1=...
            parts = line.split()
            for p in parts:
                if p.startswith("primary="):
                    wins = int(p.split("=")[1])
                elif p.startswith("opponent="):
                    losses = int(p.split("=")[1])
                elif p.startswith("draws="):
                    draws = int(p.split("=")[1])
    return wins, losses, draws


def evaluate_opponent(v14_dir: Path, opp_name: str, opp_dir: Path, total_matches: int, batch_size: int):
    print(f"\n==========================================")
    print(f"  Evaluating V14 vs {opp_name.upper()} ({total_matches} matches, batch_size={batch_size})")
    print(f"==========================================")

    total_wins = 0
    total_losses = 0
    total_draws = 0

    remaining = total_matches
    batch_count = 0

    while remaining > 0:
        current_batch = min(remaining, batch_size)
        batch_count += 1
        w, l, d = run_batch(v14_dir, opp_dir, current_batch, swap_seats=True)
        total_wins += w
        total_losses += l
        total_draws += d
        remaining -= current_batch

        played = total_wins + total_losses + total_draws
        rate = (total_wins / played * 100.0) if played > 0 else 0.0
        print(f"  Batch {batch_count}: Progress {played}/{total_matches} | Wins: {total_wins}, Losses: {total_losses}, Draws: {total_draws} ({rate:.1f}%)")

    played = total_wins + total_losses + total_draws
    rate = (total_wins / played * 100.0) if played > 0 else 0.0
    print(f"--> Final vs {opp_name.upper()}: {total_wins}-{total_losses}-{total_draws} ({rate:.2f}% Win Rate)\n")
    return total_wins, total_losses, total_draws


def main():
    parser = argparse.ArgumentParser(description="Evaluate V14 against existing agents in memory-safe batches.")
    parser.add_argument("--v14-dir", type=Path, default=ROOT / "agents" / "v14_candidate")
    parser.add_argument("--opponents", nargs="+", default=["v13", "v12", "v11", "v5", "v4", "v1"])
    parser.add_argument("--matches", type=int, default=100, help="Total matches per opponent")
    parser.add_argument("--batch-size", type=int, default=20, help="Matches per subprocess batch (low memory footprint)")
    args = parser.parse_args()

    results = {}
    for opp_name in args.opponents:
        if opp_name in OPPONENTS:
            opp_dir = OPPONENTS[opp_name]
            w, l, d = evaluate_opponent(args.v14_dir, opp_name, opp_dir, args.matches, args.batch_size)
            results[opp_name] = (w, l, d)
        else:
            print(f"Unknown opponent {opp_name}, skipping.")

    print("\n==========================================")
    print("           V14 BENCHMARK SUMMARY          ")
    print("==========================================")
    for opp_name, (w, l, d) in results.items():
        total = w + l + d
        rate = (w / total * 100.0) if total > 0 else 0.0
        print(f"  V14 vs {opp_name.upper():5s}: {w:4d} W | {l:4d} L | {d:4d} D ({rate:6.2f}%)")
    print("==========================================")


if __name__ == "__main__":
    main()
