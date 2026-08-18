"""V16 Master Agent: Airtight Meta-Consistent Master for Kaggle Pokemon TCG AI Battle Challenge.

Integrates V15's battle-tested mechanics engine (multi-card search, bounded setup deferral, exact card profiles)
with V16's four airtight strategic breakthroughs:
1. Anti-Bench-Wipe Safeguard (bench_count <= 1):
   - +25,000 / +12,000 priority boost for Buddy-Buddy Poffin, Basic Dwebble, and Cornerstone Ogerpon ex
     until at least 2 benched Pokemon are established.
   - Poffin correctly selects UP TO 2 Basic Pokemon to establish a resilient board.
2. Active Attacker Energy Acceleration & Damaging Attack Priority:
   - readiness['ready'] strictly requires damage > 0 so 0-damage utility attacks (Ascension) do not starve
     active 120/140-damage attackers of 2nd and 3rd energy.
   - Active damaging attackers (Crustle 345, Cornerstone 117) receive top priority (+1,500.0 / +1,200.0)
     to rapidly reach 3 energy and attack.
   - High priority for energy-accelerating Supporters: Crispin 1198 (+2,500.0), Waitress 1235 (+2,000.0),
     and Lillie 1227 (+1,800.0) when active needs energy.
3. Hero's Cape (+100 HP) Tool Attachment (Option Type 8) & Evolution (Type 9) & Healing (1147):
   - High priority (+4,500.0 to +5,200.0) for Hero's Cape (1159) to keep active/bench attackers out of 1-shot KO range.
   - Bounded setup deferral properly executes Evolution (Type 9), Healing (1147), and Disruption (1197).
4. Grimmsnarl ex / Munkidori / Alakazam Ability Threat Master (Cornerstone Stance & Forced-Switch Target Protection):
   - OFFENSIVE_ABILITY_THREATS = {265, 343, 678, 743} (Grimmsnarl ex, Munkidori, Alakazam ex, Froslass ex).
   - Target promotion logic applies to option types 3 & 10 (both forced switch & KO promotions) with robust bench lookup.
   - +25,000 priority boost for Cornerstone Mask Ogerpon ex (117) against offensive Ability threats
     (Cornerstone Stance blocks 100% of damage from Pokemon with Abilities).
   - Strict Anti-Retreat Invariant (-50,000.0 penalty) preventing retreat of Cornerstone Ogerpon ex away from Ability threats.
5. 100% Damaging Attack Invariant & Crash-Proof Kaggle Safety:
   - +100,000.0 priority for legal damaging attacks.
   - Raw Python execution without __file__ dependency and cross-game state isolation with try/except emergency fallback.
"""

import os


BASE_TYPE_SCORE = {
    1: 0.0,
    2: 0.0,
    3: 310.0,
    4: 330.0,
    5: 420.0,
    6: 500.0,
    7: 620.0,
    8: 720.0,
    9: 760.0,
    10: 700.0,
    12: 80.0,
    13: 2400.0,
    14: -1200.0,
    15: 210.0,
}

ENERGY_CARD_TYPES = {
    1: "G",
    2: "R",
    3: "W",
    4: "L",
    5: "P",
    6: "F",
    11: "C",
    14: "C",
    15: "RKT",
    18: "G",
}

ATTACHED_ENERGY_TYPES = {
    0: "C",
    1: "G",
    2: "R",
    3: "W",
    4: "L",
    5: "P",
    6: "F",
    7: "D",
    8: "M",
    9: "N",
    10: "*",
    11: "RKT",
}

