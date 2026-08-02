# V9 policy semantics audit 2

Scope: read-only audit of the current `agents/v9_candidate/main.py` (the
discard-only V7-derived policy). No match batch was run. Evidence comes from
the official local API schema and saved V6/V7 replays using the exact V9 deck.

## Ranked findings

### 1. High confidence: the attachment cap disables the intended Mist protection

The early return in `score_attach_or_evolve` (`main.py` lines 706-713) fires
before the threat-aware Mist branch (lines 727-740). Any Pokémon considered
attack-ready is assigned `-1800` for another Energy attachment, including a
legal Mist attachment that would prevent an effect attack. The hard
attack-safety whitelist compounds this: `bounded_setup_choice` allows a
pre-attack Energy attachment only to an unready **Benched** Pokémon
(lines 1253-1259), never a protective attachment to the Active.

This contradicts the policy's stated Mist intent and has direct live evidence:

- In V7 loss **88483285**, turn 12, the Active Dwebble had one Grass Energy,
  Mist was in hand, and opposing Alakazam (card 743) was Active. Mist-to-Active
  and Ascension were both legal.
- Mist-to-Active scored `-1800`. The policy instead evolved a Benched Dwebble,
  used Poké Pad, attached Grow Grass to the Bench, then used Ascension.
- Mist would have remained attached through Ascension and prevented Powerful
  Hand's damage-counter effect unless removed later.
- The replay ended as an Alakazam board-exhaustion loss; Alakazam finished with
  an 18-card hand and Powerful Hand reached 220-480 counters.

An exact-deck V6/V7 replay scan found **8** ready-Active + Mist-in-hand +
profiled-effect-attacker menu states. Episode 88483285 is the clearest causal
loss example; episode 88409367 exposed the same Dwebble/Alakazam menu in a win.

**One-change experiment:** add a narrow `protective_active_attachment` rule:
allow exactly one Mist-to-Active action before an attack when (a) the opposing
Active is in `MIST_ACTIVE_THREATS`, (b) our Active has no Mist currently
attached, and (c) the option is legal. Evaluate this exception before the
fully-paid cutoff and whitelist only that option in `bounded_setup_choice`.
Do not broadly exempt Spiky/Grow Grass or arbitrary over-attachment.

### 2. High confidence: retreat Energy selection is an unscored option type

The official API defines context 30 (`DISCARD_ENERGY`) with option type 6
(`ENERGY`). `score_option` only routes type 5 (`ENERGY_CARD`) through
`score_energy_source`; type 6 receives the same flat score for every attached
Energy. Stable tie-breaking therefore always pays retreat with `energyIndex 0`.

Exact-deck V6/V7 evidence:

- 29 observed context-30 selections; 12 exposed more than one Energy option.
- In Cornerstone states `[Fighting, Colorless]`, the policy discarded the only
  Fighting Energy first in episodes **88468139**, **88459353**, **88453474**,
  and **88480304**.
- The first two of those episodes were losses. This does not prove the retreat
  payment alone caused either loss, but the choice is mechanically dominated:
  discarding Colorless preserves Demolish's colored requirement.

**One-change experiment:** route context-30/type-6 options through a
retreat-payment scorer that removes the indicated `energyIndex` and maximizes
post-payment colored-cost readiness. Validate special-Energy indexing and
multi-step Crustle retreats.

### 3. High confidence but low observed exposure: discard preservation covers
only one of two discard-card contexts

`discard_preservation_score` is gated on `context == 8` (lines 810-815). The
official API separately defines context 29,
`DISCARD_CARD_OR_ATTACHED_CARD`. A hand-card option in context 29 therefore
falls back to positive `card_pick_score`, recreating the exact inversion fixed
for context 8: the most valuable card is ranked highest to be discarded.

No context-29 menu occurred for the exact V9 deck in the saved V6/V7 sample,
so this is a forward-robustness fix rather than a replay-derived loss fix.

**One-change experiment:** extend hand-card preservation to contexts `{8, 29}`
when the option belongs to us and is in our hand. Keep the existing type-5
attached-Energy scorer for attached cards; do not assume all context-29
options are hand cards.

