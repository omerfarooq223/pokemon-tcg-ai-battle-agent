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
    13: "C",
    19: "P",
    7: "D",
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

# Cost symbols use C for colorless. The profiles are intentionally compact and cover
# our deck's attackers; unknown Pokemon fall back to simple attached-energy scoring.
ATTACKS = {
    104: [{"cost": ["W", "C"], "damage": 60, "name": "Frost Smash"}],
    112: [{"cost": ["P", "C"], "damage": 60, "name": "Mind Bend"}],
    646: [{"cost": ["D"], "damage": 10, "name": "Corkscrew Punch"}],
    647: [{"cost": ["D", "D"], "damage": 60, "name": "Corkscrew Punch"}],
    648: [{"cost": ["D", "D"], "damage": 180, "name": "Shadow Bullet"}],
    860: [{"cost": ["W"], "damage": 10, "name": "Chilly"}],
    66: [{"cost": ["C", "C", "C"], "damage": 90, "name": "Land Crush"}],
    140: [{"cost": ["C", "C", "C"], "damage": 100, "name": "Cruel Arrow"}],
    305: [{"cost": ["C", "C"], "damage": 20, "name": "Ram"}],
    343: [{"cost": ["C", "C"], "damage": 30, "name": "Smash Kick"}],
    741: [{"cost": ["P"], "damage": 10, "name": "Teleportation Attack"}],
    742: [{"cost": ["P"], "damage": 30, "name": "Super Psy Bolt"}],
    743: [{"cost": ["P"], "damage": 200, "name": "Powerful Hand"}],
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
    934: 60,
    935: 10,
    936: 60,
    937: 180,
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
    1070: 30,
    1072: 200,
}