ATTACKS = {
    117: [{"cost": ["F", "C", "C"], "damage": 140, "name": "Demolish"}],
    344: [{"cost": ["C"], "damage": 0, "name": "Ascension"}],
    345: [{"cost": ["G", "C", "C"], "damage": 120, "name": "Superb Scissors"}],
    397: [{"cost": ["G"], "damage": 20, "name": "Cut Up"}],
    398: [{"cost": ["G"], "damage": 130, "name": "Petal Blade Dance"}],
    796: [{"cost": ["R"], "damage": 10, "name": "Chop"}],
    797: [{"cost": ["R"], "damage": 220, "name": "Infernal Slash"}],
    1073: [{"cost": ["C"], "damage": 10, "name": "Smash Kick"}],
    1074: [{"cost": ["C"], "damage": 140, "name": "Earthquake"}],
    756: [{"cost": ["C", "C", "C"], "damage": 200, "name": "Rapid-Fire Combo"}],
    1071: [{"cost": ["C", "C", "C"], "damage": 60, "name": "Tuck Tail"}],
    96: [{"cost": ["G", "G", "G"], "damage": 90, "name": "Myriad Leaf Shower"}],
    108: [{"cost": ["W", "C", "C"], "damage": 100, "name": "Torrential Pump"}],
    63: [{"cost": ["L", "F"], "damage": 140, "name": "Bellowing Thunder"}],
    184: [{"cost": ["P", "P", "C"], "damage": 200, "name": "Eon Blade"}],
    140: [{"cost": ["C", "C", "C"], "damage": 90, "name": "Cruel Arrow"}],
    272: [{"cost": ["P", "C"], "damage": 80, "name": "Full Moon Rondo"}],
    978: [{"cost": ["F", "C"], "damage": 80, "name": "Coordinated Throwing"}],
}

ATTACK_DAMAGE_BY_ID = {
    71: 0,
    72: 140,
    120: 90,
    135: 20,
    136: 100,
    148: 140,
    183: 100,
    371: 80,
    478: 0,
    479: 120,
    1092: 200,
    1407: 80,
    1550: 140,
    1551: 100,
}

POKEMON_ROLE = {
    117: 170.0,
    797: 165.0,
    1074: 155.0,
    398: 145.0,
    345: 140.0,
    756: 120.0,
    96: 105.0,
    184: 90.0,
    63: 88.0,
    108: 75.0,
    140: 65.0,
    1071: 60.0,
    272: 50.0,
    978: 45.0,
    344: 40.0,
    796: 40.0,
    1073: 40.0,
    397: 38.0,
}

EX_POKEMON = {
    24, 29, 30, 37, 40, 44, 46, 52, 63, 75, 79, 80, 83, 84, 96, 99, 107,
    108, 117, 121, 125, 130, 138, 139, 140, 141, 150, 153, 154, 161, 176,
    179, 184, 189, 190, 193, 198, 205, 207, 210, 223, 229, 231, 232, 236,
    239, 241, 243, 244, 246, 248, 249, 259, 269, 272, 283, 293, 299, 302,
    306, 313, 316, 320, 326, 328, 329, 331, 336, 337, 340, 357, 369, 372,
    381, 389, 404, 407, 424, 431, 447, 455, 458, 471, 481, 509, 515, 525,
    527, 547, 561, 573, 583, 598, 618, 631, 641, 648, 652, 662, 678, 687,
    695, 723, 737, 747, 754, 756, 766, 772, 781, 790, 795, 806, 813, 828,
    835, 849, 868, 886, 896, 904, 911, 919, 928, 932, 939, 944, 951,
    954, 957, 962, 968, 969, 975, 979, 984, 988, 990, 993, 997, 1002,
    1006, 1022, 1026, 1031, 1040, 1056, 1062, 1064, 1071,
}

OFFENSIVE_ABILITY_THREATS = {265, 343, 678, 743}

DRAW_SEARCH_CARDS = {1088, 1097, 1098, 1121, 1152, 1198, 1205, 1227, 1235, 1250}
DISRUPTION_CARDS = {1182, 1197}
ENERGY_CARDS = set(ENERGY_CARD_TYPES)
BASIC_SETUP_POKEMON = {117, 344, 397, 796, 1073}
CORE_BOARD_LINES = {117, 344, 345}

