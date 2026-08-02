"""Deck-specific, state-driven pilots for the V10 top-five stress league.

The project already has a broad card-semantic planner in the Grimmsnarl stress
agent.  These pilots load an independent instance of that planner, replace its
deck profile, and add deck-specific sequencing without using replay IDs, team
names, or opponent identities at runtime.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_SOURCE = ROOT / "experiments" / "stress_agents" / "grimmsnarl" / "main.py"


PROFILES = {
    "lucario_race": {
        "energy": {6: "F"},
        "attacks": {
            673: [
                {"cost": ["F"], "damage": 10, "name": "Corkscrew Punch"},
                {"cost": ["F", "F"], "damage": 30, "name": "Confront"},
            ],
            674: [{"cost": ["F", "F", "F"], "damage": 210, "name": "Wild Press"}],
            675: [{"cost": ["F", "F"], "damage": 50, "name": "Power Gem"}],
            676: [{"cost": ["F"], "damage": 70, "name": "Cosmic Beam"}],
            677: [{"cost": ["F"], "damage": 30, "name": "Accelerating Stab"}],
            678: [
                {"cost": ["F"], "damage": 130, "name": "Aura Jab"},
                {"cost": ["F", "F"], "damage": 270, "name": "Mega Brave"},
            ],
        },
        "roles": {673: 280.0, 674: 430.0, 675: 350.0, 676: 370.0, 677: 500.0, 678: 650.0},
        "basics": {673, 675, 676, 677},
        "abilities": {674, 675},
        "draw_search": {1102, 1123, 1142, 1152, 1182, 1192, 1227},
        "safe_setup": {1102, 1141, 1142, 1152, 1182, 1192, 1227, 1252},
        "attack_deferrals": 4,
    },
    "crustle_control": {
        "energy": {1: "G", 11: "C", 14: "C", 18: "G", 20: "F"},
        "attacks": {
            117: [{"cost": ["F", "C", "C"], "damage": 140, "name": "Demolish"}],
            344: [{"cost": ["C"], "damage": 0, "name": "Ascension"}],
            345: [{"cost": ["G", "C", "C"], "damage": 120, "name": "Superb Scissors"}],
            756: [{"cost": ["C", "C", "C"], "damage": 200, "name": "Rapid-Fire Combo"}],
        },
        "roles": {344: 270.0, 345: 390.0, 117: 350.0, 756: 330.0},
        "basics": {344, 117, 756},
        "abilities": {756},
        "draw_search": {1086, 1121, 1122, 1152, 1194, 1219, 1225, 1227},
        "safe_setup": {1086, 1121, 1122, 1152, 1194, 1219, 1225, 1227, 1257, 1264},
        "attack_deferrals": 3,
    },
    "ogerpon_engine": {
        "energy": {1: "G", 18: "G"},
        "attacks": {
            96: [{"cost": ["G", "G", "G"], "damage": 90, "name": "Myriad Leaf Shower"}],
        },
        "roles": {96: 520.0},
        "basics": {96},
        "abilities": {96},
        "draw_search": {1094, 1118, 1119, 1122, 1127, 1213, 1227},
        "safe_setup": {1094, 1118, 1119, 1122, 1127, 1213, 1227, 1251},
        "attack_deferrals": 4,
    },
    "grimmsnarl_spread": {
        "energy": {7: "D"},
        "attacks": {
            104: [{"cost": ["W", "C"], "damage": 60, "name": "Frost Smash"}],
            112: [{"cost": ["P", "C"], "damage": 60, "name": "Mind Bend"}],
            646: [
                {"cost": ["C"], "damage": 0, "name": "Filch"},
                {"cost": ["D"], "damage": 10, "name": "Corkscrew Punch"},
            ],
            647: [{"cost": ["D", "D"], "damage": 60, "name": "Corkscrew Punch"}],
            648: [{"cost": ["D", "D"], "damage": 180, "name": "Shadow Bullet"}],
            860: [{"cost": ["W"], "damage": 10, "name": "Chilly"}],
        },
        "roles": {646: 330.0, 647: 390.0, 648: 560.0, 112: 440.0, 860: 250.0, 104: 410.0},
        "basics": {646, 112, 860},
        "abilities": {104, 112, 648},
        "draw_search": {1079, 1080, 1086, 1097, 1122, 1152, 1219, 1227, 1231, 1259},
        "safe_setup": {1079, 1086, 1097, 1122, 1152, 1219, 1227, 1231, 1259},
        "attack_deferrals": 4,
    },
    "area_zero_toolbox": {
        "energy": {1: "G", 3: "W", 4: "L", 5: "P", 6: "F"},
        "attacks": {
            63: [
                {"cost": ["C"], "damage": 0, "name": "Burst Roar"},
                {"cost": ["L", "F"], "damage": 140, "name": "Bellowing Thunder"},
            ],
            96: [{"cost": ["G", "G", "G"], "damage": 90, "name": "Myriad Leaf Shower"}],
            108: [
                {"cost": ["C"], "damage": 20, "name": "Sob"},
                {"cost": ["W", "C", "C"], "damage": 100, "name": "Torrential Pump"},
            ],
            140: [{"cost": ["C", "C", "C"], "damage": 100, "name": "Cruel Arrow"}],
            184: [{"cost": ["P", "P", "C"], "damage": 200, "name": "Eon Blade"}],
            272: [{"cost": ["P", "C"], "damage": 80, "name": "Full Moon Rondo"}],
            756: [{"cost": ["C", "C", "C"], "damage": 200, "name": "Rapid-Fire Combo"}],
            978: [{"cost": ["F", "C"], "damage": 120, "name": "Coordinated Throwing"}],
            1071: [{"cost": ["C", "C", "C"], "damage": 60, "name": "Tuck Tail"}],
        },
        "roles": {
            63: 360.0,
            96: 420.0,
            108: 360.0,
            140: 260.0,
            184: 340.0,
            272: 270.0,
            756: 410.0,
            978: 220.0,
            1071: 320.0,
        },
        "basics": {63, 96, 108, 140, 184, 272, 756, 978, 1071},
        "abilities": {96, 140, 184, 756, 1071},
        "draw_search": {1097, 1098, 1116, 1121, 1182, 1197, 1198, 1205, 1227, 1250},
        # Energy Switch is valuable during setup but is not attack-safe: its
        # source selection can remove the only Energy from the Active.
        "safe_setup": {1097, 1098, 1121, 1198, 1205, 1227, 1250},
        "attack_deferrals": 5,
    },
}


def _load_base(tag: str):
    spec = importlib.util.spec_from_file_location(f"_v10_top5_base_{tag}_{id(tag)}", BASE_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {BASE_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(profile_name: str, deck: list[int]):
    """Return an independently configured semantic planner module."""

    profile = PROFILES[profile_name]
    base = _load_base(profile_name)
    base.DECK = list(deck)
    base.ENERGY_CARD_TYPES = dict(profile["energy"])
    base.ENERGY_CARDS = set(profile["energy"])
    base.ATTACKS = dict(profile["attacks"])
    base.POKEMON_ROLE = dict(profile["roles"])
    base.BASIC_SETUP_POKEMON = set(profile["basics"])
    base.ABILITY_POKEMON = set(profile["abilities"])
    base.DRAW_SEARCH_CARDS = set(profile["draw_search"])
    base.MAX_ATTACK_DEFERRALS = int(profile["attack_deferrals"])
    base.ATTACK_DEFERRALS.clear()
    base.ATTACK_MENU_STATES.clear()
    base.LAST_TURN_SEEN = None

    original_score_option = base.score_option
    def board_ids(state, player):
        return [base.card_id(card) for _, _, _, card in base.board_cards(state, player)]

    def missing_stage_targets(state, yi):
        ids = board_ids(state, yi)
        hand = base.hand_ids(state, yi)
        if profile_name == "crustle_control":
            return {345} if 344 in ids and 345 not in ids else ({344} if 344 not in ids else set())
        if profile_name == "grimmsnarl_spread":
            wanted = set()
            if 646 in ids and not ({647, 648} & set(ids)):
                wanted.update((647, 648))
            if 647 in ids:
                wanted.add(648)
            if 860 in ids and 104 not in ids:
                wanted.add(104)
            if not wanted and not ({646, 647, 648} & set(ids)):
                wanted.add(646)
            return wanted
        if profile_name == "ogerpon_engine":
            return {96} if ids.count(96) < min(4, 1 + len(ids)) else set()
        if profile_name == "area_zero_toolbox":
            wanted = set()
            if 184 not in ids:
                wanted.add(184)
            if 756 not in ids:
                wanted.add(756)
            if 96 not in ids and 1 in hand:
                wanted.add(96)
            if 1071 not in ids:
                wanted.add(1071)
            return wanted
        return set()

    def preservation_value(cid, state, yi):
        roles = profile["roles"]
        value = roles.get(cid, 0.0)
        if cid in profile["energy"]:
            value += 260.0
            best = base.best_board_readiness(state, yi)
            if best and not best[4]["ready"]:
                value += 360.0
        if cid in profile["draw_search"]:
            value += 180.0
        if cid in {1182, 1197, 1198, 1205, 1219, 1225, 1227, 1231}:
            value += 180.0
        if cid in {1137, 1250, 1251, 1257, 1259, 1264}:
            value -= 100.0
        if base.hand_ids(state, yi).count(cid) > 1:
            value -= 120.0
        return value

    def target_bonus(obs, option):
        state = base.current_state(obs)
        select = base.select_state(obs)
        yi = base.your_index(state)
        context = select.get("context")
        owner = option.get("playerIndex", yi)
        card = base.option_card(obs, option)
        cid = base.card_id(card)
        area = option.get("area")

        if profile_name == "grimmsnarl_spread":
            effect_id = base.card_id(select.get("effect"))
            if context == 16 and effect_id == 112 and owner == yi:
                # Adrena-Brain source: move counters off the most endangered
                # damaged Pokémon, up to the ability's three-counter limit.
                damage = max(0, base.as_int((card or {}).get("maxHp"), 0) - base.as_int((card or {}).get("hp"), 0))
                return 2500.0 + min(damage, 30) * 45.0 + (500.0 if damage >= 30 else 0.0)
            if context == 13 and effect_id == 112 and owner != yi:
                # Adrena-Brain destination: take a counter KO first, then
                # pressure low-HP or multi-prize Pokémon.
                hp = base.as_int((card or {}).get("hp"), 0)
                score = 1800.0 - hp * 2.0
                if 0 < hp <= 30:
                    score += 4000.0
                if cid in base.EX_POKEMON:
                    score += 650.0
                if area == 4:
                    score += 260.0
                return score
            if context == 15 and effect_id == 648 and owner != yi:
                # Shadow Bullet's 30 bench damage should finish a knockout or
                # concentrate pressure rather than scatter randomly.
                hp = base.as_int((card or {}).get("hp"), 0)
                score = 1600.0 - hp * 1.5
                if 0 < hp <= 30:
                    score += 4200.0
                if cid in base.EX_POKEMON:
                    score += 550.0
                if cid in base.ABILITY_POKEMON_IDS:
                    score += 220.0
                return score

        if context in (8, 29) and owner == yi and area in (2, 12):
            return -5000.0 - preservation_value(cid, state, yi)

        bonus = 0.0
        if owner == yi and area in (1, 12, 3):
            wanted = missing_stage_targets(state, yi)
            if cid in wanted:
                bonus += 900.0
            if profile_name == "ogerpon_engine":
                if cid == 96 and board_ids(state, yi).count(96) < 4:
                    bonus += 800.0
                if cid in (1, 18):
                    bonus += 520.0
            elif profile_name == "grimmsnarl_spread":
                if cid == 648 and ({646, 647} & set(board_ids(state, yi))):
                    bonus += 850.0
                if cid == 104 and 860 in board_ids(state, yi):
                    bonus += 600.0
                if cid == 112:
                    bonus += 420.0
                if cid in (860, 104) and base.opponent_ability_pressure(obs)[1]:
                    bonus += 760.0
                if cid == 7:
                    bonus += 400.0
            elif profile_name == "crustle_control":
                if cid == 345 and 344 in board_ids(state, yi):
                    bonus += 850.0
                if cid == 344 and 344 not in board_ids(state, yi):
                    bonus += 720.0
                if cid in (1, 18) and 345 in board_ids(state, yi):
                    bonus += 480.0
                if cid == 20 and 117 in board_ids(state, yi):
                    bonus += 480.0
            elif profile_name == "area_zero_toolbox":
                if cid == 1250:
                    bonus += 600.0
                if cid == 756:
                    bonus += 520.0
                if cid == 184:
                    bonus += 500.0
                if cid == 96 and 1 in base.hand_ids(state, yi):
                    bonus += 440.0
        return bonus

    def play_bonus(obs, option):
        state = base.current_state(obs)
        yi = base.your_index(state)
        cid = base.card_id(base.option_card(obs, option))
        ids = board_ids(state, yi)
        hand = base.hand_ids(state, yi)
        ps = base.players(state)
        oi = 1 - yi
        opp_hand = base.hand_count(state, oi) if oi < len(ps) else 0
        score = 0.0

        if cid == 1197:
            score += 500.0 if opp_hand >= 8 else (180.0 if opp_hand >= 5 else -900.0)
        if cid == 1227:
            score += 440.0 if len(hand) <= 4 else (-180.0 if len(hand) >= 8 else 80.0)
        if cid in profile["safe_setup"]:
            score += 130.0

        if profile_name == "crustle_control":
            if cid == 1086 and ids.count(344) < 2:
                score += 520.0
            if cid == 1152 and 344 in ids and 345 not in hand and 345 not in ids:
                score += 540.0
            if cid == 1225 and 344 in ids and 345 not in hand:
                score += 500.0
            if cid == 1219:
                score += 250.0
            if cid == 756 and 756 not in ids:
                score += 240.0
        elif profile_name == "ogerpon_engine":
            if cid == 96:
                score += 600.0 if ids.count(96) < 3 else 160.0
            if cid in (1094, 1119) and (1 not in hand and 18 not in hand):
                score += 500.0
            if cid == 1118:
                discarded = [base.card_id(c) for c in base.card_list(state, yi, 3, {})]
                score += 420.0 if 1 in discarded else -400.0
            if cid == 1213:
                score += 360.0 if opp_hand >= 7 or len(hand) <= 3 else -120.0
            if cid == 1251:
                score += 180.0
        elif profile_name == "grimmsnarl_spread":
            if cid == 1086 and (ids.count(646) < 2 or ids.count(860) < 1):
                score += 540.0
            if cid in (1079, 1231) and ({646, 647} & set(ids)):
                score += 520.0
            if cid == 1259:
                score += 450.0
            if cid == 1097:
                score += 300.0
            if cid == 112:
                score += 420.0 if ids.count(112) < 2 else 80.0
            if cid == 860 and base.opponent_ability_pressure(obs)[1]:
                score += 680.0 if 860 not in ids else 120.0
        elif profile_name == "area_zero_toolbox":
            if cid == 1250:
                score += 650.0
            if cid == 1205 and len(ids) < 5:
                score += 560.0
            if cid == 1071 and 1071 not in ids:
                score += 420.0
            if cid == 96 and 1 in hand:
                score += 440.0
            if cid == 756 and 756 not in ids:
                score += 430.0
            if cid in (1098, 1116):
                score += 280.0
        return score

    def attack_bonus(obs, option):
        state = base.current_state(obs)
        yi = base.your_index(state)
        active = base.active_card(state, yi)
        active_id = base.card_id(active)
        attack_id = option.get("attackId")
        score = 0.0
        if profile_name == "grimmsnarl_spread":
            if attack_id == 937:
                score += 900.0
            elif attack_id == 934:
                score += 180.0
            elif attack_id == 935:
                score -= 220.0
        elif profile_name == "area_zero_toolbox":
            if attack_id in (72, 1092, 136):
                score += 620.0
            if attack_id == 71:
                score -= 180.0 if len(base.hand_ids(state, yi)) <= 4 else 120.0
            if attack_id == 135 and any(o.get("attackId") == 136 for o in base.select_state(obs).get("option") or []):
                score -= 900.0
        elif profile_name == "crustle_control":
            if attack_id in (148, 479, 1092):
                score += 520.0
        elif profile_name == "ogerpon_engine" and active_id == 96:
            score += len((active or {}).get("energies") or []) * 80.0
        return score

    def semantic_score_option(obs, option):
        score = original_score_option(obs, option)
        option_type = option.get("type")
        context = base.select_state(obs).get("context")
        if option_type == 3:
            score += target_bonus(obs, option)
        elif option_type == 7:
            score += play_bonus(obs, option)
        elif option_type == 13:
            score += attack_bonus(obs, option)
        elif option_type == 9:
            state = base.current_state(obs)
            yi = base.your_index(state)
            cid = base.card_id(base.option_card(obs, option))
            # Rare Candy presents the evolution itself as the target option.
            # Prefer a Benched Impidimp and preserve an attack-ready Active.
            if profile_name == "grimmsnarl_spread" and context == 37:
                if option.get("inPlayArea") == 5:
                    score += 1400.0
                elif option.get("inPlayArea") == 4 and base.readiness(base.active_card(state, yi))["ready"]:
                    score -= 5000.0
            if profile_name == "grimmsnarl_spread" and cid == 104 and base.opponent_ability_pressure(obs)[1]:
                score += 1100.0
            if cid in missing_stage_targets(state, yi):
                score += 800.0
        elif option_type == 10:
            cid = base.card_id(base.option_card(obs, option))
            if cid in profile["abilities"]:
                score += 500.0
        elif option_type == 8 and profile_name == "grimmsnarl_spread":
            state = base.current_state(obs)
            yi = base.your_index(state)
            moving_id = base.card_id(base.option_card(obs, option))
            target = base.target_card(obs, option)
            target_id = base.card_id(target)
            if moving_id == 7:
                energized_munkidori = any(
                    base.card_id(card) == 112 and 7 in (card.get("energies") or [])
                    for _, _, _, card in base.board_cards(state, yi)
                )
                if target_id == 112 and 7 not in ((target or {}).get("energies") or []):
                    score += 2500.0 if not energized_munkidori else 1200.0
                elif target_id in (104, 860):
                    score -= 1800.0
                elif target_id in (646, 647, 648) and not energized_munkidori:
                    score -= 1250.0
        elif option_type == 0 and profile_name == "grimmsnarl_spread" and context == 40:
            score += base.as_int(option.get("number"), 0) * 1400.0
        return score

    base.score_option = semantic_score_option

    def bounded_setup(obs, ranked):
        state = base.current_state(obs)
        yi = base.your_index(state)
        turn_key = base.reset_attack_memory(state)
        signature = base.attack_menu_signature(obs)
        seen = base.ATTACK_MENU_STATES.setdefault(turn_key, set())
        if signature in seen:
            return None
        seen.add(signature)
        if base.ATTACK_DEFERRALS.get(turn_key, 0) >= base.MAX_ATTACK_DEFERRALS:
            return None

        options = base.select_state(obs).get("option") or []

        def source_id(index):
            return base.card_id(base.option_card(obs, options[index]))

        def highest(predicate):
            for _, index in ranked:
                if predicate(index):
                    return index
            return None

        def safe_evolution(index):
            option = options[index]
            if option.get("type") != 9:
                return False
            target = base.target_card(obs, option)
            if option.get("inPlayArea") != 4 or not base.readiness(target)["ready"]:
                return True
            evolution = base.option_card(obs, option)
            if not isinstance(evolution, dict) or not isinstance(target, dict):
                return False
            evolved = dict(evolution)
            evolved["energies"] = list(target.get("energies") or [])
            return base.readiness(evolved)["ready"]

        board_size = len(base.board_cards(state, yi))
        choice = None
        if board_size <= 1:
            choice = highest(
                lambda i: options[i].get("type") == 7
                and (source_id(i) in profile["basics"] or source_id(i) == 1086)
            )
        if choice is None:
            # Never turn a currently legal attack into an abandoned turn by
            # evolving the Active into an attacker that is not yet paid.
            choice = highest(safe_evolution)
        if choice is None:
            choice = highest(
                lambda i: options[i].get("type") == 10
                and source_id(i) in profile["abilities"]
            )
        if choice is None and not bool(state.get("energyAttached")):
            choice = highest(
                lambda i: options[i].get("type") == 8
                and source_id(i) in profile["energy"]
                and not base.readiness(base.target_card(obs, options[i]))["ready"]
            )
        if choice is None:
            choice = highest(
                lambda i: options[i].get("type") == 7
                and source_id(i) in profile["safe_setup"]
            )
        if choice is None:
            return None
        base.ATTACK_DEFERRALS[turn_key] = base.ATTACK_DEFERRALS.get(turn_key, 0) + 1
        return choice

    base.bounded_setup_choice = bounded_setup
    return base
