# V10 top-five state-driven pilot league

These four local opponent pilots use the exact reconstructed decks from the
2026-08-01 Top 5 replay archive:

- `flg/`: Crustle / Cornerstone / Mega Kangaskhan control
- `rmy/`: four-Teal-Mask-Ogerpon Energy engine
- `sixth_sense/`: Grimmsnarl / Munkidori / Froslass spread and counters
- `james_toolbox/`: Area Zero multi-attacker toolbox

The wrappers load independent instances of the existing card-semantic stress
planner and configure deck-specific attack costs, Energy colors, setup roles,
search targets, discard preservation, bounded attack-safe setup, and effect
targeting. Runtime choices use only visible state and card mechanics. There are
no replay IDs, player-name checks, or opponent-identity branches.

## Why these are better stress opponents than generic replay fallback

Each policy was screened against the prior semantic planner while both sides
piloted the same exact deck. Over 1,000 swapped-seat games:

| New pilot | Prior same-deck pilot | Draws |
|---|---:|---:|
| flg | 578-422 | 0 |
| Rmy | 730-270 | 0 |
| Sixth Sense | 489-501 | 10 |
| James toolbox | 503-497 | 0 |

The Sixth policy was then corrected using the supplied top decisions: regular
Darkness attachments now establish Munkidori before redundant Marnie's
attackers, Adrena-Brain moves the maximum useful counters and takes counter
knockouts, Shadow Bullet concentrates bench pressure, and Froslass setup rises
against Ability-heavy boards. After that correction it beat the prior
same-deck pilot 299-199-2 over a fresh 500 games and improved from 47-250-3 to
113-185-2 against the flg pilot over 300 games.

Fresh 100-game random screens were 93-7 flg, 98-2 Rmy, 88-12 Sixth Sense, and
63-37 James toolbox. These are sanity checks, not ladder estimates.

## Safety and trace calibration

Across a final 300-game-per-pilot attack audit against the prior same-deck
planner, all four pilots returned valid selections and had zero timeouts.
Attack-turn conversion was 99.96% flg, 100% Rmy, 98.81% Sixth Sense, and 100%
James. The rare Sixth non-conversions are bounded multi-stage evolution/ability
lines; they are well above the supplied top policy's 97.87% conversion.

Exact selected-index agreement on recorded top observations is deliberately a
strict lower bound because duplicate copies of the same card occupy different
option indexes and replay states follow actions the pilot did not choose. It was
15.3% flg, 28.7% Rmy, 23.4% Sixth Sense, and 21.0% James over 6,381 decisions.
Useful forced/effect contexts are much better: Sixth matched all 50 recorded
counter-count choices, 38/50 Adrena-Brain source choices, 22/22 retreat-Energy
choices, and 23/24 promotion choices. These policies should therefore be used
as independent structural stress opponents, not represented as recovered top
source code or exact policy clones.

## Recommended use

Run a candidate against every directory with swapped seats. Do not promote a
candidate based on the old replay fallback if it collapses against one of these
state-driven decks. The league is intentionally polarized: for example,
Crustle walls the all-ex Ogerpon engine, while counters and spread test the
Crustle board rather than ordinary attack damage.

```text
python3 tools/run_local_matches.py \
  --matches 500 \
  --agent-dir agents/v10_candidate \
  --opponent agent \
  --opponent-dir experiments/v10_top5_pilots/sixth_sense \
  --swap-seats --quiet
```
