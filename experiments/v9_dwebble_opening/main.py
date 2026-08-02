"""One-change screen: open Dwebble over Cornerstone when both are available."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_dwebble_opening_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK
_original_card_pick_score = _base.card_pick_score


def card_pick_score(obs, cid, area, context):
    score = _original_card_pick_score(obs, cid, area, context)
    if context != 1 or area != 2 or cid != 344:
        return score
    option_ids = {
        _base.card_id(_base.option_card(obs, option))
        for option in _base.select_state(obs).get("option") or []
    }
    if {117, 344}.issubset(option_ids):
        # Dwebble can attack with Ascension immediately when going second and
        # keeps Cornerstone available as the complementary Bench wall.
        score += 320.0
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