DAMAGE_COUNTER_PRESSURE = {15, 16, 17, 72, 112, 121, 163, 343, 648, 743, 1071}
BYPASS_EFFECT_ATTACKERS = {62, 80, 159, 189, 231, 241, 306, 312, 404, 527, 583, 849, 1031}

MIST_ACTIVE_THREATS = {
    29, 32, 56, 94, 121, 215, 219, 223, 245, 247, 432, 455, 593, 738,
    743, 817, 864, 876, 880, 982, 1058,
}

EXPECTED_DECK = [
    344, 344, 344, 344, 345, 345, 345, 345, 117, 117, 1086, 1086,
    1086, 1086, 1152, 1152, 1152, 1152, 1198, 1198, 1198, 1227,
    1227, 1227, 1227, 1197, 1197, 1197, 1235, 1235, 1235, 1235,
    1147, 1147, 1147, 1147, 1159, 18, 18, 18, 18, 11, 11, 11, 14,
    14, 14, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]


def load_deck():
    candidate_paths = [
        os.path.join("/kaggle_simulations/agent", "deck.csv"),
    ]
    source_path = globals().get("__file__", "")
    if source_path:
        candidate_paths.append(
            os.path.join(os.path.dirname(os.path.abspath(source_path)), "deck.csv")
        )
    candidate_paths.append(os.path.join(os.getcwd(), "deck.csv"))

    for path in candidate_paths:
        try:
            with open(path, encoding="utf-8-sig") as handle:
                deck = [
                    int(line.strip().split(",")[0])
                    for line in handle
                    if line.strip()
                ]
        except (OSError, ValueError):
            continue
        if deck == EXPECTED_DECK:
            return deck
    return EXPECTED_DECK


DECK = load_deck()
ATTACK_DEFERRALS = {}
ATTACK_MENU_STATES = {}
LAST_TURN_SEEN = None
MAX_ATTACK_DEFERRALS = 3
LILLIE_DEFERRAL_HAND_LIMIT = 8
WAITRESS_ONLY_WHEN_UNREADY = True


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def current_state(obs):
    return (obs or {}).get("current") or {}


def select_state(obs):
    return (obs or {}).get("select") or {}


def players(state):
    value = state.get("players")
    return value if isinstance(value, list) else []


def your_index(state):
    idx = state.get("yourIndex", 0)
    return idx if idx in (0, 1) else 0


def card_list(state, player, area, select):
    ps = players(state)
    if area == 1:
        return select.get("deck") or []
    if area == 12:
        return state.get("looking") or []
    if area == 7:
        return state.get("stadium") or []
    if not isinstance(player, int) or player < 0 or player >= len(ps):
        return []
    zone = {
        2: "hand",
        3: "discard",
        4: "active",
        5: "bench",
    }.get(area)
    return ps[player].get(zone) or [] if zone else []


def card_at(state, player, area, index, select):
    cards = card_list(state, player, area, select)
    if not isinstance(index, int) or index < 0 or index >= len(cards):
        return None
    card = cards[index]
    if isinstance(card, dict):
        return card
    return {"id": card}


def option_card(obs, option):
    state = current_state(obs)
    select = select_state(obs)
    owner = option.get("playerIndex", your_index(state))
    area = option.get("area")
    if area is None and option.get("type") == 7:
        area = 2
    return card_at(state, owner, area, option.get("index"), select)


def target_card(obs, option):
    state = current_state(obs)
    select = select_state(obs)
    owner = option.get("playerIndex", your_index(state))
    area = option.get("inPlayArea") if option.get("inPlayArea") is not None else option.get("area")
    if area is None:
        area = 5
    idx = option.get("inPlayIndex") if option.get("inPlayIndex") is not None else option.get("index")
    return card_at(state, owner, area, idx, select)


def attached_types(card):
    if not isinstance(card, dict):
        return []
    result = []
    for energy_id in card.get("energies") or []:
        symbol = ATTACHED_ENERGY_TYPES.get(energy_id)
        if symbol:
            result.append(symbol)
    for card_obj in card.get("energyCards") or []:
        cid = card_id(card_obj)
        symbol = ENERGY_CARD_TYPES.get(cid)
        if symbol:
            result.append(symbol)
    return result


