"""Battle Cage experiment layered on the frozen V9 discard-only policy.

This local experiment deliberately changes one deck slot and one narrow policy
decision.  It imports the comparator so every unrelated choice remains exactly
the same.  A packaged agent would inline the baseline before submission.
"""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_battle_cage_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)


BATTLE_CAGE_ID = 1264

# These IDs were derived from competition_data/EN_Card_Data.csv by selecting
# Pokémon attacks that can place or move damage counters onto an opponent's
# Benched Pokémon.  Costs are included so a visible Active is considered an
# immediate threat only when the relevant attack is actually paid.
BENCH_COUNTER_ATTACK_COSTS = {
    29: (("C",),),                    # Sinistcha ex: Re-Brew
    56: (("C", "C", "C"),),          # Flutter Mane: Hex Hurl
    94: (("G",),),                    # Sinistcha: Cursed Drop
    121: (("R", "P"),),               # Dragapult ex: Phantom Dive
    215: (("P",),),                   # Uxie: Painful Memories
    219: (("P",),),                   # Cofagrigus: Law of the Underworld
    223: (("W", "P", "F"),),          # Palossand ex: Barite Jail
    245: (("P",),),                   # Alakazam: Strange Hacking
    593: (("P", "C"),),               # Cofagrigus: Extended Damagriiigus
    817: (("P",),),                   # Bramblin: Sneaky Placement
    864: (("C", "C"),),               # N's Vanilluxe: Snow Coating
    876: (("P", "C"),),               # Mismagius: Assassin's Magic
    880: (("P", "P", "C"),),          # Spectrier: Phantasmal Barrage
}

# Persistent or immediately usable counter-placement Abilities.  Evolution
# precursors are kept separately below because a visible Duskull or Snorunt can
# evolve and place counters before our next opportunity to play a Stadium.
BENCH_COUNTER_ABILITIES = {
    104,  # Froslass: Freezing Shroud
    112,  # Munkidori: Adrena-Brain
    132,  # Dusclops: Cursed Blast
    133,  # Dusknoir: Cursed Blast
    428,  # Team Rocket's Ampharos: Darkest Impulse
    442,  # Team Rocket's Tyranitar: Sand Stream (while Active)
    457,  # Team Rocket's Golbat: Sneaky Bite
    458,  # Team Rocket's Crobat ex: Biting Spree
    882,  # Team Rocket's Dugtrio: Holes
}

# One-turn-away visible setup for Abilities that can damage the Bench on the
# opponent's next turn.  The relationships come from the CSV Previous stage
# field, rather than from replay identities.
COUNTER_ABILITY_PRECURSORS = {
    103,  # Snorunt -> Froslass
    131,  # Duskull -> Dusclops/Dusknoir
    456,  # Team Rocket's Zubat -> Golbat/Crobat ex
}


EXPECTED_DECK = [
    344, 344, 344, 344, 345, 345, 345, 345, 117, 117, 1086, 1086,
    1086, 1086, 1152, 1152, 1152, 1152, 1198, 1198, 1198, 1227,
    1227, 1227, 1227, 1197, 1197, 1197, 1235, 1235, 1235, 1235,
    1147, 1147, 1147, 1147, 1159, 1264, 18, 18, 18, 18, 11, 11,
    11, 14, 14, 14, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1,
]


def _load_deck():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck.csv")
    try:
        with open(path, encoding="utf-8-sig") as handle:
            deck = [int(line.strip().split(",")[0]) for line in handle if line.strip()]
    except (OSError, ValueError):
        return EXPECTED_DECK[:]
    return deck if deck == EXPECTED_DECK else EXPECTED_DECK[:]


DECK = _load_deck()
_base.EXPECTED_DECK = EXPECTED_DECK
_base.DECK = DECK


def _has_battle_cage(state):
    return any(
        _base.card_id(card) == BATTLE_CAGE_ID
        for card in _base.card_list(state, _base.your_index(state), 7, {})
    )


def _bench(state, player):
    return [card for _, area, _, card in _base.board_cards(state, player) if area == 5]


def _has_paid_attack(card, costs):
    energy_types = _base.attached_types(card)
    return any(_base.cost_missing(list(cost), energy_types) == 0 for cost in costs)


def _ability_bench_is_vulnerable(state, threat_id):
    yi = _base.your_index(state)
    bench = _bench(state, yi)
    if not bench:
        return False
    if threat_id == 104:
        # Freezing Shroud affects only Pokémon with Abilities.
        return any(_base.card_id(card) in _base.ABILITY_POKEMON_IDS for card in bench)
    if threat_id == 428:
        # Darkest Impulse triggers when one of these Benched Basics evolves.
        return any(_base.card_id(card) == 344 for card in bench)
    if threat_id == 442:
        # Sand Stream affects Basic Pokémon during Checkup.
        return any(_base.card_id(card) in _base.BASIC_SETUP_POKEMON for card in bench)
    if threat_id == 882:
        # Holes matters only when the current Active is likely to move to Bench.
        active = _base.active_card(state, yi)
        return isinstance(active, dict) and _base.as_int(active.get("hp"), 0) > 0
    return True


