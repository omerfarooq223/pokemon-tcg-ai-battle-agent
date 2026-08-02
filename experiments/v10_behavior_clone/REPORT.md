# V10 Lopunny behavior-clone experiment — rejected

## Scope

- Training source: all 12 unique `Majkel1337` appearances in the supplied
  `Top 5.zip` archive (7 wins, 5 losses).
- Extracted decisions: 971 total, including 633 main-menu decisions.
- The fitted runtime uses only visible public state: turn flags, hand card IDs,
  board counts, HP/Energy summaries, prizes, and the current legal-action menu.
  It contains no player names, replay IDs, episode-specific branch, or opponent
  identity feature.
- Model: 24 compact randomized classification trees blended with the standalone
  Mega Lopunny/Dudunsparce card-semantic planner. Serial numbers and option
  indexes are deliberately excluded from the learned action label.

## Agreement results

- In-sample semantic agreement: **843/971 (86.82%)**.
- Leave-one-episode-out main-menu agreement: **316/633 (49.92%)**, versus the
  rule planner's 196/633 under the same semantic comparison.
- Combining the held-out main-menu prediction with the unchanged deterministic
  non-main targeting rules gives **580/971 (59.73%)** overall semantic
  agreement. The corresponding rule-only result was 460/971 (47.37%).

This is a real improvement in held-out action imitation, but it did not become
a stronger game-playing policy.

## Direct swapped-seat results

The best-performing learned setup allowance (`V10_CLONE_DEFERRALS=8`) produced:

| Opponent | Clone | Opponent | Draws |
|---|---:|---:|---:|
| final V10 optimizer | 75 | 223 | 2 |
| V9 | 58 | 242 | 0 |
| flg top-five pilot | 109 | 191 | 0 |
| Rmy top-five pilot | 22 | 277 | 1 |
| James toolbox pilot | 143 | 157 | 0 |
| Sixth Sense pilot | 81 | 217 | 2 |

A separate 300-game attack audit against the final optimizer finished
61-234-5, with 0 timeouts but 4 abandoned attack-capable turns. Because that
violates the project safety gate, the checked-in runtime defaults to immediate
attack conversion (`V10_CLONE_DEFERRALS=0`). The strict configuration recorded
**34-257-9** against the optimizer with **0 abandoned attack turns, 0 missed
attack menus, and 0 timeouts**.

## Diagnosis and decision

The clone reproduced recorded actions but compounded small off-policy errors.
Its clearest local failure was cycling Dudunsparce and filling the Bench while
putting Energy on future Buneary targets instead of finishing the current
Lopunny. Recorded leaderboard states do not contain the counterfactual outcomes
needed to learn when that sequencing is safe. Increasing the learned setup
budget improved local win rate slightly but reintroduced abandoned-attack risk;
forcing attack safety made the already-poor direct record worse.

**Reject this experiment for V10.** It is retained as evidence that semantic
behavior agreement, even when honestly held out by episode, is not a promotion
metric. The reusable lesson is narrower: Dudunsparce cycling and free-pivot
Lopunny/Wally loops should be encoded as bounded state rules, with an explicit
override to finish an attack-ready Lopunny before powering a future Buneary.

## Validation

- `main.py` compiles.
- The exact 60-card deck validates.
- Kaggle-style raw execution without `__file__` passes.
- The submission builder produced a two-member diagnostic archive containing
  only `main.py` and `deck.csv` in `/private/tmp`; it is intentionally not a
  promotion artifact.
