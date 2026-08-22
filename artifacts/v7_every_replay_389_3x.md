# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **1167**
- Match results: **1126 wins, 41 losses, 0 draws**
- Match win rate: **96.49%**
- Per-replay majority: **386 wins, 3 losses, 0 ties**
- Recorded opponent-action usage: **54.81%**

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
| 88114269 | loss | 3-0-0 | win | improved | 41.7% | 28/28 |  |
| 88114272 | loss | 3-0-0 | win | improved | 84.6% | 11/11 |  |
| 88135168 | loss | 3-0-0 | win | improved | 77.3% | 6/6 |  |
| 88135718 | loss | 3-0-0 | win | improved | 81.2% | 12/12 |  |
| 88136757 | loss | 3-0-0 | win | improved | 85.2% | 7/7 |  |
| 88138839 | loss | 3-0-0 | win | improved | 31.3% | 18/18 |  |
| 88139351 | loss | 3-0-0 | win | improved | 32.1% | 31/31 |  |
| 88139876 | loss | 3-0-0 | win | improved | 54.9% | 9/9 |  |
| 88139877 | loss | 3-0-0 | win | improved | 63.6% | 9/9 |  |
| 88139889 | loss | 3-0-0 | win | improved | 53.7% | 23/23 |  |
| 88140397 | loss | 3-0-0 | win | improved | 33.9% | 26/26 |  |
| 88140434 | loss | 3-0-0 | win | improved | 57.7% | 13/13 |  |
| 88140934 | loss | 3-0-0 | win | improved | 51.9% | 17/17 |  |
| 88141449 | loss | 3-0-0 | win | improved | 54.0% | 20/20 |  |
| 88141464 | loss | 3-0-0 | win | improved | 78.2% | 13/13 |  |
| 88141972 | loss | 3-0-0 | win | improved | 47.2% | 16/16 |  |
| 88142495 | loss | 3-0-0 | win | improved | 86.4% | 4/4 |  |
| 88143033 | loss | 3-0-0 | win | improved | 41.4% | 28/28 |  |
| 88143428 | loss | 3-0-0 | win | improved | 62.0% | 12/12 |  |
| 88143558 | loss | 3-0-0 | win | improved | 49.6% | 15/15 |  |
| 88143960 | loss | 3-0-0 | win | improved | 87.5% | 9/9 |  |
| 88144074 | loss | 3-0-0 | win | improved | 40.8% | 25/25 |  |
| 88144497 | win | 3-0-0 | win | preserved_win | 82.6% | 18/18 |  |
| 88145058 | loss | 3-0-0 | win | improved | 76.9% | 11/11 |  |
| 88145588 | loss | 3-0-0 | win | improved | 41.0% | 12/12 |  |
| 88145696 | loss | 3-0-0 | win | improved | 57.3% | 12/12 |  |
| 88146122 | loss | 2-1-0 | win | improved | 59.8% | 14/14 |  |
| 88146648 | win | 3-0-0 | win | preserved_win | 84.0% | 13/13 |  |
| 88147191 | loss | 3-0-0 | win | improved | 34.7% | 24/24 |  |
| 88147227 | loss | 3-0-0 | win | improved | 38.4% | 13/13 |  |
| 88147702 | loss | 3-0-0 | win | improved | 83.9% | 11/11 |  |
| 88148218 | loss | 3-0-0 | win | improved | 46.9% | 21/21 |  |
| 88148312 | loss | 3-0-0 | win | improved | 30.1% | 16/16 |  |
| 88148790 | win | 3-0-0 | win | preserved_win | 77.0% | 6/6 |  |
| 88148861 | loss | 3-0-0 | win | improved | 34.3% | 29/29 |  |
| 88149240 | loss | 3-0-0 | win | improved | 65.0% | 9/9 |  |
| 88149380 | loss | 3-0-0 | win | improved | 32.5% | 23/23 |  |
| 88149406 | loss | 3-0-0 | win | improved | 76.9% | 18/18 |  |
| 88149782 | win | 3-0-0 | win | preserved_win | 68.0% | 7/7 |  |
| 88149906 | loss | 3-0-0 | win | improved | 35.1% | 18/18 |  |
| 88150296 | win | 3-0-0 | win | preserved_win | 87.3% | 9/9 |  |
| 88150868 | loss | 3-0-0 | win | improved | 68.2% | 10/10 |  |
| 88151481 | loss | 3-0-0 | win | improved | 87.8% | 44/44 |  |
| 88152037 | win | 3-0-0 | win | preserved_win | 77.9% | 13/13 |  |
| 88152577 | loss | 3-0-0 | win | improved | 82.5% | 16/16 |  |
| 88153002 | loss | 3-0-0 | win | improved | 82.1% | 11/11 |  |
| 88153112 | loss | 3-0-0 | win | improved | 60.8% | 14/14 |  |
| 88153551 | win | 3-0-0 | win | preserved_win | 90.3% | 12/12 |  |
| 88153647 | win | 3-0-0 | win | preserved_win | 85.2% | 25/25 |  |
| 88154072 | loss | 3-0-0 | win | improved | 86.3% | 9/9 |  |
| 88154188 | loss | 3-0-0 | win | improved | 69.2% | 11/11 |  |
| 88154615 | loss | 3-0-0 | win | improved | 91.7% | 9/9 |  |
| 88154720 | loss | 3-0-0 | win | improved | 75.5% | 7/7 |  |
| 88155167 | loss | 2-1-0 | win | improved | 92.2% | 8/8 |  |
| 88155258 | loss | 3-0-0 | win | improved | 90.0% | 8/8 |  |
| 88155735 | loss | 3-0-0 | win | improved | 66.2% | 11/11 |  |
| 88155807 | loss | 3-0-0 | win | improved | 73.2% | 15/15 |  |
| 88156264 | loss | 3-0-0 | win | improved | 60.0% | 7/7 |  |
| 88156364 | win | 3-0-0 | win | preserved_win | 72.2% | 9/9 |  |
| 88156894 | win | 3-0-0 | win | preserved_win | 84.6% | 13/13 |  |
| 88157011 | loss | 3-0-0 | win | improved | 39.1% | 21/21 |  |
| 88157416 | win | 2-1-0 | win | preserved_win | 32.5% | 18/18 |  |
| 88157484 | win | 3-0-0 | win | preserved_win | 83.7% | 17/17 |  |
| 88157952 | win | 3-0-0 | win | preserved_win | 86.8% | 11/11 |  |
| 88170362 | loss | 2-1-0 | win | improved | 52.8% | 22/22 |  |
| 88181889 | win | 3-0-0 | win | preserved_win | 81.6% | 3/3 |  |
| 88183542 | loss | 2-1-0 | win | improved | 62.8% | 11/11 |  |
| 88187788 | win | 2-1-0 | win | preserved_win | 75.0% | 11/11 |  |
| 88189899 | loss | 3-0-0 | win | improved | 82.4% | 11/11 |  |
| 88190488 | loss | 3-0-0 | win | improved | 47.2% | 18/18 |  |
| 88190720 | loss | 3-0-0 | win | improved | 56.1% | 15/15 |  |
| 88191459 | loss | 3-0-0 | win | improved | 73.7% | 11/11 |  |
| 88191506 | loss | 3-0-0 | win | improved | 78.9% | 9/9 |  |
| 88191988 | loss | 3-0-0 | win | improved | 40.2% | 20/20 |  |
| 88192025 | loss | 2-1-0 | win | improved | 60.0% | 14/14 |  |
| 88192363 | loss | 3-0-0 | win | improved | 55.8% | 14/14 |  |
| 88192550 | loss | 3-0-0 | win | improved | 30.7% | 25/25 |  |
| 88193019 | loss | 3-0-0 | win | improved | 76.7% | 10/10 |  |
| 88193372 | loss | 3-0-0 | win | improved | 27.8% | 24/24 |  |
| 88193551 | loss | 3-0-0 | win | improved | 76.4% | 11/11 |  |
| 88193634 | loss | 3-0-0 | win | improved | 84.8% | 6/6 |  |
| 88195735 | loss | 3-0-0 | win | improved | 91.1% | 12/12 |  |
| 88197859 | loss | 3-0-0 | win | improved | 50.5% | 20/20 |  |
| 88197860 | loss | 3-0-0 | win | improved | 68.6% | 10/10 |  |
| 88197906 | loss | 3-0-0 | win | improved | 77.1% | 12/12 |  |
| 88199435 | loss | 3-0-0 | win | improved | 32.8% | 24/24 |  |
| 88200003 | loss | 3-0-0 | win | improved | 78.4% | 11/11 |  |
| 88201040 | loss | 3-0-0 | win | improved | 39.9% | 27/27 |  |
| 88201604 | loss | 3-0-0 | win | improved | 49.5% | 18/18 |  |
| 88203591 | loss | 3-0-0 | win | improved | 68.5% | 17/17 |  |
| 88204121 | loss | 3-0-0 | win | improved | 63.2% | 14/14 |  |
| 88204232 | loss | 3-0-0 | win | improved | 36.3% | 36/36 |  |
| 88204771 | loss | 3-0-0 | win | improved | 45.9% | 13/13 |  |
| 88204990 | loss | 3-0-0 | win | improved | 37.2% | 15/15 |  |
| 88205283 | loss | 3-0-0 | win | improved | 78.8% | 9/9 |  |
| 88205289 | win | 3-0-0 | win | preserved_win | 82.8% | 14/14 |  |
| 88206332 | loss | 3-0-0 | win | improved | 72.6% | 16/16 |  |
| 88206818 | loss | 2-1-0 | win | improved | 28.7% | 18/18 |  |
| 88206895 | loss | 3-0-0 | win | improved | 53.0% | 19/19 |  |
| 88207928 | loss | 3-0-0 | win | improved | 44.9% | 14/14 |  |
| 88208293 | loss | 3-0-0 | win | improved | 44.7% | 20/20 |  |
| 88208966 | loss | 3-0-0 | win | improved | 35.6% | 18/18 |  |
| 88209048 | loss | 3-0-0 | win | improved | 27.8% | 21/21 |  |
| 88209398 | loss | 3-0-0 | win | improved | 62.7% | 17/17 |  |
| 88209472 | loss | 3-0-0 | win | improved | 31.0% | 23/23 |  |
| 88209993 | loss | 3-0-0 | win | improved | 33.0% | 25/25 |  |
| 88210517 | loss | 3-0-0 | win | improved | 83.0% | 9/9 |  |
| 88210975 | loss | 3-0-0 | win | improved | 54.7% | 13/13 |  |
| 88211042 | loss | 3-0-0 | win | improved | 35.3% | 18/18 |  |
| 88211566 | loss | 3-0-0 | win | improved | 46.8% | 23/23 |  |
| 88212701 | loss | 3-0-0 | win | improved | 32.2% | 19/19 |  |
| 88214700 | loss | 3-0-0 | win | improved | 72.5% | 15/15 |  |
| 88215619 | loss | 3-0-0 | win | improved | 40.0% | 23/23 |  |
| 88217155 | loss | 3-0-0 | win | improved | 67.7% | 13/13 |  |
| 88217476 | loss | 3-0-0 | win | improved | 56.2% | 11/11 |  |
| 88217824 | loss | 3-0-0 | win | improved | 54.4% | 16/16 |  |
| 88220136 | loss | 3-0-0 | win | improved | 53.8% | 26/26 |  |
| 88220489 | loss | 3-0-0 | win | improved | 56.8% | 13/13 |  |
| 88220566 | loss | 3-0-0 | win | improved | 70.7% | 9/9 |  |
| 88221583 | loss | 3-0-0 | win | improved | 53.2% | 12/12 |  |
| 88221669 | loss | 3-0-0 | win | improved | 57.8% | 12/12 |  |
| 88222802 | loss | 3-0-0 | win | improved | 31.2% | 19/19 |  |
| 88223081 | loss | 3-0-0 | win | improved | 76.2% | 9/9 |  |
| 88223586 | loss | 3-0-0 | win | improved | 37.6% | 24/24 |  |
| 88224733 | loss | 3-0-0 | win | improved | 38.8% | 31/31 |  |
| 88224901 | loss | 3-0-0 | win | improved | 67.8% | 17/17 |  |
| 88225199 | loss | 3-0-0 | win | improved | 68.8% | 11/11 |  |
| 88227532 | loss | 3-0-0 | win | improved | 64.9% | 14/14 |  |
| 88227555 | loss | 3-0-0 | win | improved | 49.5% | 14/14 |  |
| 88230163 | loss | 3-0-0 | win | improved | 30.2% | 19/19 |  |
| 88230176 | loss | 3-0-0 | win | improved | 65.2% | 17/17 |  |
| 88230489 | loss | 3-0-0 | win | improved | 41.5% | 26/26 |  |
| 88231229 | loss | 3-0-0 | win | improved | 73.5% | 9/9 |  |
| 88232593 | loss | 3-0-0 | win | improved | 56.7% | 19/19 |  |
| 88232765 | loss | 3-0-0 | win | improved | 68.1% | 14/14 |  |
| 88233128 | loss | 3-0-0 | win | improved | 74.1% | 12/12 |  |
| 88234701 | loss | 3-0-0 | win | improved | 55.4% | 19/19 |  |
| 88234900 | loss | 3-0-0 | win | improved | 82.4% | 16/16 |  |
| 88235276 | loss | 3-0-0 | win | improved | 38.4% | 17/17 |  |
| 88237853 | loss | 3-0-0 | win | improved | 77.1% | 12/12 |  |
| 88238542 | loss | 3-0-0 | win | improved | 83.9% | 16/16 |  |
| 88239078 | loss | 3-0-0 | win | improved | 81.2% | 23/23 |  |
| 88239095 | loss | 3-0-0 | win | improved | 65.6% | 9/9 |  |
| 88239132 | loss | 3-0-0 | win | improved | 74.2% | 11/11 |  |
| 88241784 | loss | 3-0-0 | win | improved | 43.4% | 24/24 |  |
| 88243841 | loss | 3-0-0 | win | improved | 52.3% | 18/18 |  |
| 88245069 | win | 3-0-0 | win | preserved_win | 86.0% | 5/5 |  |
| 88245592 | win | 2-1-0 | win | preserved_win | 75.9% | 6/6 |  |
| 88246129 | win | 3-0-0 | win | preserved_win | 86.8% | 10/10 |  |
| 88246713 | win | 3-0-0 | win | preserved_win | 84.0% | 11/11 |  |
| 88247233 | loss | 3-0-0 | win | improved | 72.2% | 11/11 |  |
| 88247782 | loss | 3-0-0 | win | improved | 34.4% | 24/24 |  |
| 88248321 | win | 3-0-0 | win | preserved_win | 42.2% | 9/9 |  |
| 88248844 | win | 3-0-0 | win | preserved_win | 58.2% | 9/9 |  |
| 88249366 | loss | 2-1-0 | win | improved | 54.9% | 13/13 |  |
| 88249393 | win | 3-0-0 | win | preserved_win | 70.6% | 6/6 |  |
| 88249914 | loss | 3-0-0 | win | improved | 63.0% | 9/9 |  |
| 88250446 | loss | 3-0-0 | win | improved | 35.0% | 18/18 |  |
| 88250998 | win | 3-0-0 | win | preserved_win | 47.2% | 10/10 |  |
| 88251535 | loss | 2-1-0 | win | improved | 73.4% | 15/15 |  |
| 88251789 | loss | 3-0-0 | win | improved | 73.0% | 8/8 |  |
| 88252076 | loss | 3-0-0 | win | improved | 53.8% | 21/21 |  |
| 88252610 | loss | 3-0-0 | win | improved | 84.6% | 10/10 |  |
| 88252759 | loss | 3-0-0 | win | improved | 59.3% | 13/13 |  |
| 88252837 | loss | 3-0-0 | win | improved | 29.4% | 17/17 |  |
| 88252856 | loss | 3-0-0 | win | improved | 57.0% | 19/19 |  |
| 88253125 | win | 3-0-0 | win | preserved_win | 72.3% | 16/16 |  |
| 88253320 | loss | 2-1-0 | win | improved | 28.4% | 20/20 |  |
| 88253642 | win | 3-0-0 | win | preserved_win | 87.2% | 9/9 |  |
| 88254173 | win | 3-0-0 | win | preserved_win | 65.5% | 9/9 |  |
| 88254686 | loss | 2-1-0 | win | improved | 39.8% | 6/6 |  |
| 88254832 | loss | 3-0-0 | win | improved | 48.7% | 24/24 |  |
| 88254923 | loss | 3-0-0 | win | improved | 56.4% | 18/18 |  |
| 88255227 | loss | 3-0-0 | win | improved | 42.4% | 21/21 |  |
| 88255365 | loss | 3-0-0 | win | improved | 60.3% | 12/12 |  |
| 88255773 | loss | 2-1-0 | win | improved | 80.0% | 6/6 |  |
| 88255893 | loss | 3-0-0 | win | improved | 80.6% | 7/7 |  |
| 88255975 | loss | 3-0-0 | win | improved | 84.8% | 7/7 |  |
| 88258615 | loss | 3-0-0 | win | improved | 86.5% | 7/7 |  |
| 88258639 | loss | 3-0-0 | win | improved | 63.2% | 19/19 |  |
| 88258841 | loss | 3-0-0 | win | improved | 36.0% | 25/25 |  |
| 88260624 | loss | 3-0-0 | win | improved | 35.8% | 17/17 |  |
| 88260674 | loss | 2-1-0 | win | improved | 47.3% | 17/17 |  |
| 88261149 | loss | 3-0-0 | win | improved | 70.4% | 18/18 |  |
| 88261688 | win | 3-0-0 | win | preserved_win | 81.2% | 11/11 |  |
| 88261733 | loss | 3-0-0 | win | improved | 66.3% | 15/15 |  |
| 88262219 | loss | 3-0-0 | win | improved | 71.4% | 12/12 |  |
| 88262752 | win | 3-0-0 | win | preserved_win | 79.7% | 13/13 |  |
| 88263295 | win | 3-0-0 | win | preserved_win | 57.6% | 12/12 |  |
| 88263822 | win | 3-0-0 | win | preserved_win | 61.3% | 15/15 |  |
| 88263861 | loss | 3-0-0 | win | improved | 53.6% | 22/22 |  |
| 88264373 | loss | 2-1-0 | win | improved | 88.2% | 9/9 |  |
| 88264404 | loss | 3-0-0 | win | improved | 71.6% | 20/20 |  |
| 88264935 | loss | 1-2-0 | loss | unresolved_loss | 75.0% | 5/5 | board exhausted; inspect trace |
| 88264972 | loss | 3-0-0 | win | improved | 67.9% | 8/8 |  |
| 88266013 | loss | 3-0-0 | win | improved | 32.5% | 23/23 |  |
| 88267625 | loss | 3-0-0 | win | improved | 69.7% | 6/6 |  |
| 88268465 | loss | 3-0-0 | win | improved | 83.3% | 8/8 |  |
| 88268514 | loss | 3-0-0 | win | improved | 75.0% | 5/5 |  |
| 88273125 | win | 3-0-0 | win | preserved_win | 80.6% | 12/12 |  |
| 88273894 | loss | 3-0-0 | win | improved | 79.5% | 8/8 |  |
| 88274852 | loss | 3-0-0 | win | improved | 64.2% | 14/14 |  |
| 88276586 | loss | 3-0-0 | win | improved | 41.7% | 27/27 |  |
| 88280043 | loss | 3-0-0 | win | improved | 75.0% | 10/10 |  |
| 88280276 | loss | 3-0-0 | win | improved | 56.2% | 15/15 |  |
| 88280581 | loss | 2-1-0 | win | improved | 56.3% | 13/13 |  |
| 88280592 | loss | 3-0-0 | win | improved | 47.1% | 18/18 |  |
| 88280823 | loss | 3-0-0 | win | improved | 55.4% | 17/17 |  |
| 88281112 | loss | 3-0-0 | win | improved | 83.3% | 15/15 |  |
| 88281365 | loss | 2-1-0 | win | improved | 65.9% | 9/9 |  |
| 88282965 | loss | 3-0-0 | win | improved | 69.9% | 14/14 |  |
| 88285383 | loss | 3-0-0 | win | improved | 47.3% | 30/30 |  |
| 88285882 | loss | 3-0-0 | win | improved | 60.4% | 16/16 |  |
| 88286403 | loss | 3-0-0 | win | improved | 47.9% | 18/18 |  |
| 88286429 | loss | 3-0-0 | win | improved | 31.7% | 25/25 |  |
| 88286928 | loss | 3-0-0 | win | improved | 50.0% | 21/21 |  |
| 88287449 | loss | 3-0-0 | win | improved | 80.0% | 9/9 |  |
| 88287943 | loss | 3-0-0 | win | improved | 67.5% | 10/10 |  |
| 88287982 | loss | 3-0-0 | win | improved | 70.4% | 21/21 |  |
| 88287988 | loss | 3-0-0 | win | improved | 87.9% | 9/9 |  |
| 88288578 | loss | 3-0-0 | win | improved | 25.2% | 20/20 |  |
| 88289166 | loss | 3-0-0 | win | improved | 38.5% | 30/30 |  |
| 88289703 | loss | 3-0-0 | win | improved | 27.8% | 25/25 |  |
| 88290370 | win | 3-0-0 | win | preserved_win | 88.2% | 12/12 |  |
| 88290739 | loss | 3-0-0 | win | improved | 43.1% | 24/24 |  |
| 88300893 | win | 3-0-0 | win | preserved_win | 73.1% | 14/14 |  |
| 88307667 | loss | 3-0-0 | win | improved | 84.4% | 13/13 |  |
| 88309157 | win | 3-0-0 | win | preserved_win | 79.7% | 30/30 |  |
| 88312062 | win | 3-0-0 | win | preserved_win | 55.6% | 12/12 |  |
| 88312577 | win | 3-0-0 | win | preserved_win | 84.1% | 9/9 |  |
| 88313112 | win | 3-0-0 | win | preserved_win | 40.5% | 17/17 |  |
| 88313620 | loss | 3-0-0 | win | improved | 71.7% | 21/21 |  |
| 88313673 | win | 3-0-0 | win | preserved_win | 58.9% | 20/20 |  |
| 88314138 | loss | 3-0-0 | win | improved | 40.6% | 12/12 |  |
| 88314664 | loss | 3-0-0 | win | improved | 58.5% | 11/11 |  |
| 88315183 | win | 3-0-0 | win | preserved_win | 86.6% | 18/18 |  |
| 88315493 | loss | 3-0-0 | win | improved | 54.1% | 21/21 |  |
| 88315696 | win | 3-0-0 | win | preserved_win | 67.8% | 17/17 |  |
| 88316214 | loss | 1-2-0 | loss | unresolved_loss | 37.4% | 11/11 | board exhausted; inspect trace |
| 88316726 | win | 3-0-0 | win | preserved_win | 62.2% | 11/11 |  |
| 88317257 | win | 3-0-0 | win | preserved_win | 46.5% | 13/13 |  |
| 88317769 | loss | 3-0-0 | win | improved | 48.8% | 11/11 |  |
| 88317878 | loss | 3-0-0 | win | improved | 34.5% | 16/16 |  |
| 88318294 | loss | 3-0-0 | win | improved | 59.1% | 14/14 |  |
| 88318822 | win | 3-0-0 | win | preserved_win | 81.2% | 7/7 |  |
| 88319336 | loss | 3-0-0 | win | improved | 44.0% | 9/9 |  |
| 88319853 | loss | 2-1-0 | win | improved | 67.7% | 10/10 |  |
| 88319971 | loss | 3-0-0 | win | improved | 37.8% | 12/12 |  |
| 88320365 | win | 3-0-0 | win | preserved_win | 67.4% | 10/10 |  |
| 88320386 | loss | 3-0-0 | win | improved | 75.0% | 16/16 |  |
| 88320504 | loss | 3-0-0 | win | improved | 52.1% | 14/14 |  |
| 88320896 | win | 3-0-0 | win | preserved_win | 83.3% | 13/13 |  |
| 88321003 | loss | 3-0-0 | win | improved | 73.5% | 12/12 |  |
| 88321041 | loss | 3-0-0 | win | improved | 80.8% | 11/11 |  |
| 88321420 | win | 3-0-0 | win | preserved_win | 88.9% | 17/17 |  |
| 88321956 | loss | 3-0-0 | win | improved | 39.0% | 36/36 |  |
| 88322041 | loss | 3-0-0 | win | improved | 72.7% | 16/16 |  |
| 88322048 | loss | 3-0-0 | win | improved | 62.8% | 16/16 |  |
| 88322049 | loss | 3-0-0 | win | improved | 59.1% | 16/16 |  |
| 88322536 | loss | 3-0-0 | win | improved | 59.2% | 17/17 |  |
| 88322611 | loss | 3-0-0 | win | improved | 60.7% | 15/15 |  |
| 88322619 | loss | 3-0-0 | win | improved | 75.5% | 9/9 |  |
| 88322631 | loss | 3-0-0 | win | improved | 41.2% | 16/16 |  |
| 88323052 | win | 3-0-0 | win | preserved_win | 85.7% | 12/12 |  |
| 88323135 | loss | 3-0-0 | win | improved | 82.0% | 12/12 |  |
| 88323138 | loss | 3-0-0 | win | improved | 53.5% | 16/16 |  |
| 88323140 | loss | 3-0-0 | win | improved | 74.7% | 13/13 |  |
| 88323143 | loss | 3-0-0 | win | improved | 85.2% | 11/11 |  |
| 88323585 | win | 3-0-0 | win | preserved_win | 82.6% | 9/9 |  |
| 88323647 | loss | 3-0-0 | win | improved | 63.3% | 18/18 |  |
| 88323654 | loss | 3-0-0 | win | improved | 57.4% | 12/12 |  |
| 88323655 | loss | 3-0-0 | win | improved | 82.8% | 46/46 |  |
| 88323658 | loss | 2-1-0 | win | improved | 52.6% | 20/20 |  |
| 88323669 | loss | 3-0-0 | win | improved | 66.7% | 9/9 |  |
| 88323677 | loss | 3-0-0 | win | improved | 83.6% | 15/15 |  |
| 88324102 | win | 2-1-0 | win | preserved_win | 86.7% | 6/6 |  |
| 88324178 | loss | 3-0-0 | win | improved | 77.8% | 9/9 |  |
| 88324185 | loss | 3-0-0 | win | improved | 75.5% | 12/12 |  |
| 88324192 | loss | 3-0-0 | win | improved | 75.6% | 11/11 |  |
| 88324221 | loss | 2-1-0 | win | improved | 87.7% | 42/42 |  |
| 88324625 | win | 3-0-0 | win | preserved_win | 83.3% | 15/15 |  |
| 88324685 | loss | 3-0-0 | win | improved | 47.8% | 18/18 |  |
| 88324686 | loss | 3-0-0 | win | improved | 52.9% | 17/17 |  |
| 88324689 | loss | 3-0-0 | win | improved | 78.8% | 12/12 |  |
| 88324692 | loss | 3-0-0 | win | improved | 75.0% | 5/5 |  |
| 88324700 | loss | 3-0-0 | win | improved | 76.3% | 9/9 |  |
| 88325152 | loss | 3-0-0 | win | improved | 63.8% | 19/19 |  |
| 88325690 | win | 3-0-0 | win | preserved_win | 37.3% | 23/23 |  |
| 88326205 | win | 3-0-0 | win | preserved_win | 65.3% | 11/11 |  |
| 88326718 | win | 3-0-0 | win | preserved_win | 78.6% | 13/13 |  |
| 88327230 | win | 3-0-0 | win | preserved_win | 89.1% | 13/13 |  |
| 88327756 | win | 3-0-0 | win | preserved_win | 84.4% | 7/7 |  |
| 88328259 | loss | 3-0-0 | win | improved | 70.8% | 5/5 |  |
| 88328805 | win | 3-0-0 | win | preserved_win | 87.0% | 10/10 |  |
| 88329324 | loss | 2-1-0 | win | improved | 65.6% | 17/17 |  |
| 88331455 | loss | 3-0-0 | win | improved | 80.9% | 11/11 |  |
| 88331982 | loss | 3-0-0 | win | improved | 42.5% | 13/13 |  |
| 88332513 | win | 3-0-0 | win | preserved_win | 87.5% | 23/23 |  |
| 88333025 | win | 3-0-0 | win | preserved_win | 67.7% | 15/15 |  |
| 88333545 | win | 3-0-0 | win | preserved_win | 75.0% | 25/25 |  |
| 88334078 | loss | 2-1-0 | win | improved | 93.1% | 8/8 |  |
| 88336523 | loss | 2-1-0 | win | improved | 46.5% | 17/17 |  |
| 88337057 | win | 3-0-0 | win | preserved_win | 84.4% | 10/10 |  |
| 88337586 | win | 3-0-0 | win | preserved_win | 82.8% | 11/11 |  |
| 88338118 | loss | 3-0-0 | win | improved | 69.4% | 17/17 |  |
| 88338652 | win | 3-0-0 | win | preserved_win | 58.0% | 23/23 |  |
| 88339176 | loss | 3-0-0 | win | improved | 49.1% | 25/25 |  |
| 88355725 | loss | 3-0-0 | win | improved | 37.5% | 35/35 |  |
| 88357353 | win | 3-0-0 | win | preserved_win | 87.9% | 16/16 |  |
| 88363833 | loss | 3-0-0 | win | improved | 42.5% | 23/23 |  |
| 88373545 | win | 3-0-0 | win | preserved_win | 86.0% | 9/9 |  |
| 88377883 | win | 3-0-0 | win | preserved_win | 90.9% | 5/5 |  |
| 88388662 | loss | 2-1-0 | win | improved | 84.8% | 11/11 |  |
| 88389031 | loss | 2-1-0 | win | improved | 52.6% | 17/17 |  |
| 88399423 | win | 3-0-0 | win | preserved_win | 60.6% | 18/18 |  |
| 88409367 | win | 3-0-0 | win | preserved_win | 78.0% | 51/51 |  |
| 88413119 | win | 3-0-0 | win | preserved_win | 86.8% | 14/14 |  |
| 88422207 | win | 3-0-0 | win | preserved_win | 77.2% | 10/10 |  |
| 88435827 | win | 3-0-0 | win | preserved_win | 77.8% | 9/9 |  |
| 88442046 | loss | 3-0-0 | win | improved | 39.2% | 23/23 |  |
| 88442583 | loss | 3-0-0 | win | improved | 49.6% | 18/18 |  |
| 88442585 | loss | 3-0-0 | win | improved | 49.0% | 15/15 |  |
| 88443133 | loss | 3-0-0 | win | improved | 52.3% | 17/17 |  |
| 88443655 | loss | 3-0-0 | win | improved | 37.8% | 22/22 |  |
| 88444167 | loss | 3-0-0 | win | improved | 47.2% | 15/15 |  |
| 88444648 | loss | 3-0-0 | win | improved | 47.2% | 26/26 |  |
| 88452396 | loss | 3-0-0 | win | improved | 45.7% | 26/26 |  |
| 88452950 | win | 2-1-0 | win | preserved_win | 84.8% | 10/10 |  |
| 88453474 | win | 3-0-0 | win | preserved_win | 82.7% | 10/10 |  |
| 88453996 | win | 3-0-0 | win | preserved_win | 40.5% | 16/16 |  |
| 88454521 | win | 3-0-0 | win | preserved_win | 76.7% | 19/19 |  |
| 88455120 | win | 3-0-0 | win | preserved_win | 69.8% | 15/15 |  |
| 88455645 | win | 3-0-0 | win | preserved_win | 75.8% | 8/8 |  |
| 88456174 | win | 3-0-0 | win | preserved_win | 81.4% | 14/14 |  |
| 88456712 | loss | 1-2-0 | loss | unresolved_loss | 45.5% | 14/14 | board exhausted; inspect trace |
| 88459353 | loss | 3-0-0 | win | improved | 40.4% | 13/13 |  |
| 88459908 | loss | 3-0-0 | win | improved | 25.0% | 10/10 |  |
| 88462124 | loss | 3-0-0 | win | improved | 61.5% | 16/16 |  |
| 88462569 | loss | 3-0-0 | win | improved | 43.5% | 34/34 |  |
| 88463244 | loss | 3-0-0 | win | improved | 37.1% | 17/17 |  |
| 88463694 | loss | 3-0-0 | win | improved | 44.8% | 24/24 |  |
| 88464320 | loss | 3-0-0 | win | improved | 72.0% | 6/6 |  |
| 88464738 | loss | 3-0-0 | win | improved | 50.0% | 16/16 |  |
| 88465305 | win | 3-0-0 | win | preserved_win | 82.8% | 8/8 |  |
| 88465824 | loss | 3-0-0 | win | improved | 70.7% | 17/17 |  |
| 88466344 | loss | 3-0-0 | win | improved | 35.1% | 18/18 |  |
| 88466967 | win | 3-0-0 | win | preserved_win | 57.1% | 9/9 |  |
| 88468139 | loss | 3-0-0 | win | improved | 78.2% | 15/15 |  |
| 88468688 | win | 3-0-0 | win | preserved_win | 67.7% | 16/16 |  |
| 88475900 | win | 2-1-0 | win | preserved_win | 78.5% | 31/31 |  |
| 88477511 | loss | 3-0-0 | win | improved | 29.6% | 17/17 |  |
| 88480123 | loss | 2-1-0 | win | improved | 79.2% | 13/13 |  |
| 88480304 | win | 3-0-0 | win | preserved_win | 82.5% | 10/10 |  |
| 88481733 | loss | 2-1-0 | win | improved | 88.6% | 20/20 |  |
| 88483285 | loss | 3-0-0 | win | improved | 60.9% | 14/14 |  |
| 88483990 | win | 2-1-0 | win | preserved_win | 44.8% | 24/24 |  |
| 88486593 | win | 3-0-0 | win | preserved_win | 86.1% | 16/16 |  |
| 88511515 | loss | 3-0-0 | win | improved | 70.8% | 10/10 |  |
| 88512578 | win | 3-0-0 | win | preserved_win | 81.1% | 12/12 |  |
| 88513116 | loss | 2-1-0 | win | improved | 59.6% | 15/15 |  |
| 88514796 | win | 3-0-0 | win | preserved_win | 96.7% | 9/9 |  |
| 88515340 | loss | 3-0-0 | win | improved | 62.2% | 7/7 |  |
| 88516436 | loss | 3-0-0 | win | improved | 82.1% | 10/10 |  |
| 88517037 | win | 3-0-0 | win | preserved_win | 60.4% | 17/17 |  |
| 88517460 | win | 3-0-0 | win | preserved_win | 42.2% | 23/23 |  |
| 88518016 | loss | 3-0-0 | win | improved | 66.3% | 15/15 |  |
| 88518164 | loss | 2-1-0 | win | improved | 60.6% | 21/21 |  |
| 88518572 | loss | 3-0-0 | win | improved | 65.1% | 13/13 |  |
| 88527351 | loss | 3-0-0 | win | improved | 85.2% | 7/7 |  |
| 88527969 | win | 3-0-0 | win | preserved_win | 42.7% | 10/10 |  |
| 88528562 | loss | 3-0-0 | win | improved | 65.3% | 12/12 |  |
| 88688530 | win | 3-0-0 | win | preserved_win | 68.4% | 12/12 |  |
| 88702243 | loss | 2-1-0 | win | improved | 61.2% | 11/11 |  |
| 88702773 | win | 3-0-0 | win | preserved_win | 90.0% | 6/6 |  |
| 88707615 | loss | 3-0-0 | win | improved | 40.8% | 15/15 |  |
| 88710371 | win | 3-0-0 | win | preserved_win | 71.6% | 12/12 |  |
| 88714591 | loss | 3-0-0 | win | improved | 79.6% | 15/15 |  |
| 88724413 | win | 3-0-0 | win | preserved_win | 83.9% | 20/20 |  |
| 88726741 | loss | 3-0-0 | win | improved | 84.9% | 13/13 |  |
| 88727264 | loss | 3-0-0 | win | improved | 54.9% | 18/18 |  |
| 88734629 | win | 3-0-0 | win | preserved_win | 74.5% | 10/10 |  |
| 88742222 | loss | 3-0-0 | win | improved | 83.0% | 10/10 |  |
| 88745200 | win | 3-0-0 | win | preserved_win | 90.9% | 6/6 |  |
| 88746412 | loss | 3-0-0 | win | improved | 76.0% | 15/15 |  |
| 88750615 | loss | 3-0-0 | win | improved | 78.6% | 8/8 |  |
| 88754803 | loss | 3-0-0 | win | improved | 60.6% | 10/10 |  |
| 88759036 | loss | 3-0-0 | win | improved | 72.1% | 18/18 |  |
| 88762215 | loss | 3-0-0 | win | improved | 40.6% | 22/22 |  |
| 88764905 | loss | 3-0-0 | win | improved | 76.4% | 13/13 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88264935 | board exhausted; inspect trace | 5/5 | 3.0 | {"no_active_pokemon": 3} |
| 88316214 | board exhausted; inspect trace | 11/11 | 21.0 | {"no_active_pokemon": 2, "prizes": 1} |
| 88456712 | board exhausted; inspect trace | 14/14 | 3.0 | {"no_active_pokemon": 2, "prizes": 1} |

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
