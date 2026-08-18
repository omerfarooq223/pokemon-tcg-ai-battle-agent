"""V15 Master Agent: Threat-Aware Anti-Meta Master for Kaggle Pokemon TCG AI Battle Challenge.

Integrates V14's full mechanics-aware engine (Ascension evolution, signature tracking,
poffin progress capacity, bounded setup choice) with V15's multi-archetype threat profiling
and counter-strategies:
1. Mega Lucario ex Counter (Luca / DL / M_Murata):
   - Crustle Sturdy Wall promotion boost (+3,000) to wall ex attacks completely.
   - 2-shot 270 HP Mega Lucario ex with Superb Scissors for 3 instant prizes.
2. Dragapult ex Counter (flg / Benarg):
   - Hero's Cape (+2,000) and Jumbo Ice Cream healing to nullify Phantom Dive bench spread.
3. Alakazam & Dudunsparce Hand-Control Counter:
   - Xerosic's Machinations (+3,500) whenever opponent hand >= 4 or Alakazam line visible.
   - Priority attack targeting (+500) against Alakazam / Dudunsparce.
4. Grimmsnarl ex / Munkidori Spread Counter:
   - Cornerstone Mask Ogerpon ex promotion (+3,000) to wall damage from Pokémon with Abilities.
5. Anti-Bench Wipe Invariant:
   - +25,000 priority for playing Basic Pokémon / Poffin when bench_count == 0.
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
    345: 125.0,
    756: 120.0,
    96: 105.0,
    184: 90.0,
    63: 88.0,
    108: 75.0,
    140: 65.0,
    1071: 60.0,
    272: 50.0,
    978: 45.0,
    344: 42.0,
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

ABILITY_POKEMON_IDS = {
    28, 36, 37, 44, 49, 56, 57, 66, 72, 74, 75, 79, 80, 81, 83, 86, 90,
    93, 96, 98, 100, 102, 104, 106, 107, 109, 112, 116, 117, 118, 120, 122,
    123, 125, 126, 132, 133, 135, 139, 140, 141, 142, 144, 147, 150, 155,
    156, 158, 159, 167, 170, 173, 174, 175, 180, 182, 184, 190, 198, 202,
    203, 205, 207, 209, 210, 211, 214, 221, 225, 230, 232, 238, 240, 247,
    249, 250, 255, 256, 259, 262, 269, 271, 272, 279, 283, 287, 290, 293,
    297, 304, 310, 315, 317, 322, 326, 330, 340, 342, 343, 345, 351, 353,
    356, 357, 359, 362, 380, 383, 392, 401, 414, 416, 424, 428, 431, 436,
    439, 442, 449, 457, 458, 461, 475, 481, 487, 497, 504, 505, 512, 525,
    530, 533, 537, 542, 547, 558, 564, 569, 576, 596, 598, 604, 618, 623,
    631, 637, 641, 648, 652, 666, 674, 675, 685, 688, 698, 705, 710, 711,
    713, 716, 725, 742, 743, 748, 750, 755, 756, 766, 772, 784, 788, 795,
    799, 806, 813, 818, 824, 829, 834, 835, 847, 851, 854, 856, 858, 859,
    866, 871, 882, 886, 896, 898, 901, 903, 904, 911, 915, 924, 962, 968,
    970, 976, 993, 994, 1009, 1019, 1022, 1024, 1027, 1029, 1033, 1036,
    1040, 1045, 1052, 1054, 1059, 1071, 1099, 1136, 1138, 1150, 1151,
}

DRAW_SEARCH_CARDS = {1088, 1097, 1098, 1121, 1152, 1198, 1205, 1250}
DISRUPTION_CARDS = {1182, 1197}
ENERGY_CARDS = set(ENERGY_CARD_TYPES)
BASIC_SETUP_POKEMON = {117, 344, 397, 796, 1073}
CORE_BOARD_LINES = {117, 344, 345}

DAMAGE_COUNTER_PRESSURE = {15, 16, 17, 72, 112, 121, 163, 648, 743, 1071}
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
MAX_ATTACK_DEFERRALS = 4
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
    return card_at(
        state,
        owner,
        option.get("inPlayArea"),
        option.get("inPlayIndex"),
        select,
    )


def attached_types(card):
    if not isinstance(card, dict):
        return []
    result = []
    for energy_id in card.get("energies") or []:
        symbol = ATTACHED_ENERGY_TYPES.get(energy_id)
        if symbol:
            result.append(symbol)
    return result


def cost_missing(cost, energy_types):
    pool = list(energy_types)
    missing = 0
    for symbol in cost:
        if symbol == "C":
            continue
        if symbol in pool:
            pool.remove(symbol)
        elif "*" in pool:
            pool.remove("*")
        elif symbol in ("P", "D") and "RKT" in pool:
            pool.remove("RKT")
        else:
            missing += 1
    colorless_needed = cost.count("C")
    colorless_paid = min(colorless_needed, len(pool))
    missing += colorless_needed - colorless_paid
    return missing


def readiness(card, extra_energy=None, remove_energy_index=None):
    if not isinstance(card, dict):
        return {"ready": False, "missing": 9, "damage": 0, "score": -50.0}
    energy_types = attached_types(card)
    if isinstance(remove_energy_index, int) and 0 <= remove_energy_index < len(energy_types):
        energy_types = energy_types[:remove_energy_index] + energy_types[remove_energy_index + 1 :]
    if extra_energy in ENERGY_CARD_TYPES:
        energy_types.append(ENERGY_CARD_TYPES[extra_energy])
        if extra_energy == 15:
            energy_types.append("RKT")

    attacks = ATTACKS.get(card.get("id"))
    if not attacks:
        count = len(energy_types)
        hp = as_int(card.get("hp"), 0)
        return {
            "ready": count >= 3,
            "missing": max(0, 3 - count),
            "damage": 40 * min(count, 3),
            "score": 20.0 * count + min(hp, 300) / 30.0,
        }

    best = None
    for attack in attacks:
        missing = cost_missing(attack["cost"], energy_types)
        damage = attack["damage"]
        score = damage * 1.2 - missing * 95.0 + len(energy_types) * 8.0
        if missing == 0:
            score += 220.0
        if len(energy_types) > len(attack["cost"]) + 1:
            score -= 12.0 * (len(energy_types) - len(attack["cost"]) - 1)
        candidate = {
            "ready": missing == 0,
            "missing": missing,
            "damage": damage,
            "score": score,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate
    return best


def board_cards(state, player):
    ps = players(state)
    if player < 0 or player >= len(ps):
        return []
    active = [("active", 4, i, card) for i, card in enumerate(ps[player].get("active") or [])]
    bench = [("bench", 5, i, card) for i, card in enumerate(ps[player].get("bench") or [])]
    return active + bench


def board_cards_only(state, player):
    return [card for _, _, _, card in board_cards(state, player)]


def card_id(card):
    if isinstance(card, dict):
        return as_int(card.get("id"), 0)
    return as_int(card, 0)


def hand_count(state, player):
    ps = players(state)
    if player < 0 or player >= len(ps):
        return 0
    return as_int(ps[player].get("handCount"), len(card_list(state, player, 2, {})))


def hand_ids(state, player):
    return [card_id(card) for card in card_list(state, player, 2, {})]


def active_card(state, player):
    cards = card_list(state, player, 4, {})
    return cards[0] if cards else None


def viable_line_count(state, player):
    total = 0
    for card in board_cards_only(state, player):
        if card_id(card) not in CORE_BOARD_LINES:
            continue
        hp = as_int(card.get("hp"), as_int(card.get("maxHp"), 1))
        if hp > 0:
            total += 1
    return total


def bench_count(state, player):
    ps = players(state)
    if player < 0 or player >= len(ps):
        return 0
    return len(ps[player].get("bench") or [])


def visible_copy_count(state, player, wanted_id):
    ps = players(state)
    if player < 0 or player >= len(ps):
        return 0

    seen = set()

    def count_card(card):
        if not isinstance(card, dict):
            return 0
        serial = card.get("serial")
        key = (card.get("playerIndex", player), serial)
        if serial is not None and key in seen:
            return 0
        if serial is not None:
            seen.add(key)
        count = 1 if card_id(card) == wanted_id else 0
        for pre in card.get("preEvolution") or []:
            count += count_card(pre if isinstance(pre, dict) else {"id": pre})
        return count

    player_state = ps[player]
    total = 0
    for zone in ("active", "bench", "hand", "discard", "prize"):
        for card in player_state.get(zone) or []:
            total += count_card(card)
    return total


def poffin_target_capacity(state, player):
    accounted = (
        visible_copy_count(state, player, 344)
        + visible_copy_count(state, player, 345)
    )
    return max(0, 4 - accounted)


def poffin_progress_capacity(obs):
    state = current_state(obs)
    yi = your_index(state)
    bench_room = max(0, 3 - bench_count(state, yi))
    return min(bench_room, poffin_target_capacity(state, yi))


def required_line_count(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    opp_active = active_card(state, opp)
    opp_id = card_id(opp_active) if isinstance(opp_active, dict) else None
    if opp_id in DAMAGE_COUNTER_PRESSURE or any(
        card_id(card) in DAMAGE_COUNTER_PRESSURE for card in board_cards_only(state, opp)
    ):
        return 3
    return 2


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
    active_ability = card_id(active) in ABILITY_POKEMON_IDS
    any_ability = any(card_id(card) in ABILITY_POKEMON_IDS for _, _, _, card in cards)
    return active_ability, any_ability


def opponent_bypass_pressure(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    cards = board_cards(state, opp)
    active = active_card(state, opp)
    active_bypass = card_id(active) in BYPASS_EFFECT_ATTACKERS
    any_bypass = any(card_id(card) in BYPASS_EFFECT_ATTACKERS for _, _, _, card in cards)
    return active_bypass, any_bypass


def opponent_prize_count(obs):
    state = current_state(obs)
    opp = 1 - your_index(state)
    ps = players(state)
    if opp >= len(ps):
        return 6
    prize = ps[opp].get("prize")
    if isinstance(prize, list):
        return len(prize)
    return as_int(ps[opp].get("prizeCount"), 6)


def our_prize_count(obs):
    state = current_state(obs)
    yi = your_index(state)
    ps = players(state)
    if yi >= len(ps):
        return 6
    prize = ps[yi].get("prize")
    if isinstance(prize, list):
        return len(prize)
    return as_int(ps[yi].get("prizeCount"), 6)


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

    # --- INVARIANT 1: ANTI-BENCH-WIPE SAFEGUARD ---
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

    if cid in DRAW_SEARCH_CARDS:
        score += 180.0
    lines_needed = max(0, required_line_count(obs) - viable_line_count(state, yi))
    if cid == 1086:
        capacity = poffin_progress_capacity(obs)
        if capacity <= 0:
            return -5000.0
        if cur_bench > 0 and viable_line_count(state, yi) >= 3:
            return -5000.0
        if lines_needed:
            score += 520.0 * min(lines_needed, capacity)
    elif cid == 1152 and lines_needed:
        score += 420.0
    if cid in DISRUPTION_CARDS:
        score += 70.0 + hp_pressure_bonus(obs, 90)

    # --- INVARIANT 2: ALAKAZAM & HAND CONTROL DISRUPTION ---
    opponent_hand = hand_count(state, 1 - yi)
    if cid == 1197:  # Xerosic's Machinations
        if opponent_hand <= 3:
            return -850.0
        score += (opponent_hand - 3) * 350.0
        if opponent_hand >= 4:
            score += 3500.0

    active = active_card(state, yi)
    active_missing_hp = 0
    if isinstance(active, dict):
        active_missing_hp = max(0, as_int(active.get("maxHp"), 0) - as_int(active.get("hp"), 0))

    if cid in (1147, 1212) and active_missing_hp >= 40:
        score += 850.0

    active_bypass, any_bypass = opponent_bypass_pressure(obs)
    if cid == 1159:  # Hero's Cape (+100 HP)
        if active_bypass or any_bypass:
            score += 2000.0
        elif isinstance(active, dict) and card_id(active) in (117, 345):
            score += 800.0

    if cid == 1198:
        score += 120.0
        if any(card_id(card) in ENERGY_CARDS for card in hand):
            score += 80.0
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
        if active_bypass or any_bypass:
            score += 550.0
        elif active_ability or any_ability:
            score += 280.0
        elif not active_ex and not any_ex:
            score += 180.0
    elif target_cid in (344, 345):
        if active_bypass or any_bypass:
            score -= 150.0
        elif active_ex:
            score += 350.0  # High priority to power up Crustle facing ex

    if base["ready"]:
        score -= 250.0
    elif with_energy["ready"]:
        score += 750.0
    else:
        score += (with_energy["score"] - base["score"]) * 2.2

    if option.get("inPlayArea") == 4:
        score += 80.0
    return score


def score_option(obs, option):
    if not isinstance(option, dict):
        return -5000.0
    option_type = option.get("type", 0)
    base_score = BASE_TYPE_SCORE.get(option_type, 0.0)

    if option_type == 7:
        return score_play_from_hand(obs, option)

    if option_type == 8:
        card = option_card(obs, option)
        if card_id(card) in ENERGY_CARDS:
            return score_energy_attachment(obs, option)

    if option_type == 13:
        attack_id = option.get("index")
        damage = ATTACK_DAMAGE_BY_ID.get(attack_id, 100)
        score = base_score + damage * 1.5 + hp_pressure_bonus(obs, damage)
        state = current_state(obs)
        opp_active = active_card(state, 1 - your_index(state))
        opp_id = card_id(opp_active) if isinstance(opp_active, dict) else 0
        if opp_id in DAMAGE_COUNTER_PRESSURE:
            score += 500.0

        our_active = active_card(state, your_index(state))
        if isinstance(our_active, dict) and card_id(our_active) == 344 and damage == 0:
            score += 350.0  # Ascension bonus for active Dwebble to evolve into Crustle

        return score

    if option_type == 10:  # Promotion
        target = target_card(obs, option)
        if not isinstance(target, dict):
            return -100.0
        target_id = card_id(target)
        r = readiness(target)
        state = current_state(obs)
        opp = 1 - your_index(state)
        active_ex, any_ex = opponent_ex_pressure(obs)
        active_ability, any_ability = opponent_ability_pressure(obs)

        score = base_score + r["score"]
        if target_id == 345 and (active_ex or any_ex):
            score += 3000.0  # Crustle walls ex (Mega Lucario ex)
        elif target_id == 117 and (active_ability or any_ability):
            score += 3000.0  # Cornerstone walls Ability (Grimmsnarl / Munkidori)
        return score

    return base_score


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

    opp_prizes = opponent_prize_count(obs)
    our_prizes = our_prize_count(obs)
    if cur_bench > 0 and (opp_prizes <= 1 or our_prizes <= 1):
        return None

    options = select_state(obs).get("option") or []

    def play_id(index):
        return card_id(option_card(obs, options[index]))

    def best_index(predicate):
        choices = [(score, index) for score, index in ranked if predicate(index)]
        return choices[0][1] if choices else None

    if cur_bench == 0:
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and play_id(index) in BASIC_SETUP_POKEMON
        )
        if choice is None:
            choice = best_index(
                lambda index: options[index].get("type") == 7
                and play_id(index) == 1086
                and poffin_progress_capacity(obs) > 0
            )
        if choice is None:
            choice = best_index(
                lambda index: options[index].get("type") == 7
                and play_id(index) == 1152
            )
        if choice is not None:
            ATTACK_DEFERRALS[turn_key] = ATTACK_DEFERRALS.get(turn_key, 0) + 1
            return choice

    lines_needed = max(0, required_line_count(obs) - viable_line_count(state, yi))
    choice = None
    if lines_needed:
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and play_id(index) == 344
        )
        if choice is None:
            choice = best_index(
                lambda index: options[index].get("type") == 7
                and play_id(index) == 1086
                and poffin_progress_capacity(obs) > 0
            )

    if choice is None and hand_count(state, 1 - yi) >= 4:
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and play_id(index) == 1197
        )

    if choice is None and not bool(state.get("energyAttached")):
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) in ENERGY_CARDS
            and not readiness(target_card(obs, options[index]))["ready"]
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
    reset_attack_memory(current_state(obs))
    options = select.get("option") or []
    min_count = as_int(select.get("minCount"), 0)
    max_count = as_int(select.get("maxCount"), 0)
    if not options or max_count <= 0:
        return []

    ranked = sorted(
        ((score_option(obs, option), index) for index, option in enumerate(options)),
        key=lambda item: (-item[0], item[1]),
    )

    if card_id(select.get("effect")) == 1086:
        state = current_state(obs)
        cur_bench = bench_count(state, your_index(state))
        line_capacity = 2 if cur_bench == 0 else max(0, 3 - viable_line_count(state, your_index(state)))
        take = min(max_count, line_capacity)
        if take < min_count:
            take = min_count
        return [index for score, index in ranked if score > 0][:take]

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


def agent(obs):
    """Kaggle executes the final function defined in this file."""
    return safe_action(obs)
