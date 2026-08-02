"""One-change screen: prepare Crustle before using Dwebble's Ascension."""

from __future__ import annotations

import copy
import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_dwebble_accel_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK
DWEBBLE_ID = 344
CRUSTLE_ID = 345


def _active_dwebble_energy_option(obs, option):
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    target = _base.target_card(obs, option)
    return (
        option.get("type") == 8
        and _base.card_id(_base.option_card(obs, option)) in _base.ENERGY_CARDS
        and option.get("inPlayArea") == 4
        and _base.card_id(target) == DWEBBLE_ID
        and len(_base.attached_types(target)) < 3
        and not bool(state.get("energyAttached"))
    )


_original_score_attach_or_evolve = _base.score_attach_or_evolve


def score_attach_or_evolve(obs, option):
    if not _active_dwebble_energy_option(obs, option):
        return _original_score_attach_or_evolve(obs, option)

    energy_id = _base.card_id(_base.option_card(obs, option))
    target = _base.target_card(obs, option)
    evolved = copy.deepcopy(target)
    evolved["id"] = CRUSTLE_ID
    before = _base.readiness(evolved)
    after = _base.readiness(evolved, extra_energy=energy_id)
    score = 1300.0 + (after["score"] - before["score"]) * 3.0
    if after["ready"] and not before["ready"]:
        score += 900.0
    elif after["missing"] == 1:
        score += 450.0
    if energy_id == 18:
        score += 260.0
    elif energy_id == 1:
        score += 160.0
    return score


_base.score_attach_or_evolve = score_attach_or_evolve
_original_bounded_setup_choice = _base.bounded_setup_choice


def bounded_setup_choice(obs, ranked):
    options = _base.select_state(obs).get("option") or []
    for _, index in ranked:
        if _active_dwebble_energy_option(obs, options[index]):
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
