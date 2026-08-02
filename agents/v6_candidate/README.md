# V6 candidate

V6 preserves V5's attack-safe planner and mixed Crustle/Cornerstone strategy.
It adds three general resilience improvements:

- Poké Pad prefers a Basic setup Pokémon when the board has only one Pokémon,
  Crustle is already in hand, and no benchable setup Pokémon is available.
- The final Cook is replaced by a third Xerosic's Machinations to make bounded
  hand disruption more consistent against large-hand engines.
- During a switch or promotion, a fully powered Cornerstone Mask Ogerpon is
  preferred when its 140-damage attack can immediately knock out the opposing
  Active while Crustle's 120 damage cannot.

Neither rule depends on replay IDs, opponent names, or opponent-specific
runtime branches.
