"""Cumulative V9 plus a narrow, non-regressive Froslass escape screen."""

from __future__ import annotations

import importlib.util
import os


_BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "agents", "v9_candidate", "main.py"
    )
)
_SPEC = importlib.util.spec_from_file_location("v9_cumulative_froslass_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the cumulative V9 candidate")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK


def should_escape_froslass_checkup(obs):
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    if bool(state.get("retreated")):
        return False
    opponent = 1 - yi
    froslass_count = sum(
        _base.card_id(card) == 104
        for _, _, _, card in _base.board_cards(state, opponent)
    )
    if froslass_count <= 0:
        return False
    active = _base.active_card(state, yi)
    if (
        not isinstance(active, dict)
        or _base.card_id(active) not in _base.ABILITY_POKEMON_IDS
    ):
        return False
    checkup_damage = 10 * froslass_count
    if _base.as_int(active.get("hp"), 0) > checkup_damage:
        return False

    target = _base.active_card(state, opponent)
    if isinstance(target, dict):
        target_hp = _base.as_int(target.get("hp"), 0)
        active_damage = _base.readiness(active)["damage"]
        prize_value = 2 if _base.card_id(target) in _base.EX_POKEMON else 1
        players = _base.players(state)
        own_remaining = 6
        if yi < len(players) and isinstance(players[yi].get("prize"), list):
            own_remaining = len(players[yi]["prize"])
        if (
            target_hp > 0
            and active_damage >= target_hp
            and own_remaining <= prize_value
        ):
            return False

    active_damage = _base.readiness(active)["damage"]
    for card in _base.card_list(state, yi, 5, {}):
        candidate = _base.readiness(card)
        if not isinstance(card, dict) or not candidate["ready"]:
            continue
        candidate_checkup = (
            checkup_damage
            if _base.card_id(card) in _base.ABILITY_POKEMON_IDS
            else 0
        )
        if (
            _base.as_int(card.get("hp"), 0) > candidate_checkup
            and candidate["damage"] >= active_damage
        ):
            return True
    return False


_original_bounded_setup_choice = _base.bounded_setup_choice


def bounded_setup_choice(obs, ranked):
    if should_escape_froslass_checkup(obs):
        options = _base.select_state(obs).get("option") or []
        for _, index in ranked:
            if options[index].get("type") == 12:
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
