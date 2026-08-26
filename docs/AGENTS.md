# Agent Version Lineage & Performance Summary

This document describes the design goals, historical breakthroughs, and validation results across the primary agent iterations developed for the Kaggle Pokémon TCG AI Battle Challenge.

---

## Performance Overview

*   **V11 Candidate Agent**: **Peak Leaderboard Rating of 992**. Utilized a one-prize Crustle/Cornerstone defensive stall and counter-attacker engine. Proven highly resilient against diverse meta matchups.
*   **V18 Candidate Agent (Grandmaster)**: **Final Certified Deployment**. Designed around a Mega Lopunny ex (330 HP) high-HP offensive list with dynamic damage-immunity counters and healing loops. Passed extensive local stress test certification at **91.50% Win Rate** across 294 matches.

---

## Agent Version History

### V1 to V3: The Foundations
*   **V1 (Active baseline)**: Basic legal-action execution with minimal heuristics. Rejects obviously illegal turns but lacks long-term strategy.
*   **V2 (Challenger)**: Introduced generic action-ranking tables alongside a small replay-trained sequence tie-breaker.
*   **V3 (Planner)**: Implemented state-aware, multi-turn card, attacker, and energy placement planners. Stopped spreading energy blindly and prioritized powering single active/benched attackers.

### V4 to V8: Crustle/Cornerstone Shell Refinements
*   **V4 (Attack Fix)**: Introduction of the Crustle/Cornerstone lineup. Added a bounded setup routine to ensure active/benched attackers strike as soon as energy thresholds are met.
*   **V5 (Candidate)**: Introduced hand size control heuristics to optimize drawing card actions against opponent disruption.
*   **V6 to V8**: Iterative patches focusing on retreat logic, tool attachments (like Air Balloon), and defensive safety invariants.

### V9 to V11: One-Prize Peak Performance (Rating: 992)
*   **V9 (Candidate)**: Major restructuring of search target logic (Buddy-Buddy Poffin, Ultra Ball) and optimized Poké Pad targets to cycle card-drawing Supporters.
*   **V10 (Candidate)**: Attempted to transition to a high-prize Mega Lopunny ex engine, but suffered from benchmark regressions against spread attackers.
*   **V11 (Peak Agent - 992 Leaderboard Rating)**:
    *   **Return to Core**: Reverted to the proven, robust one-prize Crustle/Cornerstone list.
    *   **Bench Management**: Controlled Buddy-Buddy Poffin and bench expansion (capped at 3 viable attacker lines) to prevent board flooding or bench space starvation.
    *   **Prize-Aware Logic**: Replaced historical zone counts with direct simulator prize-zone scanning to optimize gusting and setup.
    *   **Local Win Rate**: Stood even (50-50) against historical peak V5 snapshots while achieving 90%+ win rates against Lucario and Ogerpon stress decks.

### V12 to V18: Advanced Tactics & Lopunny ex Mastery
*   **V12 to V17 Candidates**: Explored refined energy acceleration, damage immunity detection (evaluating Cornerstone/Crustle abilities), and healing routines using Wally's Compassion.
*   **V18 Candidate (Final Certified Agent)**:
    *   **Mega Lopunny ex Core**: 3-prize high-HP line powered by Dudunsparce card-draw engine.
    *   **Universal Damage-Immunity Recognition**: Scans defender abilities (Crustle, Cornerstone, Mimikyu) and Stadiums (Neutralization Zone). Under immunity, bypasses traditional attacks to prioritize *Spiky Hopper* (160 damage) which ignores all defensive effects.
    *   **Active Support Escape**: Automatically retreats unpowered support basics (Dunsparce, Fan Rotom) using Air Balloon or single energy attachments to activate a powered Lopunny.
    *   **Gusting Finishers**: Uses Boss's Orders to gust and knockout damaged high-prize targets on the opponent's bench.
    *   **Grandmaster Stress Test**: Certified over 294 matches with a **91.50% Win Rate** overall, demonstrating absolute reliability and sub-100MB RAM usage.
