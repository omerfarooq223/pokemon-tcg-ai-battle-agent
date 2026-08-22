# V10 live audit through episode 89377182

Date: 2026-08-02

## Verdict

V10's first supplied live batch is **5 wins and 7 losses**. This is a 41.67%
observed win rate and is not a meaningful live improvement over V9's saved
7-10 record. Twelve games are too few to estimate the true win rate precisely
(the 95% Wilson interval is approximately 19.3%-68.0%), but the behavioral
evidence is already sufficient to reject V10 as a final-selection candidate in
its current form.

This is not a loader or archive failure. The frozen local V10 source reproduced
all **579/579** recorded Kaggle calls exactly, and every replay contained the
expected V10 deck.

## Replay record

| Episode | Result | Opponent archetype | First damaging attack | Attacks | Main lesson |
|---:|:---:|---|---:|---:|---|
| 89371270 | W | Great Tusk / Crustle | 3 | 9 | Spiky Hopper broke the protection matchup |
| 89371815 | L | Dragapult / Budew | 11 | 3 | Item lock delayed setup; spread took multiple small-board prizes |
| 89372365 | L | Cynthia's Garchomp | 4 | 3 | Two attacks were zero-damage switches; the first Lopunny loss ended the damage plan |
| 89372901 | W | Alakazam / Crustle | 7 | 6 | Slow start, but repeated Spiky Hopper stabilized |
| 89373427 | L | Alakazam | 3 | 3 | Powerful Hand removed the final Lopunny; no durable backup board |
| 89373970 | W | Crustle | 12 | 6 | Extremely late damage, then Spiky Hopper won the wall matchup |
| 89374507 | L | Grimmsnarl / Munkidori | 5 | 4 | Counter/spread pressure exhausted Lopunny without healing |
| 89375056 | L | Mega Abomasnow | 3 | 3 | Opponent healed and recycled attackers; V10 never took a prize |
| 89375591 | W | Mega Abomasnow | 3 | 4 | The same matchup is volatile rather than uniformly losing |
| 89376120 | L | Cynthia's Garchomp | 5 | 2 | A 10-HP Active Lopunny was powered again instead of rotated and healed |
| 89376649 | W | Alakazam | 3 | 7 | Two-Energy Spiky line survived the control race |
| 89377182 | L | Grimmsnarl / Munkidori | 5 | 5 | Repeated damaged Active Lopunny states never converted into Wally recovery |

V10 encountered 144 attack-menu decisions spanning 55 attack-capable turns and
attacked on all 55 turns. Three attacks were zero-damage Buneary/Dunsparce
switch attacks; the other 52 were damaging. There were zero abandoned attack
turns. The failure is therefore setup, recovery, pivoting, and prize trading,
not the old V1-V3 attack-skip bug.

## Material policy bug: the deck's Wally loop is disabled

V10's deck contains four Wally's Compassion, four Air Balloon, and low-retreat
pivots. The current leaderboard policy visibly uses these cards as a core
engine: move a damaged Mega Lopunny to the Bench, heal it with Wally, recover
its Energy to hand, power the new Active, and use the movement to activate
230-damage Gale Thrust.

Observed behavior on matched twelve-game samples:

| Policy | Retreats | Wally plays | Games using Wally |
|---|---:|---:|---:|
| Current exact-deck leaderboard replays | 46 | 17 | 9/12 |
| V10 live replays | 5 | 0 | 0/12 |

Wally was legally offered during at least one turn in **6 of V10's 7 losses**,
but V10 never selected it. Several were high-impact states:

- Episode 89371815, turn 11: Active Lopunny had 130/330 HP, zero Energy, an
  Air Balloon, and multiple replacement Pokemon. V10 attached Energy instead
  of healing 200 damage and preserving the three-prize attacker.
- Episode 89376120, turn 7: Active Lopunny had 10/330 HP, one Energy, and Air
  Balloon, with two healthy Lopunny on the Bench. V10 attached a second Energy
  to the dying Active and used Spiky Hopper. A free retreat, Wally heal, Energy
  recovery, attachment to the incoming Lopunny, and Gale Thrust pivot was the
  deck's intended general line.
- Episode 89377182 repeatedly offered Wally while Lopunny were damaged, but the
  policy continued ordinary evolution/attack setup and lost the two-Lopunny
  prize race.

Two V10 rules cause this behavior:

1. `retreat_score` rejects a retreat unless the destination is already a
   powered Lopunny. It therefore cannot use an unpowered Buneary, Dunsparce, or
   Lopunny as the intermediate pivot required by the Wally loop.
2. `supporter_value` gives Wally a large negative score whenever the Active
   Lopunny is damaged, even when a safe Bench target exists or a retreat-heal-
   reattach sequence is available.

The regression test named `test_active_wally_is_rejected` encodes this
overcorrection as an invariant. It should be replaced for V11 with positive
tests for safe Wally recovery sequences plus negative tests only for states
that genuinely cannot attack or preserve the board after healing.

## Structural live weaknesses

- Mega Lopunny ex gives up three prizes. Two knockouts end the game, so failing
  to heal or prepare a second attacker is much more expensive than local
  generic opponents represented.
- Cynthia's Garchomp went 2-0 against V10. Its Fighting attacks exploit
  Lopunny's Weakness and can remove a 330-HP three-prize attacker immediately.
- Grimmsnarl/Munkidori went 2-0 and Dragapult went 1-0. Spread and counters
  punish the many 70-HP setup Pokemon and make passive bench-building costly.
- V10 won both Crustle-centered matchups, confirming that Spiky Hopper's wall-
  breaking logic works. The agent is polarized, not uniformly broken.

## Why the local promotion gate failed again

The large V10-vs-V5/V9 scores mainly proved that V10 beats recent locally
piloted Crustle agents. Those agents were already poor live benchmarks. The
top-five pilots were approximations, and the chosen Lopunny planner matched
only 49.68% of held-out recorded actions. The local optimizer then promoted a
rule that looked safer in those simulations but contradicted the core retreat
and healing behavior repeatedly visible in the actual top policy.

Future promotion must include behavior-level engine invariants, not only win
rates against approximate opponents. For this deck, the minimum gate is:

- recognize and execute safe free-retreat -> Wally -> reattach -> Gale Thrust
  sequences;
- preserve a second attack-ready line before exposing a three-prize Active;
- separately stress Cynthia's Garchomp, Grimmsnarl/Munkidori, and Dragapult;
- compare decisions on the exact live states that V10 mishandled;
- retain zero invalid actions, timeouts, and abandoned attack turns.

## Recommendation

Freeze the submitted V10 snapshot and do not select it as a final submission on
the current evidence. The next code change belongs in V11. V11 should first
repair the general Wally/pivot state machine and validate it on these live
states; a deck replacement should be considered only after measuring whether
the repaired engine still loses the three-prize and Fighting-Weakness races.
