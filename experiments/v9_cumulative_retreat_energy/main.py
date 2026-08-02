"""Cumulative V9 plus colored-cost-aware retreat payment."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "agents", "v9_candidate", "main.py"
    )
)
_SPEC = importlib.util.spec_from_file_location("v9_cumulative_retreat_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the cumulative V9 candidate")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK


def _colored_missing(card, remove_energy_index):
    if not isinstance(card, dict):
        return 99
    attached = _base.attached_types(card)
    if 0 <= remove_energy_index < len(attached):
        del attached[remove_energy_index]
    attacks = _base.ATTACKS.get(_base.card_id(card)) or []
    if not attacks:
        return 0
    return min(
        _base.cost_missing(
            [symbol for symbol in attack.get("cost") or [] if symbol != "C"],
            attached,
        )
        for attack in attacks
    )


def score_retreat_energy(obs, option):
    card = _base.option_card(obs, option)
    energy_index = _base.as_int(option.get("energyIndex"), -1)
    before = _base.readiness(card)
    after = _base.readiness(card, remove_energy_index=energy_index)
    score = 500.0 + (after["score"] - before["score"]) * 2.0
    score -= _colored_missing(card, energy_index) * 1000.0
    energy_cards = card.get("energyCards") or [] if isinstance(card, dict) else []
    removed_id = (
        _base.card_id(energy_cards[energy_index])
        if 0 <= energy_index < len(energy_cards)
        else None
    )
    state = _base.current_state(obs)
    opponent_id = _base.card_id(
        _base.active_card(state, 1 - _base.your_index(state))
    )
    if removed_id == 11 and opponent_id in _base.MIST_ACTIVE_THREATS:
        score -= 700.0
    if removed_id == 18 and _base.card_id(card) in {344, 345}:
        score -= 350.0
    return score


_original_score_option = _base.score_option


def score_option(obs, option):
    if option.get("type") == 6 and _base.select_state(obs).get("context") == 30:
        return score_retreat_energy(obs, option)
    return _original_score_option(obs, option)


_base.score_option = score_option


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
