# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **389**
- Match results: **376 wins, 13 losses, 0 draws**
- Match win rate: **96.66%**
- Per-replay majority: **376 wins, 13 losses, 0 ties**
- Recorded opponent-action usage: **53.72%**

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
| 88114269 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88114272 | loss | 1-0-0 | win | improved | 78.3% | 5/5 |  |
| 88135168 | loss | 1-0-0 | win | improved | 31.6% | 7/7 |  |
| 88135718 | loss | 1-0-0 | win | improved | 78.6% | 3/3 |  |
| 88136757 | loss | 1-0-0 | win | improved | 41.3% | 6/6 |  |
| 88138839 | loss | 1-0-0 | win | improved | 41.1% | 10/10 |  |
| 88139351 | loss | 1-0-0 | win | improved | 47.1% | 8/8 |  |
| 88139876 | loss | 1-0-0 | win | improved | 28.3% | 11/11 |  |
| 88139877 | loss | 1-0-0 | win | improved | 31.2% | 8/8 |  |
| 88139889 | loss | 1-0-0 | win | improved | 28.2% | 9/9 |  |
| 88140397 | loss | 1-0-0 | win | improved | 66.7% | 6/6 |  |
| 88140434 | loss | 1-0-0 | win | improved | 50.0% | 8/8 |  |
| 88140934 | loss | 1-0-0 | win | improved | 70.0% | 2/2 |  |
| 88141449 | loss | 1-0-0 | win | improved | 49.4% | 9/9 |  |
| 88141464 | loss | 1-0-0 | win | improved | 77.8% | 3/3 |  |
| 88141972 | loss | 1-0-0 | win | improved | 48.1% | 13/13 |  |
| 88142495 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88143033 | loss | 1-0-0 | win | improved | 23.2% | 8/8 |  |
| 88143428 | loss | 1-0-0 | win | improved | 100.0% | 1/1 |  |
| 88143558 | loss | 1-0-0 | win | improved | 36.8% | 8/8 |  |
| 88143960 | loss | 1-0-0 | win | improved | 86.4% | 5/5 |  |
| 88144074 | loss | 1-0-0 | win | improved | 28.2% | 9/9 |  |
| 88144497 | win | 1-0-0 | win | preserved_win | 79.2% | 5/5 |  |
| 88145058 | loss | 1-0-0 | win | improved | 68.4% | 5/5 |  |
| 88145588 | loss | 1-0-0 | win | improved | 68.8% | 3/3 |  |
| 88145696 | loss | 1-0-0 | win | improved | 32.8% | 8/8 |  |
| 88146122 | loss | 1-0-0 | win | improved | 61.5% | 7/7 |  |
| 88146648 | win | 1-0-0 | win | preserved_win | 81.8% | 3/3 |  |
| 88147191 | loss | 1-0-0 | win | improved | 23.9% | 15/15 |  |
| 88147227 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88147702 | loss | 1-0-0 | win | improved | 64.7% | 3/3 |  |
| 88148218 | loss | 0-1-0 | loss | unresolved_loss | 86.7% | 5/5 | matchup/resource race; trace review required |
| 88148312 | loss | 1-0-0 | win | improved | 27.2% | 9/9 |  |
| 88148790 | win | 1-0-0 | win | preserved_win | 84.6% | 3/3 |  |
| 88148861 | loss | 1-0-0 | win | improved | 28.4% | 10/10 |  |
| 88149240 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88149380 | loss | 1-0-0 | win | improved | 24.0% | 9/9 |  |
| 88149406 | loss | 1-0-0 | win | improved | 72.7% | 2/2 |  |
| 88149782 | win | 1-0-0 | win | preserved_win | 77.8% | 2/2 |  |
| 88149906 | loss | 1-0-0 | win | improved | 53.8% | 9/9 |  |
| 88150296 | win | 1-0-0 | win | preserved_win | 96.4% | 3/3 |  |
| 88150868 | loss | 1-0-0 | win | improved | 90.0% | 2/2 |  |
| 88151481 | loss | 1-0-0 | win | improved | 73.3% | 3/3 |  |
| 88152037 | win | 1-0-0 | win | preserved_win | 90.9% | 2/2 |  |
| 88152577 | loss | 1-0-0 | win | improved | 69.2% | 3/3 |  |
| 88153002 | loss | 1-0-0 | win | improved | 67.2% | 4/4 |  |
| 88153112 | loss | 1-0-0 | win | improved | 85.7% | 4/4 |  |
| 88153551 | win | 1-0-0 | win | preserved_win | 63.6% | 4/4 |  |
| 88153647 | win | 1-0-0 | win | preserved_win | 87.8% | 9/9 |  |
| 88154072 | loss | 1-0-0 | win | improved | 44.9% | 10/10 |  |
| 88154188 | loss | 1-0-0 | win | improved | 57.7% | 7/7 |  |
| 88154615 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88154720 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88155167 | loss | 1-0-0 | win | improved | 76.0% | 6/6 |  |
| 88155258 | loss | 1-0-0 | win | improved | 92.3% | 3/3 |  |
| 88155735 | loss | 1-0-0 | win | improved | 57.9% | 6/6 |  |
| 88155807 | loss | 1-0-0 | win | improved | 71.4% | 5/5 |  |
| 88156264 | loss | 1-0-0 | win | improved | 73.9% | 4/4 |  |
| 88156364 | win | 1-0-0 | win | preserved_win | 61.5% | 4/4 |  |
| 88156894 | win | 1-0-0 | win | preserved_win | 90.0% | 6/6 |  |
| 88157011 | loss | 1-0-0 | win | improved | 71.4% | 6/6 |  |
| 88157416 | win | 1-0-0 | win | preserved_win | 25.5% | 6/6 |  |
| 88157484 | win | 1-0-0 | win | preserved_win | 87.5% | 7/7 |  |
| 88157952 | win | 1-0-0 | win | preserved_win | 87.5% | 3/3 |  |
| 88170362 | loss | 0-1-0 | loss | unresolved_loss | 85.2% | 4/4 | board exhausted; inspect trace |
| 88181889 | win | 1-0-0 | win | preserved_win | 84.6% | 2/2 |  |
| 88183542 | loss | 0-1-0 | loss | unresolved_loss | 53.5% | 8/8 | board exhausted; inspect trace |
| 88187788 | win | 1-0-0 | win | preserved_win | 76.5% | 4/4 |  |
| 88189899 | loss | 1-0-0 | win | improved | 63.6% | 3/3 |  |
| 88190488 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88190720 | loss | 1-0-0 | win | improved | 61.5% | 4/4 |  |
| 88191459 | loss | 1-0-0 | win | improved | 69.6% | 5/5 |  |
| 88191506 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88191988 | loss | 1-0-0 | win | improved | 40.7% | 7/7 |  |
| 88192025 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88192363 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88192550 | loss | 1-0-0 | win | improved | 42.9% | 12/12 |  |
| 88193019 | loss | 1-0-0 | win | improved | 55.6% | 5/5 |  |
| 88193372 | loss | 1-0-0 | win | improved | 35.7% | 4/4 |  |
| 88193551 | loss | 1-0-0 | win | improved | 75.0% | 6/6 |  |
| 88193634 | loss | 1-0-0 | win | improved | 85.2% | 4/4 |  |
| 88195735 | loss | 1-0-0 | win | improved | 100.0% | 3/3 |  |
| 88197859 | loss | 1-0-0 | win | improved | 32.1% | 6/6 |  |
| 88197860 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88197906 | loss | 1-0-0 | win | improved | 82.4% | 3/3 |  |
| 88199435 | loss | 1-0-0 | win | improved | 52.7% | 7/7 |  |
| 88200003 | loss | 1-0-0 | win | improved | 76.2% | 5/5 |  |
| 88201040 | loss | 1-0-0 | win | improved | 33.3% | 9/9 |  |
| 88201604 | loss | 1-0-0 | win | improved | 62.9% | 5/5 |  |
| 88203591 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88204121 | loss | 1-0-0 | win | improved | 48.2% | 5/5 |  |
| 88204232 | loss | 0-1-0 | loss | unresolved_loss | 88.2% | 5/5 | board exhausted; inspect trace |
| 88204771 | loss | 1-0-0 | win | improved | 70.0% | 2/2 |  |
| 88204990 | loss | 1-0-0 | win | improved | 37.2% | 8/8 |  |
| 88205283 | loss | 1-0-0 | win | improved | 41.8% | 8/8 |  |
| 88205289 | win | 1-0-0 | win | preserved_win | 66.7% | 3/3 |  |
| 88206332 | loss | 1-0-0 | win | improved | 64.3% | 4/4 |  |
| 88206818 | loss | 1-0-0 | win | improved | 32.8% | 4/4 |  |
| 88206895 | loss | 1-0-0 | win | improved | 24.8% | 10/10 |  |
| 88207928 | loss | 1-0-0 | win | improved | 48.9% | 7/7 |  |
| 88208293 | loss | 1-0-0 | win | improved | 55.1% | 7/7 |  |
| 88208966 | loss | 1-0-0 | win | improved | 38.5% | 11/11 |  |
| 88209048 | loss | 1-0-0 | win | improved | 51.4% | 6/6 |  |
| 88209398 | loss | 1-0-0 | win | improved | 83.3% | 1/1 |  |
| 88209472 | loss | 1-0-0 | win | improved | 29.9% | 9/9 |  |
| 88209993 | loss | 1-0-0 | win | improved | 54.2% | 9/9 |  |
| 88210517 | loss | 1-0-0 | win | improved | 84.6% | 5/5 |  |
| 88210975 | loss | 1-0-0 | win | improved | 32.5% | 7/7 |  |
| 88211042 | loss | 1-0-0 | win | improved | 58.3% | 2/2 |  |
| 88211566 | loss | 1-0-0 | win | improved | 39.1% | 9/9 |  |
| 88212701 | loss | 1-0-0 | win | improved | 40.3% | 7/7 |  |
| 88214700 | loss | 1-0-0 | win | improved | 76.9% | 4/4 |  |
| 88215619 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88217155 | loss | 1-0-0 | win | improved | 79.2% | 4/4 |  |
| 88217476 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88217824 | loss | 1-0-0 | win | improved | 46.9% | 6/6 |  |
| 88220136 | loss | 1-0-0 | win | improved | 41.7% | 7/7 |  |
| 88220489 | loss | 1-0-0 | win | improved | 66.7% | 4/4 |  |
| 88220566 | loss | 1-0-0 | win | improved | 47.5% | 7/7 |  |
| 88221583 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88221669 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88222802 | loss | 1-0-0 | win | improved | 80.0% | 4/4 |  |
| 88223081 | loss | 1-0-0 | win | improved | 87.5% | 3/3 |  |
| 88223586 | loss | 1-0-0 | win | improved | 50.6% | 9/9 |  |
| 88224733 | loss | 0-1-0 | loss | unresolved_loss | 100.0% | 1/1 | board exhausted; inspect trace |
| 88224901 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88225199 | loss | 1-0-0 | win | improved | 53.5% | 9/9 |  |
| 88227532 | loss | 1-0-0 | win | improved | 72.7% | 6/6 |  |
| 88227555 | loss | 1-0-0 | win | improved | 66.7% | 4/4 |  |
| 88230163 | loss | 1-0-0 | win | improved | 30.3% | 8/8 |  |
| 88230176 | loss | 1-0-0 | win | improved | 71.4% | 5/5 |  |
| 88230489 | loss | 1-0-0 | win | improved | 62.5% | 3/3 |  |
| 88231229 | loss | 1-0-0 | win | improved | 29.2% | 7/7 |  |
| 88232593 | loss | 1-0-0 | win | improved | 76.9% | 3/3 |  |
| 88232765 | loss | 1-0-0 | win | improved | 50.0% | 6/6 |  |
| 88233128 | loss | 1-0-0 | win | improved | 62.3% | 8/8 |  |
| 88234701 | loss | 1-0-0 | win | improved | 60.0% | 3/3 |  |
| 88234900 | loss | 1-0-0 | win | improved | 83.3% | 5/5 |  |
| 88235276 | loss | 1-0-0 | win | improved | 83.3% | 2/2 |  |
| 88237853 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88238542 | loss | 1-0-0 | win | improved | 60.0% | 2/2 |  |
| 88239078 | loss | 1-0-0 | win | improved | 77.1% | 7/7 |  |
| 88239095 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88239132 | loss | 1-0-0 | win | improved | 88.5% | 5/5 |  |
| 88241784 | loss | 1-0-0 | win | improved | 33.8% | 7/7 |  |
| 88243841 | loss | 1-0-0 | win | improved | 43.3% | 9/9 |  |
| 88245069 | win | 1-0-0 | win | preserved_win | 82.6% | 4/4 |  |
| 88245592 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88246129 | win | 1-0-0 | win | preserved_win | 92.9% | 3/3 |  |
| 88246713 | win | 1-0-0 | win | preserved_win | 64.3% | 3/3 |  |
| 88247233 | loss | 1-0-0 | win | improved | 75.0% | 7/7 |  |
| 88247782 | loss | 1-0-0 | win | improved | 59.3% | 3/3 |  |
| 88248321 | win | 1-0-0 | win | preserved_win | 72.2% | 4/4 |  |
| 88248844 | win | 0-1-0 | loss | regressed | 88.6% | 4/4 | board exhausted; inspect trace |
| 88249366 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88249393 | win | 1-0-0 | win | preserved_win | 78.6% | 3/3 |  |
| 88249914 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88250446 | loss | 1-0-0 | win | improved | 36.0% | 7/7 |  |
| 88250998 | win | 1-0-0 | win | preserved_win | 42.1% | 4/4 |  |
| 88251535 | loss | 1-0-0 | win | improved | 36.2% | 7/7 |  |
| 88251789 | loss | 1-0-0 | win | improved | 54.4% | 8/8 |  |
| 88252076 | loss | 1-0-0 | win | improved | 100.0% | 1/1 |  |
| 88252610 | loss | 1-0-0 | win | improved | 62.5% | 8/8 |  |
| 88252759 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88252837 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88252856 | loss | 1-0-0 | win | improved | 45.8% | 5/5 |  |
| 88253125 | win | 1-0-0 | win | preserved_win | 70.0% | 3/3 |  |
| 88253320 | loss | 1-0-0 | win | improved | 23.5% | 8/8 |  |
| 88253642 | win | 1-0-0 | win | preserved_win | 75.0% | 4/4 |  |
| 88254173 | win | 1-0-0 | win | preserved_win | 28.1% | 8/8 |  |
| 88254686 | loss | 1-0-0 | win | improved | 69.0% | 6/6 |  |
| 88254832 | loss | 1-0-0 | win | improved | 70.0% | 4/4 |  |
| 88254923 | loss | 1-0-0 | win | improved | 46.4% | 5/5 |  |
| 88255227 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88255365 | loss | 1-0-0 | win | improved | 50.0% | 4/4 |  |
| 88255773 | loss | 1-0-0 | win | improved | 63.3% | 5/5 |  |
| 88255893 | loss | 1-0-0 | win | improved | 83.3% | 4/4 |  |
| 88255975 | loss | 1-0-0 | win | improved | 65.2% | 7/7 |  |
| 88258615 | loss | 1-0-0 | win | improved | 50.0% | 2/2 |  |
| 88258639 | loss | 1-0-0 | win | improved | 46.8% | 9/9 |  |
| 88258841 | loss | 1-0-0 | win | improved | 30.3% | 9/9 |  |
| 88260624 | loss | 1-0-0 | win | improved | 43.5% | 7/7 |  |
| 88260674 | loss | 1-0-0 | win | improved | 33.3% | 11/11 |  |
| 88261149 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88261688 | win | 1-0-0 | win | preserved_win | 89.3% | 4/4 |  |
| 88261733 | loss | 1-0-0 | win | improved | 35.6% | 4/4 |  |
| 88262219 | loss | 1-0-0 | win | improved | 53.3% | 4/4 |  |
| 88262752 | win | 1-0-0 | win | preserved_win | 81.2% | 5/5 |  |
| 88263295 | win | 1-0-0 | win | preserved_win | 83.3% | 2/2 |  |
| 88263822 | win | 1-0-0 | win | preserved_win | 100.0% | 2/2 |  |
| 88263861 | loss | 1-0-0 | win | improved | 59.7% | 9/9 |  |
| 88264373 | loss | 1-0-0 | win | improved | 73.3% | 4/4 |  |
| 88264404 | loss | 1-0-0 | win | improved | 82.4% | 5/5 |  |
| 88264935 | loss | 1-0-0 | win | improved | 91.7% | 4/4 |  |
| 88264972 | loss | 1-0-0 | win | improved | 66.7% | 1/1 |  |
| 88266013 | loss | 1-0-0 | win | improved | 35.1% | 9/9 |  |
| 88267625 | loss | 1-0-0 | win | improved | 90.9% | 2/2 |  |
| 88268465 | loss | 1-0-0 | win | improved | 81.8% | 2/2 |  |
| 88268514 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88273125 | win | 1-0-0 | win | preserved_win | 86.4% | 7/7 |  |
| 88273894 | loss | 1-0-0 | win | improved | 81.8% | 2/2 |  |
| 88274852 | loss | 1-0-0 | win | improved | 31.1% | 8/8 |  |
| 88276586 | loss | 1-0-0 | win | improved | 45.5% | 7/7 |  |
| 88280043 | loss | 0-1-0 | loss | unresolved_loss | 58.1% | 3/3 | board exhausted; inspect trace |
| 88280276 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88280581 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88280592 | loss | 1-0-0 | win | improved | 38.7% | 7/7 |  |
| 88280823 | loss | 1-0-0 | win | improved | 87.5% | 3/3 |  |
| 88281112 | loss | 1-0-0 | win | improved | 90.0% | 2/2 |  |
| 88281365 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88282965 | loss | 1-0-0 | win | improved | 37.3% | 7/7 |  |
| 88285383 | loss | 1-0-0 | win | improved | 46.6% | 10/10 |  |
| 88285882 | loss | 1-0-0 | win | improved | 63.8% | 9/9 |  |
| 88286403 | loss | 1-0-0 | win | improved | 46.0% | 4/4 |  |
| 88286429 | loss | 1-0-0 | win | improved | 40.8% | 9/9 |  |
| 88286928 | loss | 1-0-0 | win | improved | 51.1% | 7/7 |  |
| 88287449 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88287943 | loss | 1-0-0 | win | improved | 84.0% | 3/3 |  |
| 88287982 | loss | 1-0-0 | win | improved | 77.8% | 1/1 |  |
| 88287988 | loss | 1-0-0 | win | improved | 76.9% | 3/3 |  |
| 88288578 | loss | 1-0-0 | win | improved | 37.0% | 7/7 |  |
| 88289166 | loss | 1-0-0 | win | improved | 64.3% | 5/5 |  |
| 88289703 | loss | 1-0-0 | win | improved | 19.5% | 9/9 |  |
| 88290370 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88290739 | loss | 1-0-0 | win | improved | 35.8% | 9/9 |  |
| 88300893 | win | 1-0-0 | win | preserved_win | 86.7% | 6/6 |  |
| 88307667 | loss | 1-0-0 | win | improved | 54.5% | 2/2 |  |
| 88309157 | win | 1-0-0 | win | preserved_win | 86.4% | 5/5 |  |
| 88312062 | win | 1-0-0 | win | preserved_win | 50.0% | 1/1 |  |
| 88312577 | win | 1-0-0 | win | preserved_win | 69.2% | 3/3 |  |
| 88313112 | win | 1-0-0 | win | preserved_win | 26.3% | 7/7 |  |
| 88313620 | loss | 1-0-0 | win | improved | 62.8% | 8/8 |  |
| 88313673 | win | 1-0-0 | win | preserved_win | 60.0% | 2/2 |  |
| 88314138 | loss | 1-0-0 | win | improved | 72.7% | 4/4 |  |
| 88314664 | loss | 1-0-0 | win | improved | 64.7% | 4/4 |  |
| 88315183 | win | 1-0-0 | win | preserved_win | 81.8% | 3/3 |  |
| 88315493 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88315696 | win | 1-0-0 | win | preserved_win | 62.5% | 2/2 |  |
| 88316214 | loss | 1-0-0 | win | improved | 90.0% | 2/2 |  |
| 88316726 | win | 1-0-0 | win | preserved_win | 54.1% | 8/8 |  |
| 88317257 | win | 1-0-0 | win | preserved_win | 76.5% | 3/3 |  |
| 88317769 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88317878 | loss | 1-0-0 | win | improved | 70.6% | 4/4 |  |
| 88318294 | loss | 1-0-0 | win | improved | 90.0% | 2/2 |  |
| 88318822 | win | 1-0-0 | win | preserved_win | 91.7% | 3/3 |  |
| 88319336 | loss | 1-0-0 | win | improved | 31.5% | 9/9 |  |
| 88319853 | loss | 1-0-0 | win | improved | 47.6% | 3/3 |  |
| 88319971 | loss | 0-1-0 | loss | unresolved_loss | 55.6% | 2/2 | board exhausted; inspect trace |
| 88320365 | win | 1-0-0 | win | preserved_win | 85.7% | 2/2 |  |
| 88320386 | loss | 1-0-0 | win | improved | 64.7% | 6/6 |  |
| 88320504 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88320896 | win | 0-1-0 | loss | regressed | 82.0% | 2/2 | deck/resource endurance; inspect trace |
| 88321003 | loss | 1-0-0 | win | improved | 70.6% | 5/5 |  |
| 88321041 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88321420 | win | 1-0-0 | win | preserved_win | 79.2% | 6/6 |  |
| 88321956 | loss | 1-0-0 | win | improved | 45.0% | 6/6 |  |
| 88322041 | loss | 1-0-0 | win | improved | 53.8% | 10/10 |  |
| 88322048 | loss | 1-0-0 | win | improved | 72.2% | 2/2 |  |
| 88322049 | loss | 1-0-0 | win | improved | 85.7% | 2/2 |  |
| 88322536 | loss | 1-0-0 | win | improved | 46.7% | 1/1 |  |
| 88322611 | loss | 1-0-0 | win | improved | 61.5% | 6/6 |  |
| 88322619 | loss | 1-0-0 | win | improved | 78.3% | 4/4 |  |
| 88322631 | loss | 1-0-0 | win | improved | 40.3% | 7/7 |  |
| 88323052 | win | 1-0-0 | win | preserved_win | 92.3% | 3/3 |  |
| 88323135 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88323138 | loss | 1-0-0 | win | improved | 78.6% | 2/2 |  |
| 88323140 | loss | 1-0-0 | win | improved | 100.0% | 1/1 |  |
| 88323143 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88323585 | win | 1-0-0 | win | preserved_win | 74.2% | 7/7 |  |
| 88323647 | loss | 1-0-0 | win | improved | 78.1% | 7/7 |  |
| 88323654 | loss | 1-0-0 | win | improved | 85.7% | 2/2 |  |
| 88323655 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88323658 | loss | 0-1-0 | loss | unresolved_loss | 69.0% | 1/1 | board exhausted; inspect trace |
| 88323669 | loss | 1-0-0 | win | improved | 77.8% | 5/5 |  |
| 88323677 | loss | 1-0-0 | win | improved | 32.3% | 7/7 |  |
| 88324102 | win | 0-1-0 | loss | regressed | 84.0% | 2/2 | board exhausted; inspect trace |
| 88324178 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88324185 | loss | 1-0-0 | win | improved | 68.2% | 5/5 |  |
| 88324192 | loss | 1-0-0 | win | improved | 80.0% | 1/1 |  |
| 88324221 | loss | 1-0-0 | win | improved | 81.2% | 3/3 |  |
| 88324625 | win | 1-0-0 | win | preserved_win | 90.9% | 4/4 |  |
| 88324685 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88324686 | loss | 1-0-0 | win | improved | 70.0% | 5/5 |  |
| 88324689 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88324692 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88324700 | loss | 1-0-0 | win | improved | 81.2% | 3/3 |  |
| 88325152 | loss | 1-0-0 | win | improved | 28.7% | 10/10 |  |
| 88325690 | win | 1-0-0 | win | preserved_win | 42.5% | 9/9 |  |
| 88326205 | win | 1-0-0 | win | preserved_win | 85.7% | 2/2 |  |
| 88326718 | win | 1-0-0 | win | preserved_win | 80.0% | 3/3 |  |
| 88327230 | win | 1-0-0 | win | preserved_win | 91.7% | 6/6 |  |
| 88327756 | win | 1-0-0 | win | preserved_win | 71.4% | 2/2 |  |
| 88328259 | loss | 1-0-0 | win | improved | 64.3% | 3/3 |  |
| 88328805 | win | 1-0-0 | win | preserved_win | 92.3% | 2/2 |  |
| 88329324 | loss | 1-0-0 | win | improved | 71.4% | 5/5 |  |
| 88331455 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88331982 | loss | 1-0-0 | win | improved | 70.6% | 2/2 |  |
| 88332513 | win | 1-0-0 | win | preserved_win | 81.2% | 6/6 |  |
| 88333025 | win | 1-0-0 | win | preserved_win | 80.0% | 5/5 |  |
| 88333545 | win | 1-0-0 | win | preserved_win | 72.7% | 3/3 |  |
| 88334078 | loss | 1-0-0 | win | improved | 50.0% | 4/4 |  |
| 88336523 | loss | 1-0-0 | win | improved | 55.6% | 5/5 |  |
| 88337057 | win | 1-0-0 | win | preserved_win | 71.4% | 2/2 |  |
| 88337586 | win | 1-0-0 | win | preserved_win | 83.3% | 2/2 |  |
| 88338118 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88338652 | win | 1-0-0 | win | preserved_win | 84.5% | 6/6 |  |
| 88339176 | loss | 1-0-0 | win | improved | 78.3% | 5/5 |  |
| 88355725 | loss | 0-1-0 | loss | unresolved_loss | 75.0% | 2/2 | matchup/resource race; trace review required |
| 88357353 | win | 1-0-0 | win | preserved_win | 76.9% | 4/4 |  |
| 88363833 | loss | 1-0-0 | win | improved | 34.5% | 9/9 |  |
| 88373545 | win | 1-0-0 | win | preserved_win | 85.7% | 4/4 |  |
| 88377883 | win | 1-0-0 | win | preserved_win | 95.2% | 2/2 |  |
| 88388662 | loss | 1-0-0 | win | improved | 56.5% | 10/10 |  |
| 88389031 | loss | 1-0-0 | win | improved | 88.9% | 3/3 |  |
| 88399423 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88409367 | win | 1-0-0 | win | preserved_win | 80.0% | 2/2 |  |
| 88413119 | win | 1-0-0 | win | preserved_win | 64.3% | 3/3 |  |
| 88422207 | win | 1-0-0 | win | preserved_win | 55.6% | 2/2 |  |
| 88435827 | win | 1-0-0 | win | preserved_win | 22.1% | 8/8 |  |
| 88442046 | loss | 1-0-0 | win | improved | 65.4% | 7/7 |  |
| 88442583 | loss | 1-0-0 | win | improved | 58.1% | 7/7 |  |
| 88442585 | loss | 1-0-0 | win | improved | 62.5% | 2/2 |  |
| 88443133 | loss | 1-0-0 | win | improved | 43.5% | 8/8 |  |
| 88443655 | loss | 1-0-0 | win | improved | 76.9% | 1/1 |  |
| 88444167 | loss | 1-0-0 | win | improved | 64.0% | 5/5 |  |
| 88444648 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88452396 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88452950 | win | 1-0-0 | win | preserved_win | 81.5% | 5/5 |  |
| 88453474 | win | 1-0-0 | win | preserved_win | 82.8% | 3/3 |  |
| 88453996 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88454521 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88455120 | win | 1-0-0 | win | preserved_win | 85.7% | 4/4 |  |
| 88455645 | win | 1-0-0 | win | preserved_win | 82.4% | 2/2 |  |
| 88456174 | win | 1-0-0 | win | preserved_win | 83.3% | 4/4 |  |
| 88456712 | loss | 1-0-0 | win | improved | 36.8% | 9/9 |  |
| 88459353 | loss | 1-0-0 | win | improved | 29.9% | 7/7 |  |
| 88459908 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88462124 | loss | 1-0-0 | win | improved | 83.3% | 4/4 |  |
| 88462569 | loss | 1-0-0 | win | improved | 94.1% | 4/4 |  |
| 88463244 | loss | 1-0-0 | win | improved | 23.0% | 6/6 |  |
| 88463694 | loss | 1-0-0 | win | improved | 100.0% | 3/3 |  |
| 88464320 | loss | 1-0-0 | win | improved | 80.0% | 4/4 |  |
| 88464738 | loss | 1-0-0 | win | improved | 78.6% | 3/3 |  |
| 88465305 | win | 1-0-0 | win | preserved_win | 84.6% | 3/3 |  |
| 88465824 | loss | 1-0-0 | win | improved | 60.4% | 6/6 |  |
| 88466344 | loss | 0-1-0 | loss | unresolved_loss | 52.4% | 4/4 | board exhausted; inspect trace |
| 88466967 | win | 1-0-0 | win | preserved_win | 90.0% | 0/0 |  |
| 88468139 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88468688 | win | 1-0-0 | win | preserved_win | 61.0% | 7/7 |  |
| 88475900 | win | 1-0-0 | win | preserved_win | 73.3% | 4/4 |  |
| 88477511 | loss | 1-0-0 | win | improved | 20.7% | 8/8 |  |
| 88480123 | loss | 1-0-0 | win | improved | 83.3% | 4/4 |  |
| 88480304 | win | 1-0-0 | win | preserved_win | 83.3% | 5/5 |  |
| 88481733 | loss | 1-0-0 | win | improved | 85.2% | 5/5 |  |
| 88483285 | loss | 1-0-0 | win | improved | 70.8% | 5/5 |  |
| 88483990 | win | 1-0-0 | win | preserved_win | 33.3% | 11/11 |  |
| 88486593 | win | 1-0-0 | win | preserved_win | 91.7% | 8/8 |  |
| 88511515 | loss | 1-0-0 | win | improved | 57.1% | 4/4 |  |
| 88512578 | win | 1-0-0 | win | preserved_win | 73.3% | 7/7 |  |
| 88513116 | loss | 1-0-0 | win | improved | 62.5% | 2/2 |  |
| 88514796 | win | 1-0-0 | win | preserved_win | 100.0% | 3/3 |  |
| 88515340 | loss | 1-0-0 | win | improved | 78.6% | 3/3 |  |
| 88516436 | loss | 1-0-0 | win | improved | 85.7% | 4/4 |  |
| 88517037 | win | 1-0-0 | win | preserved_win | 84.0% | 5/5 |  |
| 88517460 | win | 1-0-0 | win | preserved_win | 57.4% | 7/7 |  |
| 88518016 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88518164 | loss | 1-0-0 | win | improved | 58.8% | 6/6 |  |
| 88518572 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88527351 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88527969 | win | 1-0-0 | win | preserved_win | 88.4% | 7/7 |  |
| 88528562 | loss | 1-0-0 | win | improved | 46.2% | 9/9 |  |
| 88688530 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88702243 | loss | 1-0-0 | win | improved | 50.0% | 2/2 |  |
| 88702773 | win | 1-0-0 | win | preserved_win | 71.4% | 3/3 |  |
| 88707615 | loss | 1-0-0 | win | improved | 83.3% | 1/1 |  |
| 88710371 | win | 1-0-0 | win | preserved_win | 50.0% | 10/10 |  |
| 88714591 | loss | 1-0-0 | win | improved | 90.6% | 4/4 |  |
| 88724413 | win | 1-0-0 | win | preserved_win | 87.5% | 6/6 |  |
| 88726741 | loss | 1-0-0 | win | improved | 88.9% | 4/4 |  |
| 88727264 | loss | 1-0-0 | win | improved | 75.0% | 6/6 |  |
| 88734629 | win | 1-0-0 | win | preserved_win | 70.6% | 1/1 |  |
| 88742222 | loss | 1-0-0 | win | improved | 45.8% | 9/9 |  |
| 88745200 | win | 1-0-0 | win | preserved_win | 93.3% | 6/6 |  |
| 88746412 | loss | 1-0-0 | win | improved | 69.2% | 3/3 |  |
| 88750615 | loss | 1-0-0 | win | improved | 93.3% | 4/4 |  |
| 88754803 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88759036 | loss | 1-0-0 | win | improved | 91.7% | 3/3 |  |
| 88762215 | loss | 1-0-0 | win | improved | 52.8% | 6/6 |  |
| 88764905 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88148218 | matchup/resource race; trace review required | 5/5 | 7.0 | {"prizes": 1} |
| 88170362 | board exhausted; inspect trace | 4/4 | 4.0 | {"no_active_pokemon": 1} |
| 88183542 | board exhausted; inspect trace | 8/8 | 2.0 | {"no_active_pokemon": 1} |
| 88204232 | board exhausted; inspect trace | 5/5 | 2.0 | {"no_active_pokemon": 1} |
| 88224733 | board exhausted; inspect trace | 1/1 | 2.0 | {"no_active_pokemon": 1} |
| 88248844 | board exhausted; inspect trace | 4/4 | 3.0 | {"no_active_pokemon": 1} |
| 88280043 | board exhausted; inspect trace | 3/3 | 2.0 | {"no_active_pokemon": 1} |
| 88319971 | board exhausted; inspect trace | 2/2 | 3.0 | {"no_active_pokemon": 1} |
| 88320896 | deck/resource endurance; inspect trace | 2/2 | 7.0 | {"deck_out": 1} |
| 88323658 | board exhausted; inspect trace | 1/1 | 2.0 | {"no_active_pokemon": 1} |
| 88324102 | board exhausted; inspect trace | 2/2 | 3.0 | {"no_active_pokemon": 1} |
| 88355725 | matchup/resource race; trace review required | 2/2 | 3.0 | {"prizes": 1} |
| 88466344 | board exhausted; inspect trace | 4/4 | 3.0 | {"no_active_pokemon": 1} |

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
