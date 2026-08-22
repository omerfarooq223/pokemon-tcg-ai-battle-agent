# V9 supplied-replay audit — 2026-07-29

## Scope and integrity

- Audited all 21 JSON files supplied from `Downloads`.
- Every filename matches `info.EpisodeId`; every game has two valid 60-card deck actions.
- Every game finished `DONE/DONE`. No top-level or per-agent error was recorded. The only per-step states are `ACTIVE`, `INACTIVE`, and `DONE`.
- The current project corpus has 369 unique episodes. Twenty supplied episodes are new by both episode ID and whole-file SHA-256, so a correct import would raise it to 389 unique episodes.
- Episode `88527351` is the sole duplicate. The Downloads file and `scouting_replays/our_agent_v8/losses/88527351.json` are byte-identical, SHA-256 `4f740f7f219aca1c8d2cd1b1aa68e7edde8a11599d17091367e43aa3bfb410b5`.
- The first 11 files all contain `ROASTERS` using deck hash `4a0eca8afb080be331bd5ba4baa5f6aae2029ee326ad1376eb4b7da588010d10`, an exact match to `agents/v5_candidate/deck.csv`, `agents/v8_candidate/deck.csv`, and `agents/v8_fixed/deck.csv`, and not V6/V7. Because `88527351` is already documented as V8's first live game and these were supplied as one current batch, classify the set as V8. Deck fingerprint alone cannot distinguish V5 from V8, so the chronology and user's batch label are part of that classification.
- The final 10 files are public scouting games for `flg`. All use one fixed deck with hash `704270a2922dabe9e04a8a7da824317b637d727107f6e70afcd90c1bb1264447` and form an exact 5-win/5-loss sample.
- Deck hashes below are SHA-256 of the newline-separated 60-card sequence, including the final newline—the same representation used by project `deck.csv` files.

## V8 games

All rows have status `DONE/DONE`, no error, and target deck `4a0eca…` (4 Dwebble, 4 Crustle, 2 Cornerstone Mask Ogerpon ex; the V5/V8 deck).

| Episode | Teams (seat 0 vs seat 1) | Rewards | V8 | Steps / seed | Opponent deck | Existing corpus match | Canonical destination |
|---:|---|---|---:|---:|---|---|---|
| 88527351 | t.eno vs ROASTERS | `[1,-1]` | Loss | 130 / 44111119 | `92b92bac…` Grimmsnarl ex / Munkidori / Froslass | Exact ID + checksum duplicate | Existing `scouting_replays/our_agent_v8/losses/88527351.json`; do not copy again |
| 88528562 | ROASTERS vs Pietro | `[-1,1]` | Loss | 108 / 671829503 | `a7da4233…` Mega Starmie ex / Cinderace / Crushing Hammer | None | `scouting_replays/our_agent_v8/losses/88528562.json` |
| 88527969 | ROASTERS vs Masa | `[1,-1]` | Win | 136 / 797338819 | `b4464eb5…` Mega Lucario ex / Hariyama / Lunatone / Solrock | None | `scouting_replays/our_agent_v8/wins/88527969.json` |
| 88745200 | ROASTERS vs kaggle_bbgg | `[1,-1]` | Win | 149 / 368456840 | `f3332903…` Crustle / Mega Kangaskhan ex / Shaymin control | None | `scouting_replays/our_agent_v8/wins/88745200.json` |
| 88734629 | ezreal77 vs ROASTERS | `[-1,1]` | Win | 155 / 1408928327 | `92b92bac…` exact classic Grimmsnarl counter shell | None | `scouting_replays/our_agent_v8/wins/88734629.json` |
| 88727264 | fle3n + codex AGI X26 vs ROASTERS | `[1,-1]` | Loss | 163 / 231123142 | `92b92bac…` exact classic Grimmsnarl counter shell | None | `scouting_replays/our_agent_v8/losses/88727264.json` |
| 88724413 | Lixin Yin vs ROASTERS | `[-1,1]` | Win | 131 / 1810228550 | `2a541d7b…` Mega Lucario ex / Hariyama / Lunatone / Solrock | None | `scouting_replays/our_agent_v8/wins/88724413.json` |
| 88710371 | NayuNayu vs ROASTERS | `[-1,1]` | Win | 204 / 117707838 | `dfd74d8d…` Dragapult ex / Dusknoir / Munkidori / Budew | None | `scouting_replays/our_agent_v8/wins/88710371.json` |
| 88702773 | ROASTERS vs kkkk | `[1,-1]` | Win | 171 / 1934614308 | `a8c91773…` Alakazam / Dunsparce control | None | `scouting_replays/our_agent_v8/wins/88702773.json` |
| 88702243 | H.Ito vs ROASTERS | `[1,-1]` | Loss | 81 / 2122658015 | `7874ecb3…` Alakazam / Dunsparce / Enhanced Hammer | None | `scouting_replays/our_agent_v8/losses/88702243.json` |
| 88688530 | Linda Brown vs ROASTERS | `[-1,1]` | Win | 135 / 1490014297 | `2a541d7b…` exact Mega Lucario variant above | None | `scouting_replays/our_agent_v8/wins/88688530.json` |

