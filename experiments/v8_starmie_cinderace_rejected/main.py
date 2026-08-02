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
    17: "C",
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

# Cost symbols use C for colorless. The profiles are intentionally compact and cover
# our deck's attackers; unknown Pokemon fall back to simple attached-energy scoring.
ATTACKS = {
    666: [{"cost": ["C"], "damage": 50, "name": "Turbo Flare"}],
    1030: [{"cost": ["W"], "damage": 20, "name": "Water Gun"}],
    1031: [
        {"cost": ["W"], "damage": 120, "name": "Jetting Blow"},
        {"cost": ["C", "C", "C"], "damage": 210, "name": "Nebula Beam"},
    ],
}

ATTACK_DAMAGE_BY_ID = {
    1486: 20,
    1487: 120,
    1488: 210,
}

POKEMON_ROLE = {
    1031: 420.0,
    1030: 300.0,
    666: 230.0,
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

DRAW_SEARCH_CARDS = {1086, 1097, 1121, 1122, 1145, 1189, 1225, 1227}
DISRUPTION_CARDS = {1120, 1182, 1223}
SUPPORTER_CARDS = {1182, 1189, 1223, 1225, 1227, 1229}
ENERGY_CARDS = set(ENERGY_CARD_TYPES)
ABILITY_POKEMON = {666}
BASIC_SETUP_POKEMON = {666, 1030}

# Pokémon whose attacks place or move damage counters, cause delayed effects,
# or impose attack effects that Mist Energy can prevent. These profiles come
# from the supplied English card data and are independent of opponent identity.
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

# HP thresholds where specific attackers guarantee KO. Used to avoid
# wasting setup turns when lethal damage is already achievable.
# Crustle (117) Demolish: 140. Incineroar (797) Infernal Slash: 220.
# Diggersby (1074) Earthquake: 140. Tsareena (398) Petal Blade Dance: 130.
KO_HP_BY_ATTACKER = {666: 50, 1030: 20, 1031: 210}


def agent_path(filename):
    kaggle_path = os.path.join("/kaggle_simulations/agent", filename)
    if os.path.exists(kaggle_path):
        return kaggle_path
    source_path = globals().get("__file__", "")
    local_dir = os.path.dirname(os.path.abspath(source_path)) if source_path else os.getcwd()
    return os.path.join(local_dir, filename)


EXPECTED_DECK = [
    666, 666, 666, 666, 1030, 1030, 1030, 1031, 1031, 1031, 1086,
    1086, 1086, 1086, 1097, 1097, 1120, 1120, 1120, 1120, 1121, 1122,
    1122, 1122, 1122, 1145, 1145, 1145, 1145, 1159, 1182, 1189, 1189,
    1189, 1189, 1223, 1223, 1225, 1225, 1227, 1227, 1227, 1227, 1229,
    1229, 1229, 1229, 17, 17, 17, 17, 3, 3, 3, 3, 3, 3, 3, 3, 3,
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
    for energy_card in card.get("energyCards") or []:
        if card_id(energy_card) == 17:
            result.extend(("C", "C"))
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
        if extra_energy == 17:
            energy_types.extend(("C", "C"))
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


def opponent_prize_count(obs):
    """Estimate opponent remaining prizes from deck state."""
    state = current_state(obs)
    opp = 1 - your_index(state)
    ps = players(state)
    if opp >= len(ps):
        return 6
    return as_int(ps[opp].get("prizeCount"), 6)


def our_prize_count(obs):
    """Our remaining prizes."""
    state = current_state(obs)
    yi = your_index(state)
    ps = players(state)
    if yi >= len(ps):
        return 6
    return as_int(ps[yi].get("prizeCount"), 6)


def can_ko_active_opponent(obs, attacker_id):
    """Return True if the named attacker can OHKO the current opponent active."""
    state = current_state(obs)
    opp = 1 - your_index(state)
    target = active_card(state, opp)
    if not isinstance(target, dict):
        return False
    hp = as_int(target.get("hp"), 0)
    damage = KO_HP_BY_ATTACKER.get(attacker_id, 0)
    return hp > 0 and damage >= hp


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
    target_id = target.get("id")
    if target_id == 1031:
        score += 420.0
        if r_after["damage"] >= 210 and r_after["ready"]:
            score += 260.0
    elif target_id == 1030:
        score += 180.0
        if 1031 in hand_ids(state, yi):
            score += 160.0
    elif target_id == 666:
        score += 120.0
        if target in card_list(state, yi, 4, {}):
            score += 160.0
    score += POKEMON_ROLE.get(target.get("id"), 0.0)
    # Late-game boost: push key attackers harder when prizes are low
    opp_prizes = opponent_prize_count(obs)
    our_prizes = our_prize_count(obs)
    if opp_prizes <= 2 and target.get("id") in KO_HP_BY_ATTACKER:
        score += 200.0
    if our_prizes <= 2:
        # We're close to winning; strongly prefer ready attackers
        if r_after["ready"]:
            score += 280.0
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
    if cid in DISRUPTION_CARDS:
        score += 70.0 + hp_pressure_bonus(obs, 90)
    board_ids = {card_id(card) for card in board_cards_only(state, yi)}
    hand_size = len(hand)
    if cid == 1145:
        score += 500.0 if 1031 not in hand_ids(state, yi) else 80.0
    elif cid == 1189:
        score += 620.0 if 1030 in board_ids and 1031 not in board_ids else -180.0
    elif cid == 1225:
        score += 380.0 if 1031 not in hand_ids(state, yi) else 150.0
    elif cid == 1227:
        score += max(0, 7 - hand_size) * 95.0
    elif cid == 1229:
        active = active_card(state, yi)
        missing_hp = (
            as_int(active.get("maxHp"), 0) - as_int(active.get("hp"), 0)
            if isinstance(active, dict) and card_id(active) == 1031
            else 0
        )
        if missing_hp <= 0:
            return -900.0
        score += missing_hp * 4.0
    elif cid == 1223:
        opponent_hand = hand_count(state, 1 - yi)
        score += max(0, opponent_hand - hand_size) * 55.0
    elif cid == 1120:
        score += 120.0
    if cid in POKEMON_ROLE:
        bench = card_list(state, yi, 5, {})
        if len(bench) >= 8:
            score -= 260.0
        else:
            score += POKEMON_ROLE[cid]
            if cid == 756 and not any(card_id(c) == 756 for c in board_cards_only(state, yi)):
                score += 90.0
    if as_int(state.get("supporterPlayed"), 0) and cid in SUPPORTER_CARDS:
        score -= 1200.0
    # Healing: strongly prefer when our active is low on HP
    if cid in (1147, 1212):
        active = active_card(state, yi)
        if isinstance(active, dict):
            missing_hp = as_int(active.get("maxHp"), 0) - as_int(active.get("hp"), 0)
            if missing_hp >= 80:
                score += 180.0
            elif missing_hp >= 40:
                score += 80.0
    return score


def board_cards_only(state, player):
    return [entry[3] for entry in board_cards(state, player)]


def energy_fit_bonus(target, energy_id):
    if not isinstance(target, dict) or energy_id not in ENERGY_CARD_TYPES:
        return 0.0
    target_id = target.get("id")
    energy_type = ENERGY_CARD_TYPES[energy_id]
    attached = attached_types(target)

    if target_id in (1030, 1031):
        if energy_id == 17:
            return 520.0 if target_id == 1031 else 120.0
        if energy_type == "W":
            if "W" not in attached:
                return 260.0
            return 90.0 if len(attached) < 3 else -80.0
        return -260.0
    if target_id == 666:
        if energy_id == 17:
            return 80.0
        return 180.0 if not attached else -90.0
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


def colored_requirements_paid(card):
    attached = attached_types(card)
    attacks = ATTACKS.get(card_id(card)) or []
    for attack in attacks:
        colored_cost = [
            symbol for symbol in attack.get("cost") or [] if symbol != "C"
        ]
        if cost_missing(colored_cost, attached) == 0:
            return True
    return not attacks


def score_attach_or_evolve(obs, option):
    moving = option_card(obs, option)
    target = target_card(obs, option)
    cid = card_id(moving)
    score = BASE_TYPE_SCORE.get(option.get("type"), 0.0)
    if cid in ENERGY_CARDS:
        attacks = ATTACKS.get(card_id(target)) or []
        before = readiness(target)
        useful_cost = max(
            (len(attack.get("cost") or []) for attack in attacks),
            default=None,
        )
        if (
            before["ready"]
            and useful_cost is not None
            and len(attached_types(target)) >= useful_cost
        ):
            # Once a profiled attacker is fully paid, preserve the Energy in
            # hand/deck instead of stacking it indefinitely in control games.
            return -1800.0
        if as_int(current_state(obs).get("energyAttached"), 0) and option.get("area") == 2:
            score -= 120.0
        score += board_target_score(obs, target, extra_energy=cid)
        score += energy_fit_bonus(target, cid)
        target_area = option.get("inPlayArea")
        if card_id(target) == 1031 and cid == 17:
            score += 900.0 if target_area == 4 else 520.0
        elif card_id(target) in (1030, 1031) and cid == 3:
            score += 260.0
        elif card_id(target) == 666 and cid == 3:
            score += 160.0
        # Extra urgency: attach to active when opponent can be KO'd next turn
        if target_area == 4 and card_id(target) in KO_HP_BY_ATTACKER:
            if can_ko_active_opponent(obs, card_id(target)):
                score += 140.0
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
        if cid in ABILITY_POKEMON:
            score += 70.0
        # Prefer retreating to a KO-ready benched attacker when opponent is vulnerable
        if option.get("area") == 4 and r["ready"] and can_ko_active_opponent(obs, cid):
            score += 350.0
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
    if context == 7 and effect_id == 1121 and area == 2:
        discard_value = 0.0
        if cid in POKEMON_ROLE:
            discard_value += POKEMON_ROLE[cid]
        if cid in ENERGY_CARDS:
            discard_value += 130.0
        if cid in DRAW_SEARCH_CARDS:
            discard_value += 60.0
        return -discard_value
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
            opponent = active_card(state, 1 - yi)
            opponent_hp = (
                as_int(opponent.get("hp"), 0) if isinstance(opponent, dict) else 0
            )
            if cid == 1031 and readiness(card)["ready"] and 0 < opponent_hp <= 210:
                score += 560.0
            elif cid == 1030 and readiness(card)["ready"] and 0 < opponent_hp <= 20:
                score += 360.0
            elif cid == 666 and readiness(card)["ready"] and 0 < opponent_hp <= 50:
                score += 420.0
        if effect_id == 1229:
            missing_hp = max(
                0,
                as_int(card.get("maxHp"), 0) - as_int(card.get("hp"), 0),
            )
            if cid != 1031 or missing_hp <= 0:
                return -1200.0
            score += missing_hp * 6.0
            if area == 4:
                score += 320.0
    elif owner != yi and area in (4, 5):
        score += 130.0
        if isinstance(card, dict):
            damage = as_int(card.get("maxHp"), 0) - as_int(card.get("hp"), 0)
            score += damage * 0.7
            score += len(card.get("energies") or []) * 45.0
            if area == 4:
                score += 85.0
            if area == 5 and 0 < as_int(card.get("hp"), 0) <= 50:
                score += 700.0
            # Strongly prefer already-damaged opponent targets (closer to KO)
            opp_cid = card_id(card)
            opp_hp = as_int(card.get("hp"), 0)
            opp_max_hp = as_int(card.get("maxHp"), 0)
            if opp_max_hp and opp_hp <= opp_max_hp * 0.4:
                score += 200.0
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
    hand = hand_ids(state, yi)
    effect_id = card_id(select_state(obs).get("effect"))
    if effect_id in {1145, 1189, 1225} and cid == 1031:
        score += 720.0
    if effect_id == 1086 and cid == 1030:
        board_ids = {card_id(card) for card in board_cards_only(state, yi)}
        score += 520.0 if 1030 not in board_ids else 180.0
    if effect_id == 1097:
        if cid == 1031:
            score += 420.0
        elif cid == 1030:
            score += 280.0
        elif cid == 3:
            score += 120.0
    if effect_id == 666 and cid == 3:
        score += 650.0
    hand_has_backup = any(card in BASIC_SETUP_POKEMON for card in hand)
    if (
        effect_id == 1086
        and area == 1
        and cid == 1030
        and len(board_cards(state, yi)) == 1
        and not hand_has_backup
    ):
        score += 300.0
    # When Poké Ball (1086) or similar search effects look for Basics, prefer
    # the strongest attacker that is missing only one energy step.
    if effect_id in (1086, 1152) and area == 1 and cid in POKEMON_ROLE:
        board_ids = {card_id(c) for c in board_cards_only(state, yi)}
        if cid not in board_ids:
            score += 60.0
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
    owner = option.get("playerIndex", card.get("playerIndex", yi))
    if owner != yi:
        score = BASE_TYPE_SCORE[5] + (before["score"] - after["score"]) * 1.8
        if card in card_list(state, 1 - yi, 4, {}):
            score += 180.0
        if before["ready"] and not after["ready"]:
            score += 420.0
        return score
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
    score = BASE_TYPE_SCORE[13] + damage * 1.8 + hp_pressure_bonus(obs, damage)
    # Prize pressure: prefer attacking over setup when prizes are low on either side
    opp_prizes = opponent_prize_count(obs)
    our_prizes = our_prize_count(obs)
    if opp_prizes <= 2 or our_prizes <= 2:
        score += 300.0
    # Bonus for attacks that can KO the active opponent
    opp = 1 - yi
    opp_active = active_card(state, opp)
    if isinstance(opp_active, dict):
        opp_hp = as_int(opp_active.get("hp"), 0)
        if opp_hp and damage >= opp_hp:
            score += 500.0
    active_id = card_id(active)
    if active_id == 1031 and as_int(attack_id, -1) == 1487:
        for opponent in card_list(state, 1 - yi, 5, {}):
            hp = as_int(opponent.get("hp"), 0) if isinstance(opponent, dict) else 0
            if 0 < hp <= 50:
                score += 620.0
            elif 0 < hp <= 100:
                score += 140.0
    elif active_id == 666:
        for _, area, _, teammate in board_cards(state, yi):
            if area == 5 and card_id(teammate) in (1030, 1031):
                before = readiness(teammate)
                after = readiness(teammate, extra_energy=3)
                if not before["ready"] and after["ready"]:
                    score += 500.0
                elif not before["ready"]:
                    score += 180.0
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
    ps = players(state)
    if yi < len(ps) and as_int(ps[yi].get("deckCount"), 0) == 0:
        # A further setup action can remove the legal attack or end the turn;
        # with no cards left, attack now before the next-turn deck-out check.
        return None
    signature = attack_menu_signature(obs)
    seen = ATTACK_MENU_STATES.setdefault(turn_key, set())
    if signature in seen:
        return None
    seen.add(signature)

    if ATTACK_DEFERRALS.get(turn_key, 0) >= MAX_ATTACK_DEFERRALS:
        return None

    # Never defer setup when we are at prize parity ≤ 1 and can attack now
    opp_prizes = opponent_prize_count(obs)
    our_prizes = our_prize_count(obs)
    if opp_prizes <= 1 or our_prizes <= 1:
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

    if (
        choice is None
        and card_id(active) == 1031
        and active_missing_hp >= 90
    ):
        choice = best_index(
            lambda index: options[index].get("type") == 7
            and play_id(index) == 1229
        )

    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and play_id(index) == 1159
            and options[index].get("inPlayArea") == 4
        )

    if choice is None:
        choice = best_index(
            lambda index: options[index].get("type") == 9
            and options[index].get("inPlayArea") == 5
        )

    if choice is None and not bool(state.get("energyAttached")):
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) in ENERGY_CARDS
            and options[index].get("inPlayArea") == 5
            and not readiness(target_card(obs, options[index]))["ready"]
        )

    if choice is None and not bool(state.get("energyAttached")):
        choice = best_index(
            lambda index: options[index].get("type") == 8
            and card_id(option_card(obs, options[index])) == 17
            and options[index].get("inPlayArea") == 4
            and card_id(target_card(obs, options[index])) == 1031
            and readiness(target_card(obs, options[index]))["damage"] < 210
        )

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
