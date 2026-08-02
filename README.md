# Pokémon TCG AI Battle Agent

A rule-based, state-aware agent developed for Kaggle's
[Pokémon TCG AI Battle Challenge](https://www.kaggle.com/competitions/pokemon-tcg-ai-battle).
The project tracks the evolution from a legal-action baseline to an agent that plans
attack readiness, colored-energy placement, promotion, search targets, healing,
hand control, and bounded pre-attack setup.

## Repository layout

- `agents/` — versioned agent and deck snapshots.
- `experiments/` — rejected ideas and replay-informed stress agents.
- `tools/` — submission building, local matches, replay analysis, and evaluation.
- `artifacts/*.csv` — selected compact benchmark summaries.
- `main.py` and `deck.csv` — the original baseline retained for reproducibility.

Large or derived files are intentionally excluded from Git: the local Python
environment, official Kaggle downloads and simulator binaries, raw replay JSON,
submission archives, detailed traces, caches, and leaderboard snapshots.

## Agent versions

- **V1:** original legal-action baseline.
- **V2:** generic action ranking with a compact replay-trained tie-breaker.
- **V3:** state-aware card, attacker, and energy planner.
- **V4:** Crustle/Cornerstone deck with a bounded mandatory-attack guard.
- **V5:** V4's core plus state-driven hand control for large-hand engines.

Each version directory contains its editable `main.py` policy and 60-card
`deck.csv`. Submission archives are generated from these two source files and are
not versioned because they can be reproduced exactly with the build tool.

## Build an agent submission

For example, to package V5:

```bash
python3 tools/build_submission.py \
  --agent-dir agents/v5_candidate \
  --output artifacts/submisson_5.tar.gz
```

The builder validates Kaggle's raw-loader behavior, the 60-card deck, archive
contents, and Python compilation. Generated upload archives remain local and are
ignored by Git.

## Run local matches

After installing the official simulator files:

```bash
python3 tools/run_local_matches.py \
  --agent-dir agents/v5_candidate \
  --opponent-dir agents/v4_attackfix \
  --matches 100 \
  --swap-seats
```

Use `python3 tools/run_local_matches.py --help` for the complete set of options.

## Development principles

- Choose only from legal actions supplied by the simulator.
- Use state and card semantics rather than opponent names or replay IDs.
- Finish one compatible attacker instead of spreading energy blindly.
- Treat attack selection as a safety invariant.
- Validate challengers against frozen baselines, stress matchups, and broad
  replay-derived deck coverage.

## License and data

No open-source license has been selected yet, so normal copyright applies. Pokémon,
Pokémon TCG, and related names are trademarks of their respective owners. Official
competition files and replay data are governed by Kaggle's and the competition
organizer's terms.
