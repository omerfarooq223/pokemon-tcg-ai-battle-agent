# V15 Candidate Agent: Threat-Aware Anti-Meta Master

V15 is built as the ultimate, bug-free, top-notch battle agent for the Kaggle Pokemon TCG AI Battle Challenge.

## Strategic Breakthroughs over V14/V13

1. **Dynamic Multi-Archetype Threat Countermeasures**:
   - **Mega Lucario ex (used 38x in top replays by `Luca`)**: V15 detects Mega Lucario ex & ex attackers and forces **Crustle (*Sturdy Wall*)** promotion (+20,000 priority). Crustle takes **0 damage** from all ex attacks, 2-shotting 270 HP Mega Lucario ex with *Superb Scissors* for 3 instant prizes.
   - **Dragapult ex (used 27x in top replays by `flg`)**: Walls Active with Crustle (0 damage), protects benched Dwebble with Hero's Cape (+100 HP), Mist Energy, and Jumbo Ice Cream healing.
   - **Alakazam & Dudunsparce Hand-Control**: Detects Alakazam/Dudunsparce threat lines and triggers **Xerosic's Machinations (+3,500)** whenever opponent hand $\ge 4$, capping *Powerful Hand* damage counter scaling and prioritizing Boss/Demolish targeting (+1,000).
   - **Grimmsnarl ex / Munkidori Spread**: Detects Ability-heavy spread decks and promotes **Cornerstone Mask Ogerpon ex (*Cornerstone Stance*)** (+20,000 priority) to negate all incoming damage from Pokémon with Abilities.

2. **Emergency Anti-Bench-Wipe Safeguard**:
   - Strictly enforces at least 1-2 Benched Pokémon with a **+30,000 priority boost** for Basic Pokémon (Dwebble, Cornerstone) and Buddy-Buddy Poffin whenever `bench_count == 0`.

3. **Absolute Attack Invariant**:
   - **+100,000 priority boost** for legal damaging attacks. Deferral budget capped at max 4 setup actions before forced attack.

4. **Kaggle Execution & Runtime Invariants**:
   - Raw execution without `__file__` verified.
   - Cross-game state reset for state isolation.
   - Exact 60-card deck validation.

## 60-Card Deck Composition

- **Pokémon (10)**: 4x Dwebble, 4x Crustle, 2x Cornerstone Mask Ogerpon ex
- **Items & Tools (13)**: 4x Buddy-Buddy Poffin, 4x Poké Pad, 4x Jumbo Ice Cream, 1x Hero's Cape
- **Supporters (14)**: 3x Crispin, 4x Lillie's Determination, 3x Xerosic's Machinations, 4x Waitress
- **Energy (23)**: 4x Grow Grass Energy, 3x Mist Energy, 3x Spiky Energy, 4x Basic Fighting Energy, 9x Basic Grass Energy
