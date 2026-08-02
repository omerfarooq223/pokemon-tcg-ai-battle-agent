# V9 board-resilience experiment (rejected)

## Baseline

- Source: `experiments/v9_discard_only/main.py`
- Source SHA-256: `4ddaf1eb2a7328165a1f97b5bcb4a2d17125c4325c426bc7d399a12dccc61b8a`
- Deck SHA-256: `26243a8a4ea0a825bbcb475564140f8d2eb347ef2c5dd61139886ccbe7876eb5`
- The experiment changes policy only; its deck is byte-identical to the baseline.

The exact current delta is the unified diff between the baseline above and
`experiments/v9_board_resilience/main.py` (SHA-256
`63263d3b6850cb99b202601bd84f789bbe6a66877e9b1274960bbe1e70d76bb3`).

## General logic tested

1. Count in-play Dwebble, Crustle, and Cornerstone as independent viable lines.
2. Reject Buddy-Buddy Poffin only when zero progress is provable: no Bench
   slot, empty deck, visible deck with no Dwebble, or all four Dwebble already
   visible outside the deck (including pre-evolutions).
3. Below two lines, prefer a Dwebble already in hand, then useful Poffin, then
   Poké Pad, then another Basic. Poké Pad target scoring prefers the missing
   Dwebble rather than another redundant Crustle.
4. Permit those search plays through the existing bounded pre-attack
   whitelist. The three-deferral/repeated-menu attack guard is unchanged.
5. Bound Poffin's optional targets instead of blindly filling the Bench.

Nine synthetic assertions passed for full Bench, empty/known-exhausted search,
direct Dwebble preference, two-line recovery, and bounded Poffin target counts.

## Revision 1: strict two-line cap

Source SHA-256 during these runs:
`1814cc6bedcc6398018414b8e9b52e2208630c96cbd02927ac08c45df0c8998c`.

| Test | Board variant | Matched comparator | Decision signal |
|---|---:|---:|---|
| Direct vs discard-only V9 | 527-473 (1,000) | 473-527 | 52.7%, promising screen |
| Direct vs V7 | 299-301 (600) | 301-299 | Neutral |
| Grimmsnarl stress | 493-7 (500) | n/a | Saturated; no established gain |
| New V8 replays, 10x | 108-2 | discard-only 109-1; V7 109-1 | One-match regression |
| Full 389-replay lean pass | 376-13 | discard-only 383-6 | Seven additional losses; reject |

Attack safety stayed exact: 443/443 attack-capable turns on the new-V8 10x
suite and 1,835/1,835 on the full lean pass, with zero abandoned turns,
timeouts, or evaluation errors.

## Revision 2: relaxed three-line cap

The current source allows a third line, enough to retain a backup after one
removal, while still refusing further Poffin filling.

| Test | Board variant | Matched comparator | Decision signal |
|---|---:|---:|---|
| Direct vs discard-only V9 | 770-726-4 (1,500) | 726-770-4 | 51.47% of decisive games; below 52.5% gate |
| Grimmsnarl stress | 498-2 (500) | discard-only 496-4 | +2 wins, too small and saturated |
| New V8 replays, 3x | 33-0 | discard-only 31-2 | Small favorable sample only |

Attack safety was 130/130 on the three-line new-V8 check, with zero abandoned
turns. A second full-suite run was intentionally skipped because the direct
and stress screens did not reverse the strict revision's broad regression.

## Decision

Do **not** merge this experiment into `agents/v9_candidate`. The strict version
lost broad replay coverage, and the safer three-line relaxation failed the
direct 52.5% promotion gate. The conservative no-progress detector is locally
correct, but it was not isolated with enough evidence to justify a production
change on its own.

Keep the report and result files as negative evidence. Remove generated
`__pycache__` directories; no submission archive should be built from this
experiment.
