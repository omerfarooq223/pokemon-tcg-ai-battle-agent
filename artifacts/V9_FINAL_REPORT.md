# V9 final report

## Outcome

V9 is the strongest locally validated numbered agent in the project.

| Measure | Result |
|---|---:|
| Unique replays tested | 389 |
| Replay matchups with a winning majority | 389 |
| Replay matchups with a losing majority | 0 |
| Counterfactual trials | 3,890 |
| Trial results | 3,770 wins, 120 losses, 0 draws |
| Trial win rate | 96.92% |
| Evaluator errors / timeouts | 0 / 0 |
| Attacked turns / attack-capable turns | 100% / 100% |

The complete 389-row result table is in
`artifacts/v9_final_every_replay_389_10x.md` and the machine-readable version
is `artifacts/v9_final_every_replay_389_10x.csv`.

## What V9 changed

| General weakness | Root cause | V9 change | Validation |
|---|---|---|---|
| Valuable cards discarded | Positive card-pick scoring was reused for mandatory discards, inverting the objective. | Added discard-preservation scoring for hand-discard contexts 8 and 29. | Corrects supplied loss 88702243's exact menu; retained across the full suite. |
| Slow post-Ascension attacker | One-Energy Dwebble was considered fully paid even though its Energy remains on the resulting three-Energy Crustle. | Scores legal pre-Ascension Energy against future Crustle readiness and permits one bounded Active attachment. | 2,648-2,343-9 versus the prior V9 baseline over 5,000 games. |
| Mist protection skipped | The fully-paid cutoff ran before the threat-aware Mist logic and the attack whitelist excluded Active Energy. | Protective Mist is evaluated first and may be one bounded pre-attack action against profiled effect attackers. | Alakazam stress improved from 1,354-646 to 1,489-511. |
| Dead Poké Pad target | On a lone-Cornerstone board, Poké Pad selected Crustle without any Dwebble to evolve. | Selects Dwebble when both are offered and no Dwebble/Crustle line exists. | Exact replay state changes from Crustle to Dwebble; 187-13 versus 182-18 on a 200-trial focused screen. |
| Free mulligan cards declined | Numeric draw-count options tied and index zero meant drawing zero. | Selects the largest free draw count. | Correct option semantics; full 389-replay pass remained regression-free. |
| Doomed Froslass Active | The hard attack guard could not retreat before a guaranteed Checkup knockout. | Retreats only to a ready survivor with at least equal damage, unless the current attack wins the game. | Changes both supplied live failure states while preserving 100% attack-turn conversion. |

All changes are based on visible state and card mechanics. Runtime behavior
contains no episode IDs, opponent names, or opponent-specific branches.

## Comparison with every existing agent

| Opponent | Games | V9 W-L-D | Decisive win rate |
|---|---:|---:|---:|
| V1 | 1,000 | 880-120-0 | 88.00% |
| V2 | 1,000 | 991-9-0 | 99.10% |
| V3 | 1,000 | 996-4-0 | 99.60% |
| V4 | 1,000 | 629-370-1 | 62.96% |
| V5 | 1,000 | 566-433-1 | 56.66% |
| V6 | 1,000 | 555-442-3 | 55.67% |
| V7 | 5,000 | 2,701-2,292-7 | 54.10% |
| V8 recovery | 1,000 | 564-434-2 | 56.51% |
| V8 fixed/live | 1,000 | 596-402-2 | 59.72% |

Every pairing recorded zero abandoned attack-capable turns. Full metrics are
in `artifacts/v9_final_all_agents_h2h.md`.

## Residual trial losses

There are no replay-level majority losses. The 120 individual trial losses are
stochastic outcomes within otherwise winning replay matchups. The five closest
rows were rerun for 100 trials and all remained winning:

| Episode | 100-trial result | Root cause of residual losses | Fixed? |
|---:|---:|---|---|
| 88209048 | 90-10 | Alakazam places counters through protection when Mist is absent/removed and large hands rebuild. | Partially: Mist, discard preservation, and faster Crustle setup improved the matchup; the remaining card-draw/Hammer variance is structural. |
| 88316214 | 75-25 | Non-ex Duraludon's Raging Hammer scales after Crustle's 120-damage hit. | Partially: faster setup helps, but the 120-versus-130/140 breakpoint remains. |
| 88320896 | 93-7 | Long Duraludon/Archaludon/Cinderace resource race. | No additional change needed; V9 wins the matchup reliably. |
| 88355725 | 67-33 | Duraludon/Archaludon board-exhaustion race and setup variance. | Not fully; this is the largest residual weakness. Tested higher-damage deck packages regressed broad performance and were rejected. |
| 88513116 | 70-28-2 | Duraludon plus Full Metal Lab/healing worsens the same damage breakpoint. | Not fully; no general replacement cleared the full regression gate. |

The candidate was not changed after these reruns because Diggersby,
Mega Kangaskhan, Hop's Snorlax/Choice Band, Battle Cage, Hand Trimmer,
Night Stretcher, Pokegear, and other structural experiments either lost direct
comparisons, regressed the replay suite, or overfit one stress family.

## Replay protocol and limitation

The local API cannot exactly re-execute a Kaggle replay: `battle_start` accepts
only two 60-card decks and has no seed or state-injection argument. It cannot
restore the original shuffled order, opening hand, Prize cards, coin flips, or
opponent source.

For every replay the evaluator therefore:

1. Replaces the original project bot when its team alias is present; otherwise
   replaces the public replay's losing seat.
2. Preserves the opponent's exact 60-card deck, replacement seat, and original
   first-player seat whenever recoverable.
3. Semantically follows recorded opponent actions while they remain legal,
   then uses a generic legal fallback after trajectories diverge.
4. Runs each replay in a fresh subprocess and reports scripted-action fidelity,
   errors, timeouts, and attack coverage.

These are counterfactual robustness results, not a guarantee of Kaggle rating.
Live evaluation remains the final test.

## Package integrity

| File | SHA-256 |
|---|---|
| `agents/v9_candidate/main.py` | `a6041b6409c8280b35f13c502a28b5aa16358854204ee704a0cf0471b1d3fc57` |
| `agents/v9_candidate/deck.csv` | `26243a8a4ea0a825bbcb475564140f8d2eb347ef2c5dd61139886ccbe7876eb5` |
| `artifacts/submission_9.tar.gz` | `6b7a187d93dda84b2653654b6fa6ab7a1f8901592d3a1211cddee04f42934dfc` |

The archive passed raw execution without `__file__`, Python compilation,
exact 60-card validation, and archive-content validation. It contains only
`main.py` and `deck.csv`, and both member hashes match the source files.