### 4. Medium-high confidence: "fully paid" is wrong for an unevolved Dwebble

At one Energy, Dwebble is ready to use Ascension, so the generic fully-paid
cutoff assigns every additional manual Energy attachment to it `-1800`.
However, Energy remains attached after Ascension and Crustle needs three
Energy. This prevents useful pre-evolution acceleration and can delay Superb
Scissors by a turn.

The exact-deck V6/V7 scan found **74 replay menu snapshots** where Active
Dwebble had one Energy, Ascension was legal, and a further manual Active
attachment was legal; every Energy attachment to that Dwebble scored `-1800`.
The snapshots span both wins and losses, so the broad effect needs controlled
testing rather than being assumed beneficial.

**One-change experiment:** make the cap evolution-aware for Dwebble only:
evaluate its attached Energy against Crustle's `{G}{C}{C}` cost, prefer Grass /
Grow Grass, cap at three total Energy, and permit at most one such Active
attachment before Ascension. This is a cohesive rule, not an opponent-specific
branch.

### 5. Medium confidence: setup always promotes Cornerstone over Dwebble

Setup Active selection uses generic `POKEMON_ROLE`, so Cornerstone (170)
always outranks Dwebble (42). In the exact-deck V6/V7 corpus, both were
available in eight opening hands; the policy chose Cornerstone all eight times
and those games finished 3-5. The sample is small and confounded, but the
mechanism is strategically suspect: Dwebble can attach and Ascend immediately
when going second, whereas Cornerstone takes three Energy to attack.

**One-change experiment:** prefer Dwebble as the opening Active when both are
available, while benching Cornerstone. Test this separately from the
go-second rule so their effects are identifiable. Preserve an exception only
if a future observable setup signal genuinely establishes a better wall; do
not key on opponent identity.

### 6. Medium confidence: the hard attack guard blocks all tactical retreats

Whenever any attack is legal, `choose_action` calls `bounded_setup_choice`;
that whitelist has no retreat action, so the policy must attack. It cannot
retreat first to a better ready attacker even when the current Active will be
Knocked Out during Checkup or cannot interact effectively.

The supplied V8 losses **88527351** and **88727264** provide concrete
Froslass evidence: the Active attacker was guaranteed to self-KO from
Checkup counters while a ready replacement was on the Bench. This finding is
already covered by the separate narrow Froslass-retreat experiment and should
not be broadened without strong regression testing.

**One-change experiment:** retain the narrow, state-driven retreat gate:
only before attack when Checkup guarantees the Active's KO, a ready Benched
attacker survives the same Checkup, and the current attack does not take the
final prize. Avoid a generic "retreat if bench scores higher" rule.

## Confirmed items that do not need another broad change

- Context 38 (`DRAW_COUNT`) is a real tie bug: options are numeric and the old
  policy selects zero. The existing mulligan-compensation experiment correctly
  selects the maximum free draw.
- Context 21 (`ATTACH_FROM`) does receive the selected Energy as
  `contextCard` in saved replays despite the API comment saying it is only sent
  for Activate. The current Crispin/Waitress target scorer can therefore see
  the Energy type; this is not a bug.
- Context 22 Crispin sequencing is correct: context 7 first selects one Basic
  Energy into hand, context 22 selects a different Basic Energy to attach,
  then context 21 chooses its Pokémon target.
- The missing `prizeCount` field is a real schema mismatch (`prize` is the
  official field), but prior isolated experiments were neutral/negative. Treat
  it as known technical debt rather than reopening it during final convergence.

## Suggested evaluation order

1. Protective Mist exception.
2. Context-30 retreat Energy scoring.
3. Context-29 discard extension (synthetic invariants first).
4. Evolution-aware Dwebble attachment.
5. Dwebble opening-Active preference.
6. Keep tactical retreat narrow and validate the already-built experiment.

Each should be tested separately against the current cumulative candidate,
then against V7, Alakazam, Grimmsnarl/Froslass, and the full replay suite. The
first two are the strongest combination of semantic correctness and observed
live exposure.
