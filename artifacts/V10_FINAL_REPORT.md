# V10 final report

Date: 2026-08-01

## Outcome

The selected V10 is a new Mega Lopunny ex / Dudunsparce agent, not another
incremental patch to the Crustle line used by recent agents.

- Source: `agents/v10_candidate/`
- Upload archive: `artifacts/submission_10.tar.gz`
- Recommendation: upload V10 as the next live challenger only after explicit
  user confirmation.

The official-simulator improvement is large rather than marginal: V10 beat the
submitted V9 **1780-215-5 over 2000 alternating-seat games**. It also cleared
every recent-agent comparison by a wide margin, with no timeout or abandoned
attack turn in any final gate. This is strong local evidence, not a promise of
an exponential Kaggle rating gain. V9 demonstrated that live play remains the
only reliable final judge.

## Replay intake and audit

Both supplied archives were fully inventoried before training or evaluation.

- `Top 5.zip`: 51 files, 47 unique valid completed episodes, and 4 verified
  checksum-identical duplicates. All 47 unique episodes were imported under
  `scouting_replays/archive_import/top_leaderboard_20260801_top5/`.
- `Our agents.zip`: 34 unique valid completed episodes. The exact V8 batch was
  7-10 and the exact V9 batch was 7-10. They were imported into their matching
  versioned win/loss directories.
- The project corpus now contains **470 unique episodes and 0 duplicate
  files**, up from 389 before this import.
- The new top-five sample added current Mega Lopunny/Dudunsparce, modern
  Crustle control, pure Ogerpon, Grimmsnarl/Munkidori, and multi-attacker
  toolbox evidence.

Every imported replay was classified from its recorded reward, copied into a
canonical corpus location, and checksum-verified.

## Why V9 failed live despite its local score

The V9 investigation ruled out the most concerning deployment hypothesis.
The submitted source reproduced **679 of 679 live action calls exactly**, so
Kaggle was not running a different policy.

The main failure was evaluation fidelity:

- Only 4,975 of 133,464 recorded opponent decisions, or 3.73%, mapped at high
  confidence in the old replay evaluation.
- A nonempty recorded action could be accepted as an empty mapped action when
  the menu allowed `minCount = 0`.
- Partial feature mappings and weak candidate signatures could be treated as
  usable, causing the generic fallback policy—not the recorded top policy—to
  control most counterfactual games.
- V9 changed only about 3.8% of observed decisions relative to V7 and retained
  a six-Basic deck with an approximately 45.86% no-Basic opening probability.
  Its apparent local dominance was not the structural change implied by the
  headline scores.

`tools/evaluate_replay_suite.py` now requires an exact candidate signature,
complete recorded-feature mapping, legal min/max selection counts, and a
confidence score of at least 40 before it replays an opponent decision. New
regression tests cover the formerly accepted empty-action case. Absolute win
rates from the old replay evaluator are retired as promotion evidence.

The code audit also identified general V9 defects: reading a nonexistent
`prizeCount` field instead of the prize list, a protective-Mist override that
did not require a paid colored attack cost, faulty retreat-Energy handling in
context 30, overgeneralized Crustle/Cornerstone protection, and active-only
Mist reasoning that missed Bench counter placement.

## Selected V10 design

V10 uses this exact 60-card deck:

- 4 Buneary, 3 Mega Lopunny ex
- 4 Dunsparce, 4 Dudunsparce, 1 Fan Rotom
- 4 Buddy-Buddy Poffin, 4 Ultra Ball, 4 Pokégear 3.0, 4 Poké Pad
- 4 Air Balloon
- 3 Boss's Orders, 1 Xerosic's Machinations
- 4 Hilda, 4 Lillie's Determination, 4 Wally's Compassion
- 4 Mist Energy, 3 Spiky Energy, 1 Enriching Energy

The deck creates a materially different engine:

- Dunsparce/Dudunsparce repeatedly turns board pieces into draw-three cycles.
- Buneary and Air Balloon provide cheap pivots for Mega Lopunny's 230-damage
  Gale Thrust.
