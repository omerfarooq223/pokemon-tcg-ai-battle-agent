"""Experimental V5 overlay for replay-suite generalization checks.

This imports the frozen V5 candidate and changes only two state-driven scores.
It is intentionally not a submission source; successful changes are copied
into agents/v5_candidate/main.py only after the full regression gates pass.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "agents" / "v5_candidate" / "main.py"
SPEC = importlib.util.spec_from_file_location("v5_replay_candidate_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


_base_score_play_from_hand = BASE.score_play_from_hand
_base_score_attach_or_evolve = BASE.score_attach_or_evolve


def score_play_from_hand(obs, option):
    score = _base_score_play_from_hand(obs, option)
    state = BASE.current_state(obs)
    yi = BASE.your_index(state)
    cid = BASE.card_id(BASE.option_card(obs, option))
    board_size = len(BASE.board_cards(state, yi))

    # A lone Active is a universal early-loss risk. Poffin is the most
    # efficient insurance in this deck; a Basic from hand is the fallback.
    if board_size == 1 and cid == 1086:
        score += 1600.0
    elif board_size == 1 and cid in BASE.BASIC_SETUP_POKEMON:
        score += 900.0
    elif board_size == 2 and cid == 1086:
        score += 320.0
    return score


def score_attach_or_evolve(obs, option):
    moving = BASE.option_card(obs, option)
    target = BASE.target_card(obs, option)
    cid = BASE.card_id(moving)
    if cid in BASE.ENERGY_CARDS and isinstance(target, dict):
        attacks = BASE.ATTACKS.get(target.get("id")) or []
        before = BASE.readiness(target)
        useful_cost = max(
            (len(attack.get("cost") or []) for attack in attacks),
            default=None,
        )
        if (
            before["ready"]
            and useful_cost is not None
            and len(BASE.attached_types(target)) >= useful_cost
        ):
            return -1800.0
    return _base_score_attach_or_evolve(obs, option)


BASE.score_play_from_hand = score_play_from_hand
BASE.score_attach_or_evolve = score_attach_or_evolve

agent = BASE.agent
