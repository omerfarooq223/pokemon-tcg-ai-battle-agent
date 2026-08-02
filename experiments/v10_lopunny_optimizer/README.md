# V10 Lopunny optimizer experiment

This directory is an isolated policy experiment for the exact 60-card
Majkel1337 Mega Lopunny ex / Dudunsparce deck. It does not contain player
names, episode IDs, replay-specific decisions, or identity branches.

## Material policy corrections

- Complete the Active Mega Lopunny's second Energy when a visible opposing
  Active has a damage-prevention effect. This enables Spiky Hopper instead of
  repeatedly using a blocked Gale Thrust into Crustle or Cornerstone.
- Prefer the one-Energy pivot line when Gale Thrust's 230 damage reaches a
  knockout that Spiky Hopper's 160 does not.
- Treat both global turns 1 and 2 as a player's possible first turn for Fan
  Rotom setup and always use a legally offered Fan Call.
- Make multi-Basic searches choose complementary Buneary and Dunsparce lines.
- When Ultra Ball has already secured the evolution for a lone attacker,
  search a second Basic before taking redundant evolution pieces.
- Prevent three irreversible attack losses: unsafe Wally healing of the
  Active, removing the last Bench target for Trading Places/Run Around, and
  promoting an unpowered Pokemon after an Active Dudunsparce uses Run Away
  Draw.
- Keep bounded pre-attack setup (default cap 12) while forcing the attack after
  the budget, a repeated menu, or a long turn.

## Official-simulator results

All comparisons alternate the primary agent between seats. `abandoned` is the
strict existing audit metric: a turn offered any attack but ended without one.

| Opponent | Games | W-L-D | Seat 0 | Seat 1 | Abandoned | Timeouts |
|---|---:|---:|---:|---:|---:|---:|
| V9 | 2,000 | 1,780-215-5 | 909-89 | 871-126 | 0 | 0 |
| V7 | 500 | 441-58-1 | 226-23 | 215-35 | 0 | 0 |
| current root V10 during experiment | 500 | 286-208-6 | 136-111 | 150-97 | 0 | 0 |
| top-five flg pilot | 500 | 461-37-2 | 224-24 | 237-13 | 0 | 0 |
| top-five Rmy pilot | 1,000 | 309-689-2 | 202-297 | 107-392 | 0 | 0 |
| top-five Sixth Sense pilot | 1,000 | 473-527-0 | 271-229 | 202-298 | 0 | 0 |
| top-five James toolbox pilot | 1,000 | 617-378-5 | 315-181 | 302-197 | 0 | 0 |

Because every run has zero abandoned attack turns, abandoned damaging attack
turns are also zero. The Rmy pure-Ogerpon pilot remains the clear structural
weakness and must not be hidden by the replay evaluator. This candidate is a
large direct improvement over recent Crustle agents and the first V10 draft,
but it is not proven to dominate every current top-five archetype.

On ten Majkel replays held out from the two flg-policy traces used for detailed
diagnosis, exact recorded-action agreement was 384/773 (49.68%). Exact action
agreement is a deliberately strict secondary diagnostic: alternative setup
orders can reach the same state, and feeding recorded observations after a
different predicted action makes later per-turn memory counterfactual.