- A protection-aware second Energy enables 160-damage Spiky Hopper when damage
  prevention blocks Gale Thrust.
- Thirteen Basics reduce the seven-card no-Basic opening probability from the
  recent six-Basic lists' 45.86% to 16.28%.

The final planner adds state-driven rules for the 161-230 HP pivot-knockout
window, both possible first-turn Fan Call timings, complementary Basic search,
one-board Ultra Ball recovery, unsafe Active-Wally rejection, preservation of
the last switch target, ready-Lopunny promotion after Active Run Away Draw, and
a bounded pre-attack setup budget. Runtime code contains no player names,
episode IDs, or opponent-identity branches.

## Final official-simulator gates

All direct comparisons alternated V10 between both seats.

| Opponent | V10 W-L-D | Games | Timeouts | Abandoned attack turns |
|---|---:|---:|---:|---:|
| V9 submitted | 1780-215-5 | 2,000 | 0 | 0 |
| V8 fixed | 908-90-2 | 1,000 | 0 | 0 |
| V7 | 441-58-1 | 500 | 0 | 0 |
| V6 | 917-83-0 | 1,000 | 0 | 0 |
| V5 | 879-119-2 | 1,000 | 0 | 0 |

The V9 split was 909-89 when V10 occupied seat 0 and 871-126 when it occupied
seat 1. The gain is therefore not explained by one favorable seat.

## Top-five adversarial league

Four exact-deck, state-driven pilots were built from the supplied current
top-five replays. They use visible state and card mechanics but are not the
players' recovered source code.

| Replay-derived pilot | V10 W-L-D | Games | Interpretation |
|---|---:|---:|---|
| flg modern Crustle | 461-37-2 | 500 | Strong local matchup |
| Rmy pure Ogerpon | 309-689-2 | 1,000 | Clear structural weakness |
| Sixth Sense Grimmsnarl | 473-527-0 | 1,000 | Near-even, slightly losing |
| James toolbox | 617-378-5 | 1,000 | Favorable local matchup |

Every V10 run above had zero timeouts and zero abandoned attack turns. These
results are deliberately reported separately instead of averaged: the 30.9%
Rmy result is important and prevents a claim that V10 already dominates every
top-five archetype.

## Rejected alternatives

- A behavior clone improved held-out semantic agreement from 47.37% to 59.73%
  and reached 86.82% in-sample agreement, but lost 75-223-2 to the final V10,
  58-242 to V9, and 22-277-1 to the Rmy pilot. Its less-constrained form also
  abandoned attack turns. It was rejected rather than blended.
- The key lesson is that replay imitation is not game value. Once a predicted
  action changes the state, later recorded actions become counterfactual and
  small sequencing errors compound.
- The earlier first-draft V10 was also rejected; the final optimizer beat it
  286-208-6 over 500 alternating-seat games.

## Validation and integrity

- Raw Kaggle-style execution without `__file__`: passed
- Python compilation: passed
- Exact 60-card deck validation: passed
- Archive contents: only `main.py` and `deck.csv`
- V10 plus replay-protocol regression suite: 17/17 passed
- Invalid actions in final gates: 0
- Timeouts in final gates: 0
- Abandoned attack turns in final gates: 0

SHA256:

- `main.py`: `6cb6e1de3233609f0fa41c4019407d618c8704c179c34545ef2ae7d448f70840`
- `deck.csv`: `7fc17fc61014dc3bddec69e751eecde72588bb050b56a763d82720ce92ed1d6c`
- `submission_10.tar.gz`: `6560f348596e231886f43646d09bbc18a600aa64f60e3f490ff51eb5218887ef`

## Live decision

V10 is the strongest justified next challenger from this investigation because
it combines a structural deck change, very large direct gains over V5-V9,
attack safety, and explicit testing against four current leaderboard
archetypes. It should be uploaded only with explicit user confirmation. Once
live, every replay should be stored under `scouting_replays/our_agent_v10/` and
the first evaluation should focus on opening stability, pure Ogerpon, and
Grimmsnarl counter/spread games. No local result should override sustained live
rating and matchup evidence.
