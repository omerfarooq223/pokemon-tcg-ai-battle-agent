#!/usr/bin/env python3
"""Run an auditable counterfactual evaluation against every saved replay.

This is the reporting/orchestration layer for ``evaluate_replay_suite.py``.
It deliberately calls the test a *counterfactual*, not an exact replay.  The
public local simulator accepts only two 60-card decks; it has no API for the
Kaggle seed, shuffled deck order, opening hand, Prize cards, coin flips, or an
opponent submission.  We preserve the reconstructable conditions and report
the remaining fidelity instead of silently treating approximations as exact.

The default replacement policy is:

* replace our seat when a configured team alias is present;
* otherwise replace the public replay's losing seat, challenging V9 against
  the original winner.

Each replay runs in a fresh subprocess so module globals and simulator state
cannot leak from one episode to the next.  Within a replay, the opponent's
recorded actions are matched semantically while legal; a generic legal policy
is used after the trajectory diverges.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SAMPLE_DIR))

from tools.evaluate_replay_suite import (  # noqa: E402
    evaluate_replay,
    load_agent,
    load_module,
    read_deck,
    replay_deck,
)


PROTOCOL_ID = "counterfactual-replay-v2"
DEFAULT_ALIASES = ("MUHAMMAD UMER FAROOQ", "ROASTERS")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_cards(cards: list[int]) -> str:
    payload = ",".join(str(card) for card in cards).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def local_engine_path() -> Path:
    cg_dir = SAMPLE_DIR / "cg"
    if platform.system() == "Windows":
        return cg_dir / "cg.dll"
    if platform.system() == "Darwin":
        return cg_dir / "libcg.dylib"
    if platform.machine() in ("arm64", "aarch64"):
        return cg_dir / "libcg-arm64.so"
    return cg_dir / "libcg.so"


def replay_episode_id(path: Path, replay: dict[str, Any]) -> int:
    value = (replay.get("info") or {}).get("EpisodeId")
    if value is None and path.stem.isdigit():
        value = path.stem
    if value is None:
        raise ValueError("missing info.EpisodeId and numeric filename")
    return int(value)


def validate_replay(path: Path, replay: dict[str, Any]) -> int:
    if not isinstance(replay, dict):
        raise ValueError("top-level JSON value is not an object")
    episode_id = replay_episode_id(path, replay)
    if path.stem.isdigit() and int(path.stem) != episode_id:
        raise ValueError(
            f"numeric filename {path.stem} disagrees with EpisodeId {episode_id}"
        )
    steps = replay.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError("missing non-empty steps")
    rewards = replay.get("rewards")
    if not isinstance(rewards, list) or len(rewards) < 2:
        raise ValueError("missing two-player rewards")
    if replay.get("statuses") != ["DONE", "DONE"]:
        raise ValueError(f"replay is not DONE/DONE: {replay.get('statuses')}")
    # This also verifies that both submitted 60-card lists are recoverable.
    replay_deck(replay, 0)
    replay_deck(replay, 1)
    return episode_id


def discover_paths(corpora: list[Path], explicit: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for corpus in corpora:
        if corpus.is_file():
            paths.append(corpus.resolve())
            continue
        if not corpus.exists():
            raise FileNotFoundError(f"Replay corpus does not exist: {corpus}")
        paths.extend(
            path.resolve()
            for path in corpus.rglob("*.json")
            if path.name != "corpus_summary.json"
        )
    paths.extend(path.resolve() for path in explicit)
    return sorted(set(paths), key=str)


def catalog_replays(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate and de-duplicate without retaining the 1+ GB corpus in RAM."""
    by_episode: dict[int, dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Replay does not exist: {path}")
        with path.open(encoding="utf-8") as handle:
            replay = json.load(handle)
        episode_id = validate_replay(path, replay)
        checksum = sha256_file(path)
        item = {
            "episode_id": episode_id,
            "path": str(path),
            "sha256": checksum,
            "bytes": path.stat().st_size,
        }
        previous = by_episode.get(episode_id)
        if previous is None:
            by_episode[episode_id] = item
            continue
        if previous["sha256"] != checksum:
            raise ValueError(
                f"Conflicting files for episode {episode_id}: "
                f"{previous['path']} ({previous['sha256']}) and "
                f"{path} ({checksum})"
            )
        duplicates.append({"kept": previous["path"], "skipped": str(path), **item})
    return [by_episode[key] for key in sorted(by_episode)], duplicates


def wilson_interval(wins: int, trials: int) -> tuple[float, float]:
    if trials <= 0:
        return 0.0, 0.0
    z = 1.959963984540054
    p = wins / trials
    denominator = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denominator
    margin = (
        z
        * math.sqrt((p * (1.0 - p) + z * z / (4.0 * trials)) / trials)
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def comparison_label(original: str, counterfactual: str) -> str:
    if original == "loss" and counterfactual == "win":
        return "improved"
    if original == "loss" and counterfactual == "loss":
        return "unresolved_loss"
    if original == "win" and counterfactual == "win":
        return "preserved_win"
    if original == "win" and counterfactual == "loss":
        return "regressed"
    if original == counterfactual:
        return "unchanged"
    return f"{original}_to_{counterfactual}"


def loss_triage_signal(row: dict[str, Any]) -> str:
    """Give an evidence-based triage signal, not an invented root cause."""
    if row.get("evaluation_status") != "ok":
        return "evaluation incomplete"
    if int(row.get("timeouts") or 0):
        return "local simulation timeout"
    if int(row.get("primary_abandoned_attack_turns") or 0):
        return "legal attack turn abandoned"
    attack_turns = int(row.get("primary_attack_turns") or 0)
    if attack_turns == 0:
        return "never reached a legal attack"
    reasons_raw = row.get("result_reasons") or "{}"
    try:
        reasons = json.loads(reasons_raw) if isinstance(reasons_raw, str) else reasons_raw
    except json.JSONDecodeError:
        reasons = {}
    if reasons.get("deck_out"):
        return "deck/resource endurance; inspect trace"
    if reasons.get("no_active_pokemon"):
        return "board exhausted; inspect trace"
    first_attack = row.get("avg_first_attack_turn")
    if first_attack not in (None, "") and float(first_attack) >= 10:
        return "slow attack setup/tempo; inspect trace"
    return "matchup/resource race; trace review required"


def enrich_row(
    row: dict[str, Any],
    catalog: dict[str, Any],
    candidate_deck_sha256: str,
) -> dict[str, Any]:
    trials = int(row.get("trials") or 0)
    wins = int(row.get("wins") or 0)
    low, high = wilson_interval(wins, trials)
    scripted = int(row.get("opponent_scripted_decisions") or 0)
    fallback = int(row.get("opponent_fallback_decisions") or 0)
    if scripted and fallback:
        fidelity = "semantic_script_plus_generic_fallback"
    elif scripted:
        fidelity = "semantic_script_only"
    else:
        fidelity = "generic_fallback_only"
    evaluation_status = "timeout" if int(row.get("timeouts") or 0) else "ok"
    row = {
        "protocol_id": PROTOCOL_ID,
        "evaluation_status": evaluation_status,
        "replay_sha256": catalog["sha256"],
        "candidate_deck_sha256": candidate_deck_sha256,
        **row,
        "win_rate_ci95_low": round(low, 6),
        "win_rate_ci95_high": round(high, 6),
        "opponent_fidelity": fidelity,
    }
    row["comparison"] = (
        comparison_label(
            str(row.get("original_outcome")), str(row.get("result"))
        )
        if evaluation_status == "ok"
        else "not_evaluated"
    )
    row["loss_triage_signal"] = (
        loss_triage_signal(row)
        if row.get("result") == "loss" or evaluation_status != "ok"
        else ""
    )
    return row


def worker_main(args: argparse.Namespace) -> int:
    replay_path = args.worker_replay.resolve()
    with replay_path.open(encoding="utf-8") as handle:
        replay = json.load(handle)
    episode_id = validate_replay(replay_path, replay)
    agent_dir = args.agent_dir.resolve()
    primary_agent = load_agent(agent_dir, f"every_replay_{episode_id}")
    primary_deck = read_deck((args.agent_deck or agent_dir / "deck.csv").resolve())
    fallback_module = load_module(
        ROOT / "agents" / "generic_attack_first" / "main.py",
        f"every_replay_fallback_{episode_id}",
    )
    trace_dir = args.trace_dir.resolve() if args.trace_dir else None
    row, trials = evaluate_replay(
        episode_id,
        replay_path,
        replay,
        primary_agent,
        primary_deck,
        fallback_module,
        args.trials,
        args.max_decisions,
        args.opponent_mode,
        trace_dir,
        team_aliases=frozenset(args.team_alias or DEFAULT_ALIASES),
        public_replacement=args.public_replacement,
        force_first_player=args.force_first_player,
    )
    opponent_cards = replay_deck(replay, 1 - int(row["replacement_seat"]))
    row["opponent_deck_sha256"] = sha256_cards(opponent_cards)
    payload = {"row": row, "trials": trials}
    args.worker_output.write_text(json.dumps(payload, sort_keys=True))
    return 0


def error_row(item: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        "protocol_id": PROTOCOL_ID,
        "evaluation_status": "error",
        "episode_id": item["episode_id"],
        "path": item["path"],
        "replay_sha256": item["sha256"],
        "result": "error",
        "comparison": "not_evaluated",
        "error": message,
        "loss_triage_signal": "evaluation incomplete",
    }


def read_baseline(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None:
        return {}
    with path.open(newline="") as handle:
        return {
            int(row["episode_id"]): row
            for row in csv.DictReader(handle)
            if row.get("episode_id")
        }


def attach_baseline(rows: list[dict[str, Any]], baseline: dict[int, dict[str, str]]) -> None:
    for row in rows:
        old = baseline.get(int(row["episode_id"]))
        if old is None:
            row["baseline_result"] = ""
            row["baseline_win_rate"] = ""
            row["win_rate_delta_vs_baseline"] = ""
            row["regression_vs_baseline"] = ""
            continue
        row["baseline_result"] = old.get("result", "")
        row["baseline_win_rate"] = old.get("win_rate", "")
        try:
            delta = float(row.get("win_rate") or 0) - float(old.get("win_rate") or 0)
            row["win_rate_delta_vs_baseline"] = round(delta, 6)
        except ValueError:
            row["win_rate_delta_vs_baseline"] = ""
        row["regression_vs_baseline"] = int(
            old.get("result") == "win" and row.get("result") == "loss"
        )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    preferred = [
        "episode_id",
        "evaluation_status",
        "original_outcome",
        "result",
        "comparison",
        "wins",
        "losses",
        "draws",
        "win_rate",
        "replacement_kind",
        "replacement_seat",
        "replacement_team",
        "opponent_team",
        "original_first_player",
        "first_player_forced",
        "scripted_fraction",
        "opponent_fidelity",
        "primary_attacked_turns",
        "primary_attack_turns",
        "primary_abandoned_attack_turns",
        "loss_triage_signal",
        "path",
    ]
    keys = {key for row in rows for key in row}
    fields = [key for key in preferred if key in keys]
    fields.extend(sorted(keys - set(fields)))
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(value: Any) -> str:
    try:
        return f"{float(value):.1%}"
    except (TypeError, ValueError):
        return "n/a"


def markdown_report(metadata: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    ok = [row for row in rows if row.get("evaluation_status") == "ok"]
    errors = [row for row in rows if row.get("evaluation_status") != "ok"]
    total_wins = sum(int(row.get("wins") or 0) for row in ok)
    total_losses = sum(int(row.get("losses") or 0) for row in ok)
    total_draws = sum(int(row.get("draws") or 0) for row in ok)
    matches = total_wins + total_losses + total_draws
    majority = {label: sum(row.get("result") == label for row in ok) for label in ("win", "loss", "draw")}
    scripted = sum(int(row.get("opponent_scripted_decisions") or 0) for row in ok)
    fallback = sum(int(row.get("opponent_fallback_decisions") or 0) for row in ok)
    lines = [
        "# Every-Replay Counterfactual Evaluation",
        "",
        "> This is not an exact Kaggle replay. It is a counterfactual local simulation ",
        "> using every reconstructable replay condition and explicitly reported fallback.",
        "",
        "## Summary",
        "",
        f"- Unique replays: **{len(rows)}** ({len(ok)} evaluated, {len(errors)} errors)",
        f"- Local matches: **{matches}**",
        f"- Match results: **{total_wins} wins, {total_losses} losses, {total_draws} draws**",
        f"- Match win rate: **{total_wins / matches:.2%}**" if matches else "- Match win rate: n/a",
        f"- Per-replay majority: **{majority['win']} wins, {majority['loss']} losses, {majority['draw']} ties**",
        f"- Recorded opponent-action usage: **{scripted / (scripted + fallback):.2%}**" if scripted + fallback else "- Recorded opponent-action usage: n/a",
        "",
        "## What was preserved",
        "",
        "| Condition | Status |",
        "|---|---|",
        "| Replacement seat | Preserved |",
        "| Opponent submitted 60-card deck | Preserved exactly |",
        "| Original first-player seat | Forced when recoverable |",
        "| Opponent decisions | Recorded semantic action when still legal; generic fallback otherwise |",
        "| Game/map | Pokémon has no map parameter; local bundled engine used |",
        "| Kaggle seed | Metadata only; **not accepted by the local API** |",
        "| Initial shuffle, hand, and Prize cards | Visible in replay visualization, but not injectable through the local API |",
        "| Coin flips | Recorded after the fact, but not settable |",
        "| Original opponent source code | Not present in replay JSON |",
        "",
        "## Per-replay results",
        "",
        "| Episode | Original | Counterfactual W-L-D | Result | Comparison | Scripted | Attacked turns | Triage |",
        "|---:|---|---:|---|---|---:|---:|---|",
    ]
    for row in rows:
        if row.get("evaluation_status") != "ok":
            lines.append(
                f"| {row['episode_id']} | ? | incomplete | {row.get('evaluation_status')} | "
                f"not evaluated | n/a | n/a | {row.get('error') or row.get('loss_triage_signal', '')} |"
            )
            continue
        wld = f"{row['wins']}-{row['losses']}-{row['draws']}"
        attacked = f"{row['primary_attacked_turns']}/{row['primary_attack_turns']}"
        lines.append(
            f"| {row['episode_id']} | {row['original_outcome']} | {wld} | "
            f"{row['result']} | {row['comparison']} | {pct(row['scripted_fraction'])} | "
            f"{attacked} | {row.get('loss_triage_signal') or ''} |"
        )
    losses = [row for row in ok if row.get("result") == "loss"]
    lines.extend(
        [
            "",
            "## Loss triage",
            "",
            "The labels below are evidence-based triage signals, not automatically proven root causes. "
            "Confirm each one from its trace before changing the agent.",
            "",
            "| Episode | Signal | Attack turns | First attack | End reason(s) |",
            "|---:|---|---:|---:|---|",
        ]
    )
    if not losses:
        lines.append("| — | No majority losses | — | — | — |")
    for row in losses:
        first = row.get("avg_first_attack_turn") or "—"
        attack = f"{row['primary_attacked_turns']}/{row['primary_attack_turns']}"
        lines.append(
            f"| {row['episode_id']} | {row['loss_triage_signal']} | {attack} | "
            f"{first} | {row.get('result_reasons', '{}')} |"
        )
    regressions = [row for row in ok if int(row.get("regression_vs_baseline") or 0)]
    if metadata.get("baseline_csv"):
        lines.extend(
            [
                "",
                "## Matched baseline check",
                "",
                f"Baseline: `{metadata['baseline_csv']}`",
                "",
                f"Per-replay win-to-loss regressions: **{len(regressions)}**",
            ]
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.",
            "- The engine reads its own randomness, so rerunning the command can change draws and coin flips.",
            "- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.",
            "- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-dir", type=Path, default=ROOT / "agents" / "v9_candidate")
    parser.add_argument("--agent-deck", type=Path)
    parser.add_argument("--corpus", type=Path, action="append")
    parser.add_argument("--replay", type=Path, action="append", default=[])
    parser.add_argument("--episodes", help="Comma-separated episode IDs")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--max-decisions", type=int, default=5000)
    parser.add_argument("--opponent-mode", choices=("scripted", "generic"), default="scripted")
    parser.add_argument(
        "--team-alias",
        action="append",
        help=(
            "Additional team name whose seat should be replaced (may repeat). "
            "The two project aliases remain enabled."
        ),
    )
    parser.add_argument(
        "--public-replacement",
        choices=("loser", "seat0", "seat1"),
        default="loser",
    )
    parser.add_argument(
        "--force-first-player",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--trace-dir", type=Path)
    parser.add_argument("--baseline-csv", type=Path)
    parser.add_argument(
        "--output-prefix",
        type=Path,
        default=ROOT / "artifacts" / "v9_every_replay",
    )
    parser.add_argument("--worker-timeout", type=float, default=600.0)
    parser.add_argument("--allow-errors", action="store_true")
    # Private subprocess interface.
    parser.add_argument("--_worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--worker-replay", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--worker-output", type=Path, help=argparse.SUPPRESS)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be positive")
    if args.max_decisions < 1:
        parser.error("--max-decisions must be positive")
    if args._worker:
        if args.worker_replay is None or args.worker_output is None:
            parser.error("worker mode requires replay and output paths")
        return worker_main(args)

    corpora = args.corpus or [ROOT / "scouting_replays"]
    paths = discover_paths(corpora, args.replay)
    try:
        catalog, duplicates = catalog_replays(paths)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.episodes:
        requested = {int(value.strip()) for value in args.episodes.split(",") if value.strip()}
        catalog = [item for item in catalog if item["episode_id"] in requested]
        missing = requested - {item["episode_id"] for item in catalog}
        if missing:
            parser.error(f"Unknown episodes: {sorted(missing)}")
    if args.limit is not None:
        if args.limit < 1:
            parser.error("--limit must be positive")
        catalog = catalog[: args.limit]
    if not catalog:
        parser.error("No valid replay files selected")

    agent_dir = args.agent_dir.resolve()
    deck_path = (args.agent_deck or agent_dir / "deck.csv").resolve()
    main_path = agent_dir / "main.py"
    if not main_path.is_file() or not deck_path.is_file():
        parser.error(f"Agent source/deck missing under {agent_dir}")
    candidate_deck = read_deck(deck_path)
    output_prefix = args.output_prefix.resolve()
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    trace_dir = args.trace_dir.resolve() if args.trace_dir else None
    if trace_dir:
        trace_dir.mkdir(parents=True, exist_ok=True)

    aliases = list(dict.fromkeys([*DEFAULT_ALIASES, *(args.team_alias or [])]))
    rows: list[dict[str, Any]] = []
    details: dict[str, Any] = {}
    script_path = Path(__file__).resolve()
    with tempfile.TemporaryDirectory(
        prefix="every-replay-", dir=output_prefix.parent
    ) as temporary:
        temporary_dir = Path(temporary)
        for index, item in enumerate(catalog, 1):
            worker_output = temporary_dir / f"{item['episode_id']}.json"
            command = [
                sys.executable,
                str(script_path),
                "--_worker",
                "--worker-replay",
                item["path"],
                "--worker-output",
                str(worker_output),
                "--agent-dir",
                str(agent_dir),
                "--agent-deck",
                str(deck_path),
                "--trials",
                str(args.trials),
                "--max-decisions",
                str(args.max_decisions),
                "--opponent-mode",
                args.opponent_mode,
                "--public-replacement",
                args.public_replacement,
            ]
            command.append("--force-first-player" if args.force_first_player else "--no-force-first-player")
            for alias in aliases:
                command.extend(("--team-alias", alias))
            if trace_dir:
                command.extend(("--trace-dir", str(trace_dir)))
            try:
                completed = subprocess.run(
                    command,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=args.worker_timeout,
                    env={**os.environ, "PYTHONUNBUFFERED": "1"},
                )
                if completed.returncode != 0 or not worker_output.is_file():
                    message = (completed.stderr or completed.stdout or "worker failed").strip()
                    rows.append(error_row(item, message[-2000:]))
                    print(
                        f"{index}/{len(catalog)} episode={item['episode_id']} ERROR",
                        flush=True,
                    )
                    continue
                payload = json.loads(worker_output.read_text())
                row = enrich_row(
                    payload["row"], item, sha256_cards(candidate_deck)
                )
                rows.append(row)
                details[str(item["episode_id"])] = payload["trials"]
                print(
                    f"{index}/{len(catalog)} episode={item['episode_id']} "
                    f"result={row['wins']}-{row['losses']}-{row['draws']} "
                    f"scripted={row['scripted_fraction']:.1%} "
                    f"attacks={row['primary_attacked_turns']}/{row['primary_attack_turns']}",
                    flush=True,
                )
            except subprocess.TimeoutExpired:
                rows.append(error_row(item, f"worker exceeded {args.worker_timeout}s"))
                print(
                    f"{index}/{len(catalog)} episode={item['episode_id']} TIMEOUT",
                    flush=True,
                )

    baseline = read_baseline(args.baseline_csv.resolve() if args.baseline_csv else None)
    attach_baseline(rows, baseline)
    csv_path = output_prefix.with_suffix(".csv")
    json_path = output_prefix.with_suffix(".json")
    report_path = output_prefix.with_suffix(".md")
    write_csv(csv_path, rows)

    engine_path = local_engine_path()
    metadata = {
        "protocol_id": PROTOCOL_ID,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_dir": str(agent_dir),
        "agent_main_sha256": sha256_file(main_path),
        "agent_deck_path": str(deck_path),
        "agent_deck_file_sha256": sha256_file(deck_path),
        "agent_deck_cards_sha256": sha256_cards(candidate_deck),
        "local_engine_path": str(engine_path),
        "local_engine_sha256": sha256_file(engine_path),
        "corpora": [str(path.resolve()) for path in corpora],
        "explicit_replays": [str(path.resolve()) for path in args.replay],
        "team_aliases": aliases,
        "public_replacement": args.public_replacement,
        "opponent_mode": args.opponent_mode,
        "force_first_player": args.force_first_player,
        "trials_per_replay": args.trials,
        "max_decisions": args.max_decisions,
        "replay_process_isolation": True,
        "trial_process_isolation": False,
        "baseline_csv": str(args.baseline_csv.resolve()) if args.baseline_csv else None,
        "duplicates_skipped": duplicates,
        "conditions": {
            "replacement_seat_preserved": True,
            "opponent_deck_preserved": True,
            "original_first_player_forced_when_recoverable": args.force_first_player,
            "map_parameter": "not_applicable",
            "kaggle_seed_metadata_read": True,
            "kaggle_seed_applied_to_local_engine": False,
            "initial_shuffle_hand_prizes_visible_in_replay": True,
            "initial_shuffle_hand_prizes_preserved": False,
            "coin_flips_preserved": False,
            "opponent_source_available": False,
            "opponent_actions": "semantic replay with reported generic fallback",
        },
        "limitations": [
            "The local battle_start API accepts decks only and exposes no seed/state injection.",
            "The bundled engine obtains its own randomness, so outcomes are not bit-for-bit reproducible.",
            "The original opponent source is absent; recorded semantic actions are usable only while legal on the counterfactual trajectory.",
            "A local replay suite is a rejection and regression test, not a leaderboard-rating predictor.",
        ],
    }
    payload = {"metadata": metadata, "rows": rows, "trials": details}
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    report_path.write_text(markdown_report(metadata, rows))

    ok = [row for row in rows if row.get("evaluation_status") == "ok"]
    errors = len(rows) - len(ok)
    wins = sum(int(row.get("wins") or 0) for row in ok)
    losses = sum(int(row.get("losses") or 0) for row in ok)
    draws = sum(int(row.get("draws") or 0) for row in ok)
    total = wins + losses + draws
    print(
        f"summary replays={len(rows)} evaluated={len(ok)} errors={errors} "
        f"matches={total} wins={wins} losses={losses} draws={draws} "
        f"win_rate={wins / total:.3%}" if total else "summary no completed matches"
    )
    print(csv_path)
    print(json_path)
    print(report_path)
    if errors and not args.allow_errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