def card_id(card):
    if isinstance(card, dict):
        return as_int(card.get("id"))
    return as_int(card)


def hand_ids(state, player):
    cards = card_list(state, player, 2, {})
    return [card_id(card) for card in cards]


def board_cards(state, player):
    result = []
    active = card_list(state, player, 4, {})
    if active and isinstance(active[0], dict):
        result.append((4, player, 0, active[0]))

    bench = card_list(state, player, 5, {})
    for idx, card in enumerate(bench):
        if isinstance(card, dict):
            result.append((5, player, idx, card))
    return result


def active_card(state, player):
    cards = card_list(state, player, 4, {})
    return cards[0] if cards and isinstance(cards[0], dict) else None


def bench_cards(state, player):
    return [
        card
        for card in card_list(state, player, 5, {})
        if isinstance(card, dict)
    ]


def bench_count(state, player):
    return len(bench_cards(state, player))


def hand_count(state, player):
    return len(card_list(state, player, 2, {}))


def poffin_progress_capacity(obs):
    state = current_state(obs)
    yi = your_index(state)
    bench_spots = max(0, 5 - bench_count(state, yi))
    if bench_spots == 0:
        return 0

    deck_target_count = sum(
        1
        for cid in card_list(state, yi, 1, select_state(obs))
        if card_id(cid) == 344
    )
    if select_state(obs).get("deck"):
        return min(bench_spots, deck_target_count)

    dwebble_in_deck = sum(1 for cid in DECK if cid == 344)
    dwebble_in_play = sum(
        1 for _, _, _, card in board_cards(state, yi) if card_id(card) == 344
    )
    dwebble_in_hand = sum(1 for cid in hand_ids(state, yi) if cid == 344)
    dwebble_in_discard = sum(
        1
        for card in card_list(state, yi, 3, {})
        if card_id(card) == 344
    )
    estimated_deck_targets = max(
        0,
        dwebble_in_deck - (dwebble_in_play + dwebble_in_hand + dwebble_in_discard),
    )
    return min(bench_spots, estimated_deck_targets)


