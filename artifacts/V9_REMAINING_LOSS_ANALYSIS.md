# V9 remaining-loss analysis

## Scope and confidence

This is a read-only audit of the corrected V7 three-trial evaluation
(`v7_every_replay_389_3x.*`) and the 21-game supplied-replay audit. No new
simulation was run.

- V7 scored **1,126-41 (96.49%)** across 1,167 local matches and won the
  per-replay majority on **386/389** replays.
- All three majority-loss rows had **zero abandoned attack turns**. Their
  failures are not a return of the V1-V3 attack-selection bug.
- A three-trial majority is weak evidence. An independent discard-only V9 pass
  produced the identical aggregate **1,126-41** but moved the per-replay
  majority to 384-5; for example, `88456712` changed from 1-2 to 3-0 without a
  matchup-specific fix. Initial shuffles, Prize cards, coin flips, Kaggle seed,
  and original opponent code cannot be reproduced locally.
- Consequently, exact live evidence establishes root causes; the
  counterfactual rows identify stress clusters and candidates for larger
  reruns, not deterministic replay failures.

## Three V7 majority losses

| Episode | 3x result / fidelity | Evidence-backed root cause | General fix status |
|---:|---|---|---|
| `88264935` | 1-2; 75.0% scripted | Mega Starmie ex/Cinderace/Crushing Hammer. Both local losses ended with no Pokémon; one never reached an attack and the other attacked once. In the live game the agent established only one Dwebble/Crustle line. Nebula Beam deals 210 through defensive effects, while Crustle's 120 cannot efficiently clear 330 HP (or 430 HP with Hero's Cape). | **Unfixed structural race.** Needs a proven higher-damage/high-survivability line or resource engine. Search/attack scoring cannot repair the damage and durability gap. |
| `88316214` | 1-2; only 37.4% scripted | Duraludon/Archaludon ex/Cinderace. The local outcomes ranged from a turn-2 single-board loss with no attack, through a turn-29 win, to a turn-48 prize loss whose first attack was turn 35. In the live game V5 did build four Dwebble, but non-ex Duraludon's Raging Hammer scaled to 260 after being damaged and exhausted the board. Crustle's 120 also misses the relevant 130-140 HP knockout breakpoint. | **Unfixed, but low-confidence as a 3x majority.** A reliable 140-damage line/Cornerstone access is the general response; do not add a Duraludon-specific branch. Rerun at high trial count before treating it as a regression gate. |
| `88456712` | 1-2; 45.5% scripted | Alakazam/Dunsparce/Enhanced Hammer. The live trace exposes a genuine search bug: with only a Hero's Cape Cornerstone in play, no Bench, and no Dwebble in hand, Poké Pad offered four Dwebble and four Crustle; V7 selected Crustle. The dead evolution card never formed a backup line. Alakazam then placed counters through protection. V7 still attacked on every offered turn. | **General bug found, not yet safely fixed.** Isolate one narrow rule: when Poké Pad offers both cards, no Dwebble exists in play/hand, and the board has only one viable Pokémon, select Dwebble over unusable Crustle. The broader board-resilience experiment must remain rejected because it regressed the 389-replay lean pass from 383-6 to 376-13. |

## Contested rows (2-1, one loss in three trials)

There are **35** additional rows with one local loss. They are stochastic
warnings, not confirmed failures. Exact episode grouping:

| Cluster | Count | Episodes | General cause |
|---|---:|---|---|
| Alakazam/Dunsparce control | 19 | `88146122`, `88155167`, `88157416`, `88183542`, `88192025`, `88206818`, `88245592`, `88253320`, `88254686`, `88264373`, `88280581`, `88281365`, `88323658`, `88329324`, `88336523`, `88388662`, `88389031`, `88480123`, `88702243` | Powerful Hand places counters through both protection Abilities; Enhanced Hammer delays setup; Crustle's 120 misses 140-HP Alakazam. Xerosic helps only when drawn and timed before the large-hand attack. |
| Mega Starmie variants | 3 | `88255773`, `88334078`, `88481733` | Effect-ignoring 210, Hammer/bench pressure, and a 330-430 HP target produce the same structural race as majority loss `88264935`. |
| Duraludon/Archaludon variants | 4 | `88319853`, `88324102`, `88483990`, `88513116` | Non-ex Raging Hammer punishes the 120-damage two-shot; Full Metal Lab and healing make the breakpoint worse. Results remain volatile because this shell is also beaten frequently. |
| Crustle/slow control family | 3 | `88170362`, `88475900`, `88518164` | Long healing/Hammer mirrors and Great Tusk/Crustle races; no repeated policy defect is established. |
| Other one-off stress | 6 | `88187788`, `88249366`, `88251535`, `88260674`, `88324221`, `88452950` | Two Mega Abomasnow/Kyogre rows plus one each of Iono energy scaling, Mega Lucario tempo, Rocket/Spidops, and Grimmsnarl/Munkidori/Froslass. One loss each is insufficient to justify a branch or deck change. |

