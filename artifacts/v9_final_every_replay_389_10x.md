# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **3890**
- Match results: **3770 wins, 120 losses, 0 draws**
- Match win rate: **96.92%**
- Per-replay majority: **389 wins, 0 losses, 0 ties**
- Recorded opponent-action usage: **55.33%**

## What was preserved

| Condition | Status |
|---|---|
| Replacement seat | Preserved |
| Opponent submitted 60-card deck | Preserved exactly |
| Original first-player seat | Forced when recoverable |
| Opponent decisions | Recorded semantic action when still legal; generic fallback otherwise |
| Game/map | Pokémon has no map parameter; local bundled engine used |
| Kaggle seed | Metadata only; **not accepted by the local API** |
| Initial shuffle, hand, and Prize cards | Visible in replay visualization, but not injectable through the local API |
| Coin flips | Recorded after the fact, but not settable |
| Original opponent source code | Not present in replay JSON |

## Per-replay results

| Episode | Original | Counterfactual W-L-D | Result | Comparison | Scripted | Attacked turns | Triage |
|---:|---|---:|---|---|---:|---:|---|
| 88114269 | loss | 9-1-0 | win | improved | 52.8% | 49/49 |  |
| 88114272 | loss | 10-0-0 | win | improved | 83.8% | 38/38 |  |
| 88135168 | loss | 10-0-0 | win | improved | 46.5% | 52/52 |  |
| 88135718 | loss | 10-0-0 | win | improved | 71.2% | 38/38 |  |
| 88136757 | loss | 10-0-0 | win | improved | 58.8% | 34/34 |  |
| 88138839 | loss | 9-1-0 | win | improved | 33.7% | 73/73 |  |
| 88139351 | loss | 10-0-0 | win | improved | 41.7% | 58/58 |  |
| 88139876 | loss | 10-0-0 | win | improved | 38.3% | 59/59 |  |
| 88139877 | loss | 10-0-0 | win | improved | 32.6% | 79/79 |  |
| 88139889 | loss | 10-0-0 | win | improved | 39.4% | 80/80 |  |
| 88140397 | loss | 10-0-0 | win | improved | 39.7% | 69/69 |  |
| 88140434 | loss | 10-0-0 | win | improved | 49.8% | 41/41 |  |
| 88140934 | loss | 10-0-0 | win | improved | 56.0% | 39/39 |  |
| 88141449 | loss | 10-0-0 | win | improved | 52.5% | 67/67 |  |
| 88141464 | loss | 10-0-0 | win | improved | 59.4% | 40/40 |  |
| 88141972 | loss | 10-0-0 | win | improved | 50.1% | 87/87 |  |
| 88142495 | loss | 10-0-0 | win | improved | 54.1% | 38/38 |  |
| 88143033 | loss | 9-1-0 | win | improved | 60.4% | 101/101 |  |
| 88143428 | loss | 10-0-0 | win | improved | 55.7% | 57/57 |  |
| 88143558 | loss | 10-0-0 | win | improved | 62.3% | 48/48 |  |
| 88143960 | loss | 10-0-0 | win | improved | 88.4% | 38/38 |  |
| 88144074 | loss | 10-0-0 | win | improved | 27.4% | 84/84 |  |
| 88144497 | win | 10-0-0 | win | preserved_win | 81.4% | 33/33 |  |
| 88145058 | loss | 10-0-0 | win | improved | 77.3% | 42/42 |  |
| 88145588 | loss | 10-0-0 | win | improved | 69.0% | 37/37 |  |
| 88145696 | loss | 10-0-0 | win | improved | 41.6% | 45/45 |  |
| 88146122 | loss | 8-2-0 | win | improved | 46.2% | 56/56 |  |
| 88146648 | win | 10-0-0 | win | preserved_win | 73.3% | 30/30 |  |
| 88147191 | loss | 10-0-0 | win | improved | 29.2% | 74/74 |  |
| 88147227 | loss | 10-0-0 | win | improved | 57.7% | 44/44 |  |
| 88147702 | loss | 10-0-0 | win | improved | 81.6% | 38/38 |  |
| 88148218 | loss | 10-0-0 | win | improved | 67.9% | 61/61 |  |
| 88148312 | loss | 10-0-0 | win | improved | 33.9% | 70/70 |  |
| 88148790 | win | 10-0-0 | win | preserved_win | 80.6% | 22/22 |  |
| 88148861 | loss | 10-0-0 | win | improved | 35.3% | 63/63 |  |
| 88149240 | loss | 10-0-0 | win | improved | 71.8% | 35/35 |  |
| 88149380 | loss | 10-0-0 | win | improved | 44.6% | 83/83 |  |
| 88149406 | loss | 10-0-0 | win | improved | 74.7% | 65/65 |  |
| 88149782 | win | 10-0-0 | win | preserved_win | 48.2% | 28/28 |  |
| 88149906 | loss | 9-1-0 | win | improved | 47.4% | 76/76 |  |
| 88150296 | win | 10-0-0 | win | preserved_win | 68.5% | 42/42 |  |
| 88150868 | loss | 10-0-0 | win | improved | 56.8% | 66/66 |  |
| 88151481 | loss | 10-0-0 | win | improved | 81.6% | 70/70 |  |
| 88152037 | win | 10-0-0 | win | preserved_win | 85.9% | 26/26 |  |
| 88152577 | loss | 10-0-0 | win | improved | 74.4% | 44/44 |  |
| 88153002 | loss | 10-0-0 | win | improved | 56.9% | 41/41 |  |
| 88153112 | loss | 9-1-0 | win | improved | 68.8% | 37/37 |  |
| 88153551 | win | 10-0-0 | win | preserved_win | 86.8% | 34/34 |  |
| 88153647 | win | 10-0-0 | win | preserved_win | 86.9% | 83/83 |  |
| 88154072 | loss | 10-0-0 | win | improved | 77.9% | 31/31 |  |
| 88154188 | loss | 10-0-0 | win | improved | 65.8% | 48/48 |  |
| 88154615 | loss | 10-0-0 | win | improved | 89.7% | 31/31 |  |
| 88154720 | loss | 10-0-0 | win | improved | 72.0% | 46/46 |  |
| 88155167 | loss | 9-1-0 | win | improved | 53.8% | 60/60 |  |
| 88155258 | loss | 10-0-0 | win | improved | 91.3% | 30/30 |  |
| 88155735 | loss | 10-0-0 | win | improved | 52.7% | 35/35 |  |
| 88155807 | loss | 8-2-0 | win | improved | 70.0% | 36/36 |  |
| 88156264 | loss | 10-0-0 | win | improved | 70.3% | 25/25 |  |
| 88156364 | win | 10-0-0 | win | preserved_win | 67.6% | 29/29 |  |
| 88156894 | win | 10-0-0 | win | preserved_win | 84.2% | 57/57 |  |
| 88157011 | loss | 10-0-0 | win | improved | 50.1% | 47/47 |  |
| 88157416 | win | 9-1-0 | win | preserved_win | 40.8% | 40/40 |  |
| 88157484 | win | 10-0-0 | win | preserved_win | 85.5% | 48/48 |  |
| 88157952 | win | 10-0-0 | win | preserved_win | 85.5% | 26/26 |  |
| 88170362 | loss | 8-2-0 | win | improved | 70.2% | 44/44 |  |
| 88181889 | win | 10-0-0 | win | preserved_win | 78.5% | 16/16 |  |
| 88183542 | loss | 10-0-0 | win | improved | 53.2% | 75/75 |  |
| 88187788 | win | 10-0-0 | win | preserved_win | 58.6% | 30/30 |  |
| 88189899 | loss | 10-0-0 | win | improved | 80.2% | 43/43 |  |
| 88190488 | loss | 10-0-0 | win | improved | 60.8% | 50/50 |  |
| 88190720 | loss | 10-0-0 | win | improved | 54.9% | 47/47 |  |
| 88191459 | loss | 10-0-0 | win | improved | 68.2% | 43/43 |  |
| 88191506 | loss | 10-0-0 | win | improved | 63.0% | 50/50 |  |
| 88191988 | loss | 10-0-0 | win | improved | 53.3% | 54/54 |  |
| 88192025 | loss | 8-2-0 | win | improved | 55.5% | 42/42 |  |
| 88192363 | loss | 10-0-0 | win | improved | 67.6% | 40/40 |  |
| 88192550 | loss | 8-2-0 | win | improved | 51.1% | 54/54 |  |
| 88193019 | loss | 10-0-0 | win | improved | 64.0% | 49/49 |  |
| 88193372 | loss | 10-0-0 | win | improved | 47.3% | 44/44 |  |
| 88193551 | loss | 10-0-0 | win | improved | 82.4% | 35/35 |  |
| 88193634 | loss | 10-0-0 | win | improved | 71.8% | 39/39 |  |
| 88195735 | loss | 10-0-0 | win | improved | 79.7% | 40/40 |  |
| 88197859 | loss | 10-0-0 | win | improved | 37.0% | 58/58 |  |
| 88197860 | loss | 10-0-0 | win | improved | 72.3% | 31/31 |  |
| 88197906 | loss | 10-0-0 | win | improved | 67.8% | 48/48 |  |
| 88199435 | loss | 9-1-0 | win | improved | 33.7% | 89/89 |  |
| 88200003 | loss | 10-0-0 | win | improved | 72.3% | 43/43 |  |
| 88201040 | loss | 8-2-0 | win | improved | 47.5% | 81/81 |  |
| 88201604 | loss | 10-0-0 | win | improved | 50.1% | 58/58 |  |
| 88203591 | loss | 10-0-0 | win | improved | 57.5% | 53/53 |  |
| 88204121 | loss | 10-0-0 | win | improved | 51.9% | 49/49 |  |
| 88204232 | loss | 8-2-0 | win | improved | 48.6% | 86/86 |  |
| 88204771 | loss | 10-0-0 | win | improved | 36.5% | 57/57 |  |
| 88204990 | loss | 10-0-0 | win | improved | 53.3% | 46/46 |  |
| 88205283 | loss | 10-0-0 | win | improved | 41.8% | 67/67 |  |
| 88205289 | win | 10-0-0 | win | preserved_win | 69.8% | 44/44 |  |
| 88206332 | loss | 10-0-0 | win | improved | 74.0% | 50/50 |  |
| 88206818 | loss | 8-2-0 | win | improved | 32.2% | 56/56 |  |
| 88206895 | loss | 9-1-0 | win | improved | 39.0% | 57/57 |  |
| 88207928 | loss | 10-0-0 | win | improved | 45.6% | 55/55 |  |
| 88208293 | loss | 10-0-0 | win | improved | 53.0% | 67/67 |  |
| 88208966 | loss | 10-0-0 | win | improved | 26.6% | 82/82 |  |
| 88209048 | loss | 7-3-0 | win | improved | 43.0% | 46/46 |  |
| 88209398 | loss | 10-0-0 | win | improved | 59.7% | 40/40 |  |
| 88209472 | loss | 10-0-0 | win | improved | 28.1% | 81/81 |  |
| 88209993 | loss | 10-0-0 | win | improved | 38.3% | 80/80 |  |
| 88210517 | loss | 10-0-0 | win | improved | 80.3% | 39/39 |  |
| 88210975 | loss | 10-0-0 | win | improved | 79.4% | 27/27 |  |
| 88211042 | loss | 10-0-0 | win | improved | 56.2% | 47/47 |  |
| 88211566 | loss | 10-0-0 | win | improved | 41.2% | 101/101 |  |
| 88212701 | loss | 10-0-0 | win | improved | 39.0% | 57/57 |  |
| 88214700 | loss | 10-0-0 | win | improved | 79.5% | 79/79 |  |
| 88215619 | loss | 9-1-0 | win | improved | 53.7% | 55/55 |  |
| 88217155 | loss | 10-0-0 | win | improved | 70.8% | 37/37 |  |
| 88217476 | loss | 10-0-0 | win | improved | 49.1% | 53/53 |  |
| 88217824 | loss | 10-0-0 | win | improved | 43.9% | 57/57 |  |
| 88220136 | loss | 10-0-0 | win | improved | 51.0% | 63/63 |  |
| 88220489 | loss | 9-1-0 | win | improved | 52.5% | 41/41 |  |
| 88220566 | loss | 10-0-0 | win | improved | 46.7% | 49/49 |  |
| 88221583 | loss | 10-0-0 | win | improved | 75.9% | 28/28 |  |
| 88221669 | loss | 10-0-0 | win | improved | 72.3% | 30/30 |  |
| 88222802 | loss | 10-0-0 | win | improved | 75.6% | 30/30 |  |
| 88223081 | loss | 10-0-0 | win | improved | 74.2% | 29/29 |  |
| 88223586 | loss | 10-0-0 | win | improved | 36.2% | 71/71 |  |
| 88224733 | loss | 9-1-0 | win | improved | 51.5% | 78/78 |  |
| 88224901 | loss | 10-0-0 | win | improved | 69.0% | 71/71 |  |
| 88225199 | loss | 10-0-0 | win | improved | 57.9% | 45/45 |  |
| 88227532 | loss | 10-0-0 | win | improved | 72.5% | 35/35 |  |
| 88227555 | loss | 10-0-0 | win | improved | 65.0% | 54/54 |  |
| 88230163 | loss | 10-0-0 | win | improved | 39.1% | 63/63 |  |
| 88230176 | loss | 10-0-0 | win | improved | 74.0% | 47/47 |  |
| 88230489 | loss | 10-0-0 | win | improved | 40.4% | 66/66 |  |
| 88231229 | loss | 10-0-0 | win | improved | 54.3% | 31/31 |  |
| 88232593 | loss | 10-0-0 | win | improved | 58.0% | 62/62 |  |
| 88232765 | loss | 8-2-0 | win | improved | 52.3% | 49/49 |  |
| 88233128 | loss | 10-0-0 | win | improved | 54.4% | 51/51 |  |
| 88234701 | loss | 10-0-0 | win | improved | 71.2% | 28/28 |  |
| 88234900 | loss | 10-0-0 | win | improved | 77.8% | 43/43 |  |
| 88235276 | loss | 9-1-0 | win | improved | 53.0% | 67/67 |  |
| 88237853 | loss | 10-0-0 | win | improved | 69.4% | 36/36 |  |
| 88238542 | loss | 10-0-0 | win | improved | 79.3% | 38/38 |  |
| 88239078 | loss | 9-1-0 | win | improved | 76.5% | 59/59 |  |
| 88239095 | loss | 10-0-0 | win | improved | 70.3% | 66/66 |  |
| 88239132 | loss | 10-0-0 | win | improved | 72.9% | 39/39 |  |
| 88241784 | loss | 10-0-0 | win | improved | 43.8% | 68/68 |  |
| 88243841 | loss | 10-0-0 | win | improved | 45.2% | 82/82 |  |
| 88245069 | win | 10-0-0 | win | preserved_win | 75.0% | 34/34 |  |
| 88245592 | win | 10-0-0 | win | preserved_win | 50.5% | 30/30 |  |
| 88246129 | win | 9-1-0 | win | preserved_win | 86.9% | 51/51 |  |
| 88246713 | win | 10-0-0 | win | preserved_win | 81.8% | 38/38 |  |
| 88247233 | loss | 8-2-0 | win | improved | 67.8% | 34/34 |  |
| 88247782 | loss | 10-0-0 | win | improved | 34.0% | 74/74 |  |
| 88248321 | win | 9-1-0 | win | preserved_win | 50.4% | 37/37 |  |
| 88248844 | win | 9-1-0 | win | preserved_win | 72.7% | 47/47 |  |
| 88249366 | loss | 10-0-0 | win | improved | 60.5% | 52/52 |  |
| 88249393 | win | 10-0-0 | win | preserved_win | 74.9% | 39/39 |  |
| 88249914 | loss | 10-0-0 | win | improved | 73.3% | 33/33 |  |
| 88250446 | loss | 10-0-0 | win | improved | 43.3% | 48/48 |  |
| 88250998 | win | 9-1-0 | win | preserved_win | 52.9% | 50/50 |  |
| 88251535 | loss | 10-0-0 | win | improved | 55.4% | 50/50 |  |
| 88251789 | loss | 10-0-0 | win | improved | 59.9% | 37/37 |  |
| 88252076 | loss | 8-2-0 | win | improved | 60.0% | 75/75 |  |
| 88252610 | loss | 10-0-0 | win | improved | 54.0% | 64/64 |  |
| 88252759 | loss | 10-0-0 | win | improved | 55.2% | 39/39 |  |
| 88252837 | loss | 10-0-0 | win | improved | 31.0% | 41/41 |  |
| 88252856 | loss | 10-0-0 | win | improved | 52.1% | 53/53 |  |
| 88253125 | win | 10-0-0 | win | preserved_win | 77.3% | 33/33 |  |
| 88253320 | loss | 9-1-0 | win | improved | 42.7% | 59/59 |  |
| 88253642 | win | 9-1-0 | win | preserved_win | 77.8% | 52/52 |  |
| 88254173 | win | 9-1-0 | win | preserved_win | 58.0% | 49/49 |  |
| 88254686 | loss | 9-1-0 | win | improved | 53.0% | 31/31 |  |
| 88254832 | loss | 10-0-0 | win | improved | 55.9% | 67/67 |  |
| 88254923 | loss | 10-0-0 | win | improved | 51.5% | 47/47 |  |
| 88255227 | loss | 9-1-0 | win | improved | 50.7% | 44/44 |  |
| 88255365 | loss | 10-0-0 | win | improved | 49.7% | 44/44 |  |
| 88255773 | loss | 8-2-0 | win | improved | 77.7% | 54/54 |  |
| 88255893 | loss | 10-0-0 | win | improved | 65.6% | 29/29 |  |
| 88255975 | loss | 10-0-0 | win | improved | 49.1% | 57/57 |  |
| 88258615 | loss | 10-0-0 | win | improved | 66.8% | 49/49 |  |
| 88258639 | loss | 10-0-0 | win | improved | 65.7% | 55/55 |  |
| 88258841 | loss | 9-1-0 | win | improved | 45.3% | 77/77 |  |
| 88260624 | loss | 10-0-0 | win | improved | 50.4% | 53/53 |  |
| 88260674 | loss | 9-1-0 | win | improved | 35.7% | 73/73 |  |
| 88261149 | loss | 10-0-0 | win | improved | 68.5% | 35/35 |  |
| 88261688 | win | 10-0-0 | win | preserved_win | 81.8% | 37/37 |  |
| 88261733 | loss | 10-0-0 | win | improved | 50.4% | 48/48 |  |
| 88262219 | loss | 9-1-0 | win | improved | 61.9% | 45/45 |  |
| 88262752 | win | 10-0-0 | win | preserved_win | 81.3% | 44/44 |  |
| 88263295 | win | 10-0-0 | win | preserved_win | 57.0% | 91/91 |  |
| 88263822 | win | 10-0-0 | win | preserved_win | 60.1% | 59/59 |  |
| 88263861 | loss | 10-0-0 | win | improved | 45.1% | 68/68 |  |
| 88264373 | loss | 9-1-0 | win | improved | 65.8% | 27/27 |  |
| 88264404 | loss | 10-0-0 | win | improved | 79.1% | 40/40 |  |
| 88264935 | loss | 9-1-0 | win | improved | 65.7% | 40/40 |  |
| 88264972 | loss | 8-2-0 | win | improved | 49.4% | 43/43 |  |
| 88266013 | loss | 9-1-0 | win | improved | 31.8% | 65/65 |  |
| 88267625 | loss | 10-0-0 | win | improved | 55.8% | 37/37 |  |
| 88268465 | loss | 10-0-0 | win | improved | 74.1% | 39/39 |  |
| 88268514 | loss | 10-0-0 | win | improved | 62.2% | 40/40 |  |
| 88273125 | win | 10-0-0 | win | preserved_win | 84.8% | 30/30 |  |
| 88273894 | loss | 10-0-0 | win | improved | 62.6% | 34/34 |  |
| 88274852 | loss | 10-0-0 | win | improved | 69.1% | 43/43 |  |
| 88276586 | loss | 10-0-0 | win | improved | 59.7% | 71/71 |  |
| 88280043 | loss | 10-0-0 | win | improved | 44.8% | 34/34 |  |
| 88280276 | loss | 10-0-0 | win | improved | 50.4% | 46/46 |  |
| 88280581 | loss | 9-1-0 | win | improved | 49.1% | 53/53 |  |
| 88280592 | loss | 10-0-0 | win | improved | 50.0% | 63/63 |  |
| 88280823 | loss | 10-0-0 | win | improved | 52.0% | 84/84 |  |
| 88281112 | loss | 10-0-0 | win | improved | 74.9% | 73/73 |  |
| 88281365 | loss | 8-2-0 | win | improved | 56.1% | 69/69 |  |
| 88282965 | loss | 10-0-0 | win | improved | 56.4% | 37/37 |  |
| 88285383 | loss | 10-0-0 | win | improved | 44.9% | 89/89 |  |
| 88285882 | loss | 10-0-0 | win | improved | 49.0% | 41/41 |  |
| 88286403 | loss | 10-0-0 | win | improved | 48.0% | 63/63 |  |
| 88286429 | loss | 10-0-0 | win | improved | 37.7% | 61/61 |  |
| 88286928 | loss | 10-0-0 | win | improved | 48.0% | 57/57 |  |
| 88287449 | loss | 10-0-0 | win | improved | 41.7% | 60/60 |  |
| 88287943 | loss | 10-0-0 | win | improved | 63.1% | 42/42 |  |
| 88287982 | loss | 10-0-0 | win | improved | 47.1% | 59/59 |  |
| 88287988 | loss | 10-0-0 | win | improved | 39.7% | 72/72 |  |
| 88288578 | loss | 10-0-0 | win | improved | 27.1% | 72/72 |  |
| 88289166 | loss | 10-0-0 | win | improved | 35.4% | 91/91 |  |
| 88289703 | loss | 10-0-0 | win | improved | 32.5% | 80/80 |  |
| 88290370 | win | 10-0-0 | win | preserved_win | 87.3% | 48/48 |  |
| 88290739 | loss | 10-0-0 | win | improved | 45.9% | 77/77 |  |
| 88300893 | win | 10-0-0 | win | preserved_win | 72.7% | 56/56 |  |
| 88307667 | loss | 10-0-0 | win | improved | 85.4% | 54/54 |  |
| 88309157 | win | 10-0-0 | win | preserved_win | 79.4% | 43/43 |  |
| 88312062 | win | 10-0-0 | win | preserved_win | 57.5% | 28/28 |  |
| 88312577 | win | 10-0-0 | win | preserved_win | 83.6% | 37/37 |  |
| 88313112 | win | 8-2-0 | win | preserved_win | 44.5% | 48/48 |  |
| 88313620 | loss | 9-1-0 | win | improved | 62.5% | 58/58 |  |
| 88313673 | win | 10-0-0 | win | preserved_win | 53.9% | 64/64 |  |
| 88314138 | loss | 10-0-0 | win | improved | 46.5% | 39/39 |  |
| 88314664 | loss | 10-0-0 | win | improved | 66.7% | 29/29 |  |
| 88315183 | win | 10-0-0 | win | preserved_win | 84.8% | 53/53 |  |
| 88315493 | loss | 10-0-0 | win | improved | 66.5% | 34/34 |  |
| 88315696 | win | 10-0-0 | win | preserved_win | 67.8% | 44/44 |  |
| 88316214 | loss | 7-3-0 | win | improved | 61.5% | 39/39 |  |
| 88316726 | win | 10-0-0 | win | preserved_win | 43.4% | 80/80 |  |
| 88317257 | win | 10-0-0 | win | preserved_win | 50.9% | 60/60 |  |
| 88317769 | loss | 10-0-0 | win | improved | 56.1% | 91/91 |  |
| 88317878 | loss | 9-1-0 | win | improved | 58.8% | 51/51 |  |
| 88318294 | loss | 9-1-0 | win | improved | 49.8% | 42/42 |  |
| 88318822 | win | 10-0-0 | win | preserved_win | 74.8% | 26/26 |  |
| 88319336 | loss | 10-0-0 | win | improved | 27.0% | 73/73 |  |
| 88319853 | loss | 8-2-0 | win | improved | 57.4% | 33/33 |  |
| 88319971 | loss | 9-1-0 | win | improved | 46.3% | 63/63 |  |
| 88320365 | win | 10-0-0 | win | preserved_win | 82.9% | 52/52 |  |
| 88320386 | loss | 9-1-0 | win | improved | 54.4% | 62/62 |  |
| 88320504 | loss | 10-0-0 | win | improved | 48.5% | 49/49 |  |
| 88320896 | win | 7-3-0 | win | preserved_win | 80.2% | 71/71 |  |
| 88321003 | loss | 10-0-0 | win | improved | 73.4% | 36/36 |  |
| 88321041 | loss | 10-0-0 | win | improved | 76.3% | 27/27 |  |
| 88321420 | win | 10-0-0 | win | preserved_win | 87.5% | 66/66 |  |
| 88321956 | loss | 9-1-0 | win | improved | 57.9% | 52/52 |  |
| 88322041 | loss | 10-0-0 | win | improved | 45.9% | 63/63 |  |
| 88322048 | loss | 10-0-0 | win | improved | 54.8% | 49/49 |  |
| 88322049 | loss | 9-1-0 | win | improved | 65.5% | 34/34 |  |
| 88322536 | loss | 10-0-0 | win | improved | 48.2% | 51/51 |  |
| 88322611 | loss | 10-0-0 | win | improved | 49.1% | 69/69 |  |
| 88322619 | loss | 10-0-0 | win | improved | 65.5% | 35/35 |  |
| 88322631 | loss | 10-0-0 | win | improved | 48.5% | 68/68 |  |
| 88323052 | win | 10-0-0 | win | preserved_win | 83.5% | 71/71 |  |
| 88323135 | loss | 10-0-0 | win | improved | 67.8% | 51/51 |  |
| 88323138 | loss | 10-0-0 | win | improved | 49.8% | 50/50 |  |
| 88323140 | loss | 9-1-0 | win | improved | 80.2% | 44/44 |  |
| 88323143 | loss | 10-0-0 | win | improved | 73.9% | 31/31 |  |
| 88323585 | win | 10-0-0 | win | preserved_win | 86.7% | 45/45 |  |
| 88323647 | loss | 10-0-0 | win | improved | 61.1% | 39/39 |  |
| 88323654 | loss | 10-0-0 | win | improved | 74.2% | 43/43 |  |
| 88323655 | loss | 10-0-0 | win | improved | 53.0% | 32/32 |  |
| 88323658 | loss | 9-1-0 | win | improved | 52.8% | 35/35 |  |
| 88323669 | loss | 10-0-0 | win | improved | 62.4% | 27/27 |  |
| 88323677 | loss | 10-0-0 | win | improved | 46.0% | 50/50 |  |
| 88324102 | win | 9-1-0 | win | preserved_win | 48.1% | 54/54 |  |
| 88324178 | loss | 10-0-0 | win | improved | 74.8% | 28/28 |  |
| 88324185 | loss | 10-0-0 | win | improved | 74.6% | 47/47 |  |
| 88324192 | loss | 10-0-0 | win | improved | 78.4% | 26/26 |  |
| 88324221 | loss | 10-0-0 | win | improved | 71.2% | 38/38 |  |
| 88324625 | win | 10-0-0 | win | preserved_win | 86.0% | 35/35 |  |
| 88324685 | loss | 10-0-0 | win | improved | 55.8% | 52/52 |  |
| 88324686 | loss | 10-0-0 | win | improved | 68.6% | 36/36 |  |
| 88324689 | loss | 10-0-0 | win | improved | 73.5% | 32/32 |  |
| 88324692 | loss | 10-0-0 | win | improved | 82.8% | 20/20 |  |
| 88324700 | loss | 10-0-0 | win | improved | 61.3% | 33/33 |  |
| 88325152 | loss | 10-0-0 | win | improved | 45.2% | 71/71 |  |
| 88325690 | win | 10-0-0 | win | preserved_win | 39.1% | 88/88 |  |
| 88326205 | win | 10-0-0 | win | preserved_win | 60.5% | 32/32 |  |
| 88326718 | win | 10-0-0 | win | preserved_win | 75.1% | 40/40 |  |
| 88327230 | win | 10-0-0 | win | preserved_win | 84.7% | 29/29 |  |
| 88327756 | win | 9-1-0 | win | preserved_win | 60.2% | 41/41 |  |
| 88328259 | loss | 10-0-0 | win | improved | 60.5% | 28/28 |  |
| 88328805 | win | 10-0-0 | win | preserved_win | 81.7% | 44/44 |  |
| 88329324 | loss | 9-1-0 | win | improved | 79.7% | 43/43 |  |
| 88331455 | loss | 10-0-0 | win | improved | 83.5% | 20/20 |  |
| 88331982 | loss | 8-2-0 | win | improved | 42.5% | 39/39 |  |
| 88332513 | win | 10-0-0 | win | preserved_win | 85.3% | 56/56 |  |
| 88333025 | win | 9-1-0 | win | preserved_win | 71.4% | 38/38 |  |
| 88333545 | win | 10-0-0 | win | preserved_win | 75.8% | 71/71 |  |
| 88334078 | loss | 10-0-0 | win | improved | 64.6% | 36/36 |  |
| 88336523 | loss | 9-1-0 | win | improved | 38.1% | 61/61 |  |
| 88337057 | win | 10-0-0 | win | preserved_win | 84.3% | 29/29 |  |
| 88337586 | win | 10-0-0 | win | preserved_win | 84.2% | 32/32 |  |
| 88338118 | loss | 10-0-0 | win | improved | 71.3% | 41/41 |  |
| 88338652 | win | 10-0-0 | win | preserved_win | 56.4% | 56/56 |  |
| 88339176 | loss | 10-0-0 | win | improved | 63.7% | 65/65 |  |
| 88355725 | loss | 6-4-0 | win | improved | 63.2% | 60/60 |  |
| 88357353 | win | 10-0-0 | win | preserved_win | 81.1% | 58/58 |  |
| 88363833 | loss | 9-1-0 | win | improved | 45.5% | 51/51 |  |
| 88373545 | win | 10-0-0 | win | preserved_win | 84.0% | 31/31 |  |
| 88377883 | win | 10-0-0 | win | preserved_win | 82.7% | 21/21 |  |
| 88388662 | loss | 8-2-0 | win | improved | 83.2% | 30/30 |  |
| 88389031 | loss | 8-2-0 | win | improved | 48.8% | 60/60 |  |
| 88399423 | win | 10-0-0 | win | preserved_win | 59.6% | 71/71 |  |
| 88409367 | win | 10-0-0 | win | preserved_win | 62.7% | 30/30 |  |
| 88413119 | win | 10-0-0 | win | preserved_win | 87.8% | 38/38 |  |
| 88422207 | win | 10-0-0 | win | preserved_win | 78.7% | 30/30 |  |
| 88435827 | win | 10-0-0 | win | preserved_win | 34.7% | 50/50 |  |
| 88442046 | loss | 10-0-0 | win | improved | 38.9% | 70/70 |  |
| 88442583 | loss | 10-0-0 | win | improved | 41.7% | 52/52 |  |
| 88442585 | loss | 10-0-0 | win | improved | 46.3% | 43/43 |  |
| 88443133 | loss | 10-0-0 | win | improved | 53.5% | 57/57 |  |
| 88443655 | loss | 10-0-0 | win | improved | 74.1% | 35/35 |  |
| 88444167 | loss | 10-0-0 | win | improved | 53.1% | 52/52 |  |
| 88444648 | loss | 9-1-0 | win | improved | 85.3% | 28/28 |  |
| 88452396 | loss | 9-1-0 | win | improved | 78.4% | 34/34 |  |
| 88452950 | win | 9-1-0 | win | preserved_win | 90.8% | 47/47 |  |
| 88453474 | win | 10-0-0 | win | preserved_win | 63.6% | 49/49 |  |
| 88453996 | win | 10-0-0 | win | preserved_win | 76.7% | 27/27 |  |
| 88454521 | win | 10-0-0 | win | preserved_win | 79.9% | 67/67 |  |
| 88455120 | win | 9-1-0 | win | preserved_win | 67.7% | 46/46 |  |
| 88455645 | win | 10-0-0 | win | preserved_win | 89.5% | 51/51 |  |
| 88456174 | win | 10-0-0 | win | preserved_win | 76.8% | 37/37 |  |
| 88456712 | loss | 8-2-0 | win | improved | 47.0% | 46/46 |  |
| 88459353 | loss | 10-0-0 | win | improved | 44.9% | 54/54 |  |
| 88459908 | loss | 10-0-0 | win | improved | 57.5% | 24/24 |  |
| 88462124 | loss | 10-0-0 | win | improved | 77.9% | 30/30 |  |
| 88462569 | loss | 8-2-0 | win | improved | 62.7% | 41/41 |  |
| 88463244 | loss | 9-1-0 | win | improved | 45.7% | 47/47 |  |
| 88463694 | loss | 10-0-0 | win | improved | 56.5% | 61/61 |  |
| 88464320 | loss | 10-0-0 | win | improved | 60.8% | 29/29 |  |
| 88464738 | loss | 10-0-0 | win | improved | 55.6% | 55/55 |  |
| 88465305 | win | 10-0-0 | win | preserved_win | 83.0% | 19/19 |  |
| 88465824 | loss | 10-0-0 | win | improved | 63.9% | 46/46 |  |
| 88466344 | loss | 9-1-0 | win | improved | 37.1% | 61/61 |  |
| 88466967 | win | 10-0-0 | win | preserved_win | 61.9% | 42/42 |  |
| 88468139 | loss | 10-0-0 | win | improved | 80.7% | 29/29 |  |
| 88468688 | win | 10-0-0 | win | preserved_win | 50.1% | 59/59 |  |
| 88475900 | win | 10-0-0 | win | preserved_win | 75.2% | 39/39 |  |
| 88477511 | loss | 9-1-0 | win | improved | 42.3% | 62/62 |  |
| 88480123 | loss | 9-1-0 | win | improved | 82.2% | 30/30 |  |
| 88480304 | win | 10-0-0 | win | preserved_win | 79.1% | 45/45 |  |
| 88481733 | loss | 9-1-0 | win | improved | 92.3% | 41/41 |  |
| 88483285 | loss | 9-1-0 | win | improved | 73.0% | 44/44 |  |
| 88483990 | win | 8-2-0 | win | preserved_win | 50.8% | 57/57 |  |
| 88486593 | win | 10-0-0 | win | preserved_win | 87.4% | 43/43 |  |
| 88511515 | loss | 10-0-0 | win | improved | 68.3% | 36/36 |  |
| 88512578 | win | 10-0-0 | win | preserved_win | 76.8% | 57/57 |  |
| 88513116 | loss | 7-3-0 | win | improved | 47.8% | 55/55 |  |
| 88514796 | win | 10-0-0 | win | preserved_win | 73.4% | 38/38 |  |
| 88515340 | loss | 10-0-0 | win | improved | 56.1% | 49/49 |  |
| 88516436 | loss | 10-0-0 | win | improved | 61.2% | 28/28 |  |
| 88517037 | win | 10-0-0 | win | preserved_win | 54.3% | 68/68 |  |
| 88517460 | win | 10-0-0 | win | preserved_win | 50.5% | 70/70 |  |
| 88518016 | loss | 10-0-0 | win | improved | 65.8% | 38/38 |  |
| 88518164 | loss | 8-2-0 | win | improved | 67.5% | 54/54 |  |
| 88518572 | loss | 10-0-0 | win | improved | 71.4% | 33/33 |  |
| 88527351 | loss | 10-0-0 | win | improved | 70.8% | 35/35 |  |
| 88527969 | win | 10-0-0 | win | preserved_win | 73.4% | 34/34 |  |
| 88528562 | loss | 10-0-0 | win | improved | 66.0% | 34/34 |  |
| 88688530 | win | 10-0-0 | win | preserved_win | 82.8% | 40/40 |  |
| 88702243 | loss | 10-0-0 | win | improved | 54.7% | 52/52 |  |
| 88702773 | win | 10-0-0 | win | preserved_win | 75.4% | 29/29 |  |
| 88707615 | loss | 10-0-0 | win | improved | 51.0% | 39/39 |  |
| 88710371 | win | 10-0-0 | win | preserved_win | 52.7% | 60/60 |  |
| 88714591 | loss | 10-0-0 | win | improved | 75.8% | 34/34 |  |
| 88724413 | win | 10-0-0 | win | preserved_win | 83.5% | 37/37 |  |
| 88726741 | loss | 10-0-0 | win | improved | 73.8% | 46/46 |  |
| 88727264 | loss | 10-0-0 | win | improved | 63.9% | 49/49 |  |
| 88734629 | win | 10-0-0 | win | preserved_win | 76.9% | 27/27 |  |
| 88742222 | loss | 10-0-0 | win | improved | 50.2% | 78/78 |  |
| 88745200 | win | 10-0-0 | win | preserved_win | 91.1% | 51/51 |  |
| 88746412 | loss | 10-0-0 | win | improved | 82.0% | 42/42 |  |
| 88750615 | loss | 9-1-0 | win | improved | 59.9% | 69/69 |  |
| 88754803 | loss | 10-0-0 | win | improved | 80.7% | 23/23 |  |
| 88759036 | loss | 10-0-0 | win | improved | 61.9% | 58/58 |  |
| 88762215 | loss | 8-2-0 | win | improved | 47.4% | 59/59 |  |
| 88764905 | loss | 10-0-0 | win | improved | 75.6% | 40/40 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| — | No majority losses | — | — | — |

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
