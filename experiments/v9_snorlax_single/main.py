"""Structural screen: one Hop's Snorlax replacing one late-game Poffin."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_snorlax_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

SNORLAX_ID = 304
POKE_PAD_ID = 1152
DWEBBLE_ID = 344
CRUSTLE_ID = 345

EXPECTED_DECK = [
    344, 344, 344, 344, 345, 345, 345, 345, 117, 117, 304,
    1086, 1086, 1086, 1152, 1152, 1152, 1152, 1198, 1198, 1198,
    1227, 1227, 1227, 1227, 1197, 1197, 1197, 1235, 1235, 1235,
    1235, 1147, 1147, 1147, 1147, 1159, 18, 18, 18, 18, 11, 11,
    11, 14, 14, 14, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]

DECK = EXPECTED_DECK[:]
_base.EXPECTED_DECK = EXPECTED_DECK
_base.DECK = DECK
_base.ATTACKS[SNORLAX_ID] = [
    {"cost": ["C", "C", "C"], "damage": 170, "name": "Dynamic Press"},
]
_base.POKEMON_ROLE[SNORLAX_ID] = 155.0
_base.BASIC_SETUP_POKEMON.add(SNORLAX_ID)
_base.KO_HP_BY_ATTACKER[SNORLAX_ID] = 170

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

    if DWEBBLE_ID in board_ids and CRUSTLE_ID not in board_ids | hand_ids:
        if cid == CRUSTLE_ID:
            score += 900.0
        elif cid == SNORLAX_ID:
            score -= 500.0
    elif not ({DWEBBLE_ID, CRUSTLE_ID} & (board_ids | hand_ids)):
        if cid == DWEBBLE_ID and len(board_ids) <= 1:
            score += 900.0
        elif cid == SNORLAX_ID and len(board_ids) <= 1:
            score -= 300.0
    return score


_base.card_pick_score = card_pick_score


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
