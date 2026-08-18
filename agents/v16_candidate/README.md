# V16 Candidate Agent: Airtight Meta-Consistent Master

V16 is built as the ultimate, airtight, persistent battle agent for the Kaggle Pokemon TCG AI Battle Challenge.

## Strategic Breakthroughs over V15

1. **Anti-Bench-Wipe Resilience (`bench_count <= 1`)**:
   - Assigns a top-tier priority score boost (`+25,000.0` when `bench_count == 0`, `+18,000.0` when `bench_count == 1`) to play **Buddy-Buddy Poffin (`1086`)**, **Basic Dwebble (`344`)**, or **Cornerstone Mask Ogerpon ex (`117`)** from hand until at least **2 Benched Pokémon** are established.
   - Eliminates single-attacker bench-wipe losses.

2. **Grimmsnarl ex / Munkidori Ability Board Master (Cornerstone Stance & Anti-Retreat Guard)**:
   - Detects Ability-heavy opponent boards (Grimmsnarl ex `743`, Munkidori `343`, Alakazam `678`).
   - Assigns a **`+25,000.0` priority boost** to promote and keep **Cornerstone Mask Ogerpon ex (`117`)** Active against Ability boards (*Cornerstone Stance* blocks 100% of incoming damage from Pokémon with Abilities!).
   - **Strict Anti-Retreat Invariant**: Prevents retreating Cornerstone Ogerpon ex into unprotected Dwebble/Crustle targets when facing Ability-heavy boards.
   - Accelerates Fighting Energy (`6`) and Crispin (`1198`) onto Cornerstone Ogerpon ex to deliver *Demolish* (140 damage 1-shot KO).

3. **Non-EX & Protection-Bypass Attacker Response (Mega Lopunny ex `849` & Crustle Mirror `345`)**:
   - Detects non-ex attackers and bypass-effect attackers (`BYPASS_EFFECT_ATTACKERS` including `849` Mega Lopunny ex).
   - Prioritizes Cornerstone Ogerpon ex promotion and loading (*Demolish* deals 140 damage, 1-shotting non-ex Crustle/Spidops).
   - Boosts **Hero's Cape (`1159`, `+100 HP`)** and **Jumbo Ice Cream (`1147`)** healing (`+2,500.0`) when facing non-ex / bypass attackers to keep attackers out of 1-shot range.

4. **Alakazam ex Hand-Control & 100% Damaging Attack Execution**:
   - Xerosic's Machinations (`1197`, `+3,500.0` when opponent hand $\ge 4$).
   - `+100,000.0` priority boost for legal damaging attacks (0 abandoned attack turns).

## 60-Card Deck Composition

- **Pokémon (10)**: 4x Dwebble, 4x Crustle, 2x Cornerstone Mask Ogerpon ex
- **Items & Tools (13)**: 4x Buddy-Buddy Poffin, 4x Poké Pad, 4x Jumbo Ice Cream, 1x Hero's Cape
- **Supporters (14)**: 3x Crispin, 4x Lillie's Determination, 3x Xerosic's Machinations, 4x Waitress
- **Energy (23)**: 4x Grow Grass Energy, 3x Mist Energy, 3x Spiky Energy, 4x Basic Fighting Energy, 9x Basic Grass Energy
