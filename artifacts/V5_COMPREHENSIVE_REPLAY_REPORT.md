# V5 comprehensive replay evaluation

## Outcome

- Replays evaluated: **287 of 287** unique saved episodes.
- Current V5 uniform full-suite record: **2,272 wins, 107 losses, and 1 draw (95.46% wins)** over 2,380 matches, with 0 timeouts and 0 abandoned attack-capable turns. The three non-winning ten-trial rows stabilized at 75-25, 74-26, and 84-16 over 100 trials.
- Final V6 uniform full-suite record: **2,767 wins, 102 losses, and 1 draw (96.41% wins)** over 2,870 matches. Every replay had a winning majority.
- Frozen-V5 uniform baseline: **2,128-122 (94.58%)** over the same 225 replay matchups at ten trials each.
- Original target-seat outcomes: **51 wins, 236 losses**.

## Fidelity and interpretation

The replay JSON contains Kaggle seeds, seats, decks, observations, and actions, but the supplied local battle API accepts only two decks and exposes no seed setter. Original submitted opponent source is also unavailable. The harness therefore preserves the replacement seat and exact opponent deck, follows the opponent’s recorded semantic action sequence whenever the counterfactual state offers an equivalent action, and uses the legal generic attack-first policy after divergence. These are repeated counterfactual simulations, not byte-for-byte deterministic replay re-executions. For our 84 episodes V5 replaced our saved agent; for the 149 public episodes V5 replaced the original loser.

## Validated changes

- Stop attaching Energy after a profiled attacker’s useful attack cost is fully paid. This removed the observed 13–16 Energy over-stacking pattern and reduced control-game resource waste.
- Prefer Grow Grass on Dwebble/Crustle, Mist on a colored-ready Active facing an observed effect-based attacker, and Spiky against ordinary damaging attackers. The threat set is derived from card mechanics, not opponents or replay IDs.
- If an attack menu reappears with zero cards left in deck, attack immediately instead of taking another optional setup action.
- The proposed broad Poffin-before-disruption rule was rejected: it gained only 1 win in 800 component games and regressed several matchups by creating extra prize targets.
- The first broad single-Pokémon Poké Pad guard was rejected after episode 88314138. Episode 88314664 then repeated the exact deterministic failure, so a narrower V6 safeguard was retained: only when the board has one Pokémon, Crustle is already in hand, and no benchable setup Pokémon is in hand does Poké Pad prefer a Basic instead of a redundant evolution.
- V6 replaces V5's final Cook with a third Xerosic's Machinations. This makes the already-bounded, state-driven hand-disruption line more consistent without changing when Xerosic is considered useful.
- Final V6 adds a promotion-only knockout rule: when Cornerstone Mask Ogerpon is already powered and its 140 damage immediately knocks out a visible 121-140 HP Active, it is preferred over Crustle's 120-damage line. The rule changes no search, benching, or Energy-attachment decisions.

## Validation beyond the replay suite

