# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **383** (383 evaluated, 0 errors)
- Local matches: **383**
- Match results: **367 wins, 16 losses, 0 draws**
- Match win rate: **95.82%**
- Per-replay majority: **367 wins, 16 losses, 0 ties**
- Recorded opponent-action usage: **56.09%**

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
| 88114269 | loss | 1-0-0 | win | improved | 73.3% | 4/4 |  |
| 88114272 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88135168 | loss | 1-0-0 | win | improved | 63.8% | 7/7 |  |
| 88135718 | loss | 1-0-0 | win | improved | 72.7% | 28/28 |  |
| 88136757 | loss | 1-0-0 | win | improved | 71.0% | 7/7 |  |
| 88138839 | loss | 1-0-0 | win | improved | 70.0% | 5/5 |  |
| 88139351 | loss | 1-0-0 | win | improved | 39.4% | 7/7 |  |
| 88139876 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88139877 | loss | 1-0-0 | win | improved | 39.2% | 8/8 |  |
| 88139889 | loss | 1-0-0 | win | improved | 70.0% | 3/3 |  |
| 88140397 | loss | 1-0-0 | win | improved | 43.2% | 9/9 |  |
| 88140434 | loss | 1-0-0 | win | improved | 55.6% | 3/3 |  |
| 88140934 | loss | 1-0-0 | win | improved | 59.7% | 7/7 |  |
| 88141449 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88141464 | loss | 1-0-0 | win | improved | 39.2% | 7/7 |  |
| 88141972 | loss | 1-0-0 | win | improved | 60.0% | 3/3 |  |
| 88142495 | loss | 1-0-0 | win | improved | 86.7% | 4/4 |  |
| 88143033 | loss | 1-0-0 | win | improved | 29.0% | 10/10 |  |
| 88143428 | loss | 1-0-0 | win | improved | 84.0% | 4/4 |  |
| 88143558 | loss | 1-0-0 | win | improved | 56.7% | 8/8 |  |
| 88143960 | loss | 1-0-0 | win | improved | 88.9% | 2/2 |  |
| 88144074 | loss | 1-0-0 | win | improved | 32.1% | 6/6 |  |
| 88144497 | win | 1-0-0 | win | preserved_win | 80.8% | 6/6 |  |
| 88145058 | loss | 1-0-0 | win | improved | 70.6% | 4/4 |  |
| 88145588 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88145696 | loss | 1-0-0 | win | improved | 40.5% | 7/7 |  |
| 88146122 | loss | 1-0-0 | win | improved | 51.3% | 6/6 |  |
| 88146648 | win | 1-0-0 | win | preserved_win | 75.9% | 5/5 |  |
| 88147191 | loss | 1-0-0 | win | improved | 71.4% | 1/1 |  |
| 88147227 | loss | 1-0-0 | win | improved | 58.1% | 9/9 |  |
| 88147702 | loss | 1-0-0 | win | improved | 90.9% | 2/2 |  |
| 88148218 | loss | 1-0-0 | win | improved | 92.3% | 4/4 |  |
| 88148312 | loss | 1-0-0 | win | improved | 77.8% | 3/3 |  |
| 88148790 | win | 1-0-0 | win | preserved_win | 87.5% | 2/2 |  |
| 88148861 | loss | 1-0-0 | win | improved | 32.6% | 9/9 |  |
| 88149240 | loss | 1-0-0 | win | improved | 64.3% | 3/3 |  |
| 88149380 | loss | 1-0-0 | win | improved | 33.3% | 12/12 |  |
| 88149406 | loss | 1-0-0 | win | improved | 73.9% | 6/6 |  |
| 88149782 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88149906 | loss | 1-0-0 | win | improved | 35.8% | 8/8 |  |
| 88150296 | win | 1-0-0 | win | preserved_win | 80.6% | 6/6 |  |
| 88150868 | loss | 1-0-0 | win | improved | 83.3% | 2/2 |  |
| 88151481 | loss | 1-0-0 | win | improved | 80.8% | 5/5 |  |
| 88152037 | win | 1-0-0 | win | preserved_win | 87.5% | 2/2 |  |
| 88152577 | loss | 1-0-0 | win | improved | 78.6% | 5/5 |  |
| 88153002 | loss | 1-0-0 | win | improved | 80.6% | 8/8 |  |
| 88153112 | loss | 1-0-0 | win | improved | 62.5% | 2/2 |  |
| 88153551 | win | 1-0-0 | win | preserved_win | 82.4% | 4/4 |  |
| 88153647 | win | 1-0-0 | win | preserved_win | 74.2% | 9/9 |  |
| 88154072 | loss | 1-0-0 | win | improved | 78.6% | 2/2 |  |
| 88154188 | loss | 1-0-0 | win | improved | 65.5% | 6/6 |  |
| 88154615 | loss | 1-0-0 | win | improved | 90.9% | 3/3 |  |
| 88154720 | loss | 1-0-0 | win | improved | 60.7% | 6/6 |  |
| 88155167 | loss | 1-0-0 | win | improved | 64.3% | 4/4 |  |
| 88155258 | loss | 1-0-0 | win | improved | 93.8% | 3/3 |  |
| 88155735 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88155807 | loss | 1-0-0 | win | improved | 83.3% | 1/1 |  |
| 88156264 | loss | 1-0-0 | win | improved | 90.7% | 45/45 |  |
| 88156364 | win | 1-0-0 | win | preserved_win | 78.8% | 6/6 |  |
| 88156894 | win | 1-0-0 | win | preserved_win | 90.9% | 6/6 |  |
| 88157011 | loss | 1-0-0 | win | improved | 70.6% | 4/4 |  |
| 88157416 | win | 1-0-0 | win | preserved_win | 41.0% | 5/5 |  |
| 88157484 | win | 1-0-0 | win | preserved_win | 71.4% | 3/3 |  |
| 88157952 | win | 1-0-0 | win | preserved_win | 84.0% | 4/4 |  |
| 88170362 | loss | 1-0-0 | win | improved | 90.0% | 4/4 |  |
| 88181889 | win | 1-0-0 | win | preserved_win | 77.8% | 3/3 |  |
| 88183542 | loss | 1-0-0 | win | improved | 49.0% | 9/9 |  |
| 88187788 | win | 1-0-0 | win | preserved_win | 81.0% | 4/4 |  |
| 88189899 | loss | 1-0-0 | win | improved | 85.0% | 5/5 |  |
| 88190488 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88190720 | loss | 1-0-0 | win | improved | 40.4% | 6/6 |  |
| 88191459 | loss | 1-0-0 | win | improved | 80.0% | 4/4 |  |
| 88191506 | loss | 1-0-0 | win | improved | 81.2% | 5/5 |  |
| 88191988 | loss | 1-0-0 | win | improved | 72.2% | 4/4 |  |
| 88192025 | loss | 1-0-0 | win | improved | 61.8% | 3/3 |  |
| 88192363 | loss | 1-0-0 | win | improved | 63.6% | 2/2 |  |
| 88192550 | loss | 1-0-0 | win | improved | 49.3% | 7/7 |  |
| 88193019 | loss | 1-0-0 | win | improved | 81.8% | 4/4 |  |
| 88193372 | loss | 1-0-0 | win | improved | 48.8% | 4/4 |  |
| 88193551 | loss | 1-0-0 | win | improved | 68.2% | 6/6 |  |
| 88193634 | loss | 1-0-0 | win | improved | 93.3% | 2/2 |  |
| 88195735 | loss | 1-0-0 | win | improved | 68.4% | 4/4 |  |
| 88197859 | loss | 1-0-0 | win | improved | 28.4% | 7/7 |  |
| 88197860 | loss | 1-0-0 | win | improved | 76.9% | 2/2 |  |
| 88197906 | loss | 1-0-0 | win | improved | 79.2% | 6/6 |  |
| 88199435 | loss | 1-0-0 | win | improved | 44.9% | 10/10 |  |
| 88200003 | loss | 1-0-0 | win | improved | 90.0% | 4/4 |  |
| 88201040 | loss | 1-0-0 | win | improved | 29.9% | 10/10 |  |
| 88201604 | loss | 1-0-0 | win | improved | 64.6% | 8/8 |  |
| 88203591 | loss | 1-0-0 | win | improved | 64.7% | 4/4 |  |
| 88204121 | loss | 1-0-0 | win | improved | 45.2% | 7/7 |  |
| 88204232 | loss | 1-0-0 | win | improved | 47.4% | 9/9 |  |
| 88204771 | loss | 1-0-0 | win | improved | 33.3% | 8/8 |  |
| 88204990 | loss | 1-0-0 | win | improved | 72.0% | 6/6 |  |
| 88205283 | loss | 1-0-0 | win | improved | 29.7% | 16/16 |  |
| 88205289 | win | 1-0-0 | win | preserved_win | 66.7% | 5/5 |  |
| 88206332 | loss | 1-0-0 | win | improved | 66.7% | 4/4 |  |
| 88206818 | loss | 0-1-0 | loss | unresolved_loss | 66.0% | 3/3 | matchup/resource race; trace review required |
| 88206895 | loss | 1-0-0 | win | improved | 51.6% | 4/4 |  |
| 88207928 | loss | 1-0-0 | win | improved | 81.8% | 2/2 |  |
| 88208293 | loss | 1-0-0 | win | improved | 35.8% | 7/7 |  |
| 88208966 | loss | 1-0-0 | win | improved | 15.1% | 8/8 |  |
| 88209048 | loss | 0-1-0 | loss | unresolved_loss | 25.7% | 5/5 | board exhausted; inspect trace |
| 88209398 | loss | 1-0-0 | win | improved | 84.6% | 4/4 |  |
| 88209472 | loss | 1-0-0 | win | improved | 35.4% | 7/7 |  |
| 88209993 | loss | 1-0-0 | win | improved | 36.0% | 8/8 |  |
| 88210517 | loss | 1-0-0 | win | improved | 26.7% | 7/7 |  |
| 88210975 | loss | 1-0-0 | win | improved | 83.3% | 1/1 |  |
| 88211042 | loss | 1-0-0 | win | improved | 47.8% | 3/3 |  |
| 88211566 | loss | 1-0-0 | win | improved | 31.2% | 9/9 |  |
| 88212701 | loss | 1-0-0 | win | improved | 41.3% | 8/8 |  |
| 88214700 | loss | 1-0-0 | win | improved | 88.2% | 4/4 |  |
| 88215619 | loss | 1-0-0 | win | improved | 66.7% | 1/1 |  |
| 88217155 | loss | 1-0-0 | win | improved | 77.8% | 5/5 |  |
| 88217476 | loss | 1-0-0 | win | improved | 35.6% | 7/7 |  |
| 88217824 | loss | 1-0-0 | win | improved | 52.2% | 7/7 |  |
| 88220136 | loss | 1-0-0 | win | improved | 55.4% | 9/9 |  |
| 88220489 | loss | 1-0-0 | win | improved | 75.0% | 5/5 |  |
| 88220566 | loss | 1-0-0 | win | improved | 72.2% | 9/9 |  |
| 88221583 | loss | 1-0-0 | win | improved | 34.8% | 7/7 |  |
| 88221669 | loss | 1-0-0 | win | improved | 82.1% | 4/4 |  |
| 88222802 | loss | 1-0-0 | win | improved | 24.5% | 6/6 |  |
| 88223081 | loss | 1-0-0 | win | improved | 81.0% | 4/4 |  |
| 88223586 | loss | 1-0-0 | win | improved | 26.9% | 12/12 |  |
| 88224733 | loss | 1-0-0 | win | improved | 63.5% | 9/9 |  |
| 88224901 | loss | 1-0-0 | win | improved | 58.3% | 3/3 |  |
| 88225199 | loss | 1-0-0 | win | improved | 41.6% | 10/10 |  |
| 88227532 | loss | 1-0-0 | win | improved | 66.7% | 5/5 |  |
| 88227555 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88230163 | loss | 1-0-0 | win | improved | 32.7% | 7/7 |  |
| 88230176 | loss | 1-0-0 | win | improved | 72.7% | 6/6 |  |
| 88230489 | loss | 1-0-0 | win | improved | 46.5% | 8/8 |  |
| 88231229 | loss | 1-0-0 | win | improved | 82.8% | 5/5 |  |
| 88232593 | loss | 1-0-0 | win | improved | 71.4% | 4/4 |  |
| 88232765 | loss | 1-0-0 | win | improved | 55.6% | 6/6 |  |
| 88233128 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88234701 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88234900 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88235276 | loss | 1-0-0 | win | improved | 37.2% | 7/7 |  |
| 88237853 | loss | 1-0-0 | win | improved | 65.0% | 5/5 |  |
| 88238542 | loss | 1-0-0 | win | improved | 84.4% | 5/5 |  |
| 88239078 | loss | 1-0-0 | win | improved | 73.7% | 4/4 |  |
| 88239095 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88239132 | loss | 1-0-0 | win | improved | 80.0% | 5/5 |  |
| 88241784 | loss | 1-0-0 | win | improved | 68.8% | 4/4 |  |
| 88243841 | loss | 1-0-0 | win | improved | 83.3% | 2/2 |  |
| 88245069 | win | 1-0-0 | win | preserved_win | 85.0% | 4/4 |  |
| 88245592 | win | 1-0-0 | win | preserved_win | 100.0% | 1/1 |  |
| 88246129 | win | 1-0-0 | win | preserved_win | 91.7% | 2/2 |  |
| 88246713 | win | 1-0-0 | win | preserved_win | 70.0% | 3/3 |  |
| 88247233 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88247782 | loss | 1-0-0 | win | improved | 50.0% | 0/0 |  |
| 88248321 | win | 1-0-0 | win | preserved_win | 81.8% | 3/3 |  |
| 88248844 | win | 1-0-0 | win | preserved_win | 58.9% | 13/13 |  |
| 88249366 | loss | 1-0-0 | win | improved | 55.8% | 9/9 |  |
| 88249393 | win | 1-0-0 | win | preserved_win | 84.6% | 3/3 |  |
| 88249914 | loss | 1-0-0 | win | improved | 68.4% | 5/5 |  |
| 88250446 | loss | 1-0-0 | win | improved | 33.3% | 7/7 |  |
| 88250998 | win | 1-0-0 | win | preserved_win | 41.2% | 4/4 |  |
| 88251535 | loss | 1-0-0 | win | improved | 68.8% | 3/3 |  |
| 88251789 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88252076 | loss | 0-1-0 | loss | unresolved_loss | 79.4% | 4/4 | board exhausted; inspect trace |
| 88252610 | loss | 1-0-0 | win | improved | 59.1% | 5/5 |  |
| 88252759 | loss | 1-0-0 | win | improved | 64.3% | 4/4 |  |
| 88252837 | loss | 0-1-0 | loss | unresolved_loss | 51.9% | 3/3 | board exhausted; inspect trace |
| 88252856 | loss | 1-0-0 | win | improved | 33.7% | 10/10 |  |
| 88253125 | win | 1-0-0 | win | preserved_win | 71.4% | 1/1 |  |
| 88253320 | loss | 1-0-0 | win | improved | 49.5% | 6/6 |  |
| 88253642 | win | 1-0-0 | win | preserved_win | 88.9% | 5/5 |  |
| 88254173 | win | 1-0-0 | win | preserved_win | 58.3% | 4/4 |  |
| 88254686 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88254832 | loss | 1-0-0 | win | improved | 63.6% | 5/5 |  |
| 88254923 | loss | 1-0-0 | win | improved | 59.5% | 6/6 |  |
| 88255227 | loss | 1-0-0 | win | improved | 41.5% | 7/7 |  |
| 88255365 | loss | 1-0-0 | win | improved | 80.0% | 1/1 |  |
| 88255773 | loss | 0-1-0 | loss | unresolved_loss | 63.2% | 0/0 | never reached a legal attack |
| 88255893 | loss | 1-0-0 | win | improved | 82.4% | 1/1 |  |
| 88255975 | loss | 1-0-0 | win | improved | 60.7% | 7/7 |  |
| 88258615 | loss | 1-0-0 | win | improved | 61.5% | 5/5 |  |
| 88258639 | loss | 1-0-0 | win | improved | 73.3% | 6/6 |  |
| 88258841 | loss | 1-0-0 | win | improved | 89.5% | 3/3 |  |
| 88260624 | loss | 0-1-0 | loss | unresolved_loss | 40.6% | 5/5 | board exhausted; inspect trace |
| 88260674 | loss | 1-0-0 | win | improved | 42.1% | 9/9 |  |
| 88261149 | loss | 1-0-0 | win | improved | 81.2% | 3/3 |  |
| 88261688 | win | 1-0-0 | win | preserved_win | 80.0% | 4/4 |  |
| 88261733 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88262219 | loss | 1-0-0 | win | improved | 62.5% | 2/2 |  |
| 88262752 | win | 1-0-0 | win | preserved_win | 82.6% | 6/6 |  |
| 88263295 | win | 1-0-0 | win | preserved_win | 37.1% | 7/7 |  |
| 88263822 | win | 1-0-0 | win | preserved_win | 87.5% | 3/3 |  |
| 88263861 | loss | 1-0-0 | win | improved | 46.3% | 10/10 |  |
| 88264373 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88264404 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88264935 | loss | 1-0-0 | win | improved | 53.1% | 4/4 |  |
| 88264972 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88266013 | loss | 1-0-0 | win | improved | 32.7% | 10/10 |  |
| 88267625 | loss | 1-0-0 | win | improved | 90.9% | 3/3 |  |
| 88268465 | loss | 1-0-0 | win | improved | 81.2% | 2/2 |  |
| 88268514 | loss | 1-0-0 | win | improved | 81.8% | 3/3 |  |
| 88273125 | win | 1-0-0 | win | preserved_win | 88.9% | 5/5 |  |
| 88273894 | loss | 1-0-0 | win | improved | 71.4% | 5/5 |  |
| 88274852 | loss | 1-0-0 | win | improved | 72.7% | 4/4 |  |
| 88276586 | loss | 1-0-0 | win | improved | 48.4% | 9/9 |  |
| 88280043 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88280276 | loss | 1-0-0 | win | improved | 44.1% | 7/7 |  |
| 88280581 | loss | 1-0-0 | win | improved | 49.5% | 10/10 |  |
| 88280592 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88280823 | loss | 1-0-0 | win | improved | 41.0% | 6/6 |  |
| 88281112 | loss | 1-0-0 | win | improved | 81.2% | 8/8 |  |
| 88281365 | loss | 1-0-0 | win | improved | 58.1% | 7/7 |  |
| 88282965 | loss | 1-0-0 | win | improved | 51.4% | 2/2 |  |
| 88285383 | loss | 1-0-0 | win | improved | 52.4% | 8/8 |  |
| 88285882 | loss | 1-0-0 | win | improved | 81.8% | 3/3 |  |
| 88286403 | loss | 1-0-0 | win | improved | 47.2% | 7/7 |  |
| 88286429 | loss | 1-0-0 | win | improved | 33.0% | 8/8 |  |
| 88286928 | loss | 1-0-0 | win | improved | 85.7% | 3/3 |  |
| 88287449 | loss | 1-0-0 | win | improved | 76.2% | 3/3 |  |
| 88287943 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88287982 | loss | 1-0-0 | win | improved | 31.7% | 9/9 |  |
| 88287988 | loss | 1-0-0 | win | improved | 30.3% | 10/10 |  |
| 88288578 | loss | 1-0-0 | win | improved | 58.3% | 5/5 |  |
| 88289166 | loss | 1-0-0 | win | improved | 36.4% | 8/8 |  |
| 88289703 | loss | 1-0-0 | win | improved | 34.0% | 7/7 |  |
| 88290370 | win | 1-0-0 | win | preserved_win | 71.4% | 2/2 |  |
| 88290739 | loss | 1-0-0 | win | improved | 56.6% | 6/6 |  |
| 88300893 | win | 1-0-0 | win | preserved_win | 82.1% | 6/6 |  |
| 88307667 | loss | 1-0-0 | win | improved | 96.2% | 6/6 |  |
| 88309157 | win | 1-0-0 | win | preserved_win | 88.9% | 3/3 |  |
| 88312062 | win | 1-0-0 | win | preserved_win | 40.0% | 1/1 |  |
| 88312577 | win | 1-0-0 | win | preserved_win | 84.0% | 4/4 |  |
| 88313112 | win | 1-0-0 | win | preserved_win | 41.1% | 5/5 |  |
| 88313620 | loss | 1-0-0 | win | improved | 45.6% | 8/8 |  |
| 88313673 | win | 1-0-0 | win | preserved_win | 48.3% | 8/8 |  |
| 88314138 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88314664 | loss | 1-0-0 | win | improved | 69.6% | 5/5 |  |
| 88315183 | win | 1-0-0 | win | preserved_win | 93.8% | 7/7 |  |
| 88315493 | loss | 1-0-0 | win | improved | 67.2% | 7/7 |  |
| 88315696 | win | 1-0-0 | win | preserved_win | 78.6% | 3/3 |  |
| 88316214 | loss | 1-0-0 | win | improved | 57.1% | 1/1 |  |
| 88316726 | win | 0-1-0 | loss | regressed | 80.0% | 0/0 | never reached a legal attack |
| 88317257 | win | 1-0-0 | win | preserved_win | 38.6% | 10/10 |  |
| 88317769 | loss | 1-0-0 | win | improved | 60.0% | 2/2 |  |
| 88317878 | loss | 1-0-0 | win | improved | 44.7% | 5/5 |  |
| 88318294 | loss | 1-0-0 | win | improved | 51.9% | 4/4 |  |
| 88318822 | win | 1-0-0 | win | preserved_win | 88.9% | 3/3 |  |
| 88319336 | loss | 1-0-0 | win | improved | 55.6% | 5/5 |  |
| 88319853 | loss | 0-1-0 | loss | unresolved_loss | 100.0% | 0/0 | never reached a legal attack |
| 88319971 | loss | 1-0-0 | win | improved | 39.3% | 8/8 |  |
| 88320365 | win | 1-0-0 | win | preserved_win | 77.8% | 5/5 |  |
| 88320386 | loss | 1-0-0 | win | improved | 57.9% | 5/5 |  |
| 88320504 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88320896 | win | 1-0-0 | win | preserved_win | 61.5% | 3/3 |  |
| 88321003 | loss | 1-0-0 | win | improved | 86.7% | 4/4 |  |
| 88321041 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88321420 | win | 1-0-0 | win | preserved_win | 89.7% | 10/10 |  |
| 88321956 | loss | 1-0-0 | win | improved | 81.6% | 7/7 |  |
| 88322041 | loss | 1-0-0 | win | improved | 52.8% | 8/8 |  |
| 88322048 | loss | 1-0-0 | win | improved | 72.7% | 2/2 |  |
| 88322049 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88322536 | loss | 1-0-0 | win | improved | 78.8% | 5/5 |  |
| 88322611 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88322619 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88322631 | loss | 1-0-0 | win | improved | 32.3% | 4/4 |  |
| 88323052 | win | 1-0-0 | win | preserved_win | 83.0% | 6/6 |  |
| 88323135 | loss | 1-0-0 | win | improved | 50.0% | 7/7 |  |
| 88323138 | loss | 1-0-0 | win | improved | 73.3% | 3/3 |  |
| 88323140 | loss | 1-0-0 | win | improved | 57.1% | 1/1 |  |
| 88323143 | loss | 1-0-0 | win | improved | 85.7% | 2/2 |  |
| 88323585 | win | 1-0-0 | win | preserved_win | 83.3% | 4/4 |  |
| 88323647 | loss | 1-0-0 | win | improved | 39.8% | 10/10 |  |
| 88323654 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88323655 | loss | 1-0-0 | win | improved | 77.8% | 3/3 |  |
| 88323658 | loss | 0-1-0 | loss | unresolved_loss | 83.0% | 1/1 | board exhausted; inspect trace |
| 88323669 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88323677 | loss | 1-0-0 | win | improved | 48.4% | 8/8 |  |
| 88324102 | win | 1-0-0 | win | preserved_win | 30.0% | 12/12 |  |
| 88324178 | loss | 1-0-0 | win | improved | 66.7% | 3/3 |  |
| 88324185 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88324192 | loss | 1-0-0 | win | improved | 88.2% | 3/3 |  |
| 88324221 | loss | 1-0-0 | win | improved | 72.2% | 4/4 |  |
| 88324625 | win | 1-0-0 | win | preserved_win | 81.8% | 4/4 |  |
| 88324685 | loss | 1-0-0 | win | improved | 33.8% | 8/8 |  |
| 88324686 | loss | 1-0-0 | win | improved | 76.9% | 4/4 |  |
| 88324689 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88324692 | loss | 1-0-0 | win | improved | 85.7% | 3/3 |  |
| 88324700 | loss | 1-0-0 | win | improved | 76.2% | 4/4 |  |
| 88325152 | loss | 0-1-0 | loss | unresolved_loss | 48.8% | 7/7 | matchup/resource race; trace review required |
| 88325690 | win | 1-0-0 | win | preserved_win | 64.0% | 3/3 |  |
| 88326205 | win | 1-0-0 | win | preserved_win | 83.3% | 2/2 |  |
| 88326718 | win | 1-0-0 | win | preserved_win | 100.0% | 2/2 |  |
| 88327230 | win | 1-0-0 | win | preserved_win | 91.7% | 2/2 |  |
| 88327756 | win | 1-0-0 | win | preserved_win | 47.1% | 6/6 |  |
| 88328259 | loss | 1-0-0 | win | improved | 64.3% | 5/5 |  |
| 88328805 | win | 1-0-0 | win | preserved_win | 83.3% | 5/5 |  |
| 88329324 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88331455 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88331982 | loss | 1-0-0 | win | improved | 36.8% | 6/6 |  |
| 88332513 | win | 1-0-0 | win | preserved_win | 88.9% | 8/8 |  |
| 88333025 | win | 1-0-0 | win | preserved_win | 74.4% | 9/9 |  |
| 88333545 | win | 1-0-0 | win | preserved_win | 90.0% | 3/3 |  |
| 88334078 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88336523 | loss | 1-0-0 | win | improved | 94.4% | 2/2 |  |
| 88337057 | win | 1-0-0 | win | preserved_win | 81.8% | 10/10 |  |
| 88337586 | win | 1-0-0 | win | preserved_win | 81.2% | 3/3 |  |
| 88338118 | loss | 1-0-0 | win | improved | 78.6% | 6/6 |  |
| 88338652 | win | 1-0-0 | win | preserved_win | 27.5% | 9/9 |  |
| 88339176 | loss | 1-0-0 | win | improved | 51.2% | 10/10 |  |
| 88355725 | loss | 0-1-0 | loss | unresolved_loss | 92.0% | 3/3 | board exhausted; inspect trace |
| 88357353 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88363833 | loss | 1-0-0 | win | improved | 53.4% | 7/7 |  |
| 88373545 | win | 1-0-0 | win | preserved_win | 81.2% | 4/4 |  |
| 88377883 | win | 1-0-0 | win | preserved_win | 72.7% | 2/2 |  |
| 88388662 | loss | 1-0-0 | win | improved | 77.8% | 3/3 |  |
| 88389031 | loss | 1-0-0 | win | improved | 72.7% | 2/2 |  |
| 88399423 | win | 1-0-0 | win | preserved_win | 83.8% | 8/8 |  |
| 88409367 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88413119 | win | 1-0-0 | win | preserved_win | 80.8% | 6/6 |  |
| 88422207 | win | 1-0-0 | win | preserved_win | 66.7% | 5/5 |  |
| 88435827 | win | 1-0-0 | win | preserved_win | 21.8% | 8/8 |  |
| 88444648 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88452396 | loss | 1-0-0 | win | improved | 60.3% | 11/11 |  |
| 88452950 | win | 1-0-0 | win | preserved_win | 86.2% | 7/7 |  |
| 88453474 | win | 1-0-0 | win | preserved_win | 69.8% | 5/5 |  |
| 88453996 | win | 1-0-0 | win | preserved_win | 76.2% | 3/3 |  |
| 88454521 | win | 1-0-0 | win | preserved_win | 85.7% | 3/3 |  |
| 88455120 | win | 1-0-0 | win | preserved_win | 86.7% | 3/3 |  |
| 88455645 | win | 1-0-0 | win | preserved_win | 73.3% | 3/3 |  |
| 88456174 | win | 1-0-0 | win | preserved_win | 61.4% | 7/7 |  |
| 88456712 | loss | 1-0-0 | win | improved | 60.0% | 2/2 |  |
| 88459353 | loss | 1-0-0 | win | improved | 42.6% | 8/8 |  |
| 88459908 | loss | 1-0-0 | win | improved | 85.7% | 4/4 |  |
| 88462124 | loss | 1-0-0 | win | improved | 81.8% | 3/3 |  |
| 88462569 | loss | 1-0-0 | win | improved | 100.0% | 4/4 |  |
| 88463244 | loss | 0-1-0 | loss | unresolved_loss | 92.3% | 0/0 | never reached a legal attack |
| 88463694 | loss | 1-0-0 | win | improved | 71.0% | 8/8 |  |
| 88464320 | loss | 0-1-0 | loss | unresolved_loss | 83.3% | 3/3 | board exhausted; inspect trace |
| 88464738 | loss | 1-0-0 | win | improved | 66.7% | 7/7 |  |
| 88465305 | win | 1-0-0 | win | preserved_win | 64.3% | 3/3 |  |
| 88465824 | loss | 1-0-0 | win | improved | 71.2% | 7/7 |  |
| 88466344 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88466967 | win | 1-0-0 | win | preserved_win | 57.1% | 3/3 |  |
| 88468139 | loss | 1-0-0 | win | improved | 86.7% | 4/4 |  |
| 88468688 | win | 1-0-0 | win | preserved_win | 94.7% | 5/5 |  |
| 88475900 | win | 1-0-0 | win | preserved_win | 77.8% | 6/6 |  |
| 88477511 | loss | 1-0-0 | win | improved | 37.0% | 7/7 |  |
| 88480123 | loss | 1-0-0 | win | improved | 76.5% | 4/4 |  |
| 88480304 | win | 1-0-0 | win | preserved_win | 92.6% | 4/4 |  |
| 88481733 | loss | 1-0-0 | win | improved | 86.7% | 3/3 |  |
| 88483285 | loss | 0-1-0 | loss | unresolved_loss | 77.6% | 1/1 | board exhausted; inspect trace |
| 88483990 | win | 0-1-0 | loss | regressed | 95.7% | 1/1 | board exhausted; inspect trace |
| 88486593 | win | 1-0-0 | win | preserved_win | 86.1% | 5/5 |  |
| 88511515 | loss | 0-1-0 | loss | unresolved_loss | 100.0% | 0/0 | never reached a legal attack |
| 88512578 | win | 1-0-0 | win | preserved_win | 89.5% | 7/7 |  |
| 88513116 | loss | 1-0-0 | win | improved | 47.1% | 6/6 |  |
| 88514796 | win | 1-0-0 | win | preserved_win | 90.0% | 2/2 |  |
| 88515340 | loss | 1-0-0 | win | improved | 87.5% | 3/3 |  |
| 88516436 | loss | 1-0-0 | win | improved | 55.7% | 7/7 |  |
| 88517037 | win | 1-0-0 | win | preserved_win | 63.1% | 8/8 |  |
| 88517460 | win | 1-0-0 | win | preserved_win | 27.1% | 7/7 |  |
| 88518016 | loss | 1-0-0 | win | improved | 77.8% | 4/4 |  |
| 88518164 | loss | 1-0-0 | win | improved | 88.9% | 3/3 |  |
| 88518572 | loss | 1-0-0 | win | improved | 68.2% | 4/4 |  |
| 88527351 | loss | 1-0-0 | win | improved | 72.7% | 1/1 |  |
| 88527969 | win | 1-0-0 | win | preserved_win | 81.8% | 5/5 |  |
| 88528562 | loss | 1-0-0 | win | improved | 67.9% | 6/6 |  |
| 88688530 | win | 1-0-0 | win | preserved_win | 79.2% | 6/6 |  |
| 88702243 | loss | 1-0-0 | win | improved | 77.3% | 5/5 |  |
| 88702773 | win | 1-0-0 | win | preserved_win | 68.4% | 2/2 |  |
| 88707615 | loss | 1-0-0 | win | improved | 40.0% | 2/2 |  |
| 88710371 | win | 1-0-0 | win | preserved_win | 68.7% | 10/10 |  |
| 88714591 | loss | 1-0-0 | win | improved | 81.8% | 4/4 |  |
| 88724413 | win | 1-0-0 | win | preserved_win | 82.1% | 10/10 |  |
| 88726741 | loss | 1-0-0 | win | improved | 69.2% | 5/5 |  |
| 88727264 | loss | 1-0-0 | win | improved | 56.8% | 6/6 |  |
| 88734629 | win | 1-0-0 | win | preserved_win | 80.0% | 2/2 |  |
| 88742222 | loss | 1-0-0 | win | improved | 84.2% | 4/4 |  |
| 88745200 | win | 1-0-0 | win | preserved_win | 84.2% | 6/6 |  |
| 88746412 | loss | 1-0-0 | win | improved | 76.7% | 2/2 |  |
| 88750615 | loss | 1-0-0 | win | improved | 81.8% | 3/3 |  |
| 88754803 | loss | 1-0-0 | win | improved | 69.2% | 3/3 |  |
| 88759036 | loss | 1-0-0 | win | improved | 40.3% | 9/9 |  |
| 88762215 | loss | 1-0-0 | win | improved | 69.2% | 1/1 |  |
| 88764905 | loss | 1-0-0 | win | improved | 82.4% | 4/4 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88206818 | matchup/resource race; trace review required | 3/3 | 3.0 | {"prizes": 1} |
| 88209048 | board exhausted; inspect trace | 5/5 | 3.0 | {"no_active_pokemon": 1} |
| 88252076 | board exhausted; inspect trace | 4/4 | 2.0 | {"no_active_pokemon": 1} |
| 88252837 | board exhausted; inspect trace | 3/3 | 2.0 | {"no_active_pokemon": 1} |
| 88255773 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88260624 | board exhausted; inspect trace | 5/5 | 3.0 | {"no_active_pokemon": 1} |
| 88316726 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88319853 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88323658 | board exhausted; inspect trace | 1/1 | 4.0 | {"no_active_pokemon": 1} |
| 88325152 | matchup/resource race; trace review required | 7/7 | 3.0 | {"prizes": 1} |
| 88355725 | board exhausted; inspect trace | 3/3 | 3.0 | {"no_active_pokemon": 1} |
| 88463244 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88464320 | board exhausted; inspect trace | 3/3 | 2.0 | {"no_active_pokemon": 1} |
| 88483285 | board exhausted; inspect trace | 1/1 | 8.0 | {"no_active_pokemon": 1} |
| 88483990 | board exhausted; inspect trace | 1/1 | 3.0 | {"no_active_pokemon": 1} |
| 88511515 | never reached a legal attack | 0/0 | — | {"prizes": 1} |

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
