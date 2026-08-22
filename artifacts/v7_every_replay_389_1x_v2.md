# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **389** (389 evaluated, 0 errors)
- Local matches: **389**
- Match results: **373 wins, 16 losses, 0 draws**
- Match win rate: **95.89%**
- Per-replay majority: **373 wins, 16 losses, 0 ties**
- Recorded opponent-action usage: **55.98%**

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
| 88114269 | loss | 1-0-0 | win | improved | 53.3% | 8/8 |  |
| 88114272 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88135168 | loss | 1-0-0 | win | improved | 78.6% | 4/4 |  |
| 88135718 | loss | 1-0-0 | win | improved | 83.3% | 2/2 |  |
| 88136757 | loss | 1-0-0 | win | improved | 81.2% | 4/4 |  |
| 88138839 | loss | 1-0-0 | win | improved | 38.1% | 12/12 |  |
| 88139351 | loss | 1-0-0 | win | improved | 54.7% | 8/8 |  |
| 88139876 | loss | 1-0-0 | win | improved | 29.6% | 7/7 |  |
| 88139877 | loss | 1-0-0 | win | improved | 76.9% | 3/3 |  |
| 88139889 | loss | 1-0-0 | win | improved | 43.1% | 9/9 |  |
| 88140397 | loss | 1-0-0 | win | improved | 41.0% | 9/9 |  |
| 88140434 | loss | 1-0-0 | win | improved | 50.9% | 7/7 |  |
| 88140934 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88141449 | loss | 1-0-0 | win | improved | 69.6% | 5/5 |  |
| 88141464 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88141972 | loss | 1-0-0 | win | improved | 52.0% | 8/8 |  |
| 88142495 | loss | 0-1-0 | loss | unresolved_loss | 95.0% | 3/3 | board exhausted; inspect trace |
| 88143033 | loss | 1-0-0 | win | improved | 68.2% | 6/6 |  |
| 88143428 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88143558 | loss | 1-0-0 | win | improved | 73.4% | 8/8 |  |
| 88143960 | loss | 1-0-0 | win | improved | 100.0% | 3/3 |  |
| 88144074 | loss | 1-0-0 | win | improved | 22.2% | 9/9 |  |
| 88144497 | win | 1-0-0 | win | preserved_win | 85.0% | 4/4 |  |
| 88145058 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88145588 | loss | 1-0-0 | win | improved | 62.1% | 5/5 |  |
| 88145696 | loss | 1-0-0 | win | improved | 50.0% | 3/3 |  |
| 88146122 | loss | 1-0-0 | win | improved | 40.9% | 8/8 |  |
| 88146648 | win | 1-0-0 | win | preserved_win | 64.3% | 2/2 |  |
| 88147191 | loss | 1-0-0 | win | improved | 22.1% | 9/9 |  |
| 88147227 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88147702 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88148218 | loss | 1-0-0 | win | improved | 76.5% | 5/5 |  |
| 88148312 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88148790 | win | 1-0-0 | win | preserved_win | 91.3% | 0/0 |  |
| 88148861 | loss | 1-0-0 | win | improved | 42.4% | 8/8 |  |
| 88149240 | loss | 1-0-0 | win | improved | 78.6% | 2/2 |  |
| 88149380 | loss | 1-0-0 | win | improved | 44.9% | 7/7 |  |
| 88149406 | loss | 1-0-0 | win | improved | 83.3% | 7/7 |  |
| 88149782 | win | 1-0-0 | win | preserved_win | 66.7% | 1/1 |  |
| 88149906 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88150296 | win | 1-0-0 | win | preserved_win | 36.8% | 10/10 |  |
| 88150868 | loss | 1-0-0 | win | improved | 51.1% | 8/8 |  |
| 88151481 | loss | 1-0-0 | win | improved | 83.3% | 9/9 |  |
| 88152037 | win | 1-0-0 | win | preserved_win | 80.8% | 3/3 |  |
| 88152577 | loss | 1-0-0 | win | improved | 84.0% | 4/4 |  |
| 88153002 | loss | 1-0-0 | win | improved | 48.7% | 10/10 |  |
| 88153112 | loss | 1-0-0 | win | improved | 66.7% | 6/6 |  |
| 88153551 | win | 1-0-0 | win | preserved_win | 93.3% | 4/4 |  |
| 88153647 | win | 1-0-0 | win | preserved_win | 87.5% | 9/9 |  |
| 88154072 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88154188 | loss | 1-0-0 | win | improved | 80.0% | 6/6 |  |
| 88154615 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88154720 | loss | 1-0-0 | win | improved | 83.3% | 7/7 |  |
| 88155167 | loss | 1-0-0 | win | improved | 85.7% | 3/3 |  |
| 88155258 | loss | 1-0-0 | win | improved | 83.3% | 4/4 |  |
| 88155735 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88155807 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88156264 | loss | 1-0-0 | win | improved | 64.3% | 3/3 |  |
| 88156364 | win | 1-0-0 | win | preserved_win | 68.8% | 5/5 |  |
| 88156894 | win | 1-0-0 | win | preserved_win | 88.0% | 7/7 |  |
| 88157011 | loss | 1-0-0 | win | improved | 68.8% | 4/4 |  |
| 88157416 | win | 1-0-0 | win | preserved_win | 52.9% | 5/5 |  |
| 88157484 | win | 1-0-0 | win | preserved_win | 81.8% | 3/3 |  |
| 88157952 | win | 1-0-0 | win | preserved_win | 88.9% | 2/2 |  |
| 88170362 | loss | 1-0-0 | win | improved | 30.0% | 8/8 |  |
| 88181889 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88183542 | loss | 1-0-0 | win | improved | 76.0% | 5/5 |  |
| 88187788 | win | 1-0-0 | win | preserved_win | 88.2% | 2/2 |  |
| 88189899 | loss | 1-0-0 | win | improved | 90.0% | 3/3 |  |
| 88190488 | loss | 1-0-0 | win | improved | 77.8% | 3/3 |  |
| 88190720 | loss | 1-0-0 | win | improved | 57.6% | 8/8 |  |
| 88191459 | loss | 1-0-0 | win | improved | 81.2% | 3/3 |  |
| 88191506 | loss | 1-0-0 | win | improved | 48.4% | 7/7 |  |
| 88191988 | loss | 1-0-0 | win | improved | 37.0% | 7/7 |  |
| 88192025 | loss | 1-0-0 | win | improved | 83.3% | 4/4 |  |
| 88192363 | loss | 1-0-0 | win | improved | 93.3% | 4/4 |  |
| 88192550 | loss | 1-0-0 | win | improved | 29.5% | 11/11 |  |
| 88193019 | loss | 1-0-0 | win | improved | 65.2% | 6/6 |  |
| 88193372 | loss | 1-0-0 | win | improved | 88.0% | 4/4 |  |
| 88193551 | loss | 1-0-0 | win | improved | 76.2% | 5/5 |  |
| 88193634 | loss | 1-0-0 | win | improved | 70.8% | 7/7 |  |
| 88195735 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88197859 | loss | 1-0-0 | win | improved | 50.0% | 6/6 |  |
| 88197860 | loss | 1-0-0 | win | improved | 75.0% | 1/1 |  |
| 88197906 | loss | 1-0-0 | win | improved | 63.6% | 5/5 |  |
| 88199435 | loss | 1-0-0 | win | improved | 34.4% | 9/9 |  |
| 88200003 | loss | 1-0-0 | win | improved | 76.5% | 5/5 |  |
| 88201040 | loss | 1-0-0 | win | improved | 30.3% | 11/11 |  |
| 88201604 | loss | 1-0-0 | win | improved | 38.0% | 12/12 |  |
| 88203591 | loss | 1-0-0 | win | improved | 73.3% | 5/5 |  |
| 88204121 | loss | 1-0-0 | win | improved | 43.4% | 7/7 |  |
| 88204232 | loss | 1-0-0 | win | improved | 63.9% | 10/10 |  |
| 88204771 | loss | 1-0-0 | win | improved | 38.9% | 6/6 |  |
| 88204990 | loss | 1-0-0 | win | improved | 76.9% | 1/1 |  |
| 88205283 | loss | 1-0-0 | win | improved | 72.7% | 3/3 |  |
| 88205289 | win | 1-0-0 | win | preserved_win | 72.0% | 8/8 |  |
| 88206332 | loss | 1-0-0 | win | improved | 80.0% | 1/1 |  |
| 88206818 | loss | 1-0-0 | win | improved | 35.2% | 5/5 |  |
| 88206895 | loss | 0-1-0 | loss | unresolved_loss | 72.0% | 2/2 | board exhausted; inspect trace |
| 88207928 | loss | 1-0-0 | win | improved | 45.5% | 5/5 |  |
| 88208293 | loss | 1-0-0 | win | improved | 43.3% | 7/7 |  |
| 88208966 | loss | 1-0-0 | win | improved | 25.7% | 9/9 |  |
| 88209048 | loss | 1-0-0 | win | improved | 40.2% | 10/10 |  |
| 88209398 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88209472 | loss | 1-0-0 | win | improved | 38.5% | 8/8 |  |
| 88209993 | loss | 0-1-0 | loss | unresolved_loss | 30.4% | 13/14 | legal attack turn abandoned |
| 88210517 | loss | 1-0-0 | win | improved | 92.6% | 2/2 |  |
| 88210975 | loss | 0-1-0 | loss | unresolved_loss | 76.3% | 4/4 | board exhausted; inspect trace |
| 88211042 | loss | 1-0-0 | win | improved | 64.3% | 3/3 |  |
| 88211566 | loss | 1-0-0 | win | improved | 40.9% | 8/8 |  |
| 88212701 | loss | 1-0-0 | win | improved | 34.4% | 7/7 |  |
| 88214700 | loss | 1-0-0 | win | improved | 84.2% | 3/3 |  |
| 88215619 | loss | 1-0-0 | win | improved | 87.5% | 1/1 |  |
| 88217155 | loss | 1-0-0 | win | improved | 83.9% | 4/4 |  |
| 88217476 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88217824 | loss | 1-0-0 | win | improved | 62.2% | 7/7 |  |
| 88220136 | loss | 1-0-0 | win | improved | 63.5% | 10/10 |  |
| 88220489 | loss | 1-0-0 | win | improved | 79.2% | 3/3 |  |
| 88220566 | loss | 1-0-0 | win | improved | 58.2% | 6/6 |  |
| 88221583 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88221669 | loss | 1-0-0 | win | improved | 69.7% | 5/5 |  |
| 88222802 | loss | 1-0-0 | win | improved | 82.4% | 8/8 |  |
| 88223081 | loss | 1-0-0 | win | improved | 53.3% | 4/4 |  |
| 88223586 | loss | 1-0-0 | win | improved | 44.7% | 7/7 |  |
| 88224733 | loss | 1-0-0 | win | improved | 46.8% | 10/10 |  |
| 88224901 | loss | 1-0-0 | win | improved | 64.0% | 6/6 |  |
| 88225199 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88227532 | loss | 1-0-0 | win | improved | 66.7% | 5/5 |  |
| 88227555 | loss | 1-0-0 | win | improved | 52.5% | 8/8 |  |
| 88230163 | loss | 1-0-0 | win | improved | 33.9% | 6/6 |  |
| 88230176 | loss | 1-0-0 | win | improved | 75.7% | 6/6 |  |
| 88230489 | loss | 1-0-0 | win | improved | 33.7% | 10/10 |  |
| 88231229 | loss | 1-0-0 | win | improved | 33.3% | 7/7 |  |
| 88232593 | loss | 1-0-0 | win | improved | 81.8% | 1/1 |  |
| 88232765 | loss | 1-0-0 | win | improved | 61.9% | 7/7 |  |
| 88233128 | loss | 1-0-0 | win | improved | 71.4% | 5/5 |  |
| 88234701 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88234900 | loss | 1-0-0 | win | improved | 77.4% | 6/6 |  |
| 88235276 | loss | 1-0-0 | win | improved | 72.2% | 4/4 |  |
| 88237853 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88238542 | loss | 1-0-0 | win | improved | 62.5% | 2/2 |  |
| 88239078 | loss | 1-0-0 | win | improved | 57.1% | 3/3 |  |
| 88239095 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88239132 | loss | 1-0-0 | win | improved | 60.0% | 3/3 |  |
| 88241784 | loss | 1-0-0 | win | improved | 80.0% | 3/3 |  |
| 88243841 | loss | 1-0-0 | win | improved | 37.0% | 10/10 |  |
| 88245069 | win | 1-0-0 | win | preserved_win | 100.0% | 1/1 |  |
| 88245592 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88246129 | win | 1-0-0 | win | preserved_win | 85.0% | 3/3 |  |
| 88246713 | win | 1-0-0 | win | preserved_win | 87.0% | 3/3 |  |
| 88247233 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88247782 | loss | 1-0-0 | win | improved | 42.4% | 11/11 |  |
| 88248321 | win | 1-0-0 | win | preserved_win | 36.1% | 2/2 |  |
| 88248844 | win | 0-1-0 | loss | regressed | 50.0% | 0/0 | never reached a legal attack |
| 88249366 | loss | 1-0-0 | win | improved | 53.4% | 7/7 |  |
| 88249393 | win | 1-0-0 | win | preserved_win | 66.7% | 2/2 |  |
| 88249914 | loss | 1-0-0 | win | improved | 58.7% | 7/7 |  |
| 88250446 | loss | 1-0-0 | win | improved | 52.2% | 7/7 |  |
| 88250998 | win | 1-0-0 | win | preserved_win | 45.5% | 7/7 |  |
| 88251535 | loss | 1-0-0 | win | improved | 88.9% | 3/3 |  |
| 88251789 | loss | 1-0-0 | win | improved | 70.0% | 2/2 |  |
| 88252076 | loss | 1-0-0 | win | improved | 100.0% | 1/1 |  |
| 88252610 | loss | 1-0-0 | win | improved | 85.7% | 3/3 |  |
| 88252759 | loss | 1-0-0 | win | improved | 81.8% | 2/2 |  |
| 88252837 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88252856 | loss | 1-0-0 | win | improved | 50.0% | 8/8 |  |
| 88253125 | win | 1-0-0 | win | preserved_win | 77.8% | 6/6 |  |
| 88253320 | loss | 1-0-0 | win | improved | 41.7% | 6/6 |  |
| 88253642 | win | 1-0-0 | win | preserved_win | 80.8% | 6/6 |  |
| 88254173 | win | 1-0-0 | win | preserved_win | 72.7% | 3/3 |  |
| 88254686 | loss | 1-0-0 | win | improved | 44.4% | 9/9 |  |
| 88254832 | loss | 1-0-0 | win | improved | 81.4% | 8/8 |  |
| 88254923 | loss | 1-0-0 | win | improved | 56.9% | 7/7 |  |
| 88255227 | loss | 1-0-0 | win | improved | 59.2% | 7/7 |  |
| 88255365 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88255773 | loss | 1-0-0 | win | improved | 82.4% | 4/4 |  |
| 88255893 | loss | 1-0-0 | win | improved | 50.0% | 7/7 |  |
| 88255975 | loss | 1-0-0 | win | improved | 53.7% | 7/7 |  |
| 88258615 | loss | 1-0-0 | win | improved | 85.7% | 2/2 |  |
| 88258639 | loss | 1-0-0 | win | improved | 65.3% | 8/8 |  |
| 88258841 | loss | 1-0-0 | win | improved | 51.7% | 6/6 |  |
| 88260624 | loss | 1-0-0 | win | improved | 39.1% | 4/4 |  |
| 88260674 | loss | 1-0-0 | win | improved | 28.8% | 11/11 |  |
| 88261149 | loss | 1-0-0 | win | improved | 88.9% | 2/2 |  |
| 88261688 | win | 1-0-0 | win | preserved_win | 81.8% | 5/5 |  |
| 88261733 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88262219 | loss | 1-0-0 | win | improved | 68.8% | 5/5 |  |
| 88262752 | win | 1-0-0 | win | preserved_win | 73.3% | 8/8 |  |
| 88263295 | win | 1-0-0 | win | preserved_win | 92.9% | 4/4 |  |
| 88263822 | win | 1-0-0 | win | preserved_win | 91.7% | 3/3 |  |
| 88263861 | loss | 1-0-0 | win | improved | 29.0% | 11/11 |  |
| 88264373 | loss | 1-0-0 | win | improved | 88.9% | 2/2 |  |
| 88264404 | loss | 1-0-0 | win | improved | 75.0% | 6/6 |  |
| 88264935 | loss | 1-0-0 | win | improved | 66.7% | 5/5 |  |
| 88264972 | loss | 1-0-0 | win | improved | 84.6% | 3/3 |  |
| 88266013 | loss | 1-0-0 | win | improved | 28.1% | 8/8 |  |
| 88267625 | loss | 1-0-0 | win | improved | 69.2% | 2/2 |  |
| 88268465 | loss | 1-0-0 | win | improved | 94.4% | 3/3 |  |
| 88268514 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88273125 | win | 1-0-0 | win | preserved_win | 52.6% | 2/2 |  |
| 88273894 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88274852 | loss | 1-0-0 | win | improved | 83.3% | 1/1 |  |
| 88276586 | loss | 1-0-0 | win | improved | 70.4% | 8/8 |  |
| 88280043 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88280276 | loss | 1-0-0 | win | improved | 40.3% | 7/7 |  |
| 88280581 | loss | 0-1-0 | loss | unresolved_loss | 95.2% | 3/3 | board exhausted; inspect trace |
| 88280592 | loss | 1-0-0 | win | improved | 50.6% | 7/7 |  |
| 88280823 | loss | 1-0-0 | win | improved | 47.0% | 10/10 |  |
| 88281112 | loss | 1-0-0 | win | improved | 68.7% | 16/16 |  |
| 88281365 | loss | 1-0-0 | win | improved | 88.9% | 2/2 |  |
| 88282965 | loss | 1-0-0 | win | improved | 53.8% | 3/3 |  |
| 88285383 | loss | 1-0-0 | win | improved | 74.2% | 7/7 |  |
| 88285882 | loss | 1-0-0 | win | improved | 71.4% | 3/3 |  |
| 88286403 | loss | 1-0-0 | win | improved | 78.9% | 7/7 |  |
| 88286429 | loss | 1-0-0 | win | improved | 80.0% | 8/8 |  |
| 88286928 | loss | 1-0-0 | win | improved | 70.0% | 7/7 |  |
| 88287449 | loss | 1-0-0 | win | improved | 30.7% | 8/8 |  |
| 88287943 | loss | 1-0-0 | win | improved | 52.3% | 7/7 |  |
| 88287982 | loss | 1-0-0 | win | improved | 68.4% | 4/4 |  |
| 88287988 | loss | 1-0-0 | win | improved | 27.8% | 9/9 |  |
| 88288578 | loss | 1-0-0 | win | improved | 26.6% | 10/10 |  |
| 88289166 | loss | 1-0-0 | win | improved | 33.1% | 9/9 |  |
| 88289703 | loss | 1-0-0 | win | improved | 41.1% | 8/8 |  |
| 88290370 | win | 1-0-0 | win | preserved_win | 94.9% | 7/7 |  |
| 88290739 | loss | 1-0-0 | win | improved | 69.2% | 3/3 |  |
| 88300893 | win | 1-0-0 | win | preserved_win | 80.6% | 7/7 |  |
| 88307667 | loss | 1-0-0 | win | improved | 75.0% | 6/6 |  |
| 88309157 | win | 1-0-0 | win | preserved_win | 88.9% | 3/3 |  |
| 88312062 | win | 1-0-0 | win | preserved_win | 66.7% | 4/4 |  |
| 88312577 | win | 1-0-0 | win | preserved_win | 77.8% | 2/2 |  |
| 88313112 | win | 1-0-0 | win | preserved_win | 35.4% | 9/9 |  |
| 88313620 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88313673 | win | 1-0-0 | win | preserved_win | 53.8% | 2/2 |  |
| 88314138 | loss | 1-0-0 | win | improved | 73.3% | 5/5 |  |
| 88314664 | loss | 1-0-0 | win | improved | 93.8% | 4/4 |  |
| 88315183 | win | 1-0-0 | win | preserved_win | 80.0% | 5/5 |  |
| 88315493 | loss | 1-0-0 | win | improved | 75.0% | 1/1 |  |
| 88315696 | win | 1-0-0 | win | preserved_win | 88.9% | 3/3 |  |
| 88316214 | loss | 0-1-0 | loss | unresolved_loss | 90.0% | 0/0 | never reached a legal attack |
| 88316726 | win | 1-0-0 | win | preserved_win | 36.1% | 11/11 |  |
| 88317257 | win | 1-0-0 | win | preserved_win | 36.5% | 9/9 |  |
| 88317769 | loss | 1-0-0 | win | improved | 41.0% | 10/10 |  |
| 88317878 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88318294 | loss | 1-0-0 | win | improved | 63.3% | 5/5 |  |
| 88318822 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88319336 | loss | 1-0-0 | win | improved | 29.2% | 9/9 |  |
| 88319853 | loss | 0-1-0 | loss | unresolved_loss | 74.1% | 3/3 | board exhausted; inspect trace |
| 88319971 | loss | 0-1-0 | loss | unresolved_loss | 66.2% | 2/2 | matchup/resource race; trace review required |
| 88320365 | win | 1-0-0 | win | preserved_win | 66.7% | 4/4 |  |
| 88320386 | loss | 1-0-0 | win | improved | 69.2% | 4/4 |  |
| 88320504 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88320896 | win | 1-0-0 | win | preserved_win | 87.0% | 9/9 |  |
| 88321003 | loss | 1-0-0 | win | improved | 69.2% | 3/3 |  |
| 88321041 | loss | 1-0-0 | win | improved | 63.6% | 3/3 |  |
| 88321420 | win | 1-0-0 | win | preserved_win | 80.0% | 1/1 |  |
| 88321956 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88322041 | loss | 1-0-0 | win | improved | 47.1% | 8/8 |  |
| 88322048 | loss | 1-0-0 | win | improved | 71.4% | 2/2 |  |
| 88322049 | loss | 1-0-0 | win | improved | 78.3% | 4/4 |  |
| 88322536 | loss | 1-0-0 | win | improved | 40.6% | 7/7 |  |
| 88322611 | loss | 1-0-0 | win | improved | 56.9% | 7/7 |  |
| 88322619 | loss | 1-0-0 | win | improved | 73.7% | 3/3 |  |
| 88322631 | loss | 1-0-0 | win | improved | 50.7% | 7/7 |  |
| 88323052 | win | 1-0-0 | win | preserved_win | 69.2% | 4/4 |  |
| 88323135 | loss | 1-0-0 | win | improved | 61.4% | 6/6 |  |
| 88323138 | loss | 1-0-0 | win | improved | 41.8% | 7/7 |  |
| 88323140 | loss | 1-0-0 | win | improved | 80.6% | 3/3 |  |
| 88323143 | loss | 1-0-0 | win | improved | 72.4% | 7/7 |  |
| 88323585 | win | 1-0-0 | win | preserved_win | 81.8% | 4/4 |  |
| 88323647 | loss | 1-0-0 | win | improved | 62.5% | 3/3 |  |
| 88323654 | loss | 1-0-0 | win | improved | 90.9% | 2/2 |  |
| 88323655 | loss | 1-0-0 | win | improved | 76.5% | 3/3 |  |
| 88323658 | loss | 1-0-0 | win | improved | 34.4% | 7/7 |  |
| 88323669 | loss | 1-0-0 | win | improved | 77.8% | 2/2 |  |
| 88323677 | loss | 0-1-0 | loss | unresolved_loss | 61.4% | 7/7 | matchup/resource race; trace review required |
| 88324102 | win | 1-0-0 | win | preserved_win | 35.3% | 13/13 |  |
| 88324178 | loss | 1-0-0 | win | improved | 80.0% | 2/2 |  |
| 88324185 | loss | 1-0-0 | win | improved | 86.7% | 5/5 |  |
| 88324192 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88324221 | loss | 1-0-0 | win | improved | 66.7% | 7/7 |  |
| 88324625 | win | 1-0-0 | win | preserved_win | 73.3% | 4/4 |  |
| 88324685 | loss | 1-0-0 | win | improved | 76.2% | 3/3 |  |
| 88324686 | loss | 1-0-0 | win | improved | 63.6% | 7/7 |  |
| 88324689 | loss | 1-0-0 | win | improved | 66.7% | 4/4 |  |
| 88324692 | loss | 1-0-0 | win | improved | 81.8% | 3/3 |  |
| 88324700 | loss | 1-0-0 | win | improved | 87.5% | 3/3 |  |
| 88325152 | loss | 1-0-0 | win | improved | 87.5% | 1/1 |  |
| 88325690 | win | 1-0-0 | win | preserved_win | 37.6% | 10/10 |  |
| 88326205 | win | 1-0-0 | win | preserved_win | 50.0% | 1/1 |  |
| 88326718 | win | 1-0-0 | win | preserved_win | 78.9% | 3/3 |  |
| 88327230 | win | 1-0-0 | win | preserved_win | 92.3% | 4/4 |  |
| 88327756 | win | 1-0-0 | win | preserved_win | 93.8% | 1/1 |  |
| 88328259 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88328805 | win | 1-0-0 | win | preserved_win | 90.0% | 9/9 |  |
| 88329324 | loss | 1-0-0 | win | improved | 60.0% | 3/3 |  |
| 88331455 | loss | 1-0-0 | win | improved | 91.7% | 2/2 |  |
| 88331982 | loss | 1-0-0 | win | improved | 20.3% | 13/13 |  |
| 88332513 | win | 1-0-0 | win | preserved_win | 83.3% | 3/3 |  |
| 88333025 | win | 1-0-0 | win | preserved_win | 77.8% | 8/8 |  |
| 88333545 | win | 1-0-0 | win | preserved_win | 85.7% | 6/6 |  |
| 88334078 | loss | 1-0-0 | win | improved | 48.9% | 6/6 |  |
| 88336523 | loss | 0-1-0 | loss | unresolved_loss | 93.2% | 3/3 | board exhausted; inspect trace |
| 88337057 | win | 1-0-0 | win | preserved_win | 77.8% | 3/3 |  |
| 88337586 | win | 1-0-0 | win | preserved_win | 91.7% | 2/2 |  |
| 88338118 | loss | 1-0-0 | win | improved | 57.4% | 10/10 |  |
| 88338652 | win | 1-0-0 | win | preserved_win | 47.2% | 7/7 |  |
| 88339176 | loss | 1-0-0 | win | improved | 60.0% | 3/3 |  |
| 88355725 | loss | 0-1-0 | loss | unresolved_loss | 46.8% | 4/4 | board exhausted; inspect trace |
| 88357353 | win | 1-0-0 | win | preserved_win | 100.0% | 2/2 |  |
| 88363833 | loss | 1-0-0 | win | improved | 54.8% | 8/8 |  |
| 88373545 | win | 1-0-0 | win | preserved_win | 100.0% | 1/1 |  |
| 88377883 | win | 1-0-0 | win | preserved_win | 75.0% | 2/2 |  |
| 88388662 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88389031 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88399423 | win | 1-0-0 | win | preserved_win | 40.0% | 10/10 |  |
| 88409367 | win | 1-0-0 | win | preserved_win | 100.0% | 2/2 |  |
| 88413119 | win | 1-0-0 | win | preserved_win | 82.6% | 5/5 |  |
| 88422207 | win | 1-0-0 | win | preserved_win | 86.7% | 7/7 |  |
| 88435827 | win | 1-0-0 | win | preserved_win | 63.6% | 1/1 |  |
| 88442046 | loss | 1-0-0 | win | improved | 76.3% | 4/4 |  |
| 88442583 | loss | 1-0-0 | win | improved | 68.8% | 6/6 |  |
| 88442585 | loss | 1-0-0 | win | improved | 38.9% | 8/8 |  |
| 88443133 | loss | 1-0-0 | win | improved | 100.0% | 2/2 |  |
| 88443655 | loss | 1-0-0 | win | improved | 87.5% | 1/1 |  |
| 88444167 | loss | 1-0-0 | win | improved | 38.6% | 7/7 |  |
| 88444648 | loss | 1-0-0 | win | improved | 90.0% | 3/3 |  |
| 88452396 | loss | 1-0-0 | win | improved | 71.4% | 8/8 |  |
| 88452950 | win | 1-0-0 | win | preserved_win | 75.0% | 1/1 |  |
| 88453474 | win | 1-0-0 | win | preserved_win | 93.8% | 5/5 |  |
| 88453996 | win | 1-0-0 | win | preserved_win | 77.8% | 3/3 |  |
| 88454521 | win | 1-0-0 | win | preserved_win | 86.1% | 11/11 |  |
| 88455120 | win | 1-0-0 | win | preserved_win | 57.1% | 2/2 |  |
| 88455645 | win | 1-0-0 | win | preserved_win | 88.9% | 5/5 |  |
| 88456174 | win | 1-0-0 | win | preserved_win | 80.0% | 6/6 |  |
| 88456712 | loss | 1-0-0 | win | improved | 36.5% | 9/9 |  |
| 88459353 | loss | 1-0-0 | win | improved | 35.6% | 8/8 |  |
| 88459908 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88462124 | loss | 1-0-0 | win | improved | 78.9% | 7/7 |  |
| 88462569 | loss | 1-0-0 | win | improved | 53.2% | 10/10 |  |
| 88463244 | loss | 0-1-0 | loss | unresolved_loss | 90.3% | 1/1 | slow attack setup/tempo; inspect trace |
| 88463694 | loss | 1-0-0 | win | improved | 66.7% | 2/2 |  |
| 88464320 | loss | 1-0-0 | win | improved | 34.3% | 9/9 |  |
| 88464738 | loss | 1-0-0 | win | improved | 66.7% | 8/8 |  |
| 88465305 | win | 1-0-0 | win | preserved_win | 88.9% | 2/2 |  |
| 88465824 | loss | 1-0-0 | win | improved | 41.4% | 6/6 |  |
| 88466344 | loss | 0-1-0 | loss | unresolved_loss | 60.3% | 4/4 | matchup/resource race; trace review required |
| 88466967 | win | 1-0-0 | win | preserved_win | 68.2% | 0/0 |  |
| 88468139 | loss | 1-0-0 | win | improved | 87.5% | 2/2 |  |
| 88468688 | win | 1-0-0 | win | preserved_win | 77.8% | 2/2 |  |
| 88475900 | win | 1-0-0 | win | preserved_win | 90.9% | 10/10 |  |
| 88477511 | loss | 1-0-0 | win | improved | 46.7% | 7/7 |  |
| 88480123 | loss | 1-0-0 | win | improved | 45.8% | 8/8 |  |
| 88480304 | win | 1-0-0 | win | preserved_win | 67.9% | 5/5 |  |
| 88481733 | loss | 1-0-0 | win | improved | 84.0% | 5/5 |  |
| 88483285 | loss | 1-0-0 | win | improved | 83.3% | 5/5 |  |
| 88483990 | win | 1-0-0 | win | preserved_win | 66.7% | 4/4 |  |
| 88486593 | win | 1-0-0 | win | preserved_win | 86.0% | 7/7 |  |
| 88511515 | loss | 1-0-0 | win | improved | 73.7% | 4/4 |  |
| 88512578 | win | 1-0-0 | win | preserved_win | 84.6% | 5/5 |  |
| 88513116 | loss | 1-0-0 | win | improved | 59.3% | 3/3 |  |
| 88514796 | win | 0-1-0 | loss | regressed | 83.3% | 1/1 | board exhausted; inspect trace |
| 88515340 | loss | 1-0-0 | win | improved | 84.2% | 2/2 |  |
| 88516436 | loss | 1-0-0 | win | improved | 75.0% | 4/4 |  |
| 88517037 | win | 1-0-0 | win | preserved_win | 78.9% | 4/4 |  |
| 88517460 | win | 1-0-0 | win | preserved_win | 40.4% | 7/7 |  |
| 88518016 | loss | 1-0-0 | win | improved | 75.0% | 3/3 |  |
| 88518164 | loss | 1-0-0 | win | improved | 63.6% | 9/9 |  |
| 88518572 | loss | 1-0-0 | win | improved | 91.7% | 2/2 |  |
| 88527351 | loss | 1-0-0 | win | improved | 85.7% | 2/2 |  |
| 88527969 | win | 1-0-0 | win | preserved_win | 84.6% | 3/3 |  |
| 88528562 | loss | 1-0-0 | win | improved | 91.7% | 5/5 |  |
| 88688530 | win | 1-0-0 | win | preserved_win | 87.0% | 5/5 |  |
| 88702243 | loss | 1-0-0 | win | improved | 73.3% | 5/5 |  |
| 88702773 | win | 1-0-0 | win | preserved_win | 66.7% | 4/4 |  |
| 88707615 | loss | 1-0-0 | win | improved | 63.6% | 3/3 |  |
| 88710371 | win | 1-0-0 | win | preserved_win | 53.4% | 7/7 |  |
| 88714591 | loss | 1-0-0 | win | improved | 85.0% | 4/4 |  |
| 88724413 | win | 1-0-0 | win | preserved_win | 85.0% | 8/8 |  |
| 88726741 | loss | 1-0-0 | win | improved | 90.0% | 1/1 |  |
| 88727264 | loss | 1-0-0 | win | improved | 44.6% | 7/7 |  |
| 88734629 | win | 1-0-0 | win | preserved_win | 81.8% | 7/7 |  |
| 88742222 | loss | 1-0-0 | win | improved | 56.2% | 6/6 |  |
| 88745200 | win | 1-0-0 | win | preserved_win | 87.5% | 6/6 |  |
| 88746412 | loss | 1-0-0 | win | improved | 58.3% | 3/3 |  |
| 88750615 | loss | 1-0-0 | win | improved | 75.0% | 2/2 |  |
| 88754803 | loss | 0-1-0 | loss | unresolved_loss | 95.0% | 23/23 | deck/resource endurance; inspect trace |
| 88759036 | loss | 1-0-0 | win | improved | 65.5% | 9/9 |  |
| 88762215 | loss | 1-0-0 | win | improved | 83.3% | 3/3 |  |
| 88764905 | loss | 1-0-0 | win | improved | 67.7% | 6/6 |  |