- Direct versus frozen V5 before the terminal guard: **2,760-2,233-7** over 5,000 swapped-seat games.
- Exact final V5 versus frozen V4: **568-429-3** over 1,000 swapped-seat games.
- Final 80-deck matrix: **4,532-261-7 (94.42% raw; 95.54% replay-frequency weighted)**, versus frozen V5’s 4,418-378-4 (92.04% raw); 0 abandoned attack turns and 0 timeouts.
- Replay-informed Alakazam stress: **1,286-714** over 2,000 games before the terminal-only guard; episode 88255227 stabilized at **78-22** over 100 final-source trials.
- Legacy/stress gates: 897-100-3 vs V1, 992-8 vs V2, 992-8 vs V3, 759-232-9 vs pure Crustle, 993-7 vs Grimmsnarl, and 387-13 vs random.
- Narrow V6 safeguard versus submitted V5: **2,511-2,485-4** over 5,000 swapped-seat games. On the matched 84-deck matrix it scored **4,762-273-5 (94.48% raw; 95.77% replay-frequency weighted)** versus V5’s **4,743-296-1 (94.11% raw; 94.80% weighted)**; both had 0 abandoned attack turns and 0 timeouts.
- The V6 safeguard scored **2,252-78 (96.65%)** over the uniform 233-replay suite, with its only unstable majority stabilizing at 84-16 over 100 trials. In 1,000 focused counterfactual trials of the two repeated live failure matchups it scored 922-78 versus V5's 930-70, so the aggregate improvement is not statistically decisive. It is retained because it fixes two independently observed deterministic live errors while remaining neutral-to-positive across the broad gates.
- Standalone V6 combines that safeguard with the third Xerosic. It scored **2,295-85 (96.43%)** on the 238-replay suite versus V5's **2,272-107-1 (95.46%)**, and **5,075-257-8 (95.04% raw; 95.25% replay-frequency weighted)** on the matched 89-deck matrix versus V5's **5,043-293-4 (94.44% raw; 93.72% weighted)**. Both V6 gates recorded 0 abandoned attacks and 0 timeouts.
- The third-Xerosic component beat the single-board-only candidate **2,585-2,409-6** over 5,000 swapped-seat games and improved the Alakazam stress result from **1,330-670** to **1,375-625**.
- Standalone V6 beat submitted V5 **5,123-4,865-12** over 10,000 swapped-seat games.
- After the corpus expanded to 243 replays, standalone V6 scored **5,126-271-3 (94.93% raw; 94.53% replay-frequency weighted)** on the matched 90-deck matrix, with 0 abandoned attacks and 0 timeouts.
- After the corpus expanded to 247 replays, standalone V6 scored **5,220-294-6 (94.57% raw; 95.47% replay-frequency weighted)** on the matched 92-deck matrix, with 0 abandoned attacks and 0 timeouts.
- After the corpus expanded to 251 replays, standalone V6 scored **5,333-305-2 (94.56% raw; 94.23% replay-frequency weighted)** on the matched 94-deck matrix, with 0 abandoned attacks and 0 timeouts.
- A fourth-Xerosic variant was rejected. Although it improved dedicated Alakazam stress to 1,449-551, it lost directly to current V6 2,441-2,545-14 and reduced the raw matrix to 94.61%. V6 therefore keeps three Xerosic and four Jumbo Ice Cream.
- After the corpus expanded to 287 replays, final V6 scored **5,884-294-2 (95.21% raw; 94.93% replay-frequency weighted)** on the matched 103-deck matrix, with 0 abandoned attacks and 0 timeouts.
- The promotion-only rule beat prior V6 **5,114-4,874-12** over 10,000 swapped-seat games. It improved episode 88325152's matchup from **870-129-1** to **876-124** over 1,000 trials and improved Alakazam stress from **3,450-1,550** to **3,478-1,522** over 5,000 games.
- Two broader Cornerstone setup rules were rejected. The unconditional version reduced the matrix to 5,834-341-5; the within-one-Energy version scored 5,839-339-2 and worsened the focused matchup. This is why the retained fix is limited to promotion decisions with a powered attacker.

## Live V5 record

The twenty-seven saved V5 games are **15 wins and 12 losses (55.56%)**. A prior Kaggle display still implies one older unsaved loss, so the live display may be 15-13; the saved corpus count is definitive. Episode 88318294 is a checksum-identical duplicate and is not counted twice. Across the saved games V5 selected an attack on every one of the 148 live attack-capable turns and recorded no invalid actions, timeouts, or abandoned attack turns.