Twenty of all 38 non-perfect rows are Alakazam and four are Mega Starmie.
That concentration agrees with the live corpus and is much stronger evidence
than any individual 2-1 result.

## Supplied V8 live losses

V8 went 7-4 in the supplied batch and converted **93/93** attack-capable
turns. The four losses therefore add structural/setup evidence:

| Episode | Root cause | Fix assessment |
|---:|---|---|
| `88527351` | Grimmsnarl/Munkidori/two Froslass exhausted a two-line board after V8 took five prizes. On turn 14 the active Crustle had 20 HP, a ready benched Crustle had 100 HP, and two Froslass were in play. | Board depth and counter management are general concerns. A retreat rule should be promoted only when the replacement has a materially better attack/defensive state; retreating a Pokémon that will still be knocked out by Checkup does not itself save a prize. |
| `88528562` | Three complete Crustle lines lost to Mega Starmie's effect-ignoring 210 plus Hammer pressure. Three 120-damage attacks left the Cape Starmie at 10/430, and V8 took no prizes. | Structural and unfixed. Requires a competitive damage/durability engine, not another threshold tweak. |
| `88727264` | The same classic Grimmsnarl shell exhausted a maximum two-Pokémon board. V8 drew no Poffin or Poké Pad. On turn 14 its active Crustle was at 10 HP with a ready 120-HP Cornerstone benched and one Froslass in play. | Mostly setup variance plus counter pressure. Test only bounded, provable backup-line logic; do not blindly fill the Bench. |
| `88702243` | Against Alakazam, mandatory discard context 8 offered two Crustle, Lillie, Ice Cream, and Cook. The policy discarded **both Crustle**, because it reused positive card-pick scoring for a discard decision. V8 then made five Ascension attacks but never a damaging attack. | **Fixed in the current V9 policy:** discard-preservation scoring now keeps attackers/search and discards lower-value healing first. This is a general semantic correction, not a replay-specific hack; retain it subject to full-suite validation. |

The top-player `flg` evidence does not supply a ready deck fix. Its
Crustle/Cornerstone/Mega Kangaskhan shell lost four Grimmsnarl games
(`88764905`, `88754803`, `88726741`, `88714591`) and one Alakazam game
(`88707615`), while also abandoning 5/57 attack-capable turns. Its attacker
diversity is useful research evidence, but its exact deck/policy should not
replace V9.

## Ranked general actions

1. **Keep the mandatory-discard correction.** It repairs an inverted objective
   in every forced-discard menu and directly addresses `88702243`.
2. **Isolate the Poké Pad target fix.** Correct the unusable-Crustle choice from
   `88456712` without importing the rejected broad board-building behavior.
3. **Preserve hard attack safety.** Neither the corrected sweep nor V8 live
   losses show an attack abandonment; every candidate must retain this
   invariant.
4. **Treat Alakazam, Starmie, and the 130-140 HP breakpoint as structural deck
   research.** A broadly valid 140-plus damage line and better survivability
   could address Alakazam, Trevenant, and Duraludon together. Existing
   Mega-Kangaskhan/flg splices did not establish that improvement.
5. **Do not overfit three-trial noise.** High-trial reruns should focus first on
   `88264935`, `88316214`, and `88456712`, then validate any promoted change
   against all 389 replays and direct V7 head-to-head. Low scripted fidelity
   makes `88316214` and `88456712` especially unsuitable for replay-specific
   logic.
