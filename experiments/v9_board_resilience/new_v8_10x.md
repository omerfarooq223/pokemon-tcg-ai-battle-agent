# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **11** (11 evaluated, 0 errors)
- Local matches: **110**
- Match results: **108 wins, 2 losses, 0 draws**
- Match win rate: **98.18%**
- Per-replay majority: **11 wins, 0 losses, 0 ties**
- Recorded opponent-action usage: **71.68%**

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
| 88527351 | loss | 10-0-0 | win | improved | 78.0% | 40/40 |  |
| 88527969 | win | 10-0-0 | win | preserved_win | 73.7% | 29/29 |  |
| 88528562 | loss | 9-1-0 | win | improved | 67.6% | 35/35 |  |
| 88688530 | win | 10-0-0 | win | preserved_win | 81.8% | 59/59 |  |
| 88702243 | loss | 9-1-0 | win | improved | 46.3% | 46/46 |  |
| 88702773 | win | 10-0-0 | win | preserved_win | 72.8% | 30/30 |  |
| 88710371 | win | 10-0-0 | win | preserved_win | 63.1% | 46/46 |  |
| 88724413 | win | 10-0-0 | win | preserved_win | 84.5% | 45/45 |  |
| 88727264 | loss | 10-0-0 | win | improved | 74.6% | 41/41 |  |
| 88734629 | win | 10-0-0 | win | preserved_win | 80.4% | 28/28 |  |
| 88745200 | win | 10-0-0 | win | preserved_win | 82.0% | 44/44 |  |

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