def required_line_count(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    active = active_card(state, opp)
    opp_cid = card_id(active) if isinstance(active, dict) else None
    if opp_cid in EX_POKEMON or opp_cid in OFFENSIVE_ABILITY_THREATS:
        return 2
    return 3


def viable_line_count(state, player):
    lines = 0
    for _, _, _, card in board_cards(state, player):
        cid = card_id(card)
        if cid in CORE_BOARD_LINES:
            lines += 1
    return lines


def readiness(card, extra_energy=None):
    if not isinstance(card, dict):
        return {"ready": False, "utility_ready": False, "score": 0.0, "needed": 99, "damage": 0}
    cid = card_id(card)
    attacks = ATTACKS.get(cid, [])
    if not attacks:
        return {"ready": False, "utility_ready": False, "score": POKEMON_ROLE.get(cid, 0.0), "needed": 99, "damage": 0}

    attached = attached_types(card)
    if extra_energy is not None:
        sym = ENERGY_CARD_TYPES.get(extra_energy)
        if sym:
            attached = attached + [sym]

    best = None
    for attack in attacks:
        cost = list(attack["cost"])
        remaining = list(attached)
        matched = 0

        for req in list(cost):
            if req in remaining:
                remaining.remove(req)
                cost.remove(req)
                matched += 1

        for req in list(cost):
            if req == "C" and remaining:
                remaining.pop(0)
                cost.remove(req)
                matched += 1

        needed = len(cost)
        damage = attack.get("damage", 0)
        score = POKEMON_ROLE.get(cid, 0.0) + damage * 1.5 - needed * 120.0
        if damage == 0:
            score -= 150.0

        item = {
            "ready": (needed == 0 and damage > 0),
            "utility_ready": (needed == 0 and damage == 0),
            "score": score,
            "needed": needed,
            "damage": damage,
        }
        if best is None or item["score"] > best["score"]:
            best = item
    return best or {"ready": False, "utility_ready": False, "score": 0.0, "needed": 99, "damage": 0}


def opponent_ex_pressure(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    cards = board_cards(state, opp)
    active = active_card(state, opp)
    active_ex = card_id(active) in EX_POKEMON
    any_ex = any(card_id(card) in EX_POKEMON for _, _, _, card in cards)
    return active_ex, any_ex


def opponent_ability_pressure(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    cards = board_cards(state, opp)
    active = active_card(state, opp)
    active_ability = card_id(active) in OFFENSIVE_ABILITY_THREATS
    any_ability = any(card_id(card) in OFFENSIVE_ABILITY_THREATS for _, _, _, card in cards)
    return active_ability, any_ability


def opponent_bypass_pressure(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    cards = board_cards(state, opp)
    active = active_card(state, opp)
    active_bypass = card_id(active) in BYPASS_EFFECT_ATTACKERS
    any_bypass = any(card_id(card) in BYPASS_EFFECT_ATTACKERS for _, _, _, card in cards)
    return active_bypass, any_bypass


def hp_pressure_bonus(obs, damage):
    state = current_state(obs)
    yi = your_index(state)
    opp = 1 - yi
    target = active_card(state, opp)
    if not isinstance(target, dict):
        return 0.0
    hp = as_int(target.get("hp"), 0)
    if hp and damage >= hp:
        return 420.0
    if hp and damage >= hp * 0.65:
        return 120.0
    return min(damage, 220) * 0.12


def reset_attack_memory(state):
    global LAST_TURN_SEEN
    turn_key = (your_index(state), as_int(state.get("turn"), 0))
    if LAST_TURN_SEEN is not None and (
        turn_key[1] < LAST_TURN_SEEN or (turn_key[1] == 0 and LAST_TURN_SEEN != 0)
    ):
        ATTACK_DEFERRALS.clear()
        ATTACK_MENU_STATES.clear()
    LAST_TURN_SEEN = turn_key[1]
    return turn_key


def attack_menu_signature(obs):
    state = current_state(obs)
    yi = your_index(state)
    select = select_state(obs)
    options = select.get("option") or []
    board = tuple(
        (area, index, card_id(card), len(attached_types(card)))
        for area, _, index, card in board_cards(state, yi)
    )
    hand = tuple(sorted(hand_ids(state, yi)))
    return (
        as_int(state.get("turn"), 0),
        bool(state.get("supporterPlayed")),
        bool(state.get("energyAttached")),
        board,
        hand,
        len(options),
    )


def score_play_from_hand(obs, option):
    state = current_state(obs)
    yi = your_index(state)
    hand = card_list(state, yi, 2, {})
    idx = option.get("index")
    cid = card_id(hand[idx]) if isinstance(idx, int) and 0 <= idx < len(hand) else None
    score = BASE_TYPE_SCORE[7]

    cur_bench = bench_count(state, yi)
    if cur_bench == 0:
        if cid in BASIC_SETUP_POKEMON:
            return 25000.0
        if cid == 1086:
            capacity = poffin_progress_capacity(obs)
            if capacity > 0:
                return 22000.0
        if cid == 1152:
            return 18000.0
        if cid in (1198, 1227, 1235):
            score += 14000.0  # Draw supporters to find Basic/Poffin when 0 bench!
    elif cur_bench == 1:
        if cid in BASIC_SETUP_POKEMON:
            score += 12000.0
        if cid == 1086:
            capacity = poffin_progress_capacity(obs)
            if capacity > 0:
                score += 10000.0
        if cid in (1198, 1227, 1235):
            score += 8000.0

    if cid in DRAW_SEARCH_CARDS:
        score += 350.0
    lines_needed = max(0, required_line_count(obs) - viable_line_count(state, yi))
    if cid == 1086:
        capacity = poffin_progress_capacity(obs)
        if capacity <= 0:
            return -5000.0
        if cur_bench > 0 and viable_line_count(state, yi) >= 3:
            return -5000.0
        if lines_needed:
            score += 520.0 * min(lines_needed, capacity)
    elif cid in (1152, 1227) and lines_needed:
        score += 420.0
    if cid in DISRUPTION_CARDS:
        score += 70.0 + hp_pressure_bonus(obs, 90)

    opponent_hand = hand_count(state, 1 - yi)
    if cid == 1197:  # Xerosic's Machinations
        if opponent_hand <= 3:
            return -850.0
        score += (opponent_hand - 3) * 350.0
        if opponent_hand >= 4:
            score += 3500.0

    active = active_card(state, yi)
    active_r = readiness(active)
    active_missing_hp = 0
    if isinstance(active, dict):
        active_missing_hp = max(0, as_int(active.get("maxHp"), 0) - as_int(active.get("hp"), 0))

    if cid in (1147, 1212) and active_missing_hp >= 40:
        score += 850.0

    # Energy Acceleration Supporters (Crispin 1198, Waitress 1235, Lillie 1227)
    if active_r["needed"] > 0 and active_r["damage"] > 0:
        if cid == 1198:  # Crispin: attaches 1 energy directly + 1 to hand!
            score += 2500.0
        elif cid == 1235:  # Waitress: energy search & attachment!
            score += 2000.0
        elif cid == 1227:  # Lillie's Determination: draw 6-8 cards to find energy!
            score += 1800.0

    return score


def score_energy_attachment(obs, option):
    target = target_card(obs, option)
    card = option_card(obs, option)
    if not isinstance(target, dict) or not isinstance(card, dict):
        return -50.0
    cid = card_id(card)
    symbol = ENERGY_CARD_TYPES.get(cid)
    if not symbol:
        return -50.0

    state = current_state(obs)
    yi = your_index(state)
    active_ex, any_ex = opponent_ex_pressure(obs)
    active_ability, any_ability = opponent_ability_pressure(obs)
    active_bypass, any_bypass = opponent_bypass_pressure(obs)

    base = readiness(target)
    with_energy = readiness(target, extra_energy=cid)

    score = BASE_TYPE_SCORE[8]
    if symbol in ("G", "F", "C", "RKT"):
        score += 180.0

    target_cid = card_id(target)

    if cid == 18:  # Grow Grass Energy
        if target_cid in (344, 345):
            score += 350.0
        elif target_cid == 117:
            score -= 150.0

    if cid == 11:  # Mist Energy
        opp_active = active_card(state, 1 - yi)
        opp_active_id = card_id(opp_active) if isinstance(opp_active, dict) else None
        if option.get("inPlayArea") == 4 and with_energy["ready"]:
            score += 420.0
        elif opp_active_id in MIST_ACTIVE_THREATS and option.get("inPlayArea") == 4:
            score += 550.0
        elif option.get("inPlayArea") == 4:
            score += 260.0

    if cid == 14:  # Spiky Energy
        if option.get("inPlayArea") == 4:
            score += 220.0
        else:
            score += 80.0

    if target_cid == 117:
        if active_ability or any_ability:
            score += 3500.0  # High priority to power up Cornerstone Ogerpon ex vs Ability threats
        elif active_bypass or any_bypass:
            score += 1550.0
        elif active_ex or any_ex:
            score -= 200.0
        else:
            score += 180.0
    elif target_cid in (344, 345):
        if active_ability or any_ability:
            score -= 200.0  # Prefer Cornerstone against Ability threats
        elif active_bypass or any_bypass:
            score -= 150.0
        elif active_ex or any_ex:
            score += 450.0  # High priority to power up Crustle facing ex
        else:
            score += 350.0

    # Active attacker acceleration:
    if option.get("inPlayArea") == 4:
        if with_energy["needed"] < base["needed"] and with_energy["damage"] > 0:
            score += 1500.0  # Top priority to build towards active attack
        if with_energy["ready"]:
            score += 1200.0  # Fully powers active damaging attack
    else:
        if with_energy["ready"] and with_energy["damage"] > 0:
            score += 600.0
        elif with_energy["needed"] < base["needed"] and with_energy["damage"] > 0:
            score += 300.0

    return score


def score_option(obs, option):
    if not isinstance(option, dict):
        return -5000.0
    option_type = option.get("type", 0)
    base_score = BASE_TYPE_SCORE.get(option_type, 0.0)
    state = current_state(obs)
    yi = your_index(state)

    if option_type == 6:  # Retreat
        active = active_card(state, yi)
        if isinstance(active, dict) and card_id(active) == 117:
            active_ability, any_ability = opponent_ability_pressure(obs)
            if active_ability or any_ability:
                return -50000.0  # NEVER retreat Cornerstone Ogerpon ex away from Ability threats!

    if option_type == 7:
        return score_play_from_hand(obs, option)

    if option_type == 8:  # Energy or Tool attachment
        card = option_card(obs, option)
        cid = card_id(card)
        if cid in ENERGY_CARDS:
            return score_energy_attachment(obs, option)
        if cid == 1159:  # Hero's Cape (+100 HP) Tool
            score = base_score + 2200.0
            target = target_card(obs, option)
            target_cid = card_id(target) if isinstance(target, dict) else 0
            if target_cid in (117, 345):
                score += 1500.0
            if option.get("inPlayArea") == 4:
                score += 800.0
            return score

    if option_type == 9:  # Evolution (Dwebble -> Crustle)
        score = base_score + 1200.0
        target = target_card(obs, option)
        if isinstance(target, dict) and option.get("inPlayArea") == 4:
            score += 800.0  # Evolve active
        return score

    if option_type == 13:
        attack_id = option.get("index")
        damage = ATTACK_DAMAGE_BY_ID.get(attack_id, 100)
        score = base_score + 100000.0 + damage * 1.5 + hp_pressure_bonus(obs, damage)
        opp_active = active_card(state, 1 - yi)
        opp_id = card_id(opp_active) if isinstance(opp_active, dict) else 0
        if opp_id in DAMAGE_COUNTER_PRESSURE:
            score += 500.0

        our_active = active_card(state, yi)
        if isinstance(our_active, dict) and card_id(our_active) == 344 and damage == 0:
            score += 350.0  # Ascension bonus for active Dwebble to evolve into Crustle

        return score

    if option_type in (3, 10):  # Active Promotion / Selection from Bench
        target = target_card(obs, option)
        if not isinstance(target, dict):
            return -100.0
        target_id = card_id(target)
        r = readiness(target)
        active_ex, any_ex = opponent_ex_pressure(obs)
        active_ability, any_ability = opponent_ability_pressure(obs)

        score = base_score + r["score"]
        if target_id == 117 and (active_ability or any_ability):
            score += 25000.0  # Cornerstone Stance walls Grimmsnarl ex / Munkidori / Alakazam
        elif target_id == 345 and (active_ex or any_ex) and not (active_ability or any_ability):
            score += 20000.0  # Crustle walls ex (Mega Lucario ex, Dragapult ex)
        elif target_id == 345:
            if r["ready"]:
                score += 8000.0
            else:
                score += 4000.0
        elif target_id == 117:
            if r["ready"]:
                score += 8000.0
            else:
                score += 3000.0

        return score

    return base_score


def bounded_setup_choice(obs, ranked):
    state = current_state(obs)
    yi = your_index(state)
    turn_key = reset_attack_memory(state)
    ps = players(state)
    deck_count = ps[yi].get("deckCount") if yi < len(ps) else None
    if deck_count is not None and as_int(deck_count, -1) == 0:
        return None

    signature = attack_menu_signature(obs)
    seen = ATTACK_MENU_STATES.setdefault(turn_key, set())
    if signature in seen:
        return None
    seen.add(signature)

    cur_bench = bench_count(state, yi)
    if cur_bench > 0 and ATTACK_DEFERRALS.get(turn_key, 0) >= MAX_ATTACK_DEFERRALS:
        return None

    options = select_state(obs).get("option") or []

    def best_index(predicate):
        choices = [(score, index) for score, index in ranked if predicate(index)]
        return choices[0][1] if choices else None

    # Evolution (Type 9) setup
    choice = best_index(
        lambda index: options[index].get("type") == 9
        and card_id(option_card(obs, options[index])) == 345
    )

    # Useful setup actions: Poffin, Basic Pokemon, Supporters, Tool, Healing
    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and card_id(option_card(obs, options[index])) in (1086, 1147, 1152, 1197, 1198, 1227, 1235, 117, 344)
        )

    # Energy attachment
    if choice is None and not bool(state.get("energyAttached")):
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) in ENERGY_CARDS
            and not readiness(target_card(obs, options[index]))["ready"]
        )

    # Hero's Cape Tool attachment
    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) == 1159  # Hero's Cape
        )

    if choice is not None:
        ATTACK_DEFERRALS[turn_key] = ATTACK_DEFERRALS.get(turn_key, 0) + 1
        return choice

    return None


