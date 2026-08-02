# V10 candidate

V10 is a new Mega Lopunny ex / Dudunsparce agent built from the current
leaderboard replay set. Runtime behavior uses visible state, card IDs, and card
mechanics only. It contains no player names, replay IDs, or opponent-identity
branches.

## Exact deck

- 4 Buneary, 3 Mega Lopunny ex
- 4 Dunsparce, 4 Dudunsparce, 1 Fan Rotom
- 4 Buddy-Buddy Poffin, 4 Ultra Ball, 4 Pokégear 3.0, 4 Poké Pad
- 4 Air Balloon
- 3 Boss's Orders, 1 Xerosic's Machinations
- 4 Hilda, 4 Lillie's Determination, 4 Wally's Compassion
- 4 Mist Energy, 3 Spiky Energy, 1 Enriching Energy

## Why it is structurally different

- Dunsparce/Dudunsparce repeatedly converts board pieces into draw-three
  cycles instead of relying on the six-Basic Crustle opening.
- Thirteen Basics reduce the seven-card no-Basic opening probability from
  45.86% in the recent six-Basic lists to 16.28%.
- Air Balloon and one-Energy attackers create 230-damage Gale Thrust pivot
  turns.
- Spiky Hopper is explicitly powered to break Crustle/Cornerstone-style damage
  prevention rather than looping blocked attacks.
- The planner preserves a ready attacker through active Run Away Draw,
  complementary Basic searches, and guarded promotion/retreat choices.
- Pre-attack setup is bounded, and every final validation run had zero turns
  that offered an attack but ended without one.

## Final local gates

All matches used the official simulator with alternating seats.

| Opponent | W-L-D | Games | Timeouts | Abandoned attack turns |
|---|---:|---:|---:|---:|
| V5 | 879-119-2 | 1,000 | 0 | 0 |
| V6 | 917-83-0 | 1,000 | 0 | 0 |
| V7 | 441-58-1 | 500 | 0 | 0 |
| V8 fixed | 908-90-2 | 1,000 | 0 | 0 |
| V9 | 1,780-215-5 | 2,000 | 0 | 0 |
| Current flg exact-deck pilot | 461-37-2 | 500 | 0 | 0 |
| Current Rmy exact-deck pilot | 309-689-2 | 1,000 | 0 | 0 |
| Current Sixth Sense exact-deck pilot | 473-527-0 | 1,000 | 0 | 0 |
| Current James toolbox exact-deck pilot | 617-378-5 | 1,000 | 0 | 0 |

The Rmy pure-Ogerpon pilot remains the clearest local weakness. The four
top-five pilots are state-driven stress approximations, not recovered source,
so their percentages are matchup diagnostics rather than ladder forecasts.

## Package

The upload archive is `artifacts/submission_10.tar.gz`. It contains only
`main.py` and `deck.csv`; its member hashes match this directory.