- Episode 88313112 validates the intended Alakazam mitigation: V5 used Xerosic against 13- and 12-card hands, attacked on all seven offered turns, and won by deck-out.
- Episode 88314138 is the residual draw-dependent Alakazam weakness: V5 never drew Xerosic, had only one Pokémon in play, and Alakazam’s 200 damage counters bypassed Crustle’s protection.
- Episode 88313620 repeats the known Iono scaling weakness: Voltorb’s non-ex Voltaic Chain reached 200, 300, 340, and 380 damage as Lightning Energy accumulated across all Iono Pokémon. V5 used Ascension once but never reached a damaging attack before its board was exhausted.
- Episode 88314664 repeated the single-board search defect from 88314138. V5 had only Cornerstone in play and already held Crustle, but Poké Pad fetched a second Crustle instead of Dwebble. Mega Froslass ex then dealt 400 damage and ended the game before V5 reached an attack menu. This second independent occurrence justified retaining the narrow V6 safeguard described above.
- Episode 88315183 was a healthy win over Archaludon ex/Cinderace: V5 attacked on all 13 offered turns, used Xerosic against a 7-card hand, and finished with no skipped attack turn.
- Episode 88316214 was a volatile Archaludon/Cinderace loss. V5 attacked on both offered turns, but damaged non-ex Duraludon's Raging Hammer scaled to 260 and exhausted V5's board. Two other live games against closely related shells were wins, so no opponent-specific policy branch was justified.
- Episode 88317769 was another draw-dependent Alakazam loss. V5 attacked on all three offered turns but never drew Xerosic; Powerful Hand placed 280 and 400 counters through protection while the opponent's hand grew to 15. V6's third Xerosic addresses the general consistency issue and improved both Alakazam stress and the broad suite.
- Episodes 88318294 and 88320386 were further Alakazam losses. V5 attacked on all six combined offered turns, but opposing hands reached 17 and 16 cards and Powerful Hand placed 180-360 counters through protection. These reinforce V6's third Xerosic, but the fourth-copy experiment overcorrected and regressed broad performance.
- Episode 88319336 was a Dragapult ex/Budew/Crushing Hammer control loss. Budew temporarily blocked Items, Crushing Hammer constrained setup, and Phantom Dive spread counters around Crustle's direct-damage immunity. V5 attacked on both offered turns; this is a resource-denial matchup rather than an attack-selection bug.
- Episode 88319853 repeated the volatile Duraludon/Archaludon/Cinderace pattern. V5 attacked on both offered turns, but Crustle's damage powered Raging Hammer to 170-190. No narrow counter was added.
- Episode 88320896 was a long win over Duraludon/Archaludon/Cinderace with 11/11 attacks, confirming the matchup is volatile rather than uniformly losing.
- Episode 88321420 was a healthy win over Great Tusk/Crustle with 12/12 attacks.
- Episode 88321956 was another Duraludon loss despite 2/2 attacks. V6 improved this replay-derived matchup from 76-23-1 to 83-17 over 100 trials, but no narrower opponent-specific behavior was added.
- Episode 88322536 was another Alakazam loss and V5 first attacked only on turn 11. V6 improved the 100-trial counterfactual from 72-28 to 84-16 through its existing setup safeguard and third Xerosic.
- Episode 88323052 was a strong Alakazam win: V5 attacked on all six offered turns and used Xerosic against hands of 18 and 9 cards.
- Episode 88323585 beat Mega Lucario/Hariyama with 10/10 attacks.
- Episode 88324102 survived a long Duraludon/Archaludon game and attacked on all 15 offered turns.
- Episode 88324625 beat a Kangaskhan/Crustle shell with 3/3 attacks.
- Episode 88325152 lost to Hop's Trevenant/Snorlax despite attacking on all four offered turns. Crustle's 120 damage left the 140-HP Trevenant at 20 HP; Horrifying Revenge and Hop damage modifiers then reached 180-220 and one-shot Crustle. Final V6 addresses the general damage breakpoint only when a powered Cornerstone can be promoted for an immediate 140-damage knockout.

## Remaining stochastic loss modes

The current V5 uniform suite’s 107 individual losses occurred despite zero abandoned attack turns and zero timeouts. No replay-specific branch was added. The repeated weak clusters were:

