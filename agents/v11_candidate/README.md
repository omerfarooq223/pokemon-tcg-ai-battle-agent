# V11 final candidate

V11 is the upload candidate built after the poor live results of deployed V10
and V10 Final. It does **not** reuse Mega Lopunny's three-prize, Fighting-weak
engine. It returns to the strongest proven one-prize Crustle/Cornerstone shell
and adds the general board-resilience behavior that the newest losses require.

## What changed

- A viable backup attacker/evolution line is established before bounded setup
  gives way to an attack whenever the visible hand/menu can do so.
- Buddy-Buddy Poffin stops once three viable lines are established, preventing
  both one-board collapse and uncontrolled Bench flooding.
- Poké Pad and direct Dwebble placement receive explicit backup-line priority.
- Discard selection preserves the resources needed to finish visible attacker
  lines rather than discarding the highest-value cards first.
- Prize-aware decisions now read the simulator's real `prize` zones. The older
  `prizeCount` fallback is retained only for compatibility.
- The exact expected 60-card deck is embedded and verified, so wrong working
  directories or a missing `__file__` cannot silently load a different deck.

Runtime behavior uses visible state and card mechanics only. It contains no
opponent names, replay IDs, team names, or identity-specific branches.

## Why this structure was selected

The newest labeled evidence raised V10 Final to 7-12 and deployed V10 to 8-13.
Both snapshots reproduced their recorded actions exactly, so another loader or
attack-priority patch would not address the failure. V10 Final is 0-5 in the
supplied Mega Lucario matchup, and repeated losses ended through board
exhaustion while a Basic was held or while a lone three-prize Lopunny attacked.

Naive copies of the recent Alakazam and Mega Lucario decks were rejected because
their local policies collapsed outside the matchup that motivated them. Three
Diggersby mixes were also rejected because their 140-damage benefit came with a
clear direct regression against the proven Crustle shell. V11 instead uses the
candidate that cleared the balanced recency-weighted screen without adding a
new deck liability.

## Final local confirmation

All games alternated seats. Approximate stress pilots are diagnostics, not
recovered leaderboard source and not guarantees of Kaggle rating.

| Opponent | V11 result | Games | Timeouts | Abandoned attack turns |
|---|---:|---:|---:|---:|
| V5 historical-peak snapshot | 489-511 | 1,000 | 0 | 0 |
| V6 | 510-490 | 1,000 | 0 | 0 |
| V7 | 507-488-5 | 1,000 | 0 | 0 |
| Recent Alakazam stress deck | 328-172 | 500 | 0 | 0 |
| Recent Mega Lucario stress deck | 484-16 | 500 | 0 | 0 |
| flg current-top control pilot | 452-48 | 500 | 0 | 0 |
| Rmy pure-Ogerpon pilot | 500-0 | 500 | 0 | 0 |
| Sixth Sense spread/counter pilot | 460-40 | 500 | 0 | 0 |
| James multi-attacker pilot | 499-1 | 500 | 0 | 0 |

The V5 direct comparison is essentially even and is reported rather than
hidden. The reason to upload V11 instead of another V10 repair is its structural
fit to the newest failure clusters, its one-prize game plan, and its zero-
abandonment safety record—not a claim that local simulation guarantees an
exponential ladder jump.

## Validation and hashes

- Raw Kaggle-style execution without `__file__`: passed.
- Exact 60-card validation: passed.
- Python compilation: passed.
- Focused regression suite: 31/31 passed.
- Archive contents: only `main.py` and `deck.csv`; both match source bytes.
- `main.py`: `bd19ce350aba677351b64d6431289e9c5648375e52a993cedfdf2c5c161d11be`
- `deck.csv`: `26243a8a4ea0a825bbcb475564140f8d2eb347ef2c5dd61139886ccbe7876eb5`
- `submission_11.tar.gz`: `8bdd2e49a8f8b092510cdda7261306739ddffdb3bbfafbab464b99317203eb97`

Upload `artifacts/submission_11.tar.gz`. Freeze this source and archive after
submission; every later gameplay change belongs in V12.