def _visible_counter_threat(obs):
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    opp = 1 - yi
    if not _bench(state, yi):
        return False

    opponent_cards = _base.board_cards_only(state, opp)
    opponent_active = _base.active_card(state, opp)
    active_id = _base.card_id(opponent_active)

    costs = BENCH_COUNTER_ATTACK_COSTS.get(active_id)
    if costs and _has_paid_attack(opponent_active, costs):
        # A few attacks need an existing counter source to make progress.
        if active_id in {245, 864}:
            if not any(
                _base.as_int(card.get("maxHp"), 0) > _base.as_int(card.get("hp"), 0)
                for card in _base.board_cards_only(state, yi)
                if isinstance(card, dict)
            ):
                pass
            else:
                return True
        elif active_id == 593:
            if any(
                _base.as_int(card.get("maxHp"), 0) > _base.as_int(card.get("hp"), 0)
                for card in opponent_cards
                if isinstance(card, dict)
            ):
                return True
        else:
            return True

    for card in opponent_cards:
        threat_id = _base.card_id(card)
        if threat_id in COUNTER_ABILITY_PRECURSORS:
            return True
        if threat_id not in BENCH_COUNTER_ABILITIES:
            continue
        if not _ability_bench_is_vulnerable(state, threat_id):
            continue
        if threat_id == 104:
            return True
        if threat_id == 112:
            # Adrena-Brain requires Darkness Energy and counters to move.
            if not ({"D", "RKT"} & set(_base.attached_types(card))):
                continue
            if not any(
                _base.as_int(source.get("maxHp"), 0) > _base.as_int(source.get("hp"), 0)
                for source in opponent_cards
                if isinstance(source, dict)
            ):
                continue
            return True
        if threat_id == 442 and card is not opponent_active:
            continue
        if threat_id in {457, 458}:
            # Their on-evolution Ability has already resolved once visible.
            continue
        return True
    return False


def should_play_battle_cage(obs):
    state = _base.current_state(obs)
    if _has_battle_cage(state):
        return False
    return _visible_counter_threat(obs)


_original_score_play_from_hand = _base.score_play_from_hand


def score_play_from_hand(obs, option):
    if _base.card_id(_base.option_card(obs, option)) == BATTLE_CAGE_ID:
        return 4200.0 if should_play_battle_cage(obs) else -5000.0
    return _original_score_play_from_hand(obs, option)


_original_discard_preservation_score = _base.discard_preservation_score


def discard_preservation_score(obs, option):
    if _base.card_id(_base.option_card(obs, option)) == BATTLE_CAGE_ID:
        return 1100.0 if should_play_battle_cage(obs) else -250.0
    return _original_discard_preservation_score(obs, option)


_base.score_play_from_hand = score_play_from_hand
_base.discard_preservation_score = discard_preservation_score


def bounded_setup_choice(obs, ranked):
    """Use Cage as one existing bounded deferral, then preserve attack safety."""
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    turn_key = _base.reset_attack_memory(state)
    ps = _base.players(state)
    if yi < len(ps) and _base.as_int(ps[yi].get("deckCount"), 0) == 0:
        return None

    signature = _base.attack_menu_signature(obs)
    seen = _base.ATTACK_MENU_STATES.setdefault(turn_key, set())
    if signature in seen:
        return None
    seen.add(signature)
    if _base.ATTACK_DEFERRALS.get(turn_key, 0) >= _base.MAX_ATTACK_DEFERRALS:
        return None
    if _base.opponent_prize_count(obs) <= 1 or _base.our_prize_count(obs) <= 1:
        return None

    options = _base.select_state(obs).get("option") or []
    if should_play_battle_cage(obs):
        for _, index in ranked:
            option = options[index]
            if (
                option.get("type") == 7
                and _base.card_id(_base.option_card(obs, option)) == BATTLE_CAGE_ID
            ):
                _base.ATTACK_DEFERRALS[turn_key] = (
                    _base.ATTACK_DEFERRALS.get(turn_key, 0) + 1
                )
                return index

    # The baseline helper also owns the same-menu guard.  Remove the signature
    # we just registered so its unchanged logic can evaluate all other setup.
    seen.discard(signature)
    return _original_bounded_setup_choice(obs, ranked)


_original_bounded_setup_choice = _base.bounded_setup_choice
_base.bounded_setup_choice = bounded_setup_choice


def choose_action(obs):
    return _base.choose_action(obs)


def safe_action(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        minimum = _base.as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(select.get("option") or []))))


def agent(obs):
    return safe_action(obs)