## Loss triage

The labels below are evidence-based triage signals, not automatically proven root causes. Confirm each one from its trace before changing the agent.

| Episode | Signal | Attack turns | First attack | End reason(s) |
|---:|---|---:|---:|---|
| 88142495 | board exhausted; inspect trace | 3/3 | 6.0 | {"no_active_pokemon": 1} |
| 88206895 | board exhausted; inspect trace | 2/2 | 3.0 | {"no_active_pokemon": 1} |
| 88209993 | legal attack turn abandoned | 13/14 | 26.0 | {"deck_out": 1} |
| 88210975 | board exhausted; inspect trace | 4/4 | 2.0 | {"no_active_pokemon": 1} |
| 88248844 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88280581 | board exhausted; inspect trace | 3/3 | 2.0 | {"no_active_pokemon": 1} |
| 88316214 | never reached a legal attack | 0/0 | — | {"no_active_pokemon": 1} |
| 88319853 | board exhausted; inspect trace | 3/3 | 11.0 | {"no_active_pokemon": 1} |
| 88319971 | matchup/resource race; trace review required | 2/2 | 5.0 | {"prizes": 1} |
| 88323677 | matchup/resource race; trace review required | 7/7 | 5.0 | {"prizes": 1} |
| 88336523 | board exhausted; inspect trace | 3/3 | 3.0 | {"no_active_pokemon": 1} |
| 88355725 | board exhausted; inspect trace | 4/4 | 3.0 | {"no_active_pokemon": 1} |
| 88463244 | slow attack setup/tempo; inspect trace | 1/1 | 17.0 | {"prizes": 1} |
| 88466344 | matchup/resource race; trace review required | 4/4 | 3.0 | {"prizes": 1} |
| 88514796 | board exhausted; inspect trace | 1/1 | 5.0 | {"no_active_pokemon": 1} |
| 88754803 | deck/resource endurance; inspect trace | 23/23 | 11.0 | {"deck_out": 1} |

## Interpretation limits

- The bundled `battle_start(deck0, deck1)` interface has no seed or state-injection argument.
- The engine reads its own randomness, so rerunning the command can change draws and coin flips.
- Recorded actions cease to be exact once V9 changes the trajectory; `scripted_fraction` quantifies how often semantic replay remained usable.
- Use several trials per replay, rerun losses at higher trial counts, and confirm proposed fixes against a matched full-suite baseline.
