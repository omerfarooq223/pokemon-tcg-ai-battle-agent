# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **1167**
- Match results: **1126 wins, 41 losses, 0 draws**
- Match win rate: **96.49%**
- Per-replay majority: **384 wins, 5 losses, 0 ties**
- Recorded opponent-action usage: **55.48%**

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
| 88114269 | loss | 3-0-0 | win | improved | 72.5% | 8/8 |  |
| 88114272 | loss | 3-0-0 | win | improved | 92.1% | 13/13 |  |
| 88135168 | loss | 3-0-0 | win | improved | 43.1% | 23/23 |  |
| 88135718 | loss | 3-0-0 | win | improved | 70.6% | 18/18 |  |
| 88136757 | loss | 3-0-0 | win | improved | 76.9% | 6/6 |  |
| 88138839 | loss | 3-0-0 | win | improved | 40.7% | 21/21 |  |
| 88139351 | loss | 3-0-0 | win | improved | 58.9% | 12/12 |  |
| 88139876 | loss | 3-0-0 | win | improved | 31.4% | 18/18 |  |
| 88139877 | loss | 3-0-0 | win | improved | 41.0% | 23/23 |  |
| 88139889 | loss | 3-0-0 | win | improved | 66.4% | 20/20 |  |
| 88140397 | loss | 3-0-0 | win | improved | 42.0% | 28/28 |  |
| 88140434 | loss | 3-0-0 | win | improved | 56.8% | 9/9 |  |
| 88140934 | loss | 3-0-0 | win | improved | 42.9% | 9/9 |  |
| 88141449 | loss | 3-0-0 | win | improved | 45.2% | 22/22 |  |
| 88141464 | loss | 3-0-0 | win | improved | 72.6% | 12/12 |  |
| 88141972 | loss | 3-0-0 | win | improved | 51.1% | 20/20 |  |
| 88142495 | loss | 2-1-0 | win | improved | 89.2% | 41/41 |  |
| 88143033 | loss | 3-0-0 | win | improved | 50.9% | 22/22 |  |
| 88143428 | loss | 3-0-0 | win | improved | 74.2% | 8/8 |  |
| 88143558 | loss | 3-0-0 | win | improved | 35.9% | 23/23 |  |
| 88143960 | loss | 3-0-0 | win | improved | 76.0% | 16/16 |  |
| 88144074 | loss | 3-0-0 | win | improved | 28.9% | 27/27 |  |
| 88144497 | win | 3-0-0 | win | preserved_win | 78.7% | 13/13 |  |
| 88145058 | loss | 3-0-0 | win | improved | 77.4% | 14/14 |  |
| 88145588 | loss | 3-0-0 | win | improved | 81.4% | 8/8 |  |
| 88145696 | loss | 3-0-0 | win | improved | 57.9% | 14/14 |  |
| 88146122 | loss | 3-0-0 | win | improved | 59.4% | 3/3 |  |
| 88146648 | win | 3-0-0 | win | preserved_win | 73.9% | 13/13 |  |
| 88147191 | loss | 3-0-0 | win | improved | 68.2% | 9/9 |  |
| 88147227 | loss | 3-0-0 | win | improved | 61.3% | 17/17 |  |
| 88147702 | loss | 3-0-0 | win | improved | 86.3% | 11/11 |  |
| 88148218 | loss | 3-0-0 | win | improved | 69.2% | 18/18 |  |
| 88148312 | loss | 3-0-0 | win | improved | 43.3% | 18/18 |  |
| 88148790 | win | 3-0-0 | win | preserved_win | 50.8% | 15/15 |  |
| 88148861 | loss | 3-0-0 | win | improved | 27.3% | 25/25 |  |
| 88149240 | loss | 3-0-0 | win | improved | 77.8% | 9/9 |  |
| 88149380 | loss | 3-0-0 | win | improved | 47.3% | 18/18 |  |
| 88149406 | loss | 3-0-0 | win | improved | 80.8% | 15/15 |  |
| 88149782 | win | 3-0-0 | win | preserved_win | 41.0% | 12/12 |  |
| 88149906 | loss | 3-0-0 | win | improved | 37.7% | 23/23 |  |
| 88150296 | win | 3-0-0 | win | preserved_win | 82.8% | 7/7 |  |
| 88150868 | loss | 3-0-0 | win | improved | 55.3% | 21/21 |  |
| 88151481 | loss | 3-0-0 | win | improved | 86.4% | 17/17 |  |
| 88152037 | win | 3-0-0 | win | preserved_win | 85.3% | 5/5 |  |
| 88152577 | loss | 3-0-0 | win | improved | 72.0% | 13/13 |  |
| 88153002 | loss | 3-0-0 | win | improved | 55.0% | 18/18 |  |
| 88153112 | loss | 3-0-0 | win | improved | 71.9% | 13/13 |  |
| 88153551 | win | 3-0-0 | win | preserved_win | 88.9% | 6/6 |  |
| 88153647 | win | 3-0-0 | win | preserved_win | 80.4% | 23/23 |  |
| 88154072 | loss | 3-0-0 | win | improved | 71.0% | 15/15 |  |
| 88154188 | loss | 3-0-0 | win | improved | 69.2% | 10/10 |  |
| 88154615 | loss | 3-0-0 | win | improved | 90.0% | 9/9 |  |
| 88154720 | loss | 3-0-0 | win | improved | 55.7% | 16/16 |  |
| 88155167 | loss | 3-0-0 | win | improved | 90.0% | 7/7 |  |
| 88155258 | loss | 3-0-0 | win | improved | 90.5% | 10/10 |  |
| 88155735 | loss | 3-0-0 | win | improved | 76.0% | 6/6 |  |
| 88155807 | loss | 3-0-0 | win | improved | 71.4% | 9/9 |  |
| 88156264 | loss | 3-0-0 | win | improved | 66.7% | 7/7 |  |
| 88156364 | win | 3-0-0 | win | preserved_win | 73.8% | 9/9 |  |
| 88156894 | win | 3-0-0 | win | preserved_win | 80.9% | 10/10 |  |
| 88157011 | loss | 3-0-0 | win | improved | 76.1% | 9/9 |  |
| 88157416 | win | 3-0-0 | win | preserved_win | 39.1% | 15/15 |  |
| 88157484 | win | 3-0-0 | win | preserved_win | 86.1% | 12/12 |  |
| 88157952 | win | 3-0-0 | win | preserved_win | 74.5% | 11/11 |  |
| 88170362 | loss | 2-1-0 | win | improved | 66.7% | 11/11 |  |
| 88181889 | win | 3-0-0 | win | preserved_win | 82.5% | 10/10 |  |
| 88183542 | loss | 3-0-0 | win | improved | 54.1% | 20/20 |  |
| 88187788 | win | 3-0-0 | win | preserved_win | 75.4% | 13/13 |  |
| 88189899 | loss | 3-0-0 | win | improved | 68.2% | 14/14 |  |
| 88190488 | loss | 3-0-0 | win | improved | 49.6% | 16/16 |  |
| 88190720 | loss | 3-0-0 | win | improved | 62.1% | 15/15 |  |
| 88191459 | loss | 3-0-0 | win | improved | 62.0% | 16/16 |  |
| 88191506 | loss | 3-0-0 | win | improved | 75.3% | 12/12 |  |
| 88191988 | loss | 3-0-0 | win | improved | 47.8% | 21/21 |  |
| 88192025 | loss | 3-0-0 | win | improved | 44.8% | 18/18 |  |
| 88192363 | loss | 3-0-0 | win | improved | 45.8% | 21/21 |  |
| 88192550 | loss | 3-0-0 | win | improved | 32.3% | 19/19 |  |
| 88193019 | loss | 3-0-0 | win | improved | 78.8% | 13/13 |  |
| 88193372 | loss | 3-0-0 | win | improved | 37.9% | 17/17 |  |
| 88193551 | loss | 3-0-0 | win | improved | 77.0% | 14/14 |  |
| 88193634 | loss | 3-0-0 | win | improved | 61.0% | 13/13 |  |
| 88195735 | loss | 3-0-0 | win | improved | 79.5% | 8/8 |  |
| 88197859 | loss | 3-0-0 | win | improved | 53.6% | 17/17 |  |
| 88197860 | loss | 3-0-0 | win | improved | 66.7% | 7/7 |  |
| 88197906 | loss | 3-0-0 | win | improved | 79.1% | 11/11 |  |
| 88199435 | loss | 2-1-0 | win | improved | 36.5% | 16/16 |  |
| 88200003 | loss | 3-0-0 | win | improved | 79.7% | 13/13 |  |
| 88201040 | loss | 3-0-0 | win | improved | 38.6% | 30/30 |  |
| 88201604 | loss | 3-0-0 | win | improved | 46.8% | 20/20 |  |
| 88203591 | loss | 3-0-0 | win | improved | 66.7% | 18/18 |  |
| 88204121 | loss | 3-0-0 | win | improved | 43.6% | 14/14 |  |
| 88204232 | loss | 3-0-0 | win | improved | 64.5% | 12/12 |  |
| 88204771 | loss | 3-0-0 | win | improved | 34.1% | 26/26 |  |
| 88204990 | loss | 3-0-0 | win | improved | 56.4% | 14/14 |  |
| 88205283 | loss | 3-0-0 | win | improved | 42.4% | 31/31 |  |
| 88205289 | win | 3-0-0 | win | preserved_win | 69.6% | 48/48 |  |
| 88206332 | loss | 3-0-0 | win | improved | 75.0% | 11/11 |  |
| 88206818 | loss | 2-1-0 | win | improved | 43.8% | 17/17 |  |
| 88206895 | loss | 3-0-0 | win | improved | 50.0% | 13/13 |  |
| 88207928 | loss | 3-0-0 | win | improved | 40.2% | 17/17 |  |
| 88208293 | loss | 3-0-0 | win | improved | 47.3% | 16/16 |  |
| 88208966 | loss | 3-0-0 | win | improved | 26.7% | 16/16 |  |
| 88209048 | loss | 3-0-0 | win | improved | 34.1% | 22/22 |  |
| 88209398 | loss | 3-0-0 | win | improved | 71.4% | 7/7 |  |
| 88209472 | loss | 3-0-0 | win | improved | 26.4% | 28/28 |  |
| 88209993 | loss | 3-0-0 | win | improved | 39.9% | 23/23 |  |
| 88210517 | loss | 3-0-0 | win | improved | 86.5% | 11/11 |  |
| 88210975 | loss | 1-2-0 | loss | unresolved_loss | 55.5% | 17/17 | deck/resource endurance; inspect trace |
| 88211042 | loss | 3-0-0 | win | improved | 56.5% | 14/14 |  |
| 88211566 | loss | 3-0-0 | win | improved | 43.6% | 15/15 |  |
| 88212701 | loss | 3-0-0 | win | improved | 36.3% | 18/18 |  |
| 88214700 | loss | 3-0-0 | win | improved | 76.5% | 11/11 |  |
| 88215619 | loss | 3-0-0 | win | improved | 71.9% | 6/6 |  |
| 88217155 | loss | 3-0-0 | win | improved | 77.8% | 11/11 |  |
| 88217476 | loss | 3-0-0 | win | improved | 44.7% | 16/16 |  |
| 88217824 | loss | 3-0-0 | win | improved | 54.2% | 17/17 |  |
| 88220136 | loss | 3-0-0 | win | improved | 40.9% | 26/26 |  |
| 88220489 | loss | 3-0-0 | win | improved | 78.8% | 9/9 |  |
| 88220566 | loss | 3-0-0 | win | improved | 47.0% | 18/18 |  |
| 88221583 | loss | 3-0-0 | win | improved | 82.1% | 8/8 |  |
| 88221669 | loss | 3-0-0 | win | improved | 59.7% | 12/12 |  |
| 88222802 | loss | 3-0-0 | win | improved | 48.5% | 16/16 |  |
| 88223081 | loss | 3-0-0 | win | improved | 68.4% | 10/10 |  |
| 88223586 | loss | 2-1-0 | win | improved | 37.1% | 22/22 |  |
| 88224733 | loss | 3-0-0 | win | improved | 50.8% | 25/25 |  |
| 88224901 | loss | 3-0-0 | win | improved | 77.1% | 8/8 |  |
| 88225199 | loss | 2-1-0 | win | improved | 64.3% | 16/16 |  |
| 88227532 | loss | 3-0-0 | win | improved | 68.9% | 12/12 |  |
| 88227555 | loss | 3-0-0 | win | improved | 65.9% | 15/15 |  |
| 88230163 | loss | 3-0-0 | win | improved | 33.3% | 20/20 |  |
| 88230176 | loss | 3-0-0 | win | improved | 70.9% | 16/16 |  |
| 88230489 | loss | 3-0-0 | win | improved | 40.1% | 20/20 |  |
| 88231229 | loss | 3-0-0 | win | improved | 38.2% | 12/12 |  |
| 88232593 | loss | 3-0-0 | win | improved | 80.4% | 7/7 |  |
| 88232765 | loss | 3-0-0 | win | improved | 61.5% | 14/14 |  |
| 88233128 | loss | 3-0-0 | win | improved | 37.4% | 20/20 |  |
| 88234701 | loss | 3-0-0 | win | improved | 64.8% | 11/11 |  |
| 88234900 | loss | 3-0-0 | win | improved | 83.3% | 12/12 |  |
| 88235276 | loss | 3-0-0 | win | improved | 40.9% | 21/21 |  |
| 88237853 | loss | 3-0-0 | win | improved | 58.4% | 13/13 |  |
| 88238542 | loss | 3-0-0 | win | improved | 82.0% | 13/13 |  |
| 88239078 | loss | 3-0-0 | win | improved | 74.4% | 20/20 |  |
| 88239095 | loss | 3-0-0 | win | improved | 56.3% | 14/14 |  |
| 88239132 | loss | 3-0-0 | win | improved | 74.5% | 14/14 |  |
| 88241784 | loss | 3-0-0 | win | improved | 36.3% | 27/27 |  |
| 88243841 | loss | 3-0-0 | win | improved | 37.5% | 26/26 |  |
| 88245069 | win | 3-0-0 | win | preserved_win | 80.9% | 14/14 |  |
| 88245592 | win | 3-0-0 | win | preserved_win | 95.2% | 5/5 |  |
| 88246129 | win | 3-0-0 | win | preserved_win | 85.4% | 12/12 |  |
| 88246713 | win | 3-0-0 | win | preserved_win | 88.3% | 13/13 |  |
| 88247233 | loss | 3-0-0 | win | improved | 75.6% | 8/8 |  |
| 88247782 | loss | 3-0-0 | win | improved | 34.3% | 23/23 |  |
| 88248321 | win | 3-0-0 | win | preserved_win | 44.1% | 17/17 |  |
| 88248844 | win | 2-1-0 | win | preserved_win | 57.6% | 17/17 |  |
| 88249366 | loss | 3-0-0 | win | improved | 60.7% | 12/12 |  |
| 88249393 | win | 3-0-0 | win | preserved_win | 64.5% | 10/10 |  |
| 88249914 | loss | 3-0-0 | win | improved | 77.3% | 15/15 |  |
| 88250446 | loss | 3-0-0 | win | improved | 38.3% | 16/16 |  |
| 88250998 | win | 2-1-0 | win | preserved_win | 66.7% | 16/16 |  |
| 88251535 | loss | 3-0-0 | win | improved | 51.6% | 16/16 |  |
| 88251789 | loss | 2-1-0 | win | improved | 57.8% | 7/7 |  |
| 88252076 | loss | 3-0-0 | win | improved | 82.6% | 3/3 |  |
| 88252610 | loss | 3-0-0 | win | improved | 85.4% | 10/10 |  |
| 88252759 | loss | 3-0-0 | win | improved | 74.2% | 8/8 |  |
| 88252837 | loss | 2-1-0 | win | improved | 41.7% | 6/6 |  |
| 88252856 | loss | 3-0-0 | win | improved | 59.7% | 22/22 |  |
| 88253125 | win | 3-0-0 | win | preserved_win | 78.3% | 14/14 |  |
| 88253320 | loss | 3-0-0 | win | improved | 41.9% | 12/12 |  |
| 88253642 | win | 3-0-0 | win | preserved_win | 87.5% | 15/15 |  |
| 88254173 | win | 3-0-0 | win | preserved_win | 65.4% | 20/20 |  |
| 88254686 | loss | 3-0-0 | win | improved | 34.5% | 14/14 |  |
| 88254832 | loss | 3-0-0 | win | improved | 50.9% | 27/27 |  |
| 88254923 | loss | 3-0-0 | win | improved | 65.9% | 15/15 |  |
| 88255227 | loss | 3-0-0 | win | improved | 43.3% | 5/5 |  |
| 88255365 | loss | 3-0-0 | win | improved | 36.8% | 22/22 |  |
| 88255773 | loss | 2-1-0 | win | improved | 85.1% | 6/6 |  |
| 88255893 | loss | 3-0-0 | win | improved | 70.4% | 5/5 |  |
| 88255975 | loss | 3-0-0 | win | improved | 53.8% | 13/13 |  |
| 88258615 | loss | 3-0-0 | win | improved | 69.2% | 13/13 |  |
| 88258639 | loss | 3-0-0 | win | improved | 60.0% | 21/21 |  |
| 88258841 | loss | 2-1-0 | win | improved | 44.2% | 25/25 |  |
| 88260624 | loss | 3-0-0 | win | improved | 47.5% | 17/17 |  |
| 88260674 | loss | 3-0-0 | win | improved | 39.4% | 20/20 |  |
| 88261149 | loss | 3-0-0 | win | improved | 72.4% | 7/7 |  |
| 88261688 | win | 3-0-0 | win | preserved_win | 84.9% | 14/14 |  |
| 88261733 | loss | 3-0-0 | win | improved | 51.3% | 14/14 |  |
| 88262219 | loss | 3-0-0 | win | improved | 81.8% | 9/9 |  |
| 88262752 | win | 3-0-0 | win | preserved_win | 80.5% | 17/17 |  |
| 88263295 | win | 3-0-0 | win | preserved_win | 52.8% | 18/18 |  |
| 88263822 | win | 3-0-0 | win | preserved_win | 61.2% | 15/15 |  |
| 88263861 | loss | 3-0-0 | win | improved | 51.8% | 20/20 |  |
| 88264373 | loss | 3-0-0 | win | improved | 74.3% | 11/11 |  |
| 88264404 | loss | 3-0-0 | win | improved | 78.5% | 14/14 |  |
| 88264935 | loss | 1-2-0 | loss | unresolved_loss | 78.5% | 13/13 | board exhausted; inspect trace |
| 88264972 | loss | 3-0-0 | win | improved | 48.5% | 10/10 |  |
| 88266013 | loss | 2-1-0 | win | improved | 25.6% | 45/45 |  |
| 88267625 | loss | 3-0-0 | win | improved | 64.0% | 9/9 |  |
| 88268465 | loss | 3-0-0 | win | improved | 76.2% | 17/17 |  |
| 88268514 | loss | 3-0-0 | win | improved | 80.0% | 10/10 |  |
| 88273125 | win | 3-0-0 | win | preserved_win | 84.1% | 5/5 |  |
| 88273894 | loss | 3-0-0 | win | improved | 83.3% | 5/5 |  |
| 88274852 | loss | 3-0-0 | win | improved | 67.6% | 6/6 |  |
| 88276586 | loss | 3-0-0 | win | improved | 50.7% | 29/29 |  |
| 88280043 | loss | 3-0-0 | win | improved | 41.1% | 14/14 |  |
| 88280276 | loss | 3-0-0 | win | improved | 59.6% | 12/12 |  |
| 88280581 | loss | 3-0-0 | win | improved | 57.1% | 12/12 |  |
| 88280592 | loss | 3-0-0 | win | improved | 49.2% | 20/20 |  |
| 88280823 | loss | 3-0-0 | win | improved | 46.0% | 24/24 |  |
| 88281112 | loss | 2-1-0 | win | improved | 84.7% | 9/9 |  |
| 88281365 | loss | 2-1-0 | win | improved | 54.1% | 11/11 |  |
| 88282965 | loss | 3-0-0 | win | improved | 43.7% | 13/13 |  |
| 88285383 | loss | 3-0-0 | win | improved | 50.4% | 21/21 |  |
| 88285882 | loss | 3-0-0 | win | improved | 75.5% | 11/11 |  |
| 88286403 | loss | 3-0-0 | win | improved | 40.4% | 16/16 |  |
| 88286429 | loss | 3-0-0 | win | improved | 46.8% | 17/17 |  |
| 88286928 | loss | 3-0-0 | win | improved | 44.6% | 24/24 |  |
| 88287449 | loss | 3-0-0 | win | improved | 64.3% | 16/16 |  |
| 88287943 | loss | 3-0-0 | win | improved | 61.5% | 13/13 |  |
| 88287982 | loss | 3-0-0 | win | improved | 71.8% | 18/18 |  |
| 88287988 | loss | 2-1-0 | win | improved | 59.0% | 16/16 |  |
| 88288578 | loss | 3-0-0 | win | improved | 31.1% | 22/22 |  |
| 88289166 | loss | 3-0-0 | win | improved | 42.8% | 25/25 |  |
| 88289703 | loss | 3-0-0 | win | improved | 35.4% | 21/21 |  |
| 88290370 | win | 3-0-0 | win | preserved_win | 94.9% | 16/16 |  |
| 88290739 | loss | 3-0-0 | win | improved | 68.8% | 14/14 |  |
| 88300893 | win | 3-0-0 | win | preserved_win | 81.2% | 18/18 |  |
| 88307667 | loss | 3-0-0 | win | improved | 84.8% | 18/18 |  |
| 88309157 | win | 3-0-0 | win | preserved_win | 88.6% | 9/9 |  |
| 88312062 | win | 3-0-0 | win | preserved_win | 62.5% | 8/8 |  |
| 88312577 | win | 3-0-0 | win | preserved_win | 78.8% | 19/19 |  |
| 88313112 | win | 3-0-0 | win | preserved_win | 34.0% | 19/19 |  |
| 88313620 | loss | 3-0-0 | win | improved | 69.3% | 17/17 |  |
| 88313673 | win | 3-0-0 | win | preserved_win | 49.4% | 18/18 |  |
| 88314138 | loss | 3-0-0 | win | improved | 38.1% | 12/12 |  |
| 88314664 | loss | 3-0-0 | win | improved | 48.5% | 19/19 |  |
| 88315183 | win | 3-0-0 | win | preserved_win | 89.3% | 21/21 |  |
| 88315493 | loss | 3-0-0 | win | improved | 70.0% | 9/9 |  |
| 88315696 | win | 2-1-0 | win | preserved_win | 62.8% | 10/10 |  |
| 88316214 | loss | 2-1-0 | win | improved | 51.0% | 20/20 |  |
| 88316726 | win | 2-1-0 | win | preserved_win | 53.0% | 15/15 |  |
| 88317257 | win | 3-0-0 | win | preserved_win | 75.0% | 10/10 |  |
| 88317769 | loss | 2-1-0 | win | improved | 86.0% | 6/6 |  |
| 88317878 | loss | 3-0-0 | win | improved | 52.4% | 15/15 |  |
| 88318294 | loss | 3-0-0 | win | improved | 38.5% | 21/21 |  |
| 88318822 | win | 3-0-0 | win | preserved_win | 71.8% | 7/7 |  |
| 88319336 | loss | 3-0-0 | win | improved | 30.5% | 27/27 |  |
| 88319853 | loss | 3-0-0 | win | improved | 57.7% | 23/23 |  |
| 88319971 | loss | 3-0-0 | win | improved | 44.1% | 25/25 |  |
| 88320365 | win | 3-0-0 | win | preserved_win | 76.0% | 14/14 |  |
| 88320386 | loss | 3-0-0 | win | improved | 76.7% | 8/8 |  |
| 88320504 | loss | 3-0-0 | win | improved | 38.7% | 22/22 |  |
| 88320896 | win | 3-0-0 | win | preserved_win | 83.0% | 13/13 |  |
| 88321003 | loss | 3-0-0 | win | improved | 74.2% | 11/11 |  |
| 88321041 | loss | 3-0-0 | win | improved | 78.9% | 7/7 |  |
| 88321420 | win | 3-0-0 | win | preserved_win | 86.1% | 19/19 |  |
| 88321956 | loss | 2-1-0 | win | improved | 90.5% | 7/7 |  |
| 88322041 | loss | 3-0-0 | win | improved | 47.2% | 14/14 |  |
| 88322048 | loss | 3-0-0 | win | improved | 63.2% | 12/12 |  |
| 88322049 | loss | 3-0-0 | win | improved | 50.3% | 19/19 |  |
| 88322536 | loss | 3-0-0 | win | improved | 43.3% | 21/21 |  |
| 88322611 | loss | 3-0-0 | win | improved | 54.7% | 18/18 |  |
| 88322619 | loss | 3-0-0 | win | improved | 70.2% | 11/11 |  |
| 88322631 | loss | 3-0-0 | win | improved | 42.9% | 15/15 |  |
| 88323052 | win | 3-0-0 | win | preserved_win | 90.7% | 37/37 |  |
| 88323135 | loss | 3-0-0 | win | improved | 86.7% | 6/6 |  |
| 88323138 | loss | 3-0-0 | win | improved | 49.0% | 14/14 |  |
| 88323140 | loss | 3-0-0 | win | improved | 76.2% | 12/12 |  |
| 88323143 | loss | 3-0-0 | win | improved | 80.3% | 13/13 |  |
| 88323585 | win | 3-0-0 | win | preserved_win | 84.8% | 20/20 |  |
| 88323647 | loss | 3-0-0 | win | improved | 54.4% | 14/14 |  |
| 88323654 | loss | 3-0-0 | win | improved | 83.6% | 11/11 |  |
| 88323655 | loss | 3-0-0 | win | improved | 51.4% | 16/16 |  |
| 88323658 | loss | 2-1-0 | win | improved | 55.1% | 13/13 |  |
| 88323669 | loss | 3-0-0 | win | improved | 52.1% | 17/17 |  |
| 88323677 | loss | 3-0-0 | win | improved | 36.2% | 19/19 |  |
| 88324102 | win | 3-0-0 | win | preserved_win | 57.6% | 13/13 |  |
| 88324178 | loss | 3-0-0 | win | improved | 69.0% | 5/5 |  |
| 88324185 | loss | 3-0-0 | win | improved | 83.0% | 11/11 |  |
| 88324192 | loss | 3-0-0 | win | improved | 72.1% | 15/15 |  |
| 88324221 | loss | 3-0-0 | win | improved | 75.9% | 10/10 |  |
| 88324625 | win | 3-0-0 | win | preserved_win | 84.2% | 17/17 |  |
| 88324685 | loss | 3-0-0 | win | improved | 59.4% | 13/13 |  |
| 88324686 | loss | 3-0-0 | win | improved | 75.5% | 13/13 |  |
| 88324689 | loss | 3-0-0 | win | improved | 71.8% | 10/10 |  |
| 88324692 | loss | 3-0-0 | win | improved | 44.9% | 18/18 |  |
| 88324700 | loss | 3-0-0 | win | improved | 35.5% | 16/16 |  |
| 88325152 | loss | 2-1-0 | win | improved | 45.9% | 19/19 |  |
| 88325690 | win | 3-0-0 | win | preserved_win | 41.6% | 28/28 |  |
| 88326205 | win | 3-0-0 | win | preserved_win | 50.8% | 14/14 |  |
| 88326718 | win | 3-0-0 | win | preserved_win | 91.4% | 10/10 |  |
| 88327230 | win | 3-0-0 | win | preserved_win | 75.6% | 18/18 |  |
| 88327756 | win | 3-0-0 | win | preserved_win | 41.5% | 13/13 |  |
| 88328259 | loss | 3-0-0 | win | improved | 63.1% | 10/10 |  |
| 88328805 | win | 3-0-0 | win | preserved_win | 81.0% | 16/16 |  |
| 88329324 | loss | 3-0-0 | win | improved | 78.8% | 8/8 |  |
| 88331455 | loss | 3-0-0 | win | improved | 82.0% | 6/6 |  |
| 88331982 | loss | 1-2-0 | loss | unresolved_loss | 71.2% | 4/4 | board exhausted; inspect trace |
| 88332513 | win | 3-0-0 | win | preserved_win | 90.3% | 16/16 |  |
| 88333025 | win | 3-0-0 | win | preserved_win | 72.9% | 25/25 |  |
| 88333545 | win | 3-0-0 | win | preserved_win | 69.5% | 24/24 |  |
| 88334078 | loss | 3-0-0 | win | improved | 76.7% | 5/5 |  |
| 88336523 | loss | 3-0-0 | win | improved | 39.0% | 26/26 |  |
| 88337057 | win | 3-0-0 | win | preserved_win | 80.8% | 7/7 |  |
| 88337586 | win | 3-0-0 | win | preserved_win | 72.7% | 8/8 |  |
| 88338118 | loss | 3-0-0 | win | improved | 64.5% | 19/19 |  |
| 88338652 | win | 3-0-0 | win | preserved_win | 50.3% | 20/20 |  |
| 88339176 | loss | 3-0-0 | win | improved | 62.5% | 22/22 |  |
| 88355725 | loss | 1-2-0 | loss | unresolved_loss | 74.4% | 12/12 | board exhausted; inspect trace |
| 88357353 | win | 3-0-0 | win | preserved_win | 92.4% | 23/23 |  |
| 88363833 | loss | 3-0-0 | win | improved | 66.7% | 15/15 |  |
| 88373545 | win | 3-0-0 | win | preserved_win | 88.1% | 13/13 |  |
| 88377883 | win | 3-0-0 | win | preserved_win | 79.4% | 6/6 |  |
| 88388662 | loss | 2-1-0 | win | improved | 62.2% | 17/17 |  |
| 88389031 | loss | 2-1-0 | win | improved | 77.2% | 7/7 |  |
| 88399423 | win | 2-1-0 | win | preserved_win | 63.2% | 24/24 |  |
| 88409367 | win | 3-0-0 | win | preserved_win | 73.8% | 11/11 |  |
| 88413119 | win | 3-0-0 | win | preserved_win | 91.7% | 12/12 |  |
| 88422207 | win | 3-0-0 | win | preserved_win | 83.1% | 18/18 |  |
| 88435827 | win | 3-0-0 | win | preserved_win | 33.3% | 12/12 |  |
| 88442046 | loss | 3-0-0 | win | improved | 54.8% | 16/16 |  |
| 88442583 | loss | 2-1-0 | win | improved | 46.8% | 18/18 |  |
| 88442585 | loss | 3-0-0 | win | improved | 47.1% | 19/19 |  |
| 88443133 | loss | 3-0-0 | win | improved | 40.5% | 22/22 |  |
| 88443655 | loss | 3-0-0 | win | improved | 82.1% | 6/6 |  |
| 88444167 | loss | 3-0-0 | win | improved | 39.6% | 24/24 |  |
| 88444648 | loss | 2-1-0 | win | improved | 53.0% | 15/15 |  |
| 88452396 | loss | 3-0-0 | win | improved | 48.1% | 12/12 |  |
| 88452950 | win | 3-0-0 | win | preserved_win | 80.3% | 16/16 |  |
| 88453474 | win | 3-0-0 | win | preserved_win | 76.5% | 10/10 |  |
| 88453996 | win | 3-0-0 | win | preserved_win | 82.3% | 50/50 |  |
| 88454521 | win | 3-0-0 | win | preserved_win | 75.4% | 15/15 |  |
| 88455120 | win | 3-0-0 | win | preserved_win | 73.2% | 10/10 |  |
| 88455645 | win | 3-0-0 | win | preserved_win | 84.5% | 17/17 |  |
| 88456174 | win | 3-0-0 | win | preserved_win | 82.4% | 11/11 |  |
| 88456712 | loss | 3-0-0 | win | improved | 37.7% | 17/17 |  |
| 88459353 | loss | 3-0-0 | win | improved | 38.4% | 20/20 |  |
| 88459908 | loss | 3-0-0 | win | improved | 44.0% | 8/8 |  |
| 88462124 | loss | 3-0-0 | win | improved | 69.8% | 11/11 |  |
| 88462569 | loss | 3-0-0 | win | improved | 74.6% | 12/12 |  |
| 88463244 | loss | 3-0-0 | win | improved | 32.7% | 23/23 |  |
| 88463694 | loss | 3-0-0 | win | improved | 63.6% | 19/19 |  |
| 88464320 | loss | 3-0-0 | win | improved | 45.5% | 18/18 |  |
| 88464738 | loss | 3-0-0 | win | improved | 78.4% | 15/15 |  |
| 88465305 | win | 3-0-0 | win | preserved_win | 86.7% | 9/9 |  |
| 88465824 | loss | 3-0-0 | win | improved | 58.5% | 15/15 |  |
| 88466344 | loss | 2-1-0 | win | improved | 42.3% | 20/20 |  |
| 88466967 | win | 1-2-0 | loss | regressed | 54.8% | 30/30 | deck/resource endurance; inspect trace |
| 88468139 | loss | 3-0-0 | win | improved | 85.7% | 10/10 |  |
| 88468688 | win | 3-0-0 | win | preserved_win | 58.9% | 18/18 |  |
| 88475900 | win | 3-0-0 | win | preserved_win | 77.2% | 10/10 |  |
| 88477511 | loss | 3-0-0 | win | improved | 41.3% | 21/21 |  |
| 88480123 | loss | 3-0-0 | win | improved | 56.4% | 12/12 |  |
| 88480304 | win | 3-0-0 | win | preserved_win | 83.3% | 10/10 |  |
| 88481733 | loss | 3-0-0 | win | improved | 88.1% | 9/9 |  |
| 88483285 | loss | 3-0-0 | win | improved | 80.4% | 18/18 |  |
| 88483990 | win | 3-0-0 | win | preserved_win | 63.3% | 25/25 |  |
| 88486593 | win | 3-0-0 | win | preserved_win | 83.7% | 19/19 |  |
| 88511515 | loss | 3-0-0 | win | improved | 49.2% | 19/19 |  |
| 88512578 | win | 3-0-0 | win | preserved_win | 85.9% | 14/14 |  |
| 88513116 | loss | 2-1-0 | win | improved | 56.0% | 16/16 |  |
| 88514796 | win | 3-0-0 | win | preserved_win | 95.9% | 9/9 |  |
| 88515340 | loss | 3-0-0 | win | improved | 67.9% | 15/15 |  |
| 88516436 | loss | 3-0-0 | win | improved | 84.4% | 8/8 |  |
| 88517037 | win | 3-0-0 | win | preserved_win | 61.6% | 20/20 |  |
| 88517460 | win | 3-0-0 | win | preserved_win | 40.5% | 16/16 |  |
| 88518016 | loss | 3-0-0 | win | improved | 45.9% | 17/17 |  |
| 88518164 | loss | 3-0-0 | win | improved | 60.2% | 17/17 |  |
| 88518572 | loss | 3-0-0 | win | improved | 60.9% | 13/13 |  |
| 88527351 | loss | 3-0-0 | win | improved | 77.3% | 9/9 |  |
| 88527969 | win | 3-0-0 | win | preserved_win | 89.8% | 10/10 |  |
| 88528562 | loss | 2-1-0 | win | improved | 81.1% | 9/9 |  |
| 88688530 | win | 3-0-0 | win | preserved_win | 77.0% | 19/19 |  |
| 88702243 | loss | 3-0-0 | win | improved | 62.3% | 14/14 |  |
| 88702773 | win | 3-0-0 | win | preserved_win | 48.9% | 17/17 |  |
| 88707615 | loss | 3-0-0 | win | improved | 63.2% | 11/11 |  |
| 88710371 | win | 3-0-0 | win | preserved_win | 78.4% | 7/7 |  |
| 88714591 | loss | 3-0-0 | win | improved | 86.5% | 11/11 |  |
| 88724413 | win | 3-0-0 | win | preserved_win | 78.0% | 14/14 |  |
| 88726741 | loss | 3-0-0 | win | improved | 78.8% | 8/8 |  |
| 88727264 | loss | 3-0-0 | win | improved | 71.6% | 13/13 |  |
| 88734629 | win | 3-0-0 | win | preserved_win | 76.7% | 5/5 |  |
| 88742222 | loss | 3-0-0 | win | improved | 59.4% | 22/22 |  |
| 88745200 | win | 3-0-0 | win | preserved_win | 91.7% | 14/14 |  |
| 88746412 | loss | 3-0-0 | win | improved | 85.0% | 9/9 |  |
| 88750615 | loss | 3-0-0 | win | improved | 48.8% | 28/28 |  |
| 88754803 | loss | 3-0-0 | win | improved | 78.0% | 11/11 |  |
| 88759036 | loss | 3-0-0 | win | improved | 62.0% | 14/14 |  |
| 88762215 | loss | 3-0-0 | win | improved | 84.1% | 8/8 |  |
| 88764905 | loss | 3-0-0 | win | improved | 78.3% | 15/15 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88210975 | deck/resource endurance; inspect trace | 17/17 | 2.667 | {"deck_out": 1, "no_active_pokemon": 2} |
| 88264935 | board exhausted; inspect trace | 13/13 | 2.667 | {"no_active_pokemon": 2, "prizes": 1} |
| 88331982 | board exhausted; inspect trace | 4/4 | 13.0 | {"no_active_pokemon": 3} |
| 88355725 | board exhausted; inspect trace | 12/12 | 3.667 | {"no_active_pokemon": 3} |
| 88466967 | deck/resource endurance; inspect trace | 30/30 | 3.667 | {"deck_out": 2, "prizes": 1} |

## Matched baseline check

Baseline: `/Users/muhammadomerfarooq/Desktop/GitHub Repositories/Pokemon Challenge/artifacts/v7_every_replay_389_3x.csv`

Per-replay win-to-loss regressions: **4**

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
