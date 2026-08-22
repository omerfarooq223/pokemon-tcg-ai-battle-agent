# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **1167**
- Match results: **1127 wins, 40 losses, 0 draws**
- Match win rate: **96.57%**
- Per-replay majority: **386 wins, 3 losses, 0 ties**
- Recorded opponent-action usage: **55.26%**

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
| 88114269 | loss | 3-0-0 | win | improved | 46.3% | 19/19 |  |
| 88114272 | loss | 3-0-0 | win | improved | 85.7% | 15/15 |  |
| 88135168 | loss | 3-0-0 | win | improved | 81.8% | 7/7 |  |
| 88135718 | loss | 3-0-0 | win | improved | 65.3% | 17/17 |  |
| 88136757 | loss | 3-0-0 | win | improved | 70.5% | 12/12 |  |
| 88138839 | loss | 3-0-0 | win | improved | 47.8% | 20/20 |  |
| 88139351 | loss | 3-0-0 | win | improved | 55.6% | 11/11 |  |
| 88139876 | loss | 3-0-0 | win | improved | 44.9% | 17/17 |  |
| 88139877 | loss | 3-0-0 | win | improved | 33.1% | 17/17 |  |
| 88139889 | loss | 3-0-0 | win | improved | 42.5% | 20/20 |  |
| 88140397 | loss | 3-0-0 | win | improved | 48.4% | 14/14 |  |
| 88140434 | loss | 3-0-0 | win | improved | 79.2% | 13/13 |  |
| 88140934 | loss | 3-0-0 | win | improved | 39.0% | 16/16 |  |
| 88141449 | loss | 3-0-0 | win | improved | 54.8% | 16/16 |  |
| 88141464 | loss | 3-0-0 | win | improved | 39.3% | 20/20 |  |
| 88141972 | loss | 3-0-0 | win | improved | 46.9% | 23/23 |  |
| 88142495 | loss | 3-0-0 | win | improved | 68.1% | 14/14 |  |
| 88143033 | loss | 3-0-0 | win | improved | 36.9% | 17/17 |  |
| 88143428 | loss | 3-0-0 | win | improved | 71.7% | 10/10 |  |
| 88143558 | loss | 3-0-0 | win | improved | 34.0% | 16/16 |  |
| 88143960 | loss | 3-0-0 | win | improved | 93.5% | 9/9 |  |
| 88144074 | loss | 3-0-0 | win | improved | 29.5% | 29/29 |  |
| 88144497 | win | 3-0-0 | win | preserved_win | 78.5% | 15/15 |  |
| 88145058 | loss | 3-0-0 | win | improved | 49.1% | 16/16 |  |
| 88145588 | loss | 3-0-0 | win | improved | 73.3% | 11/11 |  |
| 88145696 | loss | 3-0-0 | win | improved | 41.5% | 18/18 |  |
| 88146122 | loss | 3-0-0 | win | improved | 38.6% | 22/22 |  |
| 88146648 | win | 3-0-0 | win | preserved_win | 75.0% | 13/13 |  |
| 88147191 | loss | 3-0-0 | win | improved | 72.5% | 8/8 |  |
| 88147227 | loss | 3-0-0 | win | improved | 74.4% | 12/12 |  |
| 88147702 | loss | 3-0-0 | win | improved | 80.8% | 12/12 |  |
| 88148218 | loss | 3-0-0 | win | improved | 88.1% | 11/11 |  |
| 88148312 | loss | 3-0-0 | win | improved | 40.8% | 15/15 |  |
| 88148790 | win | 3-0-0 | win | preserved_win | 83.3% | 6/6 |  |
| 88148861 | loss | 3-0-0 | win | improved | 31.1% | 16/16 |  |
| 88149240 | loss | 3-0-0 | win | improved | 77.8% | 14/14 |  |
| 88149380 | loss | 3-0-0 | win | improved | 25.4% | 21/21 |  |
| 88149406 | loss | 3-0-0 | win | improved | 80.7% | 21/21 |  |
| 88149782 | win | 3-0-0 | win | preserved_win | 41.0% | 11/11 |  |
| 88149906 | loss | 3-0-0 | win | improved | 40.3% | 16/16 |  |
| 88150296 | win | 3-0-0 | win | preserved_win | 80.5% | 8/8 |  |
| 88150868 | loss | 3-0-0 | win | improved | 56.7% | 17/17 |  |
| 88151481 | loss | 3-0-0 | win | improved | 78.4% | 27/27 |  |
| 88152037 | win | 3-0-0 | win | preserved_win | 79.1% | 12/12 |  |
| 88152577 | loss | 3-0-0 | win | improved | 62.9% | 8/8 |  |
| 88153002 | loss | 3-0-0 | win | improved | 64.8% | 13/13 |  |
| 88153112 | loss | 3-0-0 | win | improved | 73.7% | 12/12 |  |
| 88153551 | win | 3-0-0 | win | preserved_win | 90.5% | 22/22 |  |
| 88153647 | win | 3-0-0 | win | preserved_win | 84.7% | 15/15 |  |
| 88154072 | loss | 3-0-0 | win | improved | 56.2% | 17/17 |  |
| 88154188 | loss | 3-0-0 | win | improved | 57.0% | 18/18 |  |
| 88154615 | loss | 3-0-0 | win | improved | 93.3% | 11/11 |  |
| 88154720 | loss | 3-0-0 | win | improved | 75.9% | 38/38 |  |
| 88155167 | loss | 3-0-0 | win | improved | 40.7% | 18/18 |  |
| 88155258 | loss | 3-0-0 | win | improved | 92.3% | 8/8 |  |
| 88155735 | loss | 3-0-0 | win | improved | 78.8% | 6/6 |  |
| 88155807 | loss | 3-0-0 | win | improved | 51.4% | 12/12 |  |
| 88156264 | loss | 3-0-0 | win | improved | 80.8% | 5/5 |  |
| 88156364 | win | 3-0-0 | win | preserved_win | 68.6% | 10/10 |  |
| 88156894 | win | 3-0-0 | win | preserved_win | 90.0% | 54/54 |  |
| 88157011 | loss | 3-0-0 | win | improved | 41.5% | 18/18 |  |
| 88157416 | win | 3-0-0 | win | preserved_win | 74.1% | 9/9 |  |
| 88157484 | win | 3-0-0 | win | preserved_win | 82.4% | 17/17 |  |
| 88157952 | win | 3-0-0 | win | preserved_win | 75.0% | 8/8 |  |
| 88170362 | loss | 2-1-0 | win | improved | 53.0% | 20/20 |  |
| 88181889 | win | 3-0-0 | win | preserved_win | 75.6% | 7/7 |  |
| 88183542 | loss | 3-0-0 | win | improved | 77.5% | 18/18 |  |
| 88187788 | win | 3-0-0 | win | preserved_win | 85.7% | 7/7 |  |
| 88189899 | loss | 3-0-0 | win | improved | 71.8% | 9/9 |  |
| 88190488 | loss | 3-0-0 | win | improved | 50.0% | 15/15 |  |
| 88190720 | loss | 3-0-0 | win | improved | 54.8% | 14/14 |  |
| 88191459 | loss | 3-0-0 | win | improved | 71.4% | 13/13 |  |
| 88191506 | loss | 3-0-0 | win | improved | 53.8% | 14/14 |  |
| 88191988 | loss | 3-0-0 | win | improved | 57.4% | 18/18 |  |
| 88192025 | loss | 3-0-0 | win | improved | 51.6% | 14/14 |  |
| 88192363 | loss | 3-0-0 | win | improved | 86.4% | 11/11 |  |
| 88192550 | loss | 2-1-0 | win | improved | 42.7% | 14/14 |  |
| 88193019 | loss | 3-0-0 | win | improved | 74.5% | 12/12 |  |
| 88193372 | loss | 2-1-0 | win | improved | 37.0% | 7/7 |  |
| 88193551 | loss | 3-0-0 | win | improved | 87.3% | 9/9 |  |
| 88193634 | loss | 3-0-0 | win | improved | 68.9% | 10/10 |  |
| 88195735 | loss | 3-0-0 | win | improved | 57.9% | 24/24 |  |
| 88197859 | loss | 3-0-0 | win | improved | 30.1% | 18/18 |  |
| 88197860 | loss | 3-0-0 | win | improved | 53.9% | 12/12 |  |
| 88197906 | loss | 3-0-0 | win | improved | 68.0% | 33/33 |  |
| 88199435 | loss | 3-0-0 | win | improved | 34.4% | 25/25 |  |
| 88200003 | loss | 3-0-0 | win | improved | 82.3% | 14/14 |  |
| 88201040 | loss | 3-0-0 | win | improved | 33.0% | 23/23 |  |
| 88201604 | loss | 3-0-0 | win | improved | 63.8% | 18/18 |  |
| 88203591 | loss | 3-0-0 | win | improved | 71.4% | 13/13 |  |
| 88204121 | loss | 3-0-0 | win | improved | 74.7% | 12/12 |  |
| 88204232 | loss | 3-0-0 | win | improved | 41.3% | 21/21 |  |
| 88204771 | loss | 3-0-0 | win | improved | 50.0% | 18/18 |  |
| 88204990 | loss | 3-0-0 | win | improved | 45.0% | 34/34 |  |
| 88205283 | loss | 3-0-0 | win | improved | 60.0% | 11/11 |  |
| 88205289 | win | 3-0-0 | win | preserved_win | 67.9% | 17/17 |  |
| 88206332 | loss | 3-0-0 | win | improved | 74.8% | 14/14 |  |
| 88206818 | loss | 1-2-0 | loss | unresolved_loss | 42.2% | 15/15 | board exhausted; inspect trace |
| 88206895 | loss | 3-0-0 | win | improved | 44.0% | 18/18 |  |
| 88207928 | loss | 3-0-0 | win | improved | 47.5% | 16/16 |  |
| 88208293 | loss | 3-0-0 | win | improved | 35.1% | 20/20 |  |
| 88208966 | loss | 3-0-0 | win | improved | 32.5% | 16/16 |  |
| 88209048 | loss | 3-0-0 | win | improved | 48.4% | 20/20 |  |
| 88209398 | loss | 3-0-0 | win | improved | 53.1% | 13/13 |  |
| 88209472 | loss | 3-0-0 | win | improved | 36.7% | 24/24 |  |
| 88209993 | loss | 3-0-0 | win | improved | 46.2% | 27/27 |  |
| 88210517 | loss | 3-0-0 | win | improved | 82.4% | 14/14 |  |
| 88210975 | loss | 3-0-0 | win | improved | 75.9% | 7/7 |  |
| 88211042 | loss | 2-1-0 | win | improved | 64.4% | 16/16 |  |
| 88211566 | loss | 3-0-0 | win | improved | 43.2% | 22/22 |  |
| 88212701 | loss | 3-0-0 | win | improved | 38.2% | 21/21 |  |
| 88214700 | loss | 3-0-0 | win | improved | 66.2% | 51/51 |  |
| 88215619 | loss | 3-0-0 | win | improved | 70.5% | 17/17 |  |
| 88217155 | loss | 3-0-0 | win | improved | 71.4% | 9/9 |  |
| 88217476 | loss | 3-0-0 | win | improved | 50.0% | 48/48 |  |
| 88217824 | loss | 3-0-0 | win | improved | 47.6% | 15/15 |  |
| 88220136 | loss | 3-0-0 | win | improved | 49.2% | 18/18 |  |
| 88220489 | loss | 3-0-0 | win | improved | 73.9% | 10/10 |  |
| 88220566 | loss | 3-0-0 | win | improved | 54.3% | 16/16 |  |
| 88221583 | loss | 3-0-0 | win | improved | 93.9% | 6/6 |  |
| 88221669 | loss | 3-0-0 | win | improved | 76.7% | 8/8 |  |
| 88222802 | loss | 3-0-0 | win | improved | 29.4% | 24/24 |  |
| 88223081 | loss | 3-0-0 | win | improved | 69.7% | 8/8 |  |
| 88223586 | loss | 3-0-0 | win | improved | 37.1% | 23/23 |  |
| 88224733 | loss | 3-0-0 | win | improved | 48.0% | 23/23 |  |
| 88224901 | loss | 3-0-0 | win | improved | 65.2% | 23/23 |  |
| 88225199 | loss | 2-1-0 | win | improved | 43.0% | 21/21 |  |
| 88227532 | loss | 3-0-0 | win | improved | 73.2% | 10/10 |  |
| 88227555 | loss | 3-0-0 | win | improved | 41.6% | 17/17 |  |
| 88230163 | loss | 3-0-0 | win | improved | 38.9% | 25/25 |  |
| 88230176 | loss | 3-0-0 | win | improved | 70.3% | 14/14 |  |
| 88230489 | loss | 3-0-0 | win | improved | 39.9% | 23/23 |  |
| 88231229 | loss | 3-0-0 | win | improved | 29.5% | 16/16 |  |
| 88232593 | loss | 3-0-0 | win | improved | 68.2% | 12/12 |  |
| 88232765 | loss | 3-0-0 | win | improved | 63.4% | 11/11 |  |
| 88233128 | loss | 3-0-0 | win | improved | 80.5% | 9/9 |  |
| 88234701 | loss | 3-0-0 | win | improved | 78.4% | 45/45 |  |
| 88234900 | loss | 3-0-0 | win | improved | 82.6% | 12/12 |  |
| 88235276 | loss | 3-0-0 | win | improved | 61.8% | 13/13 |  |
| 88237853 | loss | 3-0-0 | win | improved | 77.8% | 13/13 |  |
| 88238542 | loss | 3-0-0 | win | improved | 90.1% | 56/56 |  |
| 88239078 | loss | 3-0-0 | win | improved | 77.3% | 14/14 |  |
| 88239095 | loss | 3-0-0 | win | improved | 52.1% | 13/13 |  |
| 88239132 | loss | 3-0-0 | win | improved | 68.8% | 12/12 |  |
| 88241784 | loss | 3-0-0 | win | improved | 42.3% | 22/22 |  |
| 88243841 | loss | 3-0-0 | win | improved | 35.2% | 32/32 |  |
| 88245069 | win | 3-0-0 | win | preserved_win | 70.0% | 7/7 |  |
| 88245592 | win | 3-0-0 | win | preserved_win | 55.3% | 15/15 |  |
| 88246129 | win | 2-1-0 | win | preserved_win | 96.7% | 10/10 |  |
| 88246713 | win | 3-0-0 | win | preserved_win | 78.3% | 10/10 |  |
| 88247233 | loss | 2-1-0 | win | improved | 62.4% | 14/14 |  |
| 88247782 | loss | 3-0-0 | win | improved | 33.8% | 17/17 |  |
| 88248321 | win | 3-0-0 | win | preserved_win | 38.5% | 7/7 |  |
| 88248844 | win | 3-0-0 | win | preserved_win | 70.4% | 20/20 |  |
| 88249366 | loss | 3-0-0 | win | improved | 63.0% | 7/7 |  |
| 88249393 | win | 3-0-0 | win | preserved_win | 57.3% | 18/18 |  |
| 88249914 | loss | 3-0-0 | win | improved | 60.9% | 12/12 |  |
| 88250446 | loss | 3-0-0 | win | improved | 34.4% | 16/16 |  |
| 88250998 | win | 3-0-0 | win | preserved_win | 47.5% | 23/23 |  |
| 88251535 | loss | 3-0-0 | win | improved | 47.7% | 17/17 |  |
| 88251789 | loss | 3-0-0 | win | improved | 45.3% | 14/14 |  |
| 88252076 | loss | 3-0-0 | win | improved | 53.7% | 11/11 |  |
| 88252610 | loss | 3-0-0 | win | improved | 93.8% | 10/10 |  |
| 88252759 | loss | 3-0-0 | win | improved | 67.7% | 12/12 |  |
| 88252837 | loss | 3-0-0 | win | improved | 37.7% | 11/11 |  |
| 88252856 | loss | 3-0-0 | win | improved | 55.8% | 14/14 |  |
| 88253125 | win | 3-0-0 | win | preserved_win | 62.6% | 17/17 |  |
| 88253320 | loss | 3-0-0 | win | improved | 49.1% | 21/21 |  |
| 88253642 | win | 3-0-0 | win | preserved_win | 71.4% | 10/10 |  |
| 88254173 | win | 3-0-0 | win | preserved_win | 57.4% | 18/18 |  |
| 88254686 | loss | 2-1-0 | win | improved | 36.2% | 21/21 |  |
| 88254832 | loss | 3-0-0 | win | improved | 46.7% | 28/28 |  |
| 88254923 | loss | 3-0-0 | win | improved | 58.2% | 11/11 |  |
| 88255227 | loss | 3-0-0 | win | improved | 54.2% | 13/13 |  |
| 88255365 | loss | 3-0-0 | win | improved | 35.9% | 14/14 |  |
| 88255773 | loss | 2-1-0 | win | improved | 72.8% | 19/19 |  |
| 88255893 | loss | 3-0-0 | win | improved | 82.2% | 10/10 |  |
| 88255975 | loss | 3-0-0 | win | improved | 60.1% | 18/18 |  |
| 88258615 | loss | 3-0-0 | win | improved | 58.3% | 12/12 |  |
| 88258639 | loss | 3-0-0 | win | improved | 82.6% | 13/13 |  |
| 88258841 | loss | 3-0-0 | win | improved | 49.0% | 30/30 |  |
| 88260624 | loss | 3-0-0 | win | improved | 44.4% | 22/22 |  |
| 88260674 | loss | 3-0-0 | win | improved | 34.2% | 12/12 |  |
| 88261149 | loss | 3-0-0 | win | improved | 47.3% | 13/13 |  |
| 88261688 | win | 3-0-0 | win | preserved_win | 84.6% | 7/7 |  |
| 88261733 | loss | 3-0-0 | win | improved | 41.9% | 17/17 |  |
| 88262219 | loss | 3-0-0 | win | improved | 84.6% | 7/7 |  |
| 88262752 | win | 3-0-0 | win | preserved_win | 80.6% | 16/16 |  |
| 88263295 | win | 3-0-0 | win | preserved_win | 53.4% | 18/18 |  |
| 88263822 | win | 3-0-0 | win | preserved_win | 77.4% | 16/16 |  |
| 88263861 | loss | 3-0-0 | win | improved | 45.1% | 24/24 |  |
| 88264373 | loss | 3-0-0 | win | improved | 84.4% | 6/6 |  |
| 88264404 | loss | 3-0-0 | win | improved | 83.9% | 12/12 |  |
| 88264935 | loss | 2-1-0 | win | improved | 92.7% | 9/9 |  |
| 88264972 | loss | 3-0-0 | win | improved | 87.1% | 8/8 |  |
| 88266013 | loss | 3-0-0 | win | improved | 30.3% | 19/19 |  |
| 88267625 | loss | 3-0-0 | win | improved | 81.1% | 8/8 |  |
| 88268465 | loss | 3-0-0 | win | improved | 80.9% | 13/13 |  |
| 88268514 | loss | 3-0-0 | win | improved | 80.0% | 10/10 |  |
| 88273125 | win | 2-1-0 | win | preserved_win | 86.8% | 5/5 |  |
| 88273894 | loss | 3-0-0 | win | improved | 45.0% | 10/10 |  |
| 88274852 | loss | 3-0-0 | win | improved | 84.2% | 8/8 |  |
| 88276586 | loss | 3-0-0 | win | improved | 46.7% | 25/25 |  |
| 88280043 | loss | 3-0-0 | win | improved | 65.2% | 6/6 |  |
| 88280276 | loss | 3-0-0 | win | improved | 58.3% | 12/12 |  |
| 88280581 | loss | 2-1-0 | win | improved | 49.7% | 9/9 |  |
| 88280592 | loss | 3-0-0 | win | improved | 45.5% | 16/16 |  |
| 88280823 | loss | 3-0-0 | win | improved | 43.6% | 26/26 |  |
| 88281112 | loss | 2-1-0 | win | improved | 81.0% | 11/11 |  |
| 88281365 | loss | 2-1-0 | win | improved | 63.5% | 14/14 |  |
| 88282965 | loss | 3-0-0 | win | improved | 54.7% | 21/21 |  |
| 88285383 | loss | 3-0-0 | win | improved | 52.7% | 18/18 |  |
| 88285882 | loss | 3-0-0 | win | improved | 48.7% | 23/23 |  |
| 88286403 | loss | 3-0-0 | win | improved | 40.7% | 13/13 |  |
| 88286429 | loss | 3-0-0 | win | improved | 30.3% | 28/28 |  |
| 88286928 | loss | 3-0-0 | win | improved | 36.6% | 31/31 |  |
| 88287449 | loss | 3-0-0 | win | improved | 58.9% | 13/13 |  |
| 88287943 | loss | 3-0-0 | win | improved | 63.8% | 12/12 |  |
| 88287982 | loss | 3-0-0 | win | improved | 48.2% | 22/22 |  |
| 88287988 | loss | 3-0-0 | win | improved | 47.1% | 16/16 |  |
| 88288578 | loss | 3-0-0 | win | improved | 31.5% | 23/23 |  |
| 88289166 | loss | 3-0-0 | win | improved | 40.3% | 28/28 |  |
| 88289703 | loss | 3-0-0 | win | improved | 28.1% | 26/26 |  |
| 88290370 | win | 3-0-0 | win | preserved_win | 89.7% | 15/15 |  |
| 88290739 | loss | 3-0-0 | win | improved | 48.2% | 13/13 |  |
| 88300893 | win | 3-0-0 | win | preserved_win | 70.1% | 17/17 |  |
| 88307667 | loss | 3-0-0 | win | improved | 87.0% | 13/13 |  |
| 88309157 | win | 3-0-0 | win | preserved_win | 87.2% | 11/11 |  |
| 88312062 | win | 3-0-0 | win | preserved_win | 69.2% | 6/6 |  |
| 88312577 | win | 3-0-0 | win | preserved_win | 83.3% | 18/18 |  |
| 88313112 | win | 2-1-0 | win | preserved_win | 36.9% | 15/15 |  |
| 88313620 | loss | 3-0-0 | win | improved | 57.7% | 22/22 |  |
| 88313673 | win | 2-1-0 | win | preserved_win | 70.9% | 12/12 |  |
| 88314138 | loss | 3-0-0 | win | improved | 46.4% | 11/11 |  |
| 88314664 | loss | 2-1-0 | win | improved | 66.7% | 11/11 |  |
| 88315183 | win | 3-0-0 | win | preserved_win | 81.4% | 20/20 |  |
| 88315493 | loss | 3-0-0 | win | improved | 51.3% | 19/19 |  |
| 88315696 | win | 3-0-0 | win | preserved_win | 71.4% | 16/16 |  |
| 88316214 | loss | 2-1-0 | win | improved | 82.4% | 10/10 |  |
| 88316726 | win | 3-0-0 | win | preserved_win | 45.9% | 21/21 |  |
| 88317257 | win | 3-0-0 | win | preserved_win | 40.1% | 13/13 |  |
| 88317769 | loss | 3-0-0 | win | improved | 77.3% | 7/7 |  |
| 88317878 | loss | 3-0-0 | win | improved | 52.9% | 11/11 |  |
| 88318294 | loss | 3-0-0 | win | improved | 65.2% | 10/10 |  |
| 88318822 | win | 3-0-0 | win | preserved_win | 85.0% | 7/7 |  |
| 88319336 | loss | 3-0-0 | win | improved | 19.6% | 22/22 |  |
| 88319853 | loss | 3-0-0 | win | improved | 42.2% | 18/18 |  |
| 88319971 | loss | 3-0-0 | win | improved | 39.7% | 19/19 |  |
| 88320365 | win | 3-0-0 | win | preserved_win | 84.1% | 17/17 |  |
| 88320386 | loss | 3-0-0 | win | improved | 53.2% | 15/15 |  |
| 88320504 | loss | 3-0-0 | win | improved | 45.1% | 19/19 |  |
| 88320896 | win | 2-1-0 | win | preserved_win | 90.7% | 9/9 |  |
| 88321003 | loss | 3-0-0 | win | improved | 56.6% | 16/16 |  |
| 88321041 | loss | 3-0-0 | win | improved | 80.0% | 9/9 |  |
| 88321420 | win | 3-0-0 | win | preserved_win | 89.4% | 25/25 |  |
| 88321956 | loss | 3-0-0 | win | improved | 88.4% | 8/8 |  |
| 88322041 | loss | 3-0-0 | win | improved | 55.6% | 15/15 |  |
| 88322048 | loss | 3-0-0 | win | improved | 58.7% | 20/20 |  |
| 88322049 | loss | 3-0-0 | win | improved | 82.5% | 7/7 |  |
| 88322536 | loss | 3-0-0 | win | improved | 54.3% | 13/13 |  |
| 88322611 | loss | 3-0-0 | win | improved | 60.1% | 20/20 |  |
| 88322619 | loss | 3-0-0 | win | improved | 46.3% | 11/11 |  |
| 88322631 | loss | 3-0-0 | win | improved | 58.4% | 19/19 |  |
| 88323052 | win | 3-0-0 | win | preserved_win | 87.7% | 18/18 |  |
| 88323135 | loss | 3-0-0 | win | improved | 77.3% | 11/11 |  |
| 88323138 | loss | 3-0-0 | win | improved | 46.2% | 12/12 |  |
| 88323140 | loss | 3-0-0 | win | improved | 67.9% | 15/15 |  |
| 88323143 | loss | 3-0-0 | win | improved | 78.1% | 14/14 |  |
| 88323585 | win | 3-0-0 | win | preserved_win | 84.5% | 12/12 |  |
| 88323647 | loss | 3-0-0 | win | improved | 76.4% | 10/10 |  |
| 88323654 | loss | 2-1-0 | win | improved | 69.6% | 8/8 |  |
| 88323655 | loss | 3-0-0 | win | improved | 74.5% | 10/10 |  |
| 88323658 | loss | 2-1-0 | win | improved | 67.1% | 6/6 |  |
| 88323669 | loss | 3-0-0 | win | improved | 71.8% | 10/10 |  |
| 88323677 | loss | 2-1-0 | win | improved | 56.2% | 17/17 |  |
| 88324102 | win | 3-0-0 | win | preserved_win | 56.1% | 25/25 |  |
| 88324178 | loss | 3-0-0 | win | improved | 75.9% | 8/8 |  |
| 88324185 | loss | 3-0-0 | win | improved | 85.2% | 17/17 |  |
| 88324192 | loss | 3-0-0 | win | improved | 84.1% | 13/13 |  |
| 88324221 | loss | 3-0-0 | win | improved | 76.0% | 7/7 |  |
| 88324625 | win | 3-0-0 | win | preserved_win | 86.4% | 50/50 |  |
| 88324685 | loss | 3-0-0 | win | improved | 47.3% | 16/16 |  |
| 88324686 | loss | 3-0-0 | win | improved | 71.4% | 8/8 |  |
| 88324689 | loss | 3-0-0 | win | improved | 79.1% | 12/12 |  |
| 88324692 | loss | 3-0-0 | win | improved | 81.0% | 8/8 |  |
| 88324700 | loss | 3-0-0 | win | improved | 65.1% | 9/9 |  |
| 88325152 | loss | 2-1-0 | win | improved | 62.6% | 15/15 |  |
| 88325690 | win | 3-0-0 | win | preserved_win | 27.7% | 24/24 |  |
| 88326205 | win | 3-0-0 | win | preserved_win | 81.0% | 5/5 |  |
| 88326718 | win | 3-0-0 | win | preserved_win | 82.0% | 15/15 |  |
| 88327230 | win | 3-0-0 | win | preserved_win | 79.7% | 13/13 |  |
| 88327756 | win | 2-1-0 | win | preserved_win | 43.0% | 13/13 |  |
| 88328259 | loss | 3-0-0 | win | improved | 73.1% | 8/8 |  |
| 88328805 | win | 3-0-0 | win | preserved_win | 90.6% | 12/12 |  |
| 88329324 | loss | 2-1-0 | win | improved | 85.6% | 13/13 |  |
| 88331455 | loss | 3-0-0 | win | improved | 80.8% | 6/6 |  |
| 88331982 | loss | 3-0-0 | win | improved | 63.3% | 16/16 |  |
| 88332513 | win | 3-0-0 | win | preserved_win | 83.6% | 16/16 |  |
| 88333025 | win | 3-0-0 | win | preserved_win | 74.1% | 11/11 |  |
| 88333545 | win | 3-0-0 | win | preserved_win | 64.5% | 18/18 |  |
| 88334078 | loss | 3-0-0 | win | improved | 74.2% | 9/9 |  |
| 88336523 | loss | 3-0-0 | win | improved | 47.2% | 12/12 |  |
| 88337057 | win | 3-0-0 | win | preserved_win | 94.5% | 8/8 |  |
| 88337586 | win | 3-0-0 | win | preserved_win | 87.5% | 10/10 |  |
| 88338118 | loss | 3-0-0 | win | improved | 63.9% | 24/24 |  |
| 88338652 | win | 3-0-0 | win | preserved_win | 68.5% | 22/22 |  |
| 88339176 | loss | 3-0-0 | win | improved | 41.6% | 29/29 |  |
| 88355725 | loss | 0-3-0 | loss | unresolved_loss | 59.8% | 6/6 | board exhausted; inspect trace |
| 88357353 | win | 3-0-0 | win | preserved_win | 85.6% | 20/20 |  |
| 88363833 | loss | 3-0-0 | win | improved | 47.8% | 22/22 |  |
| 88373545 | win | 3-0-0 | win | preserved_win | 84.0% | 8/8 |  |
| 88377883 | win | 3-0-0 | win | preserved_win | 88.0% | 6/6 |  |
| 88388662 | loss | 2-1-0 | win | improved | 89.6% | 12/12 |  |
| 88389031 | loss | 3-0-0 | win | improved | 75.0% | 8/8 |  |
| 88399423 | win | 2-1-0 | win | preserved_win | 60.7% | 14/14 |  |
| 88409367 | win | 3-0-0 | win | preserved_win | 43.2% | 14/14 |  |
| 88413119 | win | 3-0-0 | win | preserved_win | 89.4% | 19/19 |  |
| 88422207 | win | 3-0-0 | win | preserved_win | 80.7% | 14/14 |  |
| 88435827 | win | 3-0-0 | win | preserved_win | 25.5% | 23/23 |  |
| 88442046 | loss | 3-0-0 | win | improved | 73.6% | 11/11 |  |
| 88442583 | loss | 3-0-0 | win | improved | 43.3% | 13/13 |  |
| 88442585 | loss | 3-0-0 | win | improved | 42.7% | 19/19 |  |
| 88443133 | loss | 3-0-0 | win | improved | 40.7% | 19/19 |  |
| 88443655 | loss | 3-0-0 | win | improved | 79.5% | 9/9 |  |
| 88444167 | loss | 3-0-0 | win | improved | 50.0% | 14/14 |  |
| 88444648 | loss | 3-0-0 | win | improved | 48.0% | 14/14 |  |
| 88452396 | loss | 3-0-0 | win | improved | 83.8% | 10/10 |  |
| 88452950 | win | 3-0-0 | win | preserved_win | 87.5% | 9/9 |  |
| 88453474 | win | 3-0-0 | win | preserved_win | 68.3% | 13/13 |  |
| 88453996 | win | 3-0-0 | win | preserved_win | 77.8% | 6/6 |  |
| 88454521 | win | 3-0-0 | win | preserved_win | 74.0% | 16/16 |  |
| 88455120 | win | 3-0-0 | win | preserved_win | 48.5% | 14/14 |  |
| 88455645 | win | 3-0-0 | win | preserved_win | 91.9% | 12/12 |  |
| 88456174 | win | 3-0-0 | win | preserved_win | 73.7% | 17/17 |  |
| 88456712 | loss | 3-0-0 | win | improved | 36.7% | 20/20 |  |
| 88459353 | loss | 2-1-0 | win | improved | 39.6% | 19/19 |  |
| 88459908 | loss | 3-0-0 | win | improved | 75.7% | 8/8 |  |
| 88462124 | loss | 3-0-0 | win | improved | 76.6% | 13/13 |  |
| 88462569 | loss | 3-0-0 | win | improved | 55.1% | 22/22 |  |
| 88463244 | loss | 2-1-0 | win | improved | 38.7% | 17/17 |  |
| 88463694 | loss | 3-0-0 | win | improved | 62.8% | 16/16 |  |
| 88464320 | loss | 3-0-0 | win | improved | 66.7% | 13/13 |  |
| 88464738 | loss | 3-0-0 | win | improved | 81.2% | 14/14 |  |
| 88465305 | win | 3-0-0 | win | preserved_win | 94.0% | 7/7 |  |
| 88465824 | loss | 3-0-0 | win | improved | 73.2% | 10/10 |  |
| 88466344 | loss | 3-0-0 | win | improved | 37.5% | 24/24 |  |
| 88466967 | win | 1-2-0 | loss | regressed | 77.0% | 5/5 | deck/resource endurance; inspect trace |
| 88468139 | loss | 3-0-0 | win | improved | 84.4% | 16/16 |  |
| 88468688 | win | 3-0-0 | win | preserved_win | 50.0% | 14/14 |  |
| 88475900 | win | 3-0-0 | win | preserved_win | 88.2% | 11/11 |  |
| 88477511 | loss | 3-0-0 | win | improved | 40.7% | 15/15 |  |
| 88480123 | loss | 3-0-0 | win | improved | 45.1% | 17/17 |  |
| 88480304 | win | 3-0-0 | win | preserved_win | 80.7% | 9/9 |  |
| 88481733 | loss | 2-1-0 | win | improved | 90.5% | 8/8 |  |
| 88483285 | loss | 2-1-0 | win | improved | 77.9% | 8/8 |  |
| 88483990 | win | 2-1-0 | win | preserved_win | 32.8% | 35/35 |  |
| 88486593 | win | 3-0-0 | win | preserved_win | 89.9% | 22/22 |  |
| 88511515 | loss | 3-0-0 | win | improved | 76.6% | 13/13 |  |
| 88512578 | win | 3-0-0 | win | preserved_win | 78.8% | 18/18 |  |
| 88513116 | loss | 3-0-0 | win | improved | 45.9% | 15/15 |  |
| 88514796 | win | 3-0-0 | win | preserved_win | 87.5% | 10/10 |  |
| 88515340 | loss | 3-0-0 | win | improved | 60.6% | 14/14 |  |
| 88516436 | loss | 3-0-0 | win | improved | 76.7% | 7/7 |  |
| 88517037 | win | 3-0-0 | win | preserved_win | 57.5% | 14/14 |  |
| 88517460 | win | 3-0-0 | win | preserved_win | 40.5% | 22/22 |  |
| 88518016 | loss | 3-0-0 | win | improved | 80.6% | 6/6 |  |
| 88518164 | loss | 3-0-0 | win | improved | 67.6% | 12/12 |  |
| 88518572 | loss | 3-0-0 | win | improved | 57.9% | 17/17 |  |
| 88527351 | loss | 3-0-0 | win | improved | 56.5% | 19/19 |  |
| 88527969 | win | 3-0-0 | win | preserved_win | 87.2% | 8/8 |  |
| 88528562 | loss | 3-0-0 | win | improved | 56.0% | 24/24 |  |
| 88688530 | win | 3-0-0 | win | preserved_win | 80.9% | 16/16 |  |
| 88702243 | loss | 3-0-0 | win | improved | 34.2% | 21/21 |  |
| 88702773 | win | 3-0-0 | win | preserved_win | 71.8% | 8/8 |  |
| 88707615 | loss | 3-0-0 | win | improved | 45.3% | 18/18 |  |
| 88710371 | win | 3-0-0 | win | preserved_win | 57.0% | 17/17 |  |
| 88714591 | loss | 3-0-0 | win | improved | 86.0% | 13/13 |  |
| 88724413 | win | 3-0-0 | win | preserved_win | 83.5% | 22/22 |  |
| 88726741 | loss | 3-0-0 | win | improved | 84.6% | 46/46 |  |
| 88727264 | loss | 3-0-0 | win | improved | 56.5% | 13/13 |  |
| 88734629 | win | 3-0-0 | win | preserved_win | 75.0% | 9/9 |  |
| 88742222 | loss | 3-0-0 | win | improved | 44.9% | 23/23 |  |
| 88745200 | win | 3-0-0 | win | preserved_win | 90.2% | 17/17 |  |
| 88746412 | loss | 3-0-0 | win | improved | 73.2% | 13/13 |  |
| 88750615 | loss | 3-0-0 | win | improved | 50.0% | 29/29 |  |
| 88754803 | loss | 3-0-0 | win | improved | 76.3% | 8/8 |  |
| 88759036 | loss | 3-0-0 | win | improved | 65.3% | 15/15 |  |
| 88762215 | loss | 2-1-0 | win | improved | 51.1% | 18/18 |  |
| 88764905 | loss | 3-0-0 | win | improved | 79.0% | 13/13 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88206818 | board exhausted; inspect trace | 15/15 | 5.0 | {"no_active_pokemon": 3} |
| 88355725 | board exhausted; inspect trace | 6/6 | 7.0 | {"no_active_pokemon": 2, "prizes": 1} |
| 88466967 | deck/resource endurance; inspect trace | 5/5 | 10.0 | {"deck_out": 2, "no_active_pokemon": 1} |

## Matched baseline check

Baseline: `/Users/muhammadomerfarooq/Desktop/GitHub Repositories/Pokemon Challenge/artifacts/v7_every_replay_389_3x.csv`

Per-replay win-to-loss regressions: **3**

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
