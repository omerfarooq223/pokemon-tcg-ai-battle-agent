# V12 candidate

V12 is the challenger built from the frozen V11 one-prize Crustle/Cornerstone
shell. It keeps V11's board-resilience planner, prize-zone handling, discard
preservation, exact embedded-deck verification, and bounded attack-first guard.

## Changes from V11

- Adds one Xerosic's Machinations by replacing one Waitress, improving the
  chance of shrinking large hands before Powerful Hand resolves.
- Requires a third viable line against visible damage-counter/spread attackers
  (Powerful Hand and Shadow Bullet mechanics), while retaining the normal
  two-line opening against ordinary boards.
- Runtime uses visible mechanics only. It contains no opponent names, replay
  IDs, team names, or identity-specific branches.

## Replay evidence

The V11 import supplied 30 new Our games and 25 valid Top games. Seven new
losses use the Alakazam/Powerful Hand family, and the trace endings show that
two visible lines are not always enough when damage counters bypass both
Crustle and Cornerstone protection. The Top archive also adds repeated
Grimmsnarl/Munkidori, Ogerpon, Lucario, and high-HP energy-race shells.

## Validation

- Focused V11 + V12 policy tests: passed (8 tests).
- Python compilation: passed.
- Replay corpus scan: 565 unique valid completed episodes, 0 invalid files,
  0 conflicting duplicates. This includes the imported 30 Our and 25 Top
  replays.
- The full counterfactual simulator suite is blocked in this checkout because
  the competition `cg` runtime is not present; no simulated win-rate claim is
  made until it is restored.
