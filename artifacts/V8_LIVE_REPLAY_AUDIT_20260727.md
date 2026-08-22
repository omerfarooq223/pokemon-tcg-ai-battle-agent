# V8 Live Replay Audit — 2026-07-27

## Kaggle score decision — 2026-07-28

- V5: 965 reported peak; 790.4 latest visible snapshot before becoming inactive.
- V7: 914 reported peak; 775.8 latest visible snapshot after roughly three to four hours near that level.
- V6: 766.3 latest visible snapshot.
- V4: 730.8.
- V3: 443.6.
- V2: 397.8.
- V1: 349.7.

The displayed values are volatile live ratings, not fixed test scores. V5 can no longer receive matches because the team has two newer active agents. The user estimates the current shell's sustained level near 800. V5's 965 and V7's 914 peaks show that the shell can spike much higher, but the later fallback and repeated replay loss clusters show a matchup-polarized floor. V8 should target sustained stability above the current level, not merely a higher short-lived peak.

## V7 live sample

- Saved V7 record: 12 wins and 16 losses across 28 supplied replays.
- Replay health: all 28 completed normally with no replay-level errors.
- Policy health: 1,357 paired active decisions, 367 attack-menu decisions, 168 attack-capable turns, 168 attacked turns, and 0 abandoned attack turns.
- Conclusion: V7 did not repeat the V1–V3 attack-selection failure. Its live weakness is structural.

## Loss clusters

- Alakazam/Dunsparce control: 7 losses. Powerful Hand placed 180–480 damage counters, bypassing both Crustle and Cornerstone protection. In the two newest losses V7 did not see Xerosic and the opponent finished with 18- and 23-card hands; earlier losses showed that even repeated disruption can be rebuilt through.
- Mega Starmie/Froslass: 3 losses. Nebula Beam ignored protection for 210 damage and Jetting Blow pressured low-HP bench targets. The newest loss attacked on all 12 offered turns and still lost the race.
- Crustle/Kangaskhan control: 2 losses. Opposing Crustle reached 120–240 effective damage while V7's 120/140 attacks did not create a reliable race advantage.
- Duraludon, Cynthia's Spiritomb, and Grimmsnarl/Munkidori: 3 losses. These were non-ex scaling, spread, or damage-counter races that bypassed the shell's ex/Ability protection plan.
- Cubchoo/Beartic denial: 1 loss. Repeated attack lock plus Crushing/Enhanced Hammer created a deck-out control game despite a full late board.
- V6 also added a Mega Sharpedo ex/Seviper loss. Damaged Mega Sharpedo reached 270, while non-ex Seviper reached 240 and bypassed Crustle's ex-only protection.

## V8 experiments

### Alakazam engine prototype — rejected

The existing general Alakazam/Dunsparce stress agent and exact live-derived deck were screened as a structural V8 starting point.

- vs V7: 91–209 over 300 games.
- vs V5: 104–196 over 300 games.
- vs V4: 157–143 over 300 games.
- vs V1: 127–173 over 300 games.

It targets the correct live weakness but its current planner is not competitive enough to promote.

### Diggersby 140-damage line — rejected

Diggersby provides the exact one-Energy 140-damage breakpoint needed to knock out Alakazam and Trevenant. Four Crustle/Diggersby mixes were screened.

- Two-line variants beat the Alakazam stress agent 66–69% but won only 33–35% against V7.
- One-line light variant: 684–316 vs Alakazam, but 430–568–2 vs V7.
- One-line expanded variant: 690–310 vs Alakazam, but 426–573–1 vs V7.
- Broad 132-deck screen, 20 games per deck:
  - V7: 2,482–158, 94.02% raw and 95.10% replay-frequency weighted.
  - Light Diggersby: 2,455–182–3, 92.99% raw and 94.34% weighted.
  - Expanded Diggersby: 2,464–174–2, 93.33% raw and 91.65% weighted.

The one-line concept is worth remembering, but neither tested mix clears the adoption gate.

## Final V8 decision

- The dedicated Mega Starmie ex/Cinderace prototype was rejected after initial results of 25-15 versus random, 6-34 versus V5, and 2-38 versus V7. Older policies also performed poorly with its deck.
- The V5-deck/V7-policy recovery blend was rejected after a fresh 975-1022-3 result versus V5.
- Final V8 preserves frozen V5 gameplay and deck, adding only exact-deck loader hardening. This directly reflects the newly supplied fact that V5 reached the strongest observed peak, 965.
- Validation passed: raw loader, exact 60-card deck, Python compilation, archive contents, and package creation. The archive is `artifacts/submission_8.tar.gz`.
- A 1000-game V8-versus-V5 audit finished 489-507-4 with zero abandoned attack turns. V8 scored 630-370 against the Alakazam stress agent.
- V8 is therefore a safe **reactivation candidate**, not a demonstrated strategic improvement. Upload only if reactivating the V5 configuration is the desired use of a live slot.
- The next structural work belongs to V9 and is documented in `docs/V9_BUILD_GUIDE.md`.
