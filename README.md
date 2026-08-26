# Pokémon TCG AI Battle Agent

A highly optimized, rule-based, state-aware AI decision engine developed for Kaggle's [Pokémon TCG AI Battle Challenge](https://www.kaggle.com/competitions/pokemon-tcg-ai-battle).

This repository documents the evolution of a custom Pokémon Trading Card Game agent from a simple legal-action baseline up to a sophisticated dynamic planning system that manages energy routing, bench composition, hand size, damage immunity, healing loops, and targeted bench gusting.

---

## 🏆 Competition Achievements & Top Agents

*   **V11 Candidate Agent (Peak Leaderboard: 992)**: Reverted to a one-prize defensive *Crustle/Cornerstone* shell. Optimizes bench space (capping search targets to 3 viable lines) and actively scans prize zones to out-resource high-damage, multi-prize opponents.
*   **V18 Candidate Agent (Final Certified Deployment)**: Designed around a *Mega Lopunny ex* high-HP engine supported by *Dudunsparce* card draw. Includes dynamic damage-immunity counters, active pivot support escape, and quad-healing loops using *Wally's Compassion*. Certified locally at a **91.50% Win Rate** across 294 matches.

---

## 📂 Repository Layout

```
├── agents/             # Versioned agent policy implementations and 60-card decks (v1 to v18)
├── artifacts/          # Compact markdown report logs and final submission packages
├── docs/               # Detailed documentation (Agent Lineage, System Architecture, Build Guide)
├── experiments/        # Historical trials, rejected deck profiles, and stress agents
├── tools/              # Local simulators, benchmark evaluations, and submission builders
├── LICENSE             # MIT License
└── README.md           # Repository overview (this file)
```

---

## 🤖 Agent Evolution

Below is the evolution of the agent versions built during the competition:

| Version | Core Architecture | Key Breakthrough / Strategy |
|---|---|---|
| **V1** | Legal Action Baseline | Picks legal actions randomly, acts as the control baseline. |
| **V2** | Action Ranking | Introduces rule tables and action ranking heuristics. |
| **V3** | Multi-Turn Planner | Tracks and powers single attackers rather than spreading energy. |
| **V4** | Crustle/Cornerstone Shell | Employs one-prize stallers with bounded mandatory-attack routines. |
| **V5** | Hand size heuristics | Limits draw sequences against opponent hand disruption. |
| **V6–V8** | Pivot Optimization | Integrates Air Balloon attachments and active position safety. |
| **V9** | Supporter Cycling | Caches and cycles supporter cards using Poké Pad. |
| **V10** | Mega Lopunny ex test | Initial implementation of high-HP offensive sweepers (Mega ex). |
| **V11** | **Peak Stall (992 Rating)** | Return to 1-prize Crustle; adds bench limits and prize-zone checks. |
| **V12–V17** | Immunity & Heals | Introduces Wally healing loops and initial Cornerstone ability counters. |
| **V18** | **Final certified Lopunny** | Pierces damage-immunity with *Spiky Hopper*; quad-Wally heal loop. |

Detailed specifications and local benchmark results for all versions are documented in the [Agent Version History](file:///Users/muhammadomerfarooq/Desktop/GitHub%20Repositories/Pokemon%20Challenge/docs/AGENTS.md).

---

## 🛠️ Getting Started & Usage

### 1. Build a Submission
Submission archives (`.tar.gz`) contain `main.py` and `deck.csv` at the root. You can package any agent version using the build tool:

```bash
python3 tools/build_submission.py \
  --agent-dir agents/v18_candidate \
  --output artifacts/submission_18.tar.gz
```

The builder validates:
*   Standard library constraints (no disk path or external package assumptions).
*   Deck card count (exactly 60 cards).
*   Compilation success.

### 2. Run Local Matches
Test agent policies locally by running matches inside the simulator. Swapping seats ensures balanced evaluation:

```bash
python3 tools/run_local_matches.py \
  --agent-dir agents/v18_candidate \
  --opponent-dir agents/v11_candidate \
  --matches 100 \
  --swap-seats
```

### 3. Evaluate Benchmarks
Verify policies against custom test benches or evaluation decks:

```bash
python3 tools/run_exhaustive_v18_tests.py
```

---

## 📖 Deep Dives

*   For an in-depth walkthrough of the state evaluation engine, action heuristics, and dynamic board scoring, see the [Agent Architecture Guide](file:///Users/muhammadomerfarooq/Desktop/GitHub%20Repositories/Pokemon%20Challenge/docs/ARCHITECTURE.md).
*   For the raw build configurations and older CLI references, see the [V9 Build Guide](file:///Users/muhammadomerfarooq/Desktop/GitHub%20Repositories/Pokemon%20Challenge/docs/V9_BUILD_GUIDE.md).

---

## ⚖️ License

This project is open-sourced under the [MIT License](file:///Users/muhammadomerfarooq/Desktop/GitHub%20Repositories/Pokemon%20Challenge/LICENSE).

*Disclaimer: Pokémon, Pokémon TCG, and character names are trademarks of Nintendo, Game Freak, and The Pokémon Company.*
