"""Structural screen: Hop's Snorlax plus Hop's Choice Band."""

from __future__ import annotations

import copy
import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_snorlax_band_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

SNORLAX_ID = 304
CHOICE_BAND_ID = 1171
POKE_PAD_ID = 1152
DWEBBLE_ID = 344
CRUSTLE_ID = 345

EXPECTED_DECK = [
    344, 344, 344, 344, 345, 345, 345, 345, 117, 117, 304,
    1086, 1086, 1086, 1152, 1152, 1152, 1152, 1198, 1198, 1198,
    1227, 1227, 1227, 1227, 1197, 1197, 1197, 1235, 1235, 1235,
    1147, 1147, 1147, 1147, 1159, 1171, 18, 18, 18, 18, 11, 11,
    11, 14, 14, 14, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]

DECK = EXPECTED_DECK[:]
_base.EXPECTED_DECK = EXPECTED_DECK
_base.DECK = DECK
_base.POKEMON_ROLE[SNORLAX_ID] = 175.0
_base.BASIC_SETUP_POKEMON.add(SNORLAX_ID)
_base.KO_HP_BY_ATTACKER[SNORLAX_ID] = 200

_original_readiness = _base.readiness


def readiness(card, extra_energy=None, remove_energy_index=None):
    if _base.card_id(card) != SNORLAX_ID:
        return _original_readiness(card, extra_energy, remove_energy_index)

    energy_types = _base.attached_types(card)
    if (
        isinstance(remove_energy_index, int)
        and 0 <= remove_energy_index < len(energy_types)
    ):
        del energy_types[remove_energy_index]
    if extra_energy in _base.ENERGY_CARD_TYPES:
        energy_types.append(_base.ENERGY_CARD_TYPES[extra_energy])
        if extra_energy == 15:
            energy_types.append("RKT")

    has_band = any(
        _base.card_id(tool) == CHOICE_BAND_ID for tool in card.get("tools") or []
    )
    cost = ["C", "C"] if has_band else ["C", "C", "C"]
    damage = 200 if has_band else 170
    missing = _base.cost_missing(cost, energy_types)
    score = damage * 1.2 - missing * 95.0 + len(energy_types) * 8.0
    if missing == 0:
        score += 220.0
    if len(energy_types) > len(cost) + 1:
        score -= 12.0 * (len(energy_types) - len(cost) - 1)
    return {
        "ready": missing == 0,
        "missing": missing,
        "damage": damage,
        "score": score,
    }


_base.readiness = readiness

_original_card_pick_score = _base.card_pick_score


def card_pick_score(obs, cid, area, context):
    score = _original_card_pick_score(obs, cid, area, context)
    if area != 1 or _base.card_id(_base.select_state(obs).get("effect")) != POKE_PAD_ID:
        return score

    state = _base.current_state(obs)
    yi = _base.your_index(state)
    board_ids = {
        _base.card_id(card) for card in _base.board_cards_only(state, yi)
    }
    hand_ids = set(_base.hand_ids(state, yi))
    visible_ids = board_ids | hand_ids

    if DWEBBLE_ID in board_ids and CRUSTLE_ID not in visible_ids:
        if cid == CRUSTLE_ID:
            score += 900.0
        elif cid == SNORLAX_ID:
            score -= 500.0
    elif not ({DWEBBLE_ID, CRUSTLE_ID} & visible_ids):
        if cid == DWEBBLE_ID and len(board_ids) <= 1:
            score += 900.0
        elif cid == SNORLAX_ID and len(board_ids) <= 1:
            score -= 300.0
    return score


_base.card_pick_score = card_pick_score

_original_score_attach_or_evolve = _base.score_attach_or_evolve


def score_attach_or_evolve(obs, option):
    moving = _base.option_card(obs, option)
    if _base.card_id(moving) != CHOICE_BAND_ID:
        return _original_score_attach_or_evolve(obs, option)
    target = _base.target_card(obs, option)
    if _base.card_id(target) != SNORLAX_ID:
        return -5000.0

    before = readiness(target)
    with_band = copy.deepcopy(target)
    with_band.setdefault("tools", []).append({"id": CHOICE_BAND_ID})
    after = readiness(with_band)
    score = 1400.0 + (after["score"] - before["score"]) * 3.0
    if after["ready"] and not before["ready"]:
        score += 1200.0
    state = _base.current_state(obs)
    opponent = _base.active_card(state, 1 - _base.your_index(state))
    opponent_hp = (
        _base.as_int(opponent.get("hp"), 0) if isinstance(opponent, dict) else 0
    )
    if 0 < opponent_hp <= after["damage"]:
        score += 700.0
    return score


_base.score_attach_or_evolve = score_attach_or_evolve

_original_discard_preservation_score = _base.discard_preservation_score


def discard_preservation_score(obs, option):
    value = _original_discard_preservation_score(obs, option)
    if _base.card_id(_base.option_card(obs, option)) != CHOICE_BAND_ID:
        return value
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    has_snorlax = SNORLAX_ID in {
        _base.card_id(card)
        for card in (
            _base.board_cards_only(state, yi)
            + _base.card_list(state, yi, 2, {})
        )
    }
    return 720.0 if has_snorlax else 60.0


_base.discard_preservation_score = discard_preservation_score

_original_bounded_setup_choice = _base.bounded_setup_choice


def bounded_setup_choice(obs, ranked):
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    active = _base.active_card(state, yi)
    opponent = _base.active_card(state, 1 - yi)
    opponent_hp = (
        _base.as_int(opponent.get("hp"), 0) if isinstance(opponent, dict) else 0
    )
    if (
        _base.card_id(active) == SNORLAX_ID
        and 170 < opponent_hp <= 200
        and not any(
            _base.card_id(tool) == CHOICE_BAND_ID
            for tool in active.get("tools") or []
        )
    ):
        options = _base.select_state(obs).get("option") or []
        for _, index in ranked:
            option = options[index]
            if (
                option.get("type") == 8
                and _base.card_id(_base.option_card(obs, option)) == CHOICE_BAND_ID
                and option.get("inPlayArea") == 4
            ):
                return index
    return _original_bounded_setup_choice(obs, ranked)


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
