# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **11** (11 evaluated, 0 errors)
- Local matches: **110**
- Match results: **109 wins, 1 losses, 0 draws**
- Match win rate: **99.09%**
- Per-replay majority: **11 wins, 0 losses, 0 ties**
- Recorded opponent-action usage: **69.50%**

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
| 88527351 | loss | 10-0-0 | win | improved | 77.6% | 70/70 |  |
| 88527969 | win | 10-0-0 | win | preserved_win | 74.0% | 39/39 |  |
| 88528562 | loss | 10-0-0 | win | improved | 60.5% | 47/47 |  |
| 88688530 | win | 9-1-0 | win | preserved_win | 84.0% | 78/78 |  |
| 88702243 | loss | 10-0-0 | win | improved | 46.2% | 45/45 |  |
| 88702773 | win | 10-0-0 | win | preserved_win | 80.8% | 27/27 |  |
| 88710371 | win | 10-0-0 | win | preserved_win | 51.8% | 60/60 |  |
| 88724413 | win | 10-0-0 | win | preserved_win | 84.2% | 35/35 |  |
| 88727264 | loss | 10-0-0 | win | improved | 63.3% | 52/52 |  |
| 88734629 | win | 10-0-0 | win | preserved_win | 78.7% | 37/37 |  |
| 88745200 | win | 10-0-0 | win | preserved_win | 87.6% | 44/44 |  |

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