| Episode | Opponent | Final record | Root cause | Fix status |
|---:|---|---:|---|---|
| 88170362 | まーやん | 7-3-0 | Pure-Crustle damage race: 120 damage versus 150/170 HP creates close two-hit and setup races. | Mitigated by Grow Grass/Spiky targeting; aggressive Poffin change was rejected for regressions. |
| 88192025 | Yushin Ito | 7-3-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88206818 | Team Rot-Weiß | 7-3-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88206895 | Team Rot-Weiß | 7-3-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88252076 | UBI=ISHI | 7-3-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88255227 | Aphrodite | 78-22-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88264972 | Team Rot-Weiß | 7-3-0 | Alakazam Powerful Hand damage counters bypass damage-prevention Abilities; Enhanced Hammer can remove Mist Energy. | Mitigated: Xerosic hand control, Mist targeting, Grow Grass durability, and attachment cap; not eliminated. |
| 88313620 | mage03 | 10-0-0 | Live Iono Voltorb scaled from Energy across the full opposing board and one-shot each developing attacker before V5 reached a damaging attack. | Not fixed: the general Iono-engine replacement was already rejected for severe broad regressions, and the new single-Pokémon guard also failed its adoption gate. |
| 88314138 | Soup | 10-0-0 | Live Alakazam placed 200 damage counters through Crustle’s protection while V5 had a one-Pokémon board and did not draw Xerosic. | Mitigated: Xerosic works when drawn, and the independently repeated redundant-search failure is addressed by the narrow V6 safeguard. |
| 88314664 | 🐱KittenLeague🐱 | 10-0-0 | V5 had a lone Cornerstone and Crustle already in hand, but Poké Pad fetched another Crustle; Mega Froslass ex dealt 400 before V5 reached an attack menu. | Fixed in the V6 safeguard by preferring a Basic only in the single-board, evolution-already-secured state; full-suite and matrix gates showed no broad regression. |
| 88316214 | wsdsby | 9-1-0 | Damaged non-ex Duraludon's Raging Hammer scaled to 260 and exhausted V5's board despite V5 attacking on both offered turns. | Not directly changed: related Archaludon/Cinderace games were wins, so an opponent-specific counter would overfit. V6 retained a 9-1 majority and improved the complete matrix. |
| 88317769 | knomura03 | 9-1-0 | V5 did not draw either Xerosic; Alakazam's large hand powered 280- and 400-counter attacks through protection. | Mitigated in V6 by replacing the final Cook with a third Xerosic. Alakazam stress improved from 1,330-670 to 1,375-625 and all broad gates improved. |
| 88318294 | CMK | 90-10-0 | Alakazam reached a 17-card hand and placed 320-360 counters through protection; V5's early Xerosic was disrupted before it could control the later hand. | Mitigated by V6's third Xerosic. A fourth copy was tested and rejected for direct and raw-matrix regressions. |
| 88319336 | Impala16 | 99-1-0 | Budew Item lock and Crushing Hammer slowed setup while Dragapult ex spread damage counters around Crustle's direct-damage immunity. | Not changed: V6 already wins this counterfactual overwhelmingly, and no broader safe policy change was established. |
| 88319853 | kumk | 74-26-0 | Crustle's attack damaged Duraludon, increasing Raging Hammer to 170-190 and winning the prize race. | Not directly changed: this matchup remains volatile, and opponent-specific avoidance would overfit. |
| 88320386 | 電気通信ポケモン大学 | 89-11-0 | Alakazam reached a 16-card hand and placed 180-320 counters through protection while Enhanced Hammer constrained Energy. | Mitigated by V6's third Xerosic; fourth copy rejected after broad regression testing. |
| 88321956 | Zac Plischka | 83-17-0 | Another damaged-Duraludon Raging Hammer race; V5 attacked on both offered turns. | No new logic: related live games include both wins and losses, and V6 already improves the matchup without an opponent-specific branch. |
| 88322536 | N.Y | 84-16-0 | Alakazam built a very large hand while V5's setup delayed its first attack until turn 11. | Mitigated by V6's existing third Xerosic and single-board safeguard; full-suite validation showed no regression. |
| 88325152 | CYLik | 876-124-0 | Hop's Trevenant has 140 HP, surviving Crustle's 120 by 20, then reaches 180-220 damage through Horrifying Revenge and Hop modifiers. | Fixed generally at promotion time: choose an already-powered 140-damage Cornerstone when it immediately crosses the visible knockout breakpoint. The full 287-replay suite, 103-deck matrix, direct comparison, Alakazam stress, and legacy gates all passed. |

## Replay-by-replay results

