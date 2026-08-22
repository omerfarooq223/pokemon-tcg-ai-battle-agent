# V10 Final live audit through episode 89396175

## Verdict

V10 Final is 5-10 over the first fifteen supplied live games. The second batch
was 4-8. This is poor live performance and invalidates the local promotion
conclusion.

Kaggle is executing the intended artifact. The exact 60-card deck appeared in
all fifteen games, and the frozen local source reproduced all 629 recorded
decisions. V10 Final attacked on all 66 attack-capable turns, with no abandoned
turns, invalid actions, or timeouts. The problem is strategy and deck structure,
not loading or attack skipping.

## Second batch

Wins:

- 89396175 and 89392995: Dragapult variants.
- 89395114 and 89393517: Crustle-centered variants.

Losses:

- 89395645 and 89391927: Dragapult variants. The first was another lone-board
  knockout after Run Away Draw removed Dudunsparce before a held Buneary was
  benched; the second was a spread-damage prize race.
- 89394585 and 89390867: Mega Lucario. Together with 89386619, V10 Final is 0-3
  against supplied Lucario games. Fighting Weakness and the three-prize Mega
  rule let Lucario finish the game with two Lopunny knockouts.
- 89394058: Festival Grounds/Dipplin. V10 opened a lone Buneary, found no board
  search, never reached an attack menu, and lost when the only Pokémon was
  knocked out.
- 89392464: Mega Starmie/Cinderace. V10 attacked on every offered turn but lost
  the prize race to higher damage and pressure.
- 89391400: Crustle/Kangaskhan control. V10 took five prizes but repeatedly
  operated with a lone Mega Lopunny and eventually lost by board exhaustion
  while the opponent still had two prizes.
- 89390331: Mega Froslass/Starmie. Wally healed the lone Lopunny twice, but no
  durable Bench was established and the final knockout ended the game with the
  opponent still holding one prize.

## Root causes

1. **Three-prize brittleness.** Two Mega Lopunny knockouts end a game. Several
   opponents do not need to clear the low-value setup board.
2. **Fighting Weakness.** Mega Lucario is a demonstrated hard live counter at
   0-3, not an isolated draw.
3. **Board-exhaustion policy.** Five of ten live losses ended with no Pokémon in
   play while the opponent still had prizes. The planner sometimes uses Active
   Run Away Draw before playing a held Basic, and its attack guard can suppress
   safe bench development after an attack becomes legal.
4. **Spread and counter placement.** Dragapult and Alakazam punish 70-HP setup
   Pokémon or bypass ordinary damage defenses. Wally can extend one attacker
   but cannot repair a board that has disappeared.
5. **Insufficient damage without a fresh pivot.** Gale Thrust drops to 60 after
   the switching window; against 330-440 HP Mega attackers this loses the prize
   race even when every legal attack is taken.

The repaired Wally engine is real: the second batch used Wally eleven times and
retreated six times. It helped win long Dragapult games, but it did not solve
the deck's prize liability, weakness, or board survival. Therefore another
narrow Wally or attack-priority patch is not the correct next step.

## Recommendation

Do not final-select V10 Final on current evidence. Freeze it and build V11 as a
structural challenger. At minimum, V11 needs a general safe-Bench invariant
before self-removing abilities or lone-attacker attacks. More importantly, it
needs a deck plan that does not lose after two three-prize knockouts and a
mechanic-level answer to Fighting attackers, spread damage, and counter
placement. Preserve V5 as the historical 965-peak fallback.