POKEMON_ROLE = {
    648: 420.0,
    647: 330.0,
    646: 280.0,
    112: 230.0,
    104: 150.0,
    860: 90.0,
    743: 360.0,
    742: 300.0,
    741: 260.0,
    66: 170.0,
    305: 150.0,
    140: 115.0,
    343: 90.0,
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

# Card metadata is not included in each observation.  This compact ID set lets the
# planner distinguish the ex matchups where Crustle's damage immunity is decisive
# from ordinary one-prize attackers where Diggersby's faster damage is preferable.
EX_POKEMON = {
    24, 29, 30, 37, 40, 44, 46, 52, 63, 75, 79, 80, 83, 84, 96, 99, 107,
    108, 117, 121, 125, 130, 138, 139, 140, 141, 150, 153, 154, 161, 176,
    179, 184, 189, 190, 193, 198, 205, 207, 210, 223, 229, 231, 232, 236,
    239, 241, 243, 244, 246, 248, 249, 259, 269, 272, 283, 293, 299, 302,
    306, 313, 316, 320, 326, 328, 329, 331, 336, 337, 340, 357, 369, 372,
    381, 389, 404, 407, 424, 431, 447, 455, 458, 471, 481, 509, 515, 525,
    527, 547, 561, 573, 583, 598, 618, 631, 641, 648, 652, 662, 678, 687,
    695, 723, 737, 747, 754, 756, 766, 772, 781, 790, 795, 806, 813, 828,
    835, 849, 861, 868, 886, 896, 904, 911, 919, 928, 932, 939, 944, 951,
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

DRAW_SEARCH_CARDS = {
    1080, 1086, 1097, 1121, 1152, 1219, 1227, 1231, 1259,
}
DISRUPTION_CARDS = {1182, 1197}
ENERGY_CARDS = set(ENERGY_CARD_TYPES)
ABILITY_POKEMON = {104, 112, 648}
BASIC_SETUP_POKEMON = {112, 646, 860}


def agent_path(filename):
    kaggle_path = os.path.join("/kaggle_simulations/agent", filename)
    if os.path.exists(kaggle_path):
        return kaggle_path
    source_path = globals().get("__file__", "")
    local_dir = os.path.dirname(os.path.abspath(source_path)) if source_path else os.getcwd()
    return os.path.join(local_dir, filename)


def load_deck():
    with open(agent_path("deck.csv"), encoding="utf-8-sig") as handle:
        return [int(line.strip().split(",")[0]) for line in handle if line.strip()]


DECK = load_deck()
ATTACK_DEFERRALS = {}
ATTACK_MENU_STATES = {}
LAST_TURN_SEEN = None
MAX_ATTACK_DEFERRALS = 8
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


def active_card(state, player):
    cards = card_list(state, player, 4, {})
    return cards[0] if cards else None


def best_board_readiness(state, player):
    best = None
    for zone, area, index, card in board_cards(state, player):
        r = readiness(card)
        active_bonus = 80.0 if area == 4 else 0.0
        score = r["score"] + active_bonus + POKEMON_ROLE.get(card.get("id"), 0.0) * 0.2
        candidate = (score, area, index, card, r)
        if best is None or candidate[0] > best[0]:
            best = candidate
    return best


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
    any_ability = any(
        card_id(card) in ABILITY_POKEMON_IDS for _, _, _, card in cards
    )
    return active_ability, any_ability


def board_target_score(obs, target, extra_energy=None, source_energy_index=None):
    if not isinstance(target, dict):
        return 0.0
    state = current_state(obs)
    yi = your_index(state)
    r_now = readiness(target)
    r_after = readiness(target, extra_energy=extra_energy)
    improvement = r_after["score"] - r_now["score"]
    score = r_after["score"] + improvement * 1.8
    if r_after["ready"] and not r_now["ready"]:
        score += 340.0
    if r_after["missing"] == 1:
        score += 90.0
    if target in card_list(state, yi, 4, {}):
        score += 180.0
    else:
        active = active_card(state, yi)
        if not isinstance(active, dict) or not readiness(active)["ready"]:
            score += 45.0
    active_ex, any_ex = opponent_ex_pressure(obs)
    active_ability, any_ability = opponent_ability_pressure(obs)
    if target.get("id") == 345:
        score += 360.0 if active_ex else (150.0 if any_ex else 0.0)
    elif target.get("id") == 344:
        score += 140.0 if any_ex else 0.0
    elif target.get("id") == 117:
        score += 440.0 if active_ability else (100.0 if any_ability else -120.0)
    elif target.get("id") == 1074 and not active_ex:
        score += 180.0
    score += POKEMON_ROLE.get(target.get("id"), 0.0)
    return score


def card_id(card):
    return card.get("id") if isinstance(card, dict) else None


def hand_ids(state, player):
    return [card_id(card) for card in card_list(state, player, 2, {})]


def hand_count(state, player):
    ps = players(state)
    if player < 0 or player >= len(ps):
        return 0
    return as_int(ps[player].get("handCount"), len(card_list(state, player, 2, {})))


def score_play_from_hand(obs, option):
    state = current_state(obs)
    yi = your_index(state)
    hand = card_list(state, yi, 2, {})
    idx = option.get("index")
    cid = card_id(hand[idx]) if isinstance(idx, int) and 0 <= idx < len(hand) else None
    score = BASE_TYPE_SCORE[7]
    if cid in DRAW_SEARCH_CARDS:
        score += 180.0
    if cid in {1225, 1231}:
        score += 300.0
    if cid in DISRUPTION_CARDS:
        score += 70.0 + hp_pressure_bonus(obs, 90)
    if cid == 1198:
        score += 120.0
        if any(card_id(card) in ENERGY_CARDS for card in hand):
            score += 80.0
    if cid == 1116:
        score += 100.0
        best = best_board_readiness(state, yi)
        if best and not best[4]["ready"]:
            score += 110.0
    if cid == 1098:
        score += 120.0
    if cid == 1088:
        score += 160.0
    if cid in POKEMON_ROLE:
        bench = card_list(state, yi, 5, {})
        if len(bench) >= 8:
            score -= 260.0
        else:
            score += POKEMON_ROLE[cid]
            if cid == 741:
                score += 220.0
            if cid == 756 and not any(card_id(c) == 756 for c in board_cards_only(state, yi)):
                score += 90.0
    if as_int(state.get("supporterPlayed"), 0) and cid in {1182, 1197, 1198, 1205}:
        score -= 250.0
    return score


def board_cards_only(state, player):
    return [entry[3] for entry in board_cards(state, player)]


def energy_fit_bonus(target, energy_id):
    if not isinstance(target, dict) or energy_id not in ENERGY_CARD_TYPES:
        return 0.0
    target_id = target.get("id")
    energy_type = ENERGY_CARD_TYPES[energy_id]
    attached = attached_types(target)

    if target_id in (741, 742, 743):
        if energy_type == "P":
            return 240.0 if "P" not in attached else -20.0
        return -400.0 if "P" not in attached else 5.0
    if target_id in (112, 646, 647, 648):
        if energy_type == "D":
            return 240.0 if "D" not in attached else 60.0
        return -380.0 if "D" not in attached else 5.0
    if target_id in (66, 140, 305, 343):
        return 45.0
    if target_id == 96:
        return 130.0 if energy_type == "G" else -320.0
    if target_id == 117:
        if energy_type == "F":
            return 170.0 if "F" not in attached else 20.0
        return -260.0 if "F" not in attached else 45.0
    if target_id == 63:
        if energy_type not in ("L", "F"):
            return -300.0
        return 140.0 if energy_type not in attached else 30.0
    if target_id == 184:
        psychic_count = attached.count("P")
        if energy_type == "P":
            return 135.0 if psychic_count < 2 else 30.0
        return -240.0 if psychic_count < 2 else 15.0
    if target_id == 108:
        if energy_type == "W":
            return 130.0 if "W" not in attached else 25.0
        return -220.0 if "W" not in attached else 20.0
    if target_id == 978:
        if energy_type == "F":
            return 125.0 if "F" not in attached else 20.0
        return -210.0 if "F" not in attached else 15.0
    if target_id == 272:
        if energy_type == "P":
            return 110.0 if "P" not in attached else 25.0
        return -170.0 if "P" not in attached else 10.0
    if target_id == 345:
        if energy_type == "G":
            return 135.0 if "G" not in attached else 30.0
        return -180.0 if "G" not in attached else 5.0
    if target_id == 344:
        return 110.0 if energy_type == "G" else 45.0
    if target_id in (397, 398):
        return 145.0 if energy_type == "G" and not attached else 15.0
    if target_id in (796, 797):
        return 145.0 if energy_type == "R" and not attached else -180.0
    if target_id in (1073, 1074):
        return 150.0 if not attached else -80.0
    if target_id in (756, 1071, 140):
        return 55.0
    return 0.0


def energy_board_fit_score(obs, energy_id):
    state = current_state(obs)
    yi = your_index(state)
    best = None
    for _, area, _, card in board_cards(state, yi):
        before = readiness(card)
        after = readiness(card, extra_energy=energy_id)
        score = (after["score"] - before["score"]) * 2.0
        score += energy_fit_bonus(card, energy_id)
        if before["ready"]:
            score -= 520.0
        elif after["ready"]:
            score += 620.0
        elif after["missing"] == 1:
            score += 300.0
        elif after["missing"] == 2:
            score += 100.0
        if area == 5:
            score += 80.0
        if best is None or score > best:
            best = score
    return best if best is not None else -900.0


def score_attach_or_evolve(obs, option):
    moving = option_card(obs, option)
    target = target_card(obs, option)
    cid = card_id(moving)
    score = BASE_TYPE_SCORE.get(option.get("type"), 0.0)
    if cid in ENERGY_CARDS:
        if as_int(current_state(obs).get("energyAttached"), 0) and option.get("area") == 2:
            score -= 120.0
        score += board_target_score(obs, target, extra_energy=cid)
        score += energy_fit_bonus(target, cid)
        if target and target.get("id") == 756:
            score += 75.0
        if target and target.get("id") == 96 and cid == 1:
            score += 55.0
        if target and target.get("id") == 184 and cid == 5:
            score += 55.0
        if target and target.get("id") == 108 and cid == 3:
            score += 55.0
        if target and target.get("id") == 63 and cid in (4, 6):
            score += 45.0
    elif cid in POKEMON_ROLE:
        score += POKEMON_ROLE[cid]
        if option.get("inPlayArea") == 4:
            score += 40.0
    elif cid in DRAW_SEARCH_CARDS:
        score += 80.0
    else:
        score += 20.0
    return score


def score_board_action(obs, option):
    state = current_state(obs)
    yi = your_index(state)
    source = option_card(obs, option)
    score = BASE_TYPE_SCORE.get(option.get("type"), 0.0)
    if isinstance(source, dict):
        cid = source.get("id")
        if cid == 1248:
            # Academy at Night can create a no-progress loop by putting the only
            # hand card on top every turn and drawing it again next turn.
            return -5000.0
        score += POKEMON_ROLE.get(cid, 0.0) * 0.7
        r = readiness(source)
        if option.get("area") == 4:
            score += 90.0
        if r["ready"]:
            score += 160.0
        elif r["missing"] == 1:
            score += 120.0
        if cid == 96 and 1 in hand_ids(state, yi):
            score += 280.0
        if cid in ABILITY_POKEMON:
            score += 70.0
        if cid in (104, 112, 648):
            score += 520.0
    return score


def score_target_selection(obs, option):
    state = current_state(obs)
    select = select_state(obs)
    yi = your_index(state)
    context = select.get("context")
    owner = option.get("playerIndex", yi)
    card = option_card(obs, option)
    cid = card_id(card)
    area = option.get("area")
    score = BASE_TYPE_SCORE[3]

    effect_id = card_id(select.get("effect"))
    if (
        context == 7
        and effect_id == 1198
        and cid in ENERGY_CARDS
    ):
        # Crispin puts this first choice into hand, then attaches a different type.
        # Preserve the best-fitting energy for the following ATTACH_TO selection.
        return 3000.0 - energy_board_fit_score(obs, cid)
    if (
        context == 22
        and effect_id in {1198, 1235}
        and cid in ENERGY_CARDS
    ):
        fit = energy_board_fit_score(obs, cid)
        return score + fit if fit > 0 else -120.0

    if owner == yi and area in (4, 5):
        if context == 21:
            energy_id = card_id(select.get("contextCard"))
            before = readiness(card)
            after = readiness(card, extra_energy=energy_id)
            improvement = after["score"] - before["score"]
            score += improvement * 2.0
            if before["ready"]:
                score -= 520.0
            elif after["ready"]:
                score += 620.0
            elif after["missing"] == 1:
                score += 320.0
            elif after["missing"] == 2:
                score += 120.0
            if area == 5:
                score += 180.0
            score += POKEMON_ROLE.get(cid, 0.0) * 0.35
            return score
        score += board_target_score(obs, card)
        if context in (4, 43):
            score += 260.0 if readiness(card)["ready"] else 0.0
            score += 120.0 if area == 5 else 0.0
    elif owner != yi and area in (4, 5):
        score += 130.0
        if isinstance(card, dict):
            damage = as_int(card.get("maxHp"), 0) - as_int(card.get("hp"), 0)
            score += damage * 0.7
            score += len(card.get("energies") or []) * 45.0
            if area == 4:
                score += 85.0
    elif area in (1, 2, 12, 3):
        score += card_pick_score(obs, cid, area, context)
    return score


def card_pick_score(obs, cid, area, context):
    state = current_state(obs)
    yi = your_index(state)
    score = 0.0
    active = active_card(state, yi)
    active_r = readiness(active)
    if cid in ENERGY_CARDS:
        score += 90.0
        if active and not active_r["ready"]:
            score += board_target_score(obs, active, extra_energy=cid) * 0.35
    if cid in POKEMON_ROLE:
        score += POKEMON_ROLE[cid]
        if cid == 756:
            score += 80.0
        if len(card_list(state, yi, 5, {})) >= 7:
            score -= 130.0
    if cid in DRAW_SEARCH_CARDS:
        score += 130.0
    if cid in DISRUPTION_CARDS:
        score += 55.0
    if context == 8:
        if cid in ENERGY_CARDS and active and not active_r["ready"]:
            score += 70.0
        if cid in {184, 978, 1071}:
            score -= 35.0
    if area == 3 and cid in ENERGY_CARDS:
        score += 80.0
    return score


def score_energy_source(obs, option):
    state = current_state(obs)
    yi = your_index(state)
    card = option_card(obs, option)
    if not isinstance(card, dict):
        return BASE_TYPE_SCORE[5]
    energy_index = option.get("energyIndex")
    before = readiness(card)
    after = readiness(card, remove_energy_index=energy_index)
    score = BASE_TYPE_SCORE[5] + (after["score"] - before["score"]) * 1.4
    if before["ready"] and not after["ready"]:
        score -= 320.0
    if card in card_list(state, yi, 4, {}):
        score -= 120.0
    if before["missing"] >= 2:
        score += 90.0
    return score


def score_attack(obs, option):
    state = current_state(obs)
    yi = your_index(state)
    active = active_card(state, yi)
    r = readiness(active)
    attack_id = option.get("attackId")
    damage = ATTACK_DAMAGE_BY_ID.get(as_int(attack_id, -1), r["damage"])
    if card_id(active) == 743:
        damage = max(damage, hand_count(state, yi) * 20)
    score = BASE_TYPE_SCORE[13] + damage * 1.8 + hp_pressure_bonus(obs, damage)
    return score


def score_option(obs, option):
    option_type = option.get("type")
    if option_type == 13:
        return score_attack(obs, option)
    if option_type in (8, 9):
        return score_attach_or_evolve(obs, option)
    if option_type == 10:
        return score_board_action(obs, option)
    if option_type == 7:
        return score_play_from_hand(obs, option)
    if option_type == 3:
        return score_target_selection(obs, option)
    if option_type == 5:
        return score_energy_source(obs, option)
    score = BASE_TYPE_SCORE.get(option_type, 0.0)
    if option_type == 12:
        score += 40.0
    if option_type == 14 and any(candidate.get("type") != 14 for candidate in select_state(obs).get("option") or []):
        score -= 900.0
    return score


def attack_menu_signature(obs):
    state = current_state(obs)
    select = select_state(obs)
    yi = your_index(state)

    def card_signature(card):
        if not isinstance(card, dict):
            return None
        return (
            card.get("id"),
            card.get("serial"),
            as_int(card.get("hp"), 0),
            tuple(card.get("energies") or []),
            tuple(
                (tool.get("id"), tool.get("serial"))
                for tool in card.get("tools") or []
                if isinstance(tool, dict)
            ),
        )

    board = tuple(card_signature(card) for _, _, _, card in board_cards(state, yi))
    hand = tuple(
        (card.get("id"), card.get("serial"))
        for card in card_list(state, yi, 2, {})
        if isinstance(card, dict)
    )
    options = tuple(
        (
            option.get("type"),
            option.get("area"),
            option.get("index"),
            option.get("inPlayArea"),
            option.get("inPlayIndex"),
            option.get("attackId"),
            option.get("playerIndex"),
            option.get("energyIndex"),
            option.get("count"),
        )
        for option in select.get("option") or []
    )
    return (
        as_int(state.get("turnActionCount"), 0),
        bool(state.get("supporterPlayed")),
        bool(state.get("energyAttached")),
        board,
        hand,
        options,
    )


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
    signature = attack_menu_signature(obs)
    seen = ATTACK_MENU_STATES.setdefault(turn_key, set())
    if signature in seen:
        return None
    seen.add(signature)

    if ATTACK_DEFERRALS.get(turn_key, 0) >= MAX_ATTACK_DEFERRALS:
        return None

    options = select_state(obs).get("option") or []
    active = active_card(state, yi)
    active_missing_hp = 0
    if isinstance(active, dict):
        active_missing_hp = max(
            0,
            as_int(active.get("maxHp"), 0) - as_int(active.get("hp"), 0),
        )

    def play_id(index):
        return card_id(option_card(obs, options[index]))

    def best_index(predicate):
        choices = [(score, index) for score, index in ranked if predicate(index)]
        return choices[0][1] if choices else None

    board_size = len(board_cards(state, yi))
    choice = None
    if board_size == 1:
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and play_id(index) == 1086
        )
        if choice is None:
            choice = best_index(
                lambda index: options[index].get("type") == 7
                and play_id(index) in BASIC_SETUP_POKEMON
            )

    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 9
        )

    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 10
            and card_id(option_card(obs, options[index])) in {104, 112, 648}
        )

    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and play_id(index) == 1159
            and options[index].get("inPlayArea") == 4
        )

    if choice is None:
        has_dwebble = any(
            card_id(card) == 344 for _, _, _, card in board_cards(state, yi)
        )
        has_crustle = 345 in hand_ids(state, yi)
        can_evolve = any(option.get("type") == 9 for option in options)
        if has_dwebble and not has_crustle and not can_evolve:
            choice = best_index(
                lambda index: options[index].get("type") == 7
                and play_id(index) == 1152
            )

    if choice is None and not bool(state.get("energyAttached")):
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) in ENERGY_CARDS
            and options[index].get("inPlayArea") == 5
            and not readiness(target_card(obs, options[index]))["ready"]
        )

    if choice is None:
        for setup_id in (1219, 1227, 1231, 1152, 1086, 1097, 1259):
            choice = best_index(
                lambda index, cid=setup_id: options[index].get("type") == 7
                and play_id(index) == cid
            )
            if choice is not None:
                break

    if choice is None:
        return None

    ATTACK_DEFERRALS[turn_key] = ATTACK_DEFERRALS.get(turn_key, 0) + 1
    return choice


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


def safe_action(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        minimum = as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(select.get("option") or []))))


def agent(obs):
    """Kaggle executes the final function defined in this file."""
    return safe_action(obs)
