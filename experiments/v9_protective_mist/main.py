"""One-change screen: allow threat-aware Mist protection on a ready Active."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_protective_mist_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK
MIST_ID = 11


def _is_protective_mist_option(obs, option):
    if option.get("type") != 8:
        return False
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    opponent_id = _base.card_id(_base.active_card(state, 1 - yi))
    target = _base.target_card(obs, option)
    return (
        _base.card_id(_base.option_card(obs, option)) == MIST_ID
        and option.get("inPlayArea") == 4
        and target is not None
        and opponent_id in _base.MIST_ACTIVE_THREATS
        and not any(
            _base.card_id(energy) == MIST_ID
            for energy in target.get("energyCards") or []
        )
    )


_original_score_attach_or_evolve = _base.score_attach_or_evolve


def score_attach_or_evolve(obs, option):
    if _is_protective_mist_option(obs, option):
        # This exception intentionally precedes the generic fully-paid cutoff:
        # Mist is attached for effect protection, not additional attack cost.
        return 3600.0
    return _original_score_attach_or_evolve(obs, option)


_base.score_attach_or_evolve = score_attach_or_evolve
_original_bounded_setup_choice = _base.bounded_setup_choice


def bounded_setup_choice(obs, ranked):
    options = _base.select_state(obs).get("option") or []
    for _, index in ranked:
        if _is_protective_mist_option(obs, options[index]):
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
