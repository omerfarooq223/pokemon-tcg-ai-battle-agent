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

ENERGY_TYPES = {
    1: "G",
    3: "W",
    4: "L",
    5: "P",
    6: "F",
}

# Cost symbols use C for colorless. The profiles are intentionally compact and cover
# our deck's attackers; unknown Pokemon fall back to simple attached-energy scoring.
ATTACKS = {
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

POKEMON_ROLE = {
    756: 120.0,
    96: 105.0,
    184: 90.0,
    63: 88.0,
    108: 75.0,
    140: 65.0,
    1071: 60.0,
    272: 50.0,
    978: 45.0,
}

DRAW_SEARCH_CARDS = {1121, 1198, 1205, 1250, 1088, 1098, 1097}
DISRUPTION_CARDS = {1182, 1197}
ENERGY_CARDS = set(ENERGY_TYPES)
ABILITY_POKEMON = {96, 756, 1071, 140, 184, 272}


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
        symbol = ENERGY_TYPES.get(energy_id)
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
    if extra_energy in ENERGY_TYPES:
        energy_types.append(ENERGY_TYPES[extra_energy])

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
    score += POKEMON_ROLE.get(target.get("id"), 0.0)
    return score


def card_id(card):
    return card.get("id") if isinstance(card, dict) else None


def hand_ids(state, player):
    return [card_id(card) for card in card_list(state, player, 2, {})]


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
            if cid == 756 and not any(card_id(c) == 756 for c in board_cards_only(state, yi)):
                score += 90.0
    if as_int(state.get("supporterPlayed"), 0) and cid in {1182, 1197, 1198, 1205}:
        score -= 250.0
    return score


def board_cards_only(state, player):
    return [entry[3] for entry in board_cards(state, player)]


def score_attach_or_evolve(obs, option):
    moving = option_card(obs, option)
    target = target_card(obs, option)
    cid = card_id(moving)
    score = BASE_TYPE_SCORE.get(option.get("type"), 0.0)
    if cid in ENERGY_CARDS:
        if as_int(current_state(obs).get("energyAttached"), 0) and option.get("area") == 2:
            score -= 120.0
        score += board_target_score(obs, target, extra_energy=cid)
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

    if owner == yi and area in (4, 5):
        score += board_target_score(obs, card)
        if context in (4, 21, 43):
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
    score = BASE_TYPE_SCORE[13] + r["damage"] * 1.8 + hp_pressure_bonus(obs, r["damage"])
    attack_id = option.get("attackId")
    if attack_id is not None:
        score += (as_int(attack_id) % 31) * 0.01
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


def choose_action(obs):
    if not isinstance(obs, dict) or obs.get("select") is None:
        return DECK[:]
    select = select_state(obs)
    if select is None:
        return DECK[:]
    options = select.get("option") or []
    min_count = as_int(select.get("minCount"), 0)
    max_count = as_int(select.get("maxCount"), 0)
    if not options or max_count <= 0:
        return []

    ranked = sorted(
        ((score_option(obs, option), index) for index, option in enumerate(options)),
        key=lambda item: (-item[0], item[1]),
    )
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
