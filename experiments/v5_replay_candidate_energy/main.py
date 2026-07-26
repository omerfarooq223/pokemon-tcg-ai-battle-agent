"""Ready-attacker overattachment experiment on top of frozen V5."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "agents" / "v5_candidate" / "main.py"
SPEC = importlib.util.spec_from_file_location("v5_energy_candidate_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

_base_score_attach_or_evolve = BASE.score_attach_or_evolve


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


BASE.score_attach_or_evolve = score_attach_or_evolve
agent = BASE.agent
