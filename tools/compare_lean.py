#!/usr/bin/env python3
"""
RAM-friendly V5/V6/V7 comparison.
Each head-to-head pair runs in its own subprocess to avoid memory buildup.
Replay suite runs each replay in a fresh subprocess and reports progress in batches.
Targets <= 400 MB peak RAM with 8 GB total.

Usage:
    python3 tools/compare_lean.py              # default: 300 H2H games, 1 trial/replay
    python3 tools/compare_lean.py --h2h 200   # fewer games for faster/lighter run
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_agent(agent_dir: Path, tag: str):
    src = agent_dir / "main.py"
    spec = importlib.util.spec_from_file_location(f"agent_{tag}", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def read_deck(path: Path) -> list[int]:
    cards = [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(cards) != 60:
        raise ValueError(f"{path} has {len(cards)} cards, expected 60")
    return cards


def play_one(agents, decks, primary_seat: int, max_steps: int = 4000):
    from cg.game import battle_finish, battle_select, battle_start
    obs, start = battle_start(decks[0], decks[1])
    if obs is None:
        raise RuntimeError(f"battle_start failed: {start.errorType}")
    try:
        for _ in range(max_steps):
            cur = (obs or {}).get("current") or {}
            sel = (obs or {}).get("select") or {}
            pi = cur.get("yourIndex", 0)
            action = agents[pi](obs)
            obs = battle_select(action)
            result = ((obs or {}).get("current") or {}).get("result", -1)
            if result != -1:
                return result
    finally:
        battle_finish()
    return None


# ---------------------------------------------------------------------------
# Sub-process worker: H2H
# ---------------------------------------------------------------------------

def _h2h_worker(primary_dir: str, opponent_dir: str, n_games: int):
    """Called in a subprocess. Prints JSON summary to stdout."""
    p_dir = Path(primary_dir)
    o_dir = Path(opponent_dir)
    p_agent = load_agent(p_dir, "p")
    o_agent = load_agent(o_dir, "o")
    p_deck = read_deck(p_dir / "deck.csv")
    o_deck = read_deck(o_dir / "deck.csv")

    pw = ow = draws = timeouts = 0
    for m in range(1, n_games + 1):
        seat = m % 2  # 0 or 1, alternates
        agents = (p_agent, o_agent) if seat == 0 else (o_agent, p_agent)
        decks = (p_deck, o_deck) if seat == 0 else (o_deck, p_deck)
        result = play_one(agents, decks, seat)
        if result == seat:
            pw += 1
        elif result in (0, 1):
            ow += 1
        elif result == 2:
            draws += 1
        else:
            timeouts += 1

    print(json.dumps({
        "primary": p_dir.name,
        "opponent": o_dir.name,
        "games": n_games,
        "primary_wins": pw,
        "opponent_wins": ow,
        "draws": draws,
        "timeouts": timeouts,
        "win_pct": round(pw / n_games * 100, 1),
    }))


# ---------------------------------------------------------------------------
# Sub-process worker: replay suite (one replay at a time)
# ---------------------------------------------------------------------------

def _replay_worker(agent_dir: str, replay_file: str, trials: int):
    """
    Evaluate one replay file; print JSON result.
    Called in a subprocess per batch so memory is freed between batches.
    """
    import traceback
    try:
        from tools.evaluate_replay_suite import evaluate_replay, load_module

        p_dir = Path(agent_dir)
        agent = load_agent(p_dir, "rs")
        deck = read_deck(p_dir / "deck.csv")
        fallback_path = ROOT / "agents" / "generic_attack_first" / "main.py"
        if not fallback_path.exists():
            for candidate in (ROOT / "agents").iterdir():
                if (candidate / "main.py").exists() and candidate.name != p_dir.name:
                    fallback_path = candidate / "main.py"
                    break
        fallback = load_module(str(fallback_path), "fallback")

        rpath = Path(replay_file)           # must be Path, not str
        episode_id = int(rpath.stem)
        replay = json.loads(rpath.read_text())
        row, _ = evaluate_replay(
            episode_id, rpath, replay, agent, deck, fallback,
            trials, 4000, "scripted", None,
            force_first_player=True,
        )
        print(json.dumps({
            "episode_id": episode_id,
            "wins": row["wins"],
            "losses": row["losses"],
            "draws": row["draws"],
            "timeouts": row["timeouts"],
            "attack_freq": (
                round(row["primary_attacked_turns"] / row["primary_attack_turns"], 3)
                if row.get("primary_attack_turns", 0) > 0 else 1.0
            ),
        }))
    except Exception:
        # Surface full traceback on stderr; mark as error so caller logs it
        traceback.print_exc(file=sys.stderr)
        ep = int(Path(replay_file).stem)
        print(json.dumps({"episode_id": ep, "wins": 0, "losses": 0, "draws": 0,
                          "timeouts": 0, "error": True}))



# ---------------------------------------------------------------------------
# Orchestration helpers that call subprocesses
# ---------------------------------------------------------------------------

def run_h2h_subprocess(primary_dir: Path, opponent_dir: Path, n_games: int) -> dict:
    import subprocess
    code = (
        f"import sys; sys.path.insert(0,'{ROOT}'); sys.path.insert(0,'{SAMPLE_DIR}');\n"
        f"from tools.compare_lean import _h2h_worker\n"
        f"_h2h_worker({str(primary_dir)!r}, {str(opponent_dir)!r}, {n_games})\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0:
        print(f"  [ERROR] H2H subprocess failed:\n{result.stderr[-800:]}", file=sys.stderr)
        return {}
    return json.loads(result.stdout.strip())


def run_replay_batch_subprocess(agent_dir: Path, replay_files: list[Path], trials: int) -> list[dict]:
    """Run each replay in its own subprocess; the list is a progress batch."""
    import subprocess
    rows = []
    for rfile in replay_files:
        code = (
            f"import sys; sys.path.insert(0,'{ROOT}'); sys.path.insert(0,'{SAMPLE_DIR}');\n"
            f"from tools.compare_lean import _replay_worker\n"
            f"_replay_worker({str(agent_dir)!r}, {str(rfile)!r}, {trials})\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if result.returncode != 0:
            print(f"  [WARN] replay {rfile.stem} failed: {result.stderr[-300:]}", file=sys.stderr)
            rows.append({"episode_id": int(rfile.stem), "wins": 0, "losses": 0,
                         "draws": 0, "timeouts": 0, "error": True})
        else:
            rows.append(json.loads(result.stdout.strip()))
    return rows


def collect_replay_files(corpus_root: Path) -> list[Path]:
    files: list[Path] = []
    for folder in corpus_root.rglob("*.json"):
        try:
            int(folder.stem)
            files.append(folder)
        except ValueError:
            pass
    # deduplicate by episode ID (keep first occurrence)
    seen: set[int] = set()
    unique: list[Path] = []
    for f in sorted(files):
        eid = int(f.stem)
        if eid not in seen:
            seen.add(eid)
            unique.append(f)
    return unique


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--h2h", type=int, default=300, help="H2H games per pair")
    parser.add_argument("--trials", type=int, default=1, help="Replay trials per episode")
    parser.add_argument("--batch", type=int, default=20, help="Replays per subprocess batch")
    args = parser.parse_args()

    v5 = ROOT / "agents" / "v5_candidate"
    v6 = ROOT / "agents" / "v6_candidate"
    v7 = ROOT / "agents" / "v7_candidate"

    print("\n" + "=" * 60)
    print(f"RAM-FRIENDLY COMPARISON  (H2H={args.h2h} games, replay trials={args.trials})")
    print("=" * 60)
    t0 = time.time()

    # ------------------------------------------------------------------
    # 1. Head-to-head (each pair runs in a fresh subprocess)
    # ------------------------------------------------------------------
    h2h_results = []
    if args.h2h > 0:
        print("\n--- HEAD-TO-HEAD (separate subprocess per pair) ---")
        h2h_pairs = [
            (v6, v5),
            (v7, v5),
            (v7, v6),
        ]
        for p_dir, o_dir in h2h_pairs:
            print(f"  Running {p_dir.name} vs {o_dir.name} ({args.h2h} games)...", end=" ", flush=True)
            res = run_h2h_subprocess(p_dir, o_dir, args.h2h)
            h2h_results.append(res)
            if res:
                print(f"{res['primary_wins']}W-{res['opponent_wins']}L-{res['draws']}D  ({res['win_pct']:.1f}%)")
            else:
                print("FAILED")
    else:
        print("\n[H2H skipped (--h2h 0)]")

    # ------------------------------------------------------------------
    # 2. Replay suite for V5, V6, V7 (20 replays per subprocess batch)
    # ------------------------------------------------------------------
    corpus = ROOT / "scouting_replays"
    replay_files = collect_replay_files(corpus)
    print(f"\n--- REPLAY SUITE ({len(replay_files)} unique replays, {args.trials} trial each) ---")
    print(f"    Processing in batches of {args.batch} to limit peak RAM.")

    agents_to_eval = [("V5", v5), ("V6", v6), ("V7", v7)]
    replay_summaries = {}

    for label, agent_dir in agents_to_eval:
        wins = losses = draws = timeouts = errors = 0
        att_ok = att_total = 0
        loss_episodes = []

        for batch_start in range(0, len(replay_files), args.batch):
            batch = replay_files[batch_start: batch_start + args.batch]
            rows = run_replay_batch_subprocess(agent_dir, batch, args.trials)
            for row in rows:
                wins += row.get("wins", 0)
                losses += row.get("losses", 0)
                draws += row.get("draws", 0)
                timeouts += row.get("timeouts", 0)
                errors += int(bool(row.get("error")))
                if row.get("losses", 0) > row.get("wins", 0):
                    loss_episodes.append(row["episode_id"])
            total_so_far = wins + losses + draws
            pct = wins / total_so_far * 100 if total_so_far else 0
            end = min(batch_start + args.batch, len(replay_files))
            print(f"  [{label}] {end}/{len(replay_files)} replays  running: {wins}W {losses}L {pct:.1f}%", flush=True)

        total = wins + losses + draws
        replay_summaries[label] = {
            "agent": agent_dir.name,
            "total": total,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "timeouts": timeouts,
            "errors": errors,
            "win_rate": round(wins / total * 100, 1) if total else 0,
            "loss_episodes": loss_episodes,
        }

    # ------------------------------------------------------------------
    # 3. Print final summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print("\n  Head-to-Head:")
    print(f"  {'Pair':<22} {'W-L-D':<14} {'WinRate':>8}")
    for res in h2h_results:
        if res:
            pair = f"{res['primary']} vs {res['opponent']}"
            wld = f"{res['primary_wins']}-{res['opponent_wins']}-{res['draws']}"
            print(f"  {pair:<22} {wld:<14} {res['win_pct']:>7.1f}%")

    print("\n  Replay Suite:")
    print(f"  {'Agent':<8} {'W':>5} {'L':>5} {'D':>5} {'TO':>5} {'ERR':>5} {'WinRate':>8}")
    for label, s in replay_summaries.items():
        print(f"  {label:<8} {s['wins']:>5} {s['losses']:>5} {s['draws']:>5} "
              f"{s['timeouts']:>5} {s['errors']:>5} {s['win_rate']:>7.1f}%")
        if s["loss_episodes"]:
            print(f"           Loss episodes: {s['loss_episodes']}")

    elapsed = time.time() - t0
    print(f"\n  Done in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # Save compact CSV
    out = ROOT / "artifacts" / "lean_comparison_results.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pair_or_agent", "type", "wins", "losses", "draws", "timeouts", "errors", "win_pct"])
        w.writeheader()
        for res in h2h_results:
            if res:
                w.writerow({
                    "pair_or_agent": f"{res['primary']} vs {res['opponent']}",
                    "type": "h2h",
                    "wins": res["primary_wins"],
                    "losses": res["opponent_wins"],
                    "draws": res["draws"],
                    "timeouts": res.get("timeouts", 0),
                    "errors": 0,
                    "win_pct": res["win_pct"],
                })
        for label, s in replay_summaries.items():
            w.writerow({
                "pair_or_agent": label,
                "type": "replay",
                "wins": s["wins"],
                "losses": s["losses"],
                "draws": s["draws"],
                "timeouts": s["timeouts"],
                "errors": s["errors"],
                "win_pct": s["win_rate"],
            })
    print(f"  CSV saved: {out}")


if __name__ == "__main__":
    main()
