# V13 candidate

V13 hardens the strongest supplied live shell instead of replacing it with an
unproven deck. It uses V11's exact 60-card one-prize Crustle/Cornerstone list
(three Xerosic and four Waitress) and a corrected V12-derived planner.

## Changes

- Detects visible damage-counter/spread pressure anywhere on the opposing
  board, including Benched Dragapult ex and Munkidori, before deciding whether
  a third viable attacker line is required.
- Treats a missing `deckCount` field as unknown rather than as an empty deck.
- Uses an attack-first emergency action if an unforeseen policy exception
  occurs while an attack is legal.
- Allows four useful, bounded pre-attack actions. The repeated-menu guard,
  prize closeout guard, and empty-deck guard still force attack completion.
- Uses only visible state and card mechanics. There are no player names,
  episode IDs, replay IDs, or opponent-specific runtime branches.

## Supplied replay reconciliation

- V11: 39 unique live games, 21 wins and 18 losses.
- V12: 8 unique live games, 4 wins and 4 losses. One duplicate file in the
  supplied archive was discarded.
- New top-player archive: 47 unique completed games; 9 duplicate pairs were
  discarded.
- Full preserved corpus: 629 unique completed episodes and 0 duplicate files.

Frozen V11 reproduced all 1,661 recorded decisions exactly and attacked on all
237 attack-capable turns. Frozen V12 reproduced all 321 decisions exactly and
attacked on all 51 attack-capable turns. The submitted agents were therefore
executing correctly; their losses are strategic matchup losses rather than a
loader or attack-skipping defect.

## V13 validation

- 42 focused and project regression tests passed.
- V13 returned 0 invalid choices and raised 0 policy exceptions across 1,982
  recorded V11/V12 decision states. It attacked on all 288 attack-capable
  turns.
- New-top counterfactual pass: 44 wins and 3 losses across 47 matchups, with 0
  errors and no abandoned attack turn. The three one-trial losses stabilized
  at 78-22, 86-14, and 76-24 over 100 trials each. These are approximate
  simulations, not exact Kaggle replay re-executions.
- Direct alternating-seat screens: 260-240 vs V11 and 248-252 vs V12 over 500
  games each. Five separate 1,000-game development batches of the promoted
  V11-deck/four-action configuration totaled 2,581-2,408-11 vs V11. It should
  be described as a modest local improvement, not a guaranteed ladder gain.
- It beat V1 448-51-1, V4 286-214, V5 284-215-1, V6 270-229-1, V7 259-241,
  and V8-fixed 287-213 in 500-game screens. V9 and both three-prize Lopunny
  agents remain adverse local stress tests, despite those agents' poor live
  records.
- Raw Kaggle-style loading, Python compilation, exact 60-card validation,
  archive construction, two-member archive inspection, and member-hash checks
  passed.

The 8 GB machine could not retain the official native simulator for a single
629-replay process; macOS stopped both the monolithic run and a multi-batch
parent after 48 and 30 episodes respectively. The final coverage therefore
uses bounded direct batches, the 47 newest top matchups, and the full lightweight
recorded-state policy audit rather than making a misleading full-corpus claim.

## Artifact

- Archive: `artifacts/submission_13.tar.gz`
- `main.py` SHA256: `28176477c169cc8eadd769e2f3458b1449889f38f4d441d4b758d720e4f7e8d8`
- `deck.csv` SHA256: `26243a8a4ea0a825bbcb475564140f8d2eb347ef2c5dd61139886ccbe7876eb5`
- Archive SHA256: `7c88f1cce3625ff1e81af96989ac0956287359cdaa2d35d4de83889b8544f52c`
