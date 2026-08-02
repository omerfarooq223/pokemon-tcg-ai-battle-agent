# Every-Replay Counterfactual Evaluation

> This is not an exact Kaggle replay. It is a counterfactual local simulation 
> using every reconstructable replay condition and explicitly reported fallback.

## Summary

- Unique replays: **11** (11 evaluated, 0 errors)
- Local matches: **33**
- Match results: **31 wins, 2 losses, 0 draws**
- Match win rate: **93.94%**
- Per-replay majority: **11 wins, 0 losses, 0 ties**
- Recorded opponent-action usage: **73.61%**

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
| 88527351 | loss | 3-0-0 | win | improved | 60.0% | 14/14 |  |
| 88527969 | win | 3-0-0 | win | preserved_win | 61.4% | 12/12 |  |
| 88528562 | loss | 3-0-0 | win | improved | 50.7% | 15/15 |  |
| 88688530 | win | 3-0-0 | win | preserved_win | 78.2% | 16/16 |  |
| 88702243 | loss | 2-1-0 | win | improved | 78.3% | 9/9 |  |
| 88702773 | win | 2-1-0 | win | preserved_win | 75.0% | 32/32 |  |
| 88710371 | win | 3-0-0 | win | preserved_win | 82.5% | 11/11 |  |
| 88724413 | win | 3-0-0 | win | preserved_win | 89.0% | 19/19 |  |
| 88727264 | loss | 3-0-0 | win | improved | 70.0% | 7/7 |  |
| 88734629 | win | 3-0-0 | win | preserved_win | 73.2% | 11/11 |  |
| 88745200 | win | 3-0-0 | win | preserved_win | 87.2% | 20/20 |  |

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
