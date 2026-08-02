# V9 candidate

V9 is the strongest locally validated agent in this project. It keeps the
proven V6/V7 Crustle/Cornerstone deck and improves general decision semantics
without using replay IDs, opponent names, or matchup-specific branches.

## General improvements

- Preserves attackers, search, and setup cards when a rule forces discards.
- Draws the maximum free compensation after an opponent mulligan.
- Builds Energy toward the Crustle that Dwebble's Ascension will create.
- Attaches Mist before a profiled effect attack even when the Active can
  already use a cheaper attack.
- Chooses Dwebble instead of an unusable Crustle in a one-Pokémon Poké Pad
  recovery state.
- Retreats before Froslass Checkup only when the current Active is guaranteed
  to fall and an equally strong ready replacement survives.
- Retains V4-V7's bounded setup and hard guarantee to attack before ending an
  attack-capable turn.

## Final validation

- Every-replay suite: 389/389 winning matchup majorities; 3,770-120 across
  3,890 trials (96.92%); 0 errors, timeouts, or abandoned attack turns.
- Head-to-head versus V7: 2,701-2,292-7 over 5,000 games (54.10% decisive).
- Beat every preserved V1-V8 snapshot in the final tournament.
- Alakazam stress: 1,489-511 over 2,000 games.

The replay suite is counterfactual because the bundled simulator cannot inject
Kaggle seeds, shuffled state, Prize cards, or the original opponent source.
See `artifacts/V9_FINAL_REPORT.md` for the exact protocol and complete results.

## Package

Build and validate with:

```bash
python3 tools/build_submission.py \
  --agent-dir agents/v9_candidate \
  --output artifacts/submission_9.tar.gz
```

The validated archive contains only `main.py` and `deck.csv`.
