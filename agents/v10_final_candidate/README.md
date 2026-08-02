# V10 Final submitted snapshot

This is the corrected Mega Lopunny ex / Dudunsparce candidate built after the
deployed V10 started 5-7 live. The deployed snapshot remains frozen in
`agents/v10_candidate/`; this directory is the separately submitted V10 Final
snapshot and must remain frozen.

## Live results

The first fifteen supplied V10 Final games are 5-10. Kaggle used the exact deck,
the frozen source reproduced all 629 recorded decisions, and the agent attacked
on all 66 attack-capable turns. The losses are therefore not a loading or
attack-skip regression.

- Mega Lucario is 3-0 against V10 Final. Lopunny's Fighting Weakness and its
  three-prize value let Lucario finish games with two Lopunny knockouts.
- Five losses ended by board exhaustion while the opponent still had prizes.
  The policy can use Run Away Draw before playing a held Basic, and its attack
  guard can suppress safe Bench setup after an attack becomes legal.
- Alakazam counter placement, Dragapult spread, and Mega Starmie/Froslass
  pressure punish the fragile 70-HP setup board or the lone Mega attacker.
- Wally was used eleven times in the second batch and helped produce two long
  Dragapult wins, so the repair functions. It cannot solve the deck's prize,
  weakness, damage, and board-survival problems.

V10 Final is no longer recommended for final selection. Any correction belongs
in a structural V11, not this frozen submitted snapshot. See
`artifacts/V10_FINAL_LIVE_AUDIT_THROUGH_89396175.md`.

## What changed

- Replaced the blanket rejection of Wally's Compassion on a damaged Active
  Lopunny with a state-checked heal, Energy recovery, reattachment, and pivot
  sequence.
- Requires the retreat action to be genuinely available before relying on a
  Wally pivot, and rechecks the post-heal menu before attaching to the Bench.
- Preserves a legal Spiky Hopper attack against damage-protection Pokémon.
- Resets all turn and Wally state between games.
- Counts Mega Pokémon as three-prize targets and makes Boss/attack closeout
  scoring prize-aware.
- Corrects protection-aware damage estimates so Gale Thrust is not treated as
  a knockout through protection.
- Preserves Wally during discard choices when a Lopunny recovery line exists.

Runtime behavior uses visible state, fixed card metadata, and card mechanics
only. It contains no opponent names, replay IDs, or identity branches.

## Exact deck

- 4 Buneary, 3 Mega Lopunny ex
- 4 Dunsparce, 4 Dudunsparce, 1 Fan Rotom
- 4 Buddy-Buddy Poffin, 4 Ultra Ball, 4 Pokégear 3.0, 4 Poké Pad
- 4 Air Balloon
- 3 Boss's Orders, 1 Xerosic's Machinations
- 4 Hilda, 4 Lillie's Determination, 4 Wally's Compassion
- 4 Mist Energy, 3 Spiky Energy, 1 Enriching Energy

## Final validation

All matches used the official simulator with alternating seats.

| Opponent | V10 Final W-L-D | Games | Timeouts | Abandoned attack turns |
|---|---:|---:|---:|---:|
| Deployed V10 | 787-213-0 | 1,000 | 0 | 0 |
| flg exact-deck pilot | 952-45-3 | 1,000 | 0 | 0 |
| Rmy exact-deck pilot | 425-570-5 | 1,000 | 0 | 0 |
| Sixth Sense exact-deck pilot | 726-274-0 | 1,000 | 0 | 0 |
| James toolbox exact-deck pilot | 790-208-2 | 1,000 | 0 | 0 |

Separate targeted searches ran 5,000 games against deployed V10 and 5,000
against the James control pilot after the final safety patches, with no
abandoned attack turn found. Ten V10-Final-specific tests cover the complete
Wally pivot, protection, spent-retreat, lost-retreat-option, cross-game reset,
Mega prize value, and four high-impact live replay states. The full focused and
replay-protocol suite has 27 tests.

The Rmy pure-Ogerpon pilot remains a losing stress matchup, although this is a
meaningful improvement over deployed V10's 309-689-2 result. These pilots are
state-driven approximations, not recovered leaderboard source.

## Upload package

Upload `artifacts/submission_10_final.tar.gz`. It contains only `main.py` and
`deck.csv` and passes raw execution without `__file__`, compilation, exact
60-card validation, and archive-member verification.

- `main.py`: `099bd68d3d4d5d08c1e80734505131a2887d774f65d9b95b4c32e8882bc6c458`
- `deck.csv`: `7fc17fc61014dc3bddec69e751eecde72588bb050b56a763d82720ce92ed1d6c`
- archive: `9551b217416744b25b464232833ac40b66fdd57b84f6b0699ba459cc4a41b14a`
