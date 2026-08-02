# V5 candidate

V5 keeps V4's balanced Crustle/Cornerstone core and attack-safe planner. It
replaces two Cook with two Xerosic's Machinations and uses Xerosic only when
the opponent's visible hand size makes it useful.

The replay-wide robustness pass added two general Energy rules. V5 stops
attaching to a profiled attacker after its useful attack cost is fully paid,
preventing extreme Energy over-stacking in control games. It also uses the
actual effects of Grow Grass, Mist, and Spiky Energy: Grow Grass is preferred
on the Dwebble/Crustle line, Mist is preferred on a colored-ready Active facing
an observed effect-based attacker, and Spiky is the default Active protection
against ordinary damaging attackers.

No replay IDs, opponent names, or opponent-specific runtime branches are used.