| Episode | Opponent | Original | Final record | Result | Comparison |
|---:|---|---:|---:|:---:|---|
| 88114269 | Dieter | loss | 10-0-0 | W | flipped loss |
| 88114272 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88135168 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88135718 | jiatu.l | loss | 10-0-0 | W | flipped loss |
| 88136757 | カントー地方マスター | loss | 10-0-0 | W | flipped loss |
| 88138839 | Brahim | loss | 9-1-0 | W | flipped loss |
| 88139351 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88139876 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88139877 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88139889 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88140397 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88140434 | Benarg | loss | 9-1-0 | W | flipped loss |
| 88140934 | Dominic Peel | loss | 10-0-0 | W | flipped loss |
| 88141449 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88141464 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88141972 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88142495 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88143033 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88143428 | Snow Yan | loss | 10-0-0 | W | flipped loss |
| 88143558 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88143960 | Yuminosuke Sato | loss | 9-1-0 | W | flipped loss |
| 88144074 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88144497 | curry panda ex | win | 10-0-0 | W | retained win |
| 88145058 | minoruno | loss | 10-0-0 | W | flipped loss |
| 88145588 | HATODADON | loss | 10-0-0 | W | flipped loss |
| 88145696 | PP kawada | loss | 10-0-0 | W | flipped loss |
| 88146122 | daiki_pyonkichi | loss | 8-2-0 | W | flipped loss |
| 88146648 | Jonathan Amdam | win | 10-0-0 | W | retained win |
| 88147191 | Thomas Cook | loss | 10-0-0 | W | flipped loss |
| 88147227 | junlee789 | loss | 10-0-0 | W | flipped loss |
| 88147702 | NorthStar | loss | 10-0-0 | W | flipped loss |
| 88148218 | sakura_atm | loss | 8-2-0 | W | flipped loss |
| 88148312 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88148790 | cherlilly | win | 9-1-0 | W | retained win |
| 88148861 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88149240 | AmeliaLL | loss | 10-0-0 | W | flipped loss |
| 88149380 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88149406 | THIRD PTCG Club | loss | 10-0-0 | W | flipped loss |
| 88149782 | Yohanchen | win | 10-0-0 | W | retained win |
| 88149906 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88150296 | BioMath | win | 10-0-0 | W | retained win |
| 88150868 | FabrizioFedericoni | loss | 10-0-0 | W | flipped loss |
| 88151481 | HSBMAX | loss | 10-0-0 | W | flipped loss |
| 88152037 | Nicola Li | win | 10-0-0 | W | retained win |
| 88152577 | Dancing_RYAN | loss | 10-0-0 | W | flipped loss |
| 88153002 | Satoluca | loss | 10-0-0 | W | flipped loss |
| 88153112 | Kyles Light | loss | 10-0-0 | W | flipped loss |
| 88153551 | Brian | win | 9-1-0 | W | retained win |
| 88153647 | ジェニファー | win | 10-0-0 | W | retained win |
| 88154072 | Gary | loss | 10-0-0 | W | flipped loss |
| 88154188 | yasuna | loss | 10-0-0 | W | flipped loss |
| 88154615 | currentbranch | loss | 8-2-0 | W | flipped loss |
| 88154720 | sai vineeth | loss | 10-0-0 | W | flipped loss |
| 88155167 | shiiin9 | loss | 8-2-0 | W | flipped loss |
| 88155258 | poket monster | loss | 10-0-0 | W | flipped loss |
| 88155735 | Junichi Saigou | loss | 10-0-0 | W | flipped loss |
| 88155807 | Koikoiiinami | loss | 10-0-0 | W | flipped loss |
| 88156264 | pickles0923 | loss | 10-0-0 | W | flipped loss |
| 88156364 | wonjae | win | 10-0-0 | W | retained win |
| 88156894 | pattikamo | win | 10-0-0 | W | retained win |
| 88157011 | __Taichicchi__ | loss | 9-1-0 | W | flipped loss |
| 88157416 | Leocthl | win | 10-0-0 | W | retained win |
| 88157484 | Saianiruth M | win | 10-0-0 | W | retained win |
| 88157952 | chenzhengy | win | 10-0-0 | W | retained win |
| 88170362 | まーやん | loss | 7-3-0 | W | flipped loss |
| 88181889 | AI部 | win | 10-0-0 | W | retained win |
| 88183542 | Yushin Ito | loss | 10-0-0 | W | flipped loss |
| 88187788 | EunchaeSong | win | 10-0-0 | W | retained win |
| 88189899 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88190488 | THIRD PTCG Club | loss | 10-0-0 | W | flipped loss |
| 88190720 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88191459 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88191506 | __Taichicchi__ | loss | 10-0-0 | W | flipped loss |
| 88191988 | KawattaTaido | loss | 10-0-0 | W | flipped loss |
| 88192025 | Yushin Ito | loss | 7-3-0 | W | flipped loss |
| 88192363 | pop-ketle | loss | 10-0-0 | W | flipped loss |
| 88192550 | LiamK | loss | 8-2-0 | W | flipped loss |
| 88193019 | __Taichicchi__ | loss | 10-0-0 | W | flipped loss |
| 88193372 | bono | loss | 9-1-0 | W | flipped loss |
| 88193551 | __Taichicchi__ | loss | 10-0-0 | W | flipped loss |
| 88193634 | NguyenThanhNhan | loss | 10-0-0 | W | flipped loss |
| 88195735 | Marshall Maximizer | loss | 10-0-0 | W | flipped loss |
| 88197859 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88197860 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88197906 | __Taichicchi__ | loss | 10-0-0 | W | flipped loss |
| 88199435 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88200003 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88201040 | LiamK | loss | 10-0-0 | W | flipped loss |
| 88201604 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88203591 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88204121 | JZ | loss | 10-0-0 | W | flipped loss |
| 88204232 | THIRD PTCG Club | loss | 10-0-0 | W | flipped loss |
| 88204771 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88204990 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88205283 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88205289 | ZhWing Fence | win | 10-0-0 | W | retained win |
| 88206332 | Azat Akhtyamov | loss | 10-0-0 | W | flipped loss |
| 88206818 | Team Rot-Weiß | loss | 7-3-0 | W | flipped loss |
| 88206895 | Team Rot-Weiß | loss | 7-3-0 | W | flipped loss |
| 88207928 | Dominic Peel | loss | 10-0-0 | W | flipped loss |
| 88208293 | Zhenyu Zhang | loss | 10-0-0 | W | flipped loss |
| 88208966 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88209048 | msd0110 | loss | 8-2-0 | W | flipped loss |
| 88209398 | Zhenyu Zhang | loss | 10-0-0 | W | flipped loss |
| 88209472 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88209993 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88210517 | JZ | loss | 10-0-0 | W | flipped loss |
| 88210975 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88211042 | Yushin Ito | loss | 10-0-0 | W | flipped loss |
| 88211566 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88212701 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88214700 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88215619 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88217155 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88217476 | KawattaTaido | loss | 10-0-0 | W | flipped loss |
| 88217824 | Marshall Maximizer | loss | 10-0-0 | W | flipped loss |
| 88220136 | zoroark190 | loss | 9-1-0 | W | flipped loss |
| 88220489 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88220566 | wwwwwwwwwwwwwwwwwwwwwwwwwwwwww | loss | 10-0-0 | W | flipped loss |
| 88221583 | NekoChan-NekoChan | loss | 10-0-0 | W | flipped loss |
| 88221669 | __Taichicchi__ | loss | 10-0-0 | W | flipped loss |
| 88222802 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88223081 | macaron | loss | 10-0-0 | W | flipped loss |
| 88223586 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88224733 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88224901 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88225199 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88227532 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88227555 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88230163 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88230176 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88230489 | zoroark190 | loss | 10-0-0 | W | flipped loss |
| 88231229 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88232593 | Budew | loss | 10-0-0 | W | flipped loss |
| 88232765 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88233128 | Luca | loss | 10-0-0 | W | flipped loss |
| 88234701 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88234900 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88235276 | Luca | loss | 10-0-0 | W | flipped loss |
| 88237853 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88238542 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88239078 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88239095 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88239132 | JZ | loss | 10-0-0 | W | flipped loss |
| 88241784 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88243841 | THIRD PTCG Club | loss | 10-0-0 | W | flipped loss |
| 88245069 | Alexandr Utkov | win | 10-0-0 | W | retained win |
| 88245592 | Kucing Garong | win | 10-0-0 | W | retained win |
| 88246129 | GIVE ME A JOB | win | 9-1-0 | W | retained win |
| 88246713 | itohudo | win | 10-0-0 | W | retained win |
| 88247233 | OverfitOracle | loss | 10-0-0 | W | flipped loss |
| 88247782 | 一石三頭 | loss | 10-0-0 | W | flipped loss |
| 88248321 | Mote Zhuang | win | 9-1-0 | W | retained win |
| 88248844 | unknown | win | 8-2-0 | W | retained win |
| 88249366 | machapin | loss | 10-0-0 | W | flipped loss |
| 88249393 | qb | win | 10-0-0 | W | retained win |
| 88249914 | Ye | loss | 10-0-0 | W | flipped loss |
| 88250446 | ghostiee11 | loss | 10-0-0 | W | flipped loss |
| 88250998 | Xxbozohead | win | 9-1-0 | W | retained win |
| 88251535 | Marron22246 | loss | 9-1-0 | W | flipped loss |
| 88251789 | Yushin Ito | loss | 10-0-0 | W | flipped loss |
| 88252076 | UBI=ISHI | loss | 7-3-0 | W | flipped loss |
| 88252610 | Adi Kusuma | loss | 10-0-0 | W | flipped loss |
| 88252759 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88252837 | Yushin Ito | loss | 10-0-0 | W | flipped loss |
| 88252856 | junlee789 | loss | 10-0-0 | W | flipped loss |
| 88253125 | yyou97 | win | 10-0-0 | W | retained win |
| 88253320 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88253642 | Kaikaku | win | 10-0-0 | W | retained win |
| 88254173 | bin luo1 | win | 9-1-0 | W | retained win |
| 88254686 | Khaledalnuaimi | loss | 8-2-0 | W | flipped loss |
| 88254832 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88254923 | szlachetny snieg | loss | 10-0-0 | W | flipped loss |
| 88255227 | Aphrodite | loss | 78-22-0 | W | flipped loss |
| 88255365 | Luca | loss | 10-0-0 | W | flipped loss |
| 88255773 | Nora | loss | 8-2-0 | W | flipped loss |
| 88255893 | Luca | loss | 10-0-0 | W | flipped loss |
| 88255975 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88258615 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88258639 | タニシ | loss | 10-0-0 | W | flipped loss |
| 88258841 | Majkel1337 | loss | 8-2-0 | W | flipped loss |
| 88260624 | wingsyuyi-satori | loss | 10-0-0 | W | flipped loss |
| 88260674 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88261149 | rumbling_b | loss | 10-0-0 | W | flipped loss |
| 88261688 | Rian | win | 10-0-0 | W | retained win |
| 88261733 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88262219 | Sohshi Nakamura | loss | 9-1-0 | W | flipped loss |
| 88262752 | BabyCows | win | 10-0-0 | W | retained win |
| 88263295 | YG JH | win | 10-0-0 | W | retained win |
| 88263822 | Mathurin Ache | win | 10-0-0 | W | retained win |
| 88263861 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88264373 | PieForever | loss | 10-0-0 | W | flipped loss |
| 88264404 | Team Rot-Weiß | loss | 9-1-0 | W | flipped loss |
| 88264935 | jin hiratsuka | loss | 8-2-0 | W | flipped loss |
| 88264972 | Team Rot-Weiß | loss | 7-3-0 | W | flipped loss |
| 88266013 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88267625 | KawattaTaido | loss | 10-0-0 | W | flipped loss |
| 88268465 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88268514 | Dominic Peel | loss | 10-0-0 | W | flipped loss |
| 88273125 | Binghui Xu | win | 10-0-0 | W | retained win |
| 88273894 | 田原 | loss | 8-2-0 | W | flipped loss |
| 88274852 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88276586 | Majkel1337 | loss | 9-1-0 | W | flipped loss |
| 88280043 | masspeaks | loss | 9-1-0 | W | flipped loss |
| 88280276 | Luca | loss | 10-0-0 | W | flipped loss |
| 88280581 | masspeaks | loss | 9-1-0 | W | flipped loss |
| 88280592 | Zhenyu Zhang | loss | 10-0-0 | W | flipped loss |
| 88280823 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88281112 | Yushin Ito | loss | 9-1-0 | W | flipped loss |
| 88281365 | ei ei ei yikuso | loss | 8-2-0 | W | flipped loss |
| 88282965 | Pokémon Day Care | loss | 10-0-0 | W | flipped loss |
| 88285383 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88285882 | flg | loss | 10-0-0 | W | flipped loss |
| 88286403 | flg | loss | 10-0-0 | W | flipped loss |
| 88286429 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88286928 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88287449 | flg | loss | 10-0-0 | W | flipped loss |
| 88287943 | flg | loss | 10-0-0 | W | flipped loss |
| 88287982 | Majkel1337 | loss | 10-0-0 | W | flipped loss |
| 88287988 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88288578 | flg | loss | 10-0-0 | W | flipped loss |
| 88289166 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88289703 | flg | loss | 10-0-0 | W | flipped loss |
| 88290370 | VMelville | win | 10-0-0 | W | retained win |
| 88290739 | flg | loss | 10-0-0 | W | flipped loss |
| 88312062 | primal | win | 10-0-0 | W | retained win |
| 88312577 | 土佐黒潮共和国 | win | 10-0-0 | W | retained win |
| 88313112 | Yasuharu Hirado | win | 7-3-0 | W | retained win |
| 88313620 | mage03 | loss | 10-0-0 | W | flipped loss |
| 88313673 | Asa-sotta | win | 9-1-0 | W | retained win |
| 88314138 | Soup | loss | 9-1-0 | W | flipped loss |
| 88314664 | 🐱KittenLeague🐱 | loss | 10-0-0 | W | flipped loss |
| 88315183 | dajiaohuang | win | 10-0-0 | W | retained win |
| 88315696 | TTU Thome | win | 10-0-0 | W | retained win |
| 88316214 | wsdsby | loss | 9-1-0 | W | flipped loss |
| 88316726 | Yxy2001 | win | 7-3-0 | W | retained win |
| 88317257 | The Debauchery Tea Party | win | 10-0-0 | W | retained win |
| 88317769 | knomura03 | loss | 9-1-0 | W | flipped loss |
| 88318294 | CMK | loss | 10-0-0 | W | flipped loss |
| 88318822 | Jaisal K Jain | win | 10-0-0 | W | retained win |
| 88319336 | Impala16 | loss | 10-0-0 | W | flipped loss |
| 88319853 | kumk | loss | 7-3-0 | W | flipped loss |
| 88320386 | 電気通信ポケモン大学 | loss | 8-2-0 | W | flipped loss |
| 88320896 | Yuto Muroshima | win | 7-3-0 | W | retained win |
| 88321420 | tereka | win | 10-0-0 | W | retained win |
| 88321956 | Zac Plischka | loss | 9-1-0 | W | flipped loss |
| 88322536 | N.Y | loss | 7-3-0 | W | flipped loss |
| 88323052 | t.eno | win | 10-0-0 | W | retained win |
| 88323585 | Editor Jugnu AI | win | 10-0-0 | W | retained win |
| 88324102 | Cam-Luan Truong | win | 8-2-0 | W | retained win |
| 88324625 | Latios17 | win | 10-0-0 | W | retained win |
| 88300893 | TLM13 LABS | win | 9-1-0 | W | retained win |
| 88307667 | Vibrava | loss | 10-0-0 | W | flipped loss |
| 88309157 | CoCoSh | win | 10-0-0 | W | retained win |
| 88315493 | ubunbun18 | loss | 10-0-0 | W | flipped loss |
| 88317878 | srikalyan | loss | 10-0-0 | W | flipped loss |
| 88319971 | 齐乐 | loss | 7-3-0 | W | flipped loss |
| 88320365 | TmDofi | win | 10-0-0 | W | retained win |
| 88320504 | THIRD PTCG Club | loss | 10-0-0 | W | flipped loss |
| 88321003 | JZ | loss | 10-0-0 | W | flipped loss |
| 88321041 | 213tubo | loss | 10-0-0 | W | flipped loss |
| 88322041 | James Cox | loss | 10-0-0 | W | flipped loss |
| 88322048 | jiatu.l | loss | 10-0-0 | W | flipped loss |
| 88322049 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88322611 | flg | loss | 10-0-0 | W | flipped loss |
| 88322619 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88322631 | Dries @ Tufa Labs | loss | 10-0-0 | W | flipped loss |
| 88323135 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88323138 | 懒惰的金枪鱼 | loss | 10-0-0 | W | flipped loss |
| 88323140 | Team Rot-Weiß | loss | 10-0-0 | W | flipped loss |
| 88323143 | Team Rot-Weiß | loss | 10-0-0 | W | flipped loss |
| 88323647 | flg | loss | 10-0-0 | W | flipped loss |
| 88323654 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88323655 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88323658 | Team Rot-Weiß | loss | 6-4-0 | W | flipped loss |
| 88323669 | KawattaTaido | loss | 10-0-0 | W | flipped loss |
| 88323677 | Team Rot-Weiß | loss | 9-1-0 | W | flipped loss |
| 88324178 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88324185 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88324192 | Luca | loss | 10-0-0 | W | flipped loss |
| 88324221 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88324685 | flg | loss | 10-0-0 | W | flipped loss |
| 88324686 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88324689 | e-toppo + kurupical | loss | 10-0-0 | W | flipped loss |
| 88324692 | Pokemon Siuuuu | loss | 10-0-0 | W | flipped loss |
| 88324700 | Team Rot-Weiß | loss | 8-2-0 | W | flipped loss |
| 88325152 | CYLik | loss | 9-1-0 | W | flipped loss |

The current 287-replay final V6 trial details are in `artifacts/v6_candidate_replay_results_after_88325152_archive_final.csv`, with matching JSON. The current 103-deck matrix is `artifacts/v6_candidate_matrix_after_88325152_archive_final_60.csv`. The new loss matchup was confirmed over 1,000 trials for both prior V6 (`artifacts/v6_candidate_88325152_1000.csv`) and final V6 (`artifacts/v6_final_88325152_1000.csv`). The earlier finalized 225-replay root-cause table remains in `artifacts/v5_final_replay_results.csv`.
