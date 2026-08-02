"""Local one-change screen for the single-board Poké Pad target bug."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_pokepad_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK
_original_card_pick_score = _base.card_pick_score


def card_pick_score(obs, cid, area, context):
    score = _original_card_pick_score(obs, cid, area, context)
    if area != 1 or cid != 344:
        return score

    state = _base.current_state(obs)
    yi = _base.your_index(state)
    select = _base.select_state(obs)
    if _base.card_id(select.get("effect")) != 1152:
        return score

    board = _base.board_cards_only(state, yi)
    visible_ids = {
        _base.card_id(card)
        for card in board + _base.card_list(state, yi, 2, {})
    }
    offered_ids = {
        _base.card_id(card)
        for card in (select.get("deck") or [])
        if isinstance(card, dict)
    }
    if (
        len(board) == 1
        and 344 not in visible_ids
        and 345 not in visible_ids
        and {344, 345}.issubset(offered_ids)
    ):
        # Crustle cannot be played without Dwebble.  Establish the missing
        # evolution line instead of taking an unusable Stage 1 into a
        # one-Pokémon board.
        score += 900.0
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
