"""Poffin/Basic board-insurance experiment on top of frozen V5."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "agents" / "v5_candidate" / "main.py"
SPEC = importlib.util.spec_from_file_location("v5_poffin_candidate_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

_base_score_play_from_hand = BASE.score_play_from_hand


def score_play_from_hand(obs, option):
    score = _base_score_play_from_hand(obs, option)
    state = BASE.current_state(obs)
    yi = BASE.your_index(state)
    cid = BASE.card_id(BASE.option_card(obs, option))
    board_size = len(BASE.board_cards(state, yi))
    if board_size == 1 and cid == 1086:
        score += 1600.0
    elif board_size == 1 and cid in BASE.BASIC_SETUP_POKEMON:
        score += 900.0
    elif board_size == 2 and cid == 1086:
        score += 320.0
    return score


BASE.score_play_from_hand = score_play_from_hand
agent = BASE.agent