Batch result: **7 wins, 4 losses (63.64%)**. Ten new files add 7 wins and 3 losses to the already-preserved `88527351` loss.

Actual-live behavior audit: V8 made 538 active menu decisions, saw 198 attack menus spanning 93 attack-capable turns, and attacked on all 93 turns. There were **0 abandoned attack turns**, no invalid action, no timeout, and mean first attack turn was 2.91. These losses are not a recurrence of the V1–V3 attack-selection bug.

## Public `flg` scouting games

All rows have status `DONE/DONE`, no error, and target deck `704270a2…`: 4 Dwebble, 3 Crustle, 1 Cornerstone Mask Ogerpon ex, and 2 Mega Kangaskhan ex, backed by Rock Fighting/Grow Grass/Mist/Spiky Energy, Petrel, Boss, Pokégear, Ultra Ball, Colress, one Xerosic, and two Stadiums.

| Episode | Teams (seat 0 vs seat 1) | Rewards | `flg` | Steps / seed | Opponent deck | Existing corpus match | Canonical destination |
|---:|---|---|---:|---:|---|---|---|
| 88762215 | flg vs Harsh Patel | `[1,-1]` | Win | 76 / 246806836 | `730515d5…` Dragapult ex / Munkidori / Budew / Hammer | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88762215.json` |
| 88764905 | flg vs e-toppo + kurupical | `[-1,1]` | Loss | 211 / 567058776 | `fb6fa9f2…` Grimmsnarl / Munkidori / Froslass / Budew / Yveltal | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88764905.json` |
| 88759036 | flg vs LiamK | `[1,-1]` | Win | 185 / 674445900 | `92b92bac…` classic Grimmsnarl counter shell | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88759036.json` |
| 88754803 | flg vs Dries @ Tufa Labs | `[-1,1]` | Loss | 262 / 466957633 | `c960f712…` Grimmsnarl / Munkidori / Froslass / Handheld Fan | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88754803.json` |
| 88750615 | flg vs James Cox & Henry Chao | `[1,-1]` | Win | 186 / 1292686392 | `5e6ff390…` Area Zero Ogerpon / Raging Bolt / Kangaskhan toolbox | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88750615.json` |
| 88746412 | flg vs unknown | `[1,-1]` | Win | 37 / 1344355627 | `fbe6ab59…` Duraludon / Archaludon ex / Cinderace | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88746412.json` |
| 88742222 | Lunariz vs flg | `[-1,1]` | Win | 177 / 1730319446 | `cd7bfdfa…` Crustle / Mega Kangaskhan hand-control mirror | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88742222.json` |
| 88726741 | Dries @ Tufa Labs vs flg | `[1,-1]` | Loss | 190 / 1515206247 | `92b92bac…` exact classic Grimmsnarl counter shell | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88726741.json` |
| 88714591 | 想要成为kaggle大师 vs flg | `[1,-1]` | Loss | 228 / 325811628 | `92b92bac…` exact classic Grimmsnarl counter shell | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88714591.json` |
| 88707615 | flg vs syuuuuu | `[-1,1]` | Loss | 132 / 1047144193 | `ce1409a5…` Alakazam / Dunsparce / Fezandipiti / Hammer | None | `scouting_replays/archive_import/top_leaderboard_20260729_flg/88707615.json` |

Batch result: **5 wins, 5 losses (50.0%)**. Four of five losses were to Grimmsnarl/Munkidori/Froslass variants; the fifth was to Alakazam counter placement. The same classic Grimmsnarl 60 (`92b92bac…`) went 1-2 against V8 and 1-2 against `flg`, showing high variance but a stable adverse cluster.

Unlike V8, `flg` abandoned 5 of 57 attack-capable turns across four games. It explicitly ended turns with a legal attack still offered in episodes 88759036, 88754803 (twice), and 88714591; episode 88707615 manually evolved Dwebble instead of using the offered Ascension, after which no attack remained. Its mean first attack turn was 6.1. The deck is valuable evidence; its policy should not be copied wholesale, and V9 must preserve V8's hard attack-safety invariant.

## Full deck fingerprint catalog

| SHA-256 | Archetype / first appearance |
|---|---|
| `4a0eca8afb080be331bd5ba4baa5f6aae2029ee326ad1376eb4b7da588010d10` | V5/V8 Dwebble / Crustle / Cornerstone |
| `704270a2922dabe9e04a8a7da824317b637d727107f6e70afcd90c1bb1264447` | `flg` Crustle / Cornerstone / Mega Kangaskhan |
| `92b92bac9f9163ecff933b3dc39294d2cc154c8684f3c8497877661419ebc59d` | classic Grimmsnarl / Munkidori / Froslass |
| `a7da4233609d925c28a2b5567685b8c3c42306b36b6f25848fbf32579cef10fc` | Pietro Mega Starmie / Cinderace / Hammer |
| `b4464eb525a25e6598a972d00efc5e5b5156372e77f51853f4076d8ebb34fd7d` | Masa Mega Lucario variant |
| `f3332903a3b2827a104d2cf62b5c70391ea9393b9667014de07b1365f94a04a1` | kaggle_bbgg Crustle / Kangaskhan / Shaymin |
| `2a541d7bf3d9e6b36037123f53f4dfef6348223f79fd27095dafc602a5357c19` | Lixin Yin / Linda Brown Mega Lucario variant |
| `dfd74d8d44b24f7c975baff70a5a9a8b99f37ea9d4d3f5e85d1d392777dedbf8` | NayuNayu Dragapult / Dusknoir / Munkidori |
| `a8c9177354b92abe5fb877f46b792b86f8ec9c4bc3551d5d16d4a89128f00976` | kkkk Alakazam / Dunsparce |
| `7874ecb3cb87b7da4dc85fb35e7c35fa604a12cb18cc2626b03a6b1f128308c3` | H.Ito Alakazam / Dunsparce |
| `730515d5b8e9d6f7b9a87c160cd87b43c95535c917688d2b15f46d82fc054485` | Harsh Patel Dragapult / Munkidori / Budew |
| `fb6fa9f20e9681aa61aa5258640172cfc3d39e8159ca5934f190ad67f1be0e1a` | e-toppo Grimmsnarl counter variant |
| `c960f71296a4ca797d8b8421f8c3d059752296ba34721108e6b625e02ca0410a` | Dries Grimmsnarl counter variant |
| `5e6ff39035d9d5b37ce0908929b87a56fdb8d1dfe6fc712c90353511756bf5ea` | Area Zero toolbox; also the V2/V3 deck hash |
| `fbe6ab59992260b0d6774abed19469be315521b5ed0546de8c20f329607693e6` | Archaludon / Duraludon / Cinderace |
| `cd7bfdfa205c4c3743aada1dc62293bf5a669fa8cbbac759a527ddd7d15bbb8f` | Lunariz Crustle / Mega Kangaskhan control |
| `ce1409a564fca4ff525bf367787064eec6c44b63db1affbe055afee1be4049fe` | syuuuuu Alakazam / Dunsparce / Fezandipiti |

## Loss analysis and general V9 lessons

### V8 loss 88527351 — counter/spread board exhaustion

V8 attacked on all 6 offered turns, starting turn 2, and took five prizes by clearing two 320-HP Grimmsnarl ex plus a one-prize Pokémon. It established only two Dwebble/Crustle lines. Froslass checkup counters and repeated Munkidori transfers eventually exhausted both; V8 ended with no Pokémon while the opponent still had five prizes remaining. A late Poffin made no board progress after eligible small Basics were exhausted.

General response worth testing: a state-aware backup-line/search safeguard when fewer than two viable attackers remain, plus refusal of provably no-progress Poffin. Do not blindly fill the Bench; earlier broad Poffin-first work regressed by exposing extra prizes.

### V8 loss 88528562 — effect-ignoring 210 and the 120-damage ceiling

V8 attacked on all 4 offered turns, starting turn 3, and lost three complete Crustle lines. Mega Starmie's Nebula Beam deals 210 through defensive effects—exactly enough for Cornerstone and more than enough for ordinary Crustle—while Jetting Blow pressures the Bench and Crushing Hammer restricts setup. V8's three 120-damage Crustle attacks plus incidental damage left the Hero's Cape Starmie at 10/430 rather than taking a knockout, and V8 took zero prizes before its last Cornerstone was cleared.

This is structural, not an attack heuristic. A general fix requires a genuinely competitive higher-damage/high-survivability line or a resource engine that changes the race. Threshold-only scoring cannot make 120 damage clear 330–430 HP.

### V8 loss 88727264 — shallow setup against the same counter shell

V8 attacked on all 5 offered turns, starting turn 2, and took four prizes, but its maximum board was only two Pokémon: one Dwebble/Crustle line and one Cornerstone. It played no Poffin or Poké Pad in the recorded game; only Waitress, Lillie, and healing. The exact same opponent 60 was beaten in 88734629 when V8 reached a five-Pokémon board with four Dwebble/Crustle lines. Counter placement then exhausted the shallow board.

This same-deck contrast makes board/search consistency the strongest broadly applicable lesson in this batch. It supports a bounded backup-line safeguard and/or a better consistency engine, while also showing that unavoidable draw variance remains.

### V8 loss 88702243 — Alakazam tempo and counter placement

V8 selected an attack on all 5 offered turns, but every attack was Dwebble's Ascension; it never made a damaging attack and took zero prizes. Alakazam attacked on turns 5 and 7 with 12- and 15-card hands, placing 240 and 300 counters through protection. V8's second Xerosic arrived on turn 8 against a 16-card hand—after the decisive tempo loss—and the opponent continued to recycle and remove evolving lines. V8 lost all four Dwebble, three Crustle, and Cornerstone.

The established general targets remain: earlier reliable disruption and/or a competitive 140-plus-damage line that can immediately clear 140-HP Alakazam/Trevenant. A threshold-only Xerosic tweak and the previously rejected Diggersby mixes should not be revived without full-suite evidence.

## Cross-batch conclusions

1. **Preserve attack safety.** V8 converted 93/93 attack-capable turns; `flg` converted only 52/57. This is a proven V8 strength.
2. **Counter placement is the dominant structural cluster.** V8 went 1-2 against an identical Grimmsnarl 60 and split two Alakazam games. `flg`, despite Mega Kangaskhan diversification, went 1-4 against Grimmsnarl variants and 0-1 against Alakazam.
3. **Board depth matters within the same matchup.** V8's two Grimmsnarl losses peaked at two Pokémon in play, while its win against the exact same 60 reached five with four evolution lines.
4. **Mega Kangaskhan is evidence, not a solved upgrade.** The `flg` shell has better attacker diversity, draw, Boss access, and 200-plus damage, but its 1-4 Grimmsnarl record shows that simply splicing Kangaskhan into V8 is unlikely to solve spread/counters and may add a two-prize liability.
5. **The damage breakpoints are real.** Crustle's 120 misses 140-HP Alakazam/Trevenant and is far below Starmie's 330–430 HP; Cornerstone's 140 helps the first breakpoint but not effect-ignoring 210 or counter placement.
6. **Do not treat local replay replacement as exact re-execution.** Kaggle seeds are recorded, but the local battle API cannot inject them and opponent source is unavailable. These files provide exact live outcomes and semantic opponent/deck evidence; V9 counterfactual runs remain approximations and must be paired with direct head-to-head, stress-agent, matrix, and attack-invariant gates.

## Duplicate handling

- `Downloads/88527351.json` is safe to delete now because its canonical V8 copy is byte-identical.
- Do not delete the other 20 Downloads files until each has been copied to the destination above and the copied file's SHA-256 has been verified.
- After import, rerun `python3 tools/analyze_replay_corpus.py`; expected corpus count is 389 unique episodes and 0 duplicate files.