def choose_action(obs):
    if not isinstance(obs, dict) or obs.get("select") is None:
        return DECK[:]
    select = select_state(obs)
    if select is None:
        return DECK[:]

    options = select.get("option") or []
    if not options:
        return []

    min_count = as_int(select.get("minCount"), 0)
    max_count = as_int(select.get("maxCount"), 0)
    if max_count == 60:
        return list(range(len(options)))
    if max_count <= 0:
        return []

    reset_attack_memory(current_state(obs))

    ranked = sorted(
        ((score_option(obs, option), index) for index, option in enumerate(options)),
        key=lambda item: (-item[0], item[1]),
    )

    # Buddy-Buddy Poffin multi-card selection (up to 2 Basic Pokemon)
    if card_id(select.get("effect")) == 1086:
        state = current_state(obs)
        cur_bench = bench_count(state, your_index(state))
        line_capacity = 2 if cur_bench == 0 else max(0, 3 - viable_line_count(state, your_index(state)))
        take = min(max_count, max(min_count, line_capacity))
        return [index for score, index in ranked if score > 0][:take]

    # Crispin energy multi-card selection (up to 2 energies)
    if card_id(select.get("effect")) == 1198:
        take = min(max_count, 2)
        return [index for score, index in ranked if score > 0][:take]

    # Damaging Attack Execution with bounded setup
    attack_choices = [
        (score, index)
        for score, index in ranked
        if options[index].get("type") == 13
    ]
    if attack_choices and min_count <= 1 <= max_count:
        _, attack_index = attack_choices[0]
        setup_index = bounded_setup_choice(obs, ranked)
        if setup_index is not None:
            return [setup_index]
        return [attack_index]

    chosen = [index for _, index in ranked[:min_count]]
    for score, index in ranked[min_count:max_count]:
        if score <= 0:
            break
        chosen.append(index)
    return chosen


def emergency_action(obs):
    select = obs.get("select") if isinstance(obs, dict) else None
    if select is None:
        return DECK[:]
    options = select.get("option") or []
    minimum = max(0, as_int(select.get("minCount"), 0))
    maximum = max(0, as_int(select.get("maxCount"), 0))
    if not options or maximum == 0:
        return []
    if minimum <= 1 <= maximum:
        for index, option in enumerate(options):
            if isinstance(option, dict) and option.get("type") == 13:
                return [index]
    return list(range(min(minimum, maximum, len(options))))


def safe_action(obs):
    try:
        return choose_action(obs)
    except Exception:
        return emergency_action(obs)


def agent(obs, proc=None):
    return safe_action(obs)
