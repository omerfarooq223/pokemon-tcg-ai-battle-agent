"""Energy-cap plus special-Energy semantics experiment on frozen V5."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "agents" / "v5_candidate" / "main.py"
SPEC = importlib.util.spec_from_file_location(
    "v5_energy_semantics_candidate_base", BASE_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

_base_score_attach_or_evolve = BASE.score_attach_or_evolve

# Pokémon whose attacks place/move damage counters, cause delayed effects, or
# impose attack effects that Mist Energy can prevent.  These are card-mechanic
# profiles from the supplied English card data, not replay/opponent identifiers.
MIST_ACTIVE_THREATS = {
    29,
    32,
    56,
    94,
    121,
    215,
    219,
    223,
    245,
    247,
    432,
    455,
    593,
    738,
    743,
    817,
    864,
    876,
    880,
    982,
    1058,
}


def colored_requirements_paid(card):
    attached = BASE.attached_types(card)
    attacks = BASE.ATTACKS.get(BASE.card_id(card)) or []
    for attack in attacks:
        colored_cost = [
            symbol for symbol in attack.get("cost") or [] if symbol != "C"
        ]
        if BASE.cost_missing(colored_cost, attached) == 0:
            return True
    return not attacks


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

    score = _base_score_attach_or_evolve(obs, option)
    if cid not in BASE.ENERGY_CARDS or not isinstance(target, dict):
        return score

    target_id = BASE.card_id(target)
    target_area = option.get("inPlayArea")
    if cid == 18 and target_id in {344, 345}:
        # Grow Grass both satisfies the line's Grass requirement and preserves
        # its +20 HP through evolution.
        score += 220.0

    state = BASE.current_state(obs)
    opp = 1 - BASE.your_index(state)
    opponent_active = BASE.active_card(state, opp)
    opponent_id = BASE.card_id(opponent_active)
    colored_paid = colored_requirements_paid(target)
    if (
        cid == 11
        and target_area == 4
        and colored_paid
        and opponent_id in MIST_ACTIVE_THREATS
    ):
        score += 1050.0
    elif (
        cid == 14
        and target_area == 4
        and colored_paid
        and opponent_id not in MIST_ACTIVE_THREATS
    ):
        score += 190.0
    return score


BASE.score_attach_or_evolve = score_attach_or_evolve
agent = BASE.agent
