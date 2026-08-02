#!/usr/bin/env python3
"""RAM-safe final V9 comparison against every numbered agent snapshot."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "agents" / "v9_candidate"
OPPONENTS = [
    "v1_active",
    "v2_challenger",
    "v3_planner",
    "v4_attackfix",
    "v5_candidate",
    "v6_candidate",
    "v7_candidate",
    "v8_candidate",
    "v8_fixed",
]


def run_pair(opponent: str, games: int) -> dict:
    code = "\n".join(
        [
            "import json",
            "from pathlib import Path",
            "from tools.compare_v5_v6_v7 import head_to_head",
            f"result = head_to_head(Path({str(PRIMARY)!r}), "
            f"Path({str(ROOT / 'agents' / opponent)!r}), {games})",
            "print('FINAL_JSON=' + json.dumps(result, sort_keys=True))",
        ]
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{opponent} comparison failed:\n{completed.stderr[-2000:]}"
        )
    for line in reversed(completed.stdout.splitlines()):
        if line.startswith("FINAL_JSON="):
            return json.loads(line.removeprefix("FINAL_JSON="))
    raise RuntimeError(f"{opponent} comparison produced no result")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--v7-games", type=int, default=5000)
    parser.add_argument(
        "--output-prefix",
        type=Path,
        default=ROOT / "artifacts" / "v9_all_agents_h2h",
    )
    args = parser.parse_args()
    if args.games < 1 or args.v7_games < 1:
        parser.error("game counts must be positive")

    results = []
    for opponent in OPPONENTS:
        games = args.v7_games if opponent == "v7_candidate" else args.games
        print(f"running V9 vs {opponent}: {games} games", flush=True)
        result = run_pair(opponent, games)
        results.append(result)
        print(
            f"  {result['primary_wins']}-{result['opponent_wins']}-"
            f"{result['draws']} decisive={result['decisive_win_rate']:.2%} "
            f"attacks={result['attack_rate']:.2%} "
            f"abandoned={result['abandoned_attack_turns']}",
            flush=True,
        )

    output_prefix = args.output_prefix
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    output_prefix.with_suffix(".json").write_text(
        json.dumps(results, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# V9 head-to-head tournament",
        "",
        "| Opponent | Games | V9 W-L-D | Decisive win rate | "
        "Attack-menu selections | Abandoned attack turns |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        lines.append(
            f"| {row['opponent']} | {row['matches']} | "
            f"{row['primary_wins']}-{row['opponent_wins']}-{row['draws']} | "
            f"{row['decisive_win_rate']:.2%} | {row['attack_rate']:.2%} | "
            f"{row['abandoned_attack_turns']} |"
        )
    output_prefix.with_suffix(".md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print(output_prefix.with_suffix(".json"))
    print(output_prefix.with_suffix(".md"))


if __name__ == "__main__":
    main()
