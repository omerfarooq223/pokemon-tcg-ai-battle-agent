# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **1167**
- Match results: **1131 wins, 36 losses, 0 draws**
- Match win rate: **96.92%**
- Per-replay majority: **386 wins, 3 losses, 0 ties**
- Recorded opponent-action usage: **54.76%**

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
| 88114269 | loss | 3-0-0 | win | improved | 77.8% | 11/11 |  |
| 88114272 | loss | 3-0-0 | win | improved | 80.3% | 16/16 |  |
| 88135168 | loss | 3-0-0 | win | improved | 57.3% | 13/13 |  |
| 88135718 | loss | 3-0-0 | win | improved | 81.9% | 14/14 |  |
| 88136757 | loss | 3-0-0 | win | improved | 48.9% | 17/17 |  |
| 88138839 | loss | 3-0-0 | win | improved | 47.5% | 23/23 |  |
| 88139351 | loss | 3-0-0 | win | improved | 46.3% | 17/17 |  |
| 88139876 | loss | 3-0-0 | win | improved | 49.5% | 18/18 |  |
| 88139877 | loss | 3-0-0 | win | improved | 48.6% | 18/18 |  |
| 88139889 | loss | 3-0-0 | win | improved | 36.1% | 30/30 |  |
| 88140397 | loss | 3-0-0 | win | improved | 42.6% | 26/26 |  |
| 88140434 | loss | 3-0-0 | win | improved | 55.4% | 18/18 |  |
| 88140934 | loss | 3-0-0 | win | improved | 70.6% | 7/7 |  |
| 88141449 | loss | 3-0-0 | win | improved | 56.5% | 24/24 |  |
| 88141464 | loss | 3-0-0 | win | improved | 77.2% | 12/12 |  |
| 88141972 | loss | 3-0-0 | win | improved | 42.6% | 26/26 |  |
| 88142495 | loss | 2-1-0 | win | improved | 40.2% | 12/12 |  |
| 88143033 | loss | 3-0-0 | win | improved | 68.8% | 19/19 |  |
| 88143428 | loss | 2-1-0 | win | improved | 56.3% | 12/12 |  |
| 88143558 | loss | 3-0-0 | win | improved | 42.5% | 22/22 |  |
| 88143960 | loss | 3-0-0 | win | improved | 84.1% | 16/16 |  |
| 88144074 | loss | 3-0-0 | win | improved | 25.3% | 29/29 |  |
| 88144497 | win | 3-0-0 | win | preserved_win | 70.8% | 6/6 |  |
| 88145058 | loss | 3-0-0 | win | improved | 54.9% | 17/17 |  |
| 88145588 | loss | 3-0-0 | win | improved | 53.6% | 12/12 |  |
| 88145696 | loss | 3-0-0 | win | improved | 43.4% | 10/10 |  |
| 88146122 | loss | 3-0-0 | win | improved | 41.8% | 19/19 |  |
| 88146648 | win | 3-0-0 | win | preserved_win | 72.6% | 9/9 |  |
| 88147191 | loss | 3-0-0 | win | improved | 34.4% | 23/23 |  |
| 88147227 | loss | 3-0-0 | win | improved | 51.2% | 21/21 |  |
| 88147702 | loss | 3-0-0 | win | improved | 71.6% | 14/14 |  |
| 88148218 | loss | 3-0-0 | win | improved | 60.4% | 17/17 |  |
| 88148312 | loss | 3-0-0 | win | improved | 31.4% | 29/29 |  |
| 88148790 | win | 3-0-0 | win | preserved_win | 84.2% | 7/7 |  |
| 88148861 | loss | 3-0-0 | win | improved | 69.7% | 8/8 |  |
| 88149240 | loss | 3-0-0 | win | improved | 79.3% | 15/15 |  |
| 88149380 | loss | 3-0-0 | win | improved | 30.9% | 19/19 |  |
| 88149406 | loss | 3-0-0 | win | improved | 84.1% | 8/8 |  |
| 88149782 | win | 3-0-0 | win | preserved_win | 84.2% | 6/6 |  |
| 88149906 | loss | 3-0-0 | win | improved | 31.7% | 25/25 |  |
| 88150296 | win | 3-0-0 | win | preserved_win | 61.4% | 12/12 |  |
| 88150868 | loss | 3-0-0 | win | improved | 58.9% | 13/13 |  |
| 88151481 | loss | 3-0-0 | win | improved | 84.4% | 20/20 |  |
| 88152037 | win | 3-0-0 | win | preserved_win | 80.9% | 8/8 |  |
| 88152577 | loss | 3-0-0 | win | improved | 72.3% | 14/14 |  |
| 88153002 | loss | 3-0-0 | win | improved | 76.5% | 9/9 |  |
| 88153112 | loss | 3-0-0 | win | improved | 75.6% | 10/10 |  |
| 88153551 | win | 3-0-0 | win | preserved_win | 84.6% | 11/11 |  |
| 88153647 | win | 3-0-0 | win | preserved_win | 87.0% | 26/26 |  |
| 88154072 | loss | 3-0-0 | win | improved | 73.9% | 14/14 |  |
| 88154188 | loss | 3-0-0 | win | improved | 62.0% | 15/15 |  |
| 88154615 | loss | 3-0-0 | win | improved | 81.6% | 12/12 |  |
| 88154720 | loss | 3-0-0 | win | improved | 50.5% | 18/18 |  |
| 88155167 | loss | 3-0-0 | win | improved | 78.4% | 9/9 |  |
| 88155258 | loss | 3-0-0 | win | improved | 89.6% | 9/9 |  |
| 88155735 | loss | 3-0-0 | win | improved | 47.7% | 16/16 |  |
| 88155807 | loss | 3-0-0 | win | improved | 89.2% | 8/8 |  |
| 88156264 | loss | 3-0-0 | win | improved | 69.2% | 8/8 |  |
| 88156364 | win | 3-0-0 | win | preserved_win | 65.5% | 6/6 |  |
| 88156894 | win | 3-0-0 | win | preserved_win | 82.3% | 17/17 |  |
| 88157011 | loss | 3-0-0 | win | improved | 58.1% | 14/14 |  |
| 88157416 | win | 3-0-0 | win | preserved_win | 38.7% | 21/21 |  |
| 88157484 | win | 3-0-0 | win | preserved_win | 88.1% | 12/12 |  |
| 88157952 | win | 3-0-0 | win | preserved_win | 84.5% | 12/12 |  |
| 88170362 | loss | 1-2-0 | loss | unresolved_loss | 66.3% | 11/11 | board exhausted; inspect trace |
| 88181889 | win | 3-0-0 | win | preserved_win | 84.2% | 4/4 |  |
| 88183542 | loss | 3-0-0 | win | improved | 73.7% | 15/15 |  |
| 88187788 | win | 3-0-0 | win | preserved_win | 90.0% | 7/7 |  |
| 88189899 | loss | 3-0-0 | win | improved | 80.8% | 12/12 |  |
| 88190488 | loss | 3-0-0 | win | improved | 82.9% | 8/8 |  |
| 88190720 | loss | 3-0-0 | win | improved | 59.5% | 16/16 |  |
| 88191459 | loss | 3-0-0 | win | improved | 70.0% | 16/16 |  |
| 88191506 | loss | 3-0-0 | win | improved | 63.8% | 18/18 |  |
| 88191988 | loss | 3-0-0 | win | improved | 53.5% | 19/19 |  |
| 88192025 | loss | 3-0-0 | win | improved | 69.2% | 8/8 |  |
| 88192363 | loss | 3-0-0 | win | improved | 78.9% | 16/16 |  |
| 88192550 | loss | 3-0-0 | win | improved | 33.2% | 23/23 |  |
| 88193019 | loss | 3-0-0 | win | improved | 83.3% | 11/11 |  |
| 88193372 | loss | 3-0-0 | win | improved | 38.2% | 10/10 |  |
| 88193551 | loss | 3-0-0 | win | improved | 76.6% | 14/14 |  |
| 88193634 | loss | 3-0-0 | win | improved | 87.0% | 8/8 |  |
| 88195735 | loss | 3-0-0 | win | improved | 78.0% | 9/9 |  |
| 88197859 | loss | 3-0-0 | win | improved | 35.6% | 14/14 |  |
| 88197860 | loss | 3-0-0 | win | improved | 72.5% | 9/9 |  |
| 88197906 | loss | 3-0-0 | win | improved | 42.2% | 17/17 |  |
| 88199435 | loss | 3-0-0 | win | improved | 54.0% | 23/23 |  |
| 88200003 | loss | 3-0-0 | win | improved | 78.8% | 8/8 |  |
| 88201040 | loss | 3-0-0 | win | improved | 47.9% | 25/25 |  |
| 88201604 | loss | 3-0-0 | win | improved | 62.9% | 20/20 |  |
| 88203591 | loss | 3-0-0 | win | improved | 57.3% | 16/16 |  |
| 88204121 | loss | 3-0-0 | win | improved | 46.6% | 20/20 |  |
| 88204232 | loss | 3-0-0 | win | improved | 45.8% | 22/22 |  |
| 88204771 | loss | 3-0-0 | win | improved | 37.1% | 27/27 |  |
| 88204990 | loss | 3-0-0 | win | improved | 38.2% | 17/17 |  |
| 88205283 | loss | 3-0-0 | win | improved | 31.7% | 20/20 |  |
| 88205289 | win | 3-0-0 | win | preserved_win | 86.6% | 17/17 |  |
| 88206332 | loss | 3-0-0 | win | improved | 83.2% | 16/16 |  |
| 88206818 | loss | 3-0-0 | win | improved | 23.2% | 13/13 |  |
| 88206895 | loss | 3-0-0 | win | improved | 40.4% | 12/12 |  |
| 88207928 | loss | 3-0-0 | win | improved | 42.9% | 17/17 |  |
| 88208293 | loss | 3-0-0 | win | improved | 52.9% | 22/22 |  |
| 88208966 | loss | 3-0-0 | win | improved | 27.9% | 36/36 |  |
| 88209048 | loss | 2-1-0 | win | improved | 38.7% | 15/15 |  |
| 88209398 | loss | 3-0-0 | win | improved | 68.7% | 12/12 |  |
| 88209472 | loss | 3-0-0 | win | improved | 20.8% | 24/24 |  |
| 88209993 | loss | 2-1-0 | win | improved | 34.8% | 26/26 |  |
| 88210517 | loss | 3-0-0 | win | improved | 52.9% | 21/21 |  |
| 88210975 | loss | 3-0-0 | win | improved | 46.9% | 8/8 |  |
| 88211042 | loss | 3-0-0 | win | improved | 53.3% | 18/18 |  |
| 88211566 | loss | 3-0-0 | win | improved | 61.8% | 7/7 |  |
| 88212701 | loss | 3-0-0 | win | improved | 36.3% | 20/20 |  |
| 88214700 | loss | 3-0-0 | win | improved | 89.9% | 53/53 |  |
| 88215619 | loss | 3-0-0 | win | improved | 70.0% | 8/8 |  |
| 88217155 | loss | 3-0-0 | win | improved | 79.2% | 11/11 |  |
| 88217476 | loss | 3-0-0 | win | improved | 40.5% | 16/16 |  |
| 88217824 | loss | 3-0-0 | win | improved | 38.5% | 21/21 |  |
| 88220136 | loss | 3-0-0 | win | improved | 59.1% | 19/19 |  |
| 88220489 | loss | 3-0-0 | win | improved | 69.1% | 12/12 |  |
| 88220566 | loss | 3-0-0 | win | improved | 48.0% | 20/20 |  |
| 88221583 | loss | 3-0-0 | win | improved | 73.8% | 8/8 |  |
| 88221669 | loss | 3-0-0 | win | improved | 69.2% | 5/5 |  |
| 88222802 | loss | 3-0-0 | win | improved | 29.3% | 14/14 |  |
| 88223081 | loss | 3-0-0 | win | improved | 70.0% | 8/8 |  |
| 88223586 | loss | 3-0-0 | win | improved | 31.0% | 26/26 |  |
| 88224733 | loss | 2-1-0 | win | improved | 61.4% | 20/20 |  |
| 88224901 | loss | 3-0-0 | win | improved | 57.1% | 31/31 |  |
| 88225199 | loss | 3-0-0 | win | improved | 70.6% | 10/10 |  |
| 88227532 | loss | 3-0-0 | win | improved | 82.6% | 10/10 |  |
| 88227555 | loss | 3-0-0 | win | improved | 38.7% | 20/20 |  |
| 88230163 | loss | 3-0-0 | win | improved | 35.1% | 16/16 |  |
| 88230176 | loss | 3-0-0 | win | improved | 65.8% | 16/16 |  |
| 88230489 | loss | 3-0-0 | win | improved | 84.6% | 10/10 |  |
| 88231229 | loss | 3-0-0 | win | improved | 41.9% | 11/11 |  |
| 88232593 | loss | 3-0-0 | win | improved | 42.9% | 16/16 |  |
| 88232765 | loss | 3-0-0 | win | improved | 59.4% | 7/7 |  |
| 88233128 | loss | 3-0-0 | win | improved | 62.3% | 14/14 |  |
| 88234701 | loss | 3-0-0 | win | improved | 75.0% | 5/5 |  |
| 88234900 | loss | 3-0-0 | win | improved | 82.9% | 11/11 |  |
| 88235276 | loss | 3-0-0 | win | improved | 47.3% | 15/15 |  |
| 88237853 | loss | 3-0-0 | win | improved | 78.9% | 8/8 |  |
| 88238542 | loss | 3-0-0 | win | improved | 52.1% | 16/16 |  |
| 88239078 | loss | 3-0-0 | win | improved | 79.5% | 24/24 |  |
| 88239095 | loss | 3-0-0 | win | improved | 71.9% | 10/10 |  |
| 88239132 | loss | 3-0-0 | win | improved | 75.0% | 12/12 |  |
| 88241784 | loss | 3-0-0 | win | improved | 37.4% | 26/26 |  |
| 88243841 | loss | 2-1-0 | win | improved | 47.5% | 20/20 |  |
| 88245069 | win | 3-0-0 | win | preserved_win | 76.0% | 12/12 |  |
| 88245592 | win | 3-0-0 | win | preserved_win | 40.1% | 18/18 |  |
| 88246129 | win | 3-0-0 | win | preserved_win | 86.0% | 12/12 |  |
| 88246713 | win | 3-0-0 | win | preserved_win | 80.4% | 8/8 |  |
| 88247233 | loss | 3-0-0 | win | improved | 64.9% | 9/9 |  |
| 88247782 | loss | 3-0-0 | win | improved | 30.9% | 23/23 |  |
| 88248321 | win | 2-1-0 | win | preserved_win | 81.6% | 9/9 |  |
| 88248844 | win | 2-1-0 | win | preserved_win | 45.2% | 29/29 |  |
| 88249366 | loss | 3-0-0 | win | improved | 43.7% | 21/21 |  |
| 88249393 | win | 3-0-0 | win | preserved_win | 57.4% | 12/12 |  |
| 88249914 | loss | 3-0-0 | win | improved | 80.0% | 8/8 |  |
| 88250446 | loss | 3-0-0 | win | improved | 40.3% | 17/17 |  |
| 88250998 | win | 3-0-0 | win | preserved_win | 48.2% | 20/20 |  |
| 88251535 | loss | 3-0-0 | win | improved | 47.8% | 19/19 |  |
| 88251789 | loss | 2-1-0 | win | improved | 62.2% | 11/11 |  |
| 88252076 | loss | 3-0-0 | win | improved | 82.6% | 4/4 |  |
| 88252610 | loss | 2-1-0 | win | improved | 77.8% | 19/19 |  |
| 88252759 | loss | 3-0-0 | win | improved | 66.2% | 8/8 |  |
| 88252837 | loss | 3-0-0 | win | improved | 67.4% | 6/6 |  |
| 88252856 | loss | 3-0-0 | win | improved | 50.5% | 12/12 |  |
| 88253125 | win | 3-0-0 | win | preserved_win | 66.7% | 16/16 |  |
| 88253320 | loss | 2-1-0 | win | improved | 60.3% | 12/12 |  |
| 88253642 | win | 3-0-0 | win | preserved_win | 86.9% | 10/10 |  |
| 88254173 | win | 3-0-0 | win | preserved_win | 42.7% | 12/12 |  |
| 88254686 | loss | 3-0-0 | win | improved | 53.1% | 11/11 |  |
| 88254832 | loss | 3-0-0 | win | improved | 61.6% | 16/16 |  |
| 88254923 | loss | 3-0-0 | win | improved | 73.2% | 10/10 |  |
| 88255227 | loss | 3-0-0 | win | improved | 33.5% | 16/16 |  |
| 88255365 | loss | 3-0-0 | win | improved | 67.8% | 12/12 |  |
| 88255773 | loss | 3-0-0 | win | improved | 64.4% | 15/15 |  |
| 88255893 | loss | 3-0-0 | win | improved | 85.2% | 7/7 |  |
| 88255975 | loss | 3-0-0 | win | improved | 68.8% | 17/17 |  |
| 88258615 | loss | 3-0-0 | win | improved | 60.4% | 13/13 |  |
| 88258639 | loss | 3-0-0 | win | improved | 57.0% | 21/21 |  |
| 88258841 | loss | 2-1-0 | win | improved | 55.2% | 19/19 |  |
| 88260624 | loss | 3-0-0 | win | improved | 38.6% | 20/20 |  |
| 88260674 | loss | 3-0-0 | win | improved | 39.3% | 25/25 |  |
| 88261149 | loss | 3-0-0 | win | improved | 78.8% | 12/12 |  |
| 88261688 | win | 3-0-0 | win | preserved_win | 79.6% | 13/13 |  |
| 88261733 | loss | 3-0-0 | win | improved | 70.2% | 7/7 |  |
| 88262219 | loss | 2-1-0 | win | improved | 69.1% | 9/9 |  |
| 88262752 | win | 3-0-0 | win | preserved_win | 84.7% | 15/15 |  |
| 88263295 | win | 3-0-0 | win | preserved_win | 64.9% | 18/18 |  |
| 88263822 | win | 3-0-0 | win | preserved_win | 72.3% | 14/14 |  |
| 88263861 | loss | 3-0-0 | win | improved | 54.7% | 20/20 |  |
| 88264373 | loss | 3-0-0 | win | improved | 76.2% | 6/6 |  |
| 88264404 | loss | 3-0-0 | win | improved | 74.3% | 17/17 |  |
| 88264935 | loss | 2-1-0 | win | improved | 76.6% | 9/9 |  |
| 88264972 | loss | 2-1-0 | win | improved | 83.1% | 7/7 |  |
| 88266013 | loss | 3-0-0 | win | improved | 26.3% | 13/13 |  |
| 88267625 | loss | 3-0-0 | win | improved | 55.9% | 13/13 |  |
| 88268465 | loss | 3-0-0 | win | improved | 80.0% | 12/12 |  |
| 88268514 | loss | 3-0-0 | win | improved | 53.3% | 11/11 |  |
| 88273125 | win | 3-0-0 | win | preserved_win | 87.2% | 9/9 |  |
| 88273894 | loss | 3-0-0 | win | improved | 88.5% | 5/5 |  |
| 88274852 | loss | 3-0-0 | win | improved | 75.6% | 20/20 |  |
| 88276586 | loss | 3-0-0 | win | improved | 44.1% | 33/33 |  |
| 88280043 | loss | 3-0-0 | win | improved | 78.6% | 6/6 |  |
| 88280276 | loss | 3-0-0 | win | improved | 36.9% | 11/11 |  |
| 88280581 | loss | 3-0-0 | win | improved | 79.1% | 13/13 |  |
| 88280592 | loss | 3-0-0 | win | improved | 37.1% | 20/20 |  |
| 88280823 | loss | 3-0-0 | win | improved | 44.6% | 28/28 |  |
| 88281112 | loss | 3-0-0 | win | improved | 76.2% | 12/12 |  |
| 88281365 | loss | 3-0-0 | win | improved | 53.4% | 9/9 |  |
| 88282965 | loss | 3-0-0 | win | improved | 76.8% | 11/11 |  |
| 88285383 | loss | 3-0-0 | win | improved | 39.5% | 21/21 |  |
| 88285882 | loss | 3-0-0 | win | improved | 58.3% | 16/16 |  |
| 88286403 | loss | 3-0-0 | win | improved | 79.3% | 9/9 |  |
| 88286429 | loss | 3-0-0 | win | improved | 37.2% | 18/18 |  |
| 88286928 | loss | 3-0-0 | win | improved | 56.6% | 16/16 |  |
| 88287449 | loss | 3-0-0 | win | improved | 35.6% | 19/19 |  |
| 88287943 | loss | 3-0-0 | win | improved | 94.1% | 6/6 |  |
| 88287982 | loss | 3-0-0 | win | improved | 56.9% | 23/23 |  |
| 88287988 | loss | 3-0-0 | win | improved | 34.4% | 28/28 |  |
| 88288578 | loss | 3-0-0 | win | improved | 28.7% | 22/22 |  |
| 88289166 | loss | 3-0-0 | win | improved | 49.0% | 27/27 |  |
| 88289703 | loss | 3-0-0 | win | improved | 33.8% | 24/24 |  |
| 88290370 | win | 3-0-0 | win | preserved_win | 94.4% | 12/12 |  |
| 88290739 | loss | 3-0-0 | win | improved | 62.1% | 13/13 |  |
| 88300893 | win | 2-1-0 | win | preserved_win | 84.2% | 14/14 |  |
| 88307667 | loss | 3-0-0 | win | improved | 95.0% | 24/24 |  |
| 88309157 | win | 3-0-0 | win | preserved_win | 86.5% | 12/12 |  |
| 88312062 | win | 3-0-0 | win | preserved_win | 64.0% | 10/10 |  |
| 88312577 | win | 3-0-0 | win | preserved_win | 76.6% | 14/14 |  |
| 88313112 | win | 3-0-0 | win | preserved_win | 33.8% | 14/14 |  |
| 88313620 | loss | 3-0-0 | win | improved | 62.6% | 20/20 |  |
| 88313673 | win | 2-1-0 | win | preserved_win | 56.7% | 7/7 |  |
| 88314138 | loss | 3-0-0 | win | improved | 65.9% | 13/13 |  |
| 88314664 | loss | 3-0-0 | win | improved | 75.0% | 5/5 |  |
| 88315183 | win | 3-0-0 | win | preserved_win | 85.5% | 13/13 |  |
| 88315493 | loss | 3-0-0 | win | improved | 68.5% | 11/11 |  |
| 88315696 | win | 3-0-0 | win | preserved_win | 60.6% | 20/20 |  |
| 88316214 | loss | 2-1-0 | win | improved | 67.6% | 8/8 |  |
| 88316726 | win | 2-1-0 | win | preserved_win | 47.6% | 22/22 |  |
| 88317257 | win | 3-0-0 | win | preserved_win | 44.6% | 17/17 |  |
| 88317769 | loss | 3-0-0 | win | improved | 66.0% | 15/15 |  |
| 88317878 | loss | 3-0-0 | win | improved | 56.4% | 12/12 |  |
| 88318294 | loss | 2-1-0 | win | improved | 77.1% | 10/10 |  |
| 88318822 | win | 3-0-0 | win | preserved_win | 80.0% | 6/6 |  |
| 88319336 | loss | 3-0-0 | win | improved | 28.9% | 18/18 |  |
| 88319853 | loss | 3-0-0 | win | improved | 41.5% | 21/21 |  |
| 88319971 | loss | 2-1-0 | win | improved | 55.8% | 14/14 |  |
| 88320365 | win | 3-0-0 | win | preserved_win | 80.7% | 11/11 |  |
| 88320386 | loss | 1-2-0 | loss | unresolved_loss | 87.2% | 8/8 | board exhausted; inspect trace |
| 88320504 | loss | 3-0-0 | win | improved | 48.3% | 19/19 |  |
| 88320896 | win | 3-0-0 | win | preserved_win | 78.0% | 11/11 |  |
| 88321003 | loss | 3-0-0 | win | improved | 61.8% | 11/11 |  |
| 88321041 | loss | 3-0-0 | win | improved | 80.8% | 5/5 |  |
| 88321420 | win | 3-0-0 | win | preserved_win | 82.1% | 17/17 |  |
| 88321956 | loss | 3-0-0 | win | improved | 38.8% | 23/23 |  |
| 88322041 | loss | 3-0-0 | win | improved | 44.5% | 22/22 |  |
| 88322048 | loss | 3-0-0 | win | improved | 57.4% | 15/15 |  |
| 88322049 | loss | 3-0-0 | win | improved | 81.0% | 8/8 |  |
| 88322536 | loss | 3-0-0 | win | improved | 68.8% | 17/17 |  |
| 88322611 | loss | 3-0-0 | win | improved | 49.3% | 15/15 |  |
| 88322619 | loss | 3-0-0 | win | improved | 71.0% | 7/7 |  |
| 88322631 | loss | 2-1-0 | win | improved | 34.1% | 19/19 |  |
| 88323052 | win | 3-0-0 | win | preserved_win | 83.9% | 10/10 |  |
| 88323135 | loss | 3-0-0 | win | improved | 77.1% | 12/12 |  |
| 88323138 | loss | 3-0-0 | win | improved | 52.6% | 8/8 |  |
| 88323140 | loss | 3-0-0 | win | improved | 84.5% | 16/16 |  |
| 88323143 | loss | 3-0-0 | win | improved | 51.8% | 15/15 |  |
| 88323585 | win | 3-0-0 | win | preserved_win | 85.7% | 12/12 |  |
| 88323647 | loss | 3-0-0 | win | improved | 43.2% | 13/13 |  |
| 88323654 | loss | 3-0-0 | win | improved | 81.8% | 5/5 |  |
| 88323655 | loss | 3-0-0 | win | improved | 58.3% | 14/14 |  |
| 88323658 | loss | 2-1-0 | win | improved | 75.9% | 6/6 |  |
| 88323669 | loss | 3-0-0 | win | improved | 41.4% | 11/11 |  |
| 88323677 | loss | 2-1-0 | win | improved | 43.5% | 15/15 |  |
| 88324102 | win | 2-1-0 | win | preserved_win | 37.0% | 26/26 |  |
| 88324178 | loss | 3-0-0 | win | improved | 71.7% | 9/9 |  |
| 88324185 | loss | 3-0-0 | win | improved | 80.6% | 15/15 |  |
| 88324192 | loss | 3-0-0 | win | improved | 78.0% | 9/9 |  |
| 88324221 | loss | 3-0-0 | win | improved | 68.5% | 14/14 |  |
| 88324625 | win | 3-0-0 | win | preserved_win | 76.7% | 10/10 |  |
| 88324685 | loss | 3-0-0 | win | improved | 76.1% | 10/10 |  |
| 88324686 | loss | 3-0-0 | win | improved | 73.6% | 10/10 |  |
| 88324689 | loss | 3-0-0 | win | improved | 69.4% | 15/15 |  |
| 88324692 | loss | 3-0-0 | win | improved | 72.2% | 8/8 |  |
| 88324700 | loss | 3-0-0 | win | improved | 67.9% | 17/17 |  |
| 88325152 | loss | 3-0-0 | win | improved | 48.7% | 14/14 |  |
| 88325690 | win | 3-0-0 | win | preserved_win | 31.9% | 29/29 |  |
| 88326205 | win | 3-0-0 | win | preserved_win | 75.0% | 5/5 |  |
| 88326718 | win | 3-0-0 | win | preserved_win | 88.1% | 12/12 |  |
| 88327230 | win | 3-0-0 | win | preserved_win | 88.6% | 9/9 |  |
| 88327756 | win | 3-0-0 | win | preserved_win | 85.3% | 6/6 |  |
| 88328259 | loss | 3-0-0 | win | improved | 52.1% | 14/14 |  |
| 88328805 | win | 3-0-0 | win | preserved_win | 89.0% | 14/14 |  |
| 88329324 | loss | 3-0-0 | win | improved | 54.0% | 9/9 |  |
| 88331455 | loss | 3-0-0 | win | improved | 86.1% | 7/7 |  |
| 88331982 | loss | 3-0-0 | win | improved | 37.0% | 25/25 |  |
| 88332513 | win | 3-0-0 | win | preserved_win | 87.5% | 13/13 |  |
| 88333025 | win | 3-0-0 | win | preserved_win | 71.8% | 16/16 |  |
| 88333545 | win | 3-0-0 | win | preserved_win | 71.3% | 15/15 |  |
| 88334078 | loss | 3-0-0 | win | improved | 66.7% | 9/9 |  |
| 88336523 | loss | 3-0-0 | win | improved | 48.9% | 13/13 |  |
| 88337057 | win | 3-0-0 | win | preserved_win | 82.6% | 8/8 |  |
| 88337586 | win | 3-0-0 | win | preserved_win | 79.3% | 14/14 |  |
| 88338118 | loss | 3-0-0 | win | improved | 70.7% | 11/11 |  |
| 88338652 | win | 3-0-0 | win | preserved_win | 40.1% | 21/21 |  |
| 88339176 | loss | 3-0-0 | win | improved | 43.7% | 33/33 |  |
| 88355725 | loss | 1-2-0 | loss | unresolved_loss | 53.1% | 17/17 | board exhausted; inspect trace |
| 88357353 | win | 3-0-0 | win | preserved_win | 82.2% | 19/19 |  |
| 88363833 | loss | 3-0-0 | win | improved | 48.8% | 22/22 |  |
| 88373545 | win | 3-0-0 | win | preserved_win | 85.7% | 11/11 |  |
| 88377883 | win | 3-0-0 | win | preserved_win | 81.6% | 6/6 |  |
| 88388662 | loss | 3-0-0 | win | improved | 81.5% | 12/12 |  |
| 88389031 | loss | 3-0-0 | win | improved | 36.0% | 21/21 |  |
| 88399423 | win | 3-0-0 | win | preserved_win | 54.4% | 28/28 |  |
| 88409367 | win | 3-0-0 | win | preserved_win | 85.7% | 4/4 |  |
| 88413119 | win | 3-0-0 | win | preserved_win | 87.8% | 9/9 |  |
| 88422207 | win | 3-0-0 | win | preserved_win | 89.2% | 15/15 |  |
| 88435827 | win | 3-0-0 | win | preserved_win | 34.4% | 17/17 |  |
| 88442046 | loss | 3-0-0 | win | improved | 37.8% | 28/28 |  |
| 88442583 | loss | 3-0-0 | win | improved | 40.9% | 10/10 |  |
| 88442585 | loss | 3-0-0 | win | improved | 67.2% | 12/12 |  |
| 88443133 | loss | 3-0-0 | win | improved | 42.0% | 14/14 |  |
| 88443655 | loss | 3-0-0 | win | improved | 72.3% | 9/9 |  |
| 88444167 | loss | 3-0-0 | win | improved | 70.2% | 14/14 |  |
| 88444648 | loss | 3-0-0 | win | improved | 85.7% | 7/7 |  |
| 88452396 | loss | 3-0-0 | win | improved | 89.7% | 8/8 |  |
| 88452950 | win | 3-0-0 | win | preserved_win | 89.7% | 16/16 |  |
| 88453474 | win | 3-0-0 | win | preserved_win | 76.1% | 12/12 |  |
| 88453996 | win | 3-0-0 | win | preserved_win | 37.3% | 25/25 |  |
| 88454521 | win | 3-0-0 | win | preserved_win | 75.6% | 17/17 |  |
| 88455120 | win | 3-0-0 | win | preserved_win | 63.4% | 11/11 |  |
| 88455645 | win | 3-0-0 | win | preserved_win | 89.1% | 12/12 |  |
| 88456174 | win | 3-0-0 | win | preserved_win | 71.6% | 12/12 |  |
| 88456712 | loss | 3-0-0 | win | improved | 44.8% | 12/12 |  |
| 88459353 | loss | 3-0-0 | win | improved | 45.7% | 24/24 |  |
| 88459908 | loss | 3-0-0 | win | improved | 72.3% | 9/9 |  |
| 88462124 | loss | 3-0-0 | win | improved | 81.2% | 39/39 |  |
| 88462569 | loss | 3-0-0 | win | improved | 41.0% | 20/20 |  |
| 88463244 | loss | 2-1-0 | win | improved | 80.7% | 12/12 |  |
| 88463694 | loss | 3-0-0 | win | improved | 60.2% | 15/15 |  |
| 88464320 | loss | 3-0-0 | win | improved | 81.0% | 6/6 |  |
| 88464738 | loss | 3-0-0 | win | improved | 50.6% | 18/18 |  |
| 88465305 | win | 3-0-0 | win | preserved_win | 82.7% | 7/7 |  |
| 88465824 | loss | 3-0-0 | win | improved | 58.4% | 16/16 |  |
| 88466344 | loss | 3-0-0 | win | improved | 34.7% | 17/17 |  |
| 88466967 | win | 2-1-0 | win | preserved_win | 80.5% | 10/10 |  |
| 88468139 | loss | 3-0-0 | win | improved | 81.7% | 13/13 |  |
| 88468688 | win | 3-0-0 | win | preserved_win | 76.8% | 10/10 |  |
| 88475900 | win | 3-0-0 | win | preserved_win | 84.4% | 33/33 |  |
| 88477511 | loss | 3-0-0 | win | improved | 33.6% | 18/18 |  |
| 88480123 | loss | 3-0-0 | win | improved | 44.9% | 14/14 |  |
| 88480304 | win | 3-0-0 | win | preserved_win | 80.2% | 12/12 |  |
| 88481733 | loss | 3-0-0 | win | improved | 97.7% | 8/8 |  |
| 88483285 | loss | 2-1-0 | win | improved | 73.7% | 8/8 |  |
| 88483990 | win | 2-1-0 | win | preserved_win | 60.0% | 13/13 |  |
| 88486593 | win | 3-0-0 | win | preserved_win | 81.2% | 13/13 |  |
| 88511515 | loss | 3-0-0 | win | improved | 66.7% | 8/8 |  |
| 88512578 | win | 3-0-0 | win | preserved_win | 84.6% | 13/13 |  |
| 88513116 | loss | 3-0-0 | win | improved | 38.2% | 11/11 |  |
| 88514796 | win | 3-0-0 | win | preserved_win | 91.2% | 9/9 |  |
| 88515340 | loss | 3-0-0 | win | improved | 70.4% | 6/6 |  |
| 88516436 | loss | 3-0-0 | win | improved | 70.6% | 15/15 |  |
| 88517037 | win | 3-0-0 | win | preserved_win | 43.2% | 20/20 |  |
| 88517460 | win | 3-0-0 | win | preserved_win | 51.8% | 24/24 |  |
| 88518016 | loss | 3-0-0 | win | improved | 85.4% | 9/9 |  |
| 88518164 | loss | 3-0-0 | win | improved | 100.0% | 10/10 |  |
| 88518572 | loss | 3-0-0 | win | improved | 82.1% | 4/4 |  |
| 88527351 | loss | 3-0-0 | win | improved | 86.7% | 8/8 |  |
| 88527969 | win | 3-0-0 | win | preserved_win | 62.7% | 8/8 |  |
| 88528562 | loss | 3-0-0 | win | improved | 75.0% | 14/14 |  |
| 88688530 | win | 3-0-0 | win | preserved_win | 82.5% | 14/14 |  |
| 88702243 | loss | 3-0-0 | win | improved | 52.6% | 18/18 |  |
| 88702773 | win | 3-0-0 | win | preserved_win | 78.6% | 12/12 |  |
| 88707615 | loss | 3-0-0 | win | improved | 47.5% | 10/10 |  |
| 88710371 | win | 3-0-0 | win | preserved_win | 77.4% | 11/11 |  |
| 88714591 | loss | 3-0-0 | win | improved | 87.0% | 11/11 |  |
| 88724413 | win | 3-0-0 | win | preserved_win | 90.5% | 10/10 |  |
| 88726741 | loss | 3-0-0 | win | improved | 81.1% | 11/11 |  |
| 88727264 | loss | 3-0-0 | win | improved | 56.4% | 17/17 |  |
| 88734629 | win | 3-0-0 | win | preserved_win | 76.5% | 5/5 |  |
| 88742222 | loss | 3-0-0 | win | improved | 45.0% | 26/26 |  |
| 88745200 | win | 3-0-0 | win | preserved_win | 90.7% | 12/12 |  |
| 88746412 | loss | 3-0-0 | win | improved | 78.2% | 10/10 |  |
| 88750615 | loss | 3-0-0 | win | improved | 52.0% | 19/19 |  |
| 88754803 | loss | 3-0-0 | win | improved | 71.8% | 10/10 |  |
| 88759036 | loss | 3-0-0 | win | improved | 45.0% | 11/11 |  |
| 88762215 | loss | 2-1-0 | win | improved | 72.6% | 10/10 |  |
| 88764905 | loss | 3-0-0 | win | improved | 75.4% | 13/13 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88170362 | board exhausted; inspect trace | 11/11 | 3.0 | {"no_active_pokemon": 2, "prizes": 1} |
| 88320386 | board exhausted; inspect trace | 8/8 | 2.0 | {"no_active_pokemon": 3} |
| 88355725 | board exhausted; inspect trace | 17/17 | 4.0 | {"no_active_pokemon": 2, "prizes": 1} |

## Matched baseline check

Baseline: `/Users/muhammadomerfarooq/Desktop/GitHub Repositories/Pokemon Challenge/artifacts/v7_every_replay_389_3x.csv`

Per-replay win-to-loss regressions: **3**

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
