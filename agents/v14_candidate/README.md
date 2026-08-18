# V14 Candidate Agent Architecture & Guide

V14 is built as a bug-free, highly resilient agent for the Kaggle Pokemon TCG AI Battle Challenge.

## Key Improvements Over V13

1. **Anti-Bench-Wipe Safeguard (Bench Protection Invariant)**
   - Identified from V13 loss replays (episodes 91506962 and 91524974) where V13 was knocked out with `bench_count == 0`, causing instant game loss.
   - V14 introduces a top-tier score override (`+25,000.0` priority) for benching Basic Pokémon (Dwebble, Cornerstone Mask Ogerpon ex) and searching via Buddy-Buddy Poffin whenever `bench_count == 0`.
   - Overrides attack deferral limits when `bench_count == 0` so the agent never attacks without a backup benched Pokémon when legal setup actions exist.

2. **Alakazam & Dudunsparce Hand-Control Counter**
   - Alakazam's *Powerful Hand* scales damage counters with opponent hand size.
   - V14 adds Alakazam and Dudunsparce/Dunsparce line to threat profiling.
   - Boosts Xerosic's Machinations (`+1,200.0`) when opponent hand size $\ge 5$ to force hand drop to 3 cards, mitigating high damage counter attacks.
   - Boosts attack targeting priority against Alakazam and Dudunsparce engines (`+500.0`).

3. **Optimized Attacker Readiness & Energy Placement**
   - Refined energy scoring for Crispin and Waitress.
   - Enhanced Grow Grass, Mist, and Spiky Energy placement priority based on opponent threat profile.

4. **Kaggle Loader Safety & Execution Verification**
   - Tested and verified raw-loader execution without `__file__` defined.
   - Exact 60-card deck verification.

## 60-Card Deck Composition

- **Pokémon (10)**: 4x Dwebble, 4x Crustle, 2x Cornerstone Mask Ogerpon ex
- **Items & Tools (13)**: 4x Buddy-Buddy Poffin, 4x Poké Pad, 4x Jumbo Ice Cream, 1x Hero's Cape
- **Supporters (14)**: 3x Crispin, 4x Lillie's Determination, 3x Xerosic's Machinations, 4x Waitress
- **Energy (23)**: 4x Grow Grass Energy, 3x Mist Energy, 3x Spiky Energy, 4x Basic Fighting Energy, 9x Basic Grass Energy
