# V10 Final upload report

## Decision

The upload candidate is `artifacts/submission_10_final.tar.gz`. It is a separate
corrected snapshot; the deployed 5-7 V10 remains frozen and reproducible.

## Live defect repaired

The deployed V10 reproduced Kaggle exactly but played Wally's Compassion zero
times in twelve games. Its safety rule disabled the deck's main recovery and
pivot engine. V10 Final permits Wally only when the resulting turn has a legal
completion: reattach to the healed Active, pivot into a ready attacker, or
power a Bench Lopunny and then retreat.

Three additional internal failure paths were found during stress testing and
fixed before packaging:

1. Wally could remove a live two-Energy Spiky Hopper attack against a protected
   Pokémon and fail to restore it that turn.
2. Wally could be played after retreat and attachment were already spent.
3. An opposing effect could remove the expected retreat option; V10 now records
   the actual legal menu and reattaches to the Active when the pivot disappears.

Other corrected semantics include cross-game memory reset, three-prize Mega
closeout logic, protection-aware damage estimates, prize-aware target choice,
and Wally preservation in discard choices.

## Evidence

The final candidate beat deployed V10 787-213 over 1,000 swapped-seat games.
Across the same 1,000-game format it scored 952-45-3 against the flg pilot,
425-570-5 against the Rmy pilot, 726-274 against Sixth Sense, and 790-208-2
against the James toolbox pilot. Every final tournament row had zero timeouts
and zero abandoned attack turns.

After the last sequencing patch, separate 5,000-game targeted searches against
deployed V10 and the James control pilot found no abandoned attack turn. The
candidate passes 27 focused and replay-protocol tests, including exact live
states from episodes 89371815, 89374507, 89376120, and 89377182.

The Rmy pure-Ogerpon approximation remains the main known matchup weakness.
Its 42.7% decisive result is still substantially better than deployed V10's
30.9% result, but it prevents an honest claim that local V10 Final beats every
approximate top-five pilot. Kaggle performance remains the decisive test.

## Package integrity

The builder passed raw Kaggle-style execution without `__file__`, Python
compilation, exact 60-card validation, archive creation, and member validation.
The archive contains only `main.py` and `deck.csv`. Runtime source contains no
opponent names, team names, replay IDs, or episode-specific behavior.

- `main.py` SHA256: `099bd68d3d4d5d08c1e80734505131a2887d774f65d9b95b4c32e8882bc6c458`
- `deck.csv` SHA256: `7fc17fc61014dc3bddec69e751eecde72588bb050b56a763d82720ce92ed1d6c`
- archive SHA256: `9551b217416744b25b464232833ac40b66fdd57b84f6b0699ba459cc4a41b14a`
