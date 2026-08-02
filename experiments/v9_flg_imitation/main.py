import json
import os


BASE_TYPE_SCORE = {
    3: 320.0,
    4: 380.0,
    5: 410.0,
    6: 520.0,
    7: 610.0,
    8: 680.0,
    9: 720.0,
    10: 760.0,
    12: 80.0,
    13: 1000.0,
    14: -900.0,
    15: 260.0,
}

LEARNED_WEIGHT_SCALE = float(os.environ.get("POLICY_WEIGHT_SCALE", "2.0"))

ENERGY_CARD_TYPES = {
    1: "G",
    11: "C",
    14: "C",
    18: "G",
    20: "F",
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
}

ATTACK_COSTS = {
    117: [("F", "C", "C")],
    344: [("C",)],
    345: [("G", "C", "C")],
    756: [("C", "C", "C")],
    1071: [("C", "C", "C")],
    96: [("G", "G", "G")],
    108: [("W", "C", "C")],
    63: [("L", "F")],
    184: [("P", "P", "C")],
    140: [("C", "C", "C")],
    272: [("P", "C")],
    978: [("F", "C")],
}

ATTACKER_PRIORITY = {
    117: 170.0,
    345: 125.0,
    756: 130.0,
    96: 110.0,
    63: 95.0,
    184: 90.0,
    108: 80.0,
    140: 70.0,
    1071: 62.0,
    272: 54.0,
    978: 50.0,
}


def agent_path(filename):
    kaggle_path = os.path.join("/kaggle_simulations/agent", filename)
    if os.path.exists(kaggle_path):
        return kaggle_path
    source_path = globals().get("__file__", "")
    local_dir = os.path.dirname(os.path.abspath(source_path)) if source_path else os.getcwd()
    return os.path.join(local_dir, filename)


def load_deck():
    with open(agent_path("deck.csv")) as handle:
        return [int(line.strip()) for line in handle if line.strip()]


def load_weights():
    with open(agent_path("policy.json")) as handle:
        return json.load(handle).get("weights", {})


DECK = load_deck()
WEIGHTS = load_weights()


def card_at(state, player, area, index, select):
    players = state.get("players") or []
    if area == 1:
        cards = select.get("deck") or []
    elif area == 2 and player < len(players):
        cards = players[player].get("hand") or []
    elif area == 3 and player < len(players):
        cards = players[player].get("discard") or []
    elif area == 4 and player < len(players):
        cards = players[player].get("active") or []
    elif area == 5 and player < len(players):
        cards = players[player].get("bench") or []
    elif area == 12:
        cards = state.get("looking") or []
    else:
        cards = []
    if not isinstance(index, int) or not 0 <= index < len(cards):
        return None
    card = cards[index]
    return card.get("id") if isinstance(card, dict) else None


def full_card_at(state, player, area, index, select):
    players = state.get("players") or []
    if area == 1:
        cards = select.get("deck") or []
    elif area == 2 and player < len(players):
        cards = players[player].get("hand") or []
    elif area == 3 and player < len(players):
        cards = players[player].get("discard") or []
    elif area == 4 and player < len(players):
        cards = players[player].get("active") or []
    elif area == 5 and player < len(players):
        cards = players[player].get("bench") or []
    elif area == 12:
        cards = state.get("looking") or []
    else:
        cards = []
    if not isinstance(index, int) or not 0 <= index < len(cards):
        return None
    card = cards[index]
    return card if isinstance(card, dict) else None


def attached_types(card):
    return [
        ATTACHED_ENERGY_TYPES[energy_id]
        for energy_id in (card or {}).get("energies") or []
        if energy_id in ATTACHED_ENERGY_TYPES
    ]


def missing_cost(cost, energies):
    pool = list(energies)
    missing = 0
    for symbol in cost:
        if symbol == "C":
            continue
        if symbol in pool:
            pool.remove(symbol)
        else:
            missing += 1
    colorless = cost.count("C")
    missing += max(0, colorless - len(pool))
    return missing


def readiness_score(card, extra_energy_id=None):
    if not isinstance(card, dict):
        return -100.0
    energies = attached_types(card)
    if extra_energy_id in ENERGY_CARD_TYPES:
        energies.append(ENERGY_CARD_TYPES[extra_energy_id])
    costs = ATTACK_COSTS.get(card.get("id"))
    if not costs:
        return len(energies) * 20.0
    best = -100.0
    for cost in costs:
        missing = missing_cost(cost, energies)
        score = 160.0 - missing * 90.0 + len(energies) * 10.0
        if missing == 0:
            score += 260.0
        elif missing == 1:
            score += 85.0
        best = max(best, score)
    return best + ATTACKER_PRIORITY.get(card.get("id"), 0.0)


def energy_attachment_bonus(obs, option):
    select = obs.get("select") or {}
    state = obs.get("current") or {}
    your_index = state.get("yourIndex", 0)
    source_id = full_card_at(
        state,
        option.get("playerIndex", your_index),
        option.get("area"),
        option.get("index"),
        select,
    )
    source_id = source_id.get("id") if isinstance(source_id, dict) else None
    if source_id not in ENERGY_CARD_TYPES:
        return 0.0
    target = full_card_at(
        state,
        option.get("playerIndex", your_index),
        option.get("inPlayArea"),
        option.get("inPlayIndex"),
        select,
    )
    before = readiness_score(target)
    after = readiness_score(target, source_id)
    bonus = (after - before) * 2.0 + after * 0.35
    if option.get("inPlayArea") == 4:
        bonus += 80.0
    target_id = target.get("id") if isinstance(target, dict) else None
    if target_id == 63 and source_id not in (4, 6):
        bonus -= 220.0
    if target_id == 978 and source_id != 6:
        bonus -= 160.0
    if target_id == 108 and source_id == 3:
        bonus += 120.0
    if target_id == 184 and source_id == 5:
        bonus += 120.0
    if target_id == 96 and source_id == 1:
        bonus += 90.0
    return bonus


def option_features(obs, option):
    select = obs.get("select") or {}
    state = obs.get("current") or {}
    context = select.get("context")
    option_type = option.get("type")
    your_index = state.get("yourIndex", 0)
    owner = option.get("playerIndex", your_index)
    features = [
        f"type:{option_type}",
        f"context:{context}:type:{option_type}",
    ]

    area = option.get("area")
    index = option.get("index")
    if area is None and option_type == 7:
        area = 2
    if isinstance(area, int) and isinstance(index, int):
        card_id = card_at(state, owner, area, index, select)
        if card_id is not None:
            features.extend((f"card:{card_id}", f"context:{context}:card:{card_id}"))

    target_area = option.get("inPlayArea")
    target_index = option.get("inPlayIndex")
    if isinstance(target_area, int) and isinstance(target_index, int):
        target_owner = option.get("playerIndex", your_index)
        target_id = card_at(state, target_owner, target_area, target_index, select)
        if target_id is not None:
            features.extend(
                (f"target:{target_id}", f"context:{context}:target:{target_id}")
            )

    if option.get("attackId") is not None:
        features.append(f"attack:{option['attackId']}")
    if option.get("cardId") is not None:
        features.append(f"skill-card:{option['cardId']}")
    if owner == your_index:
        features.append("owner:self")
    elif option.get("playerIndex") is not None:
        features.append("owner:opponent")
    return features


def score_option(obs, option):
    option_type = option.get("type")
    score = BASE_TYPE_SCORE.get(option_type, 0.0)
    for feature in option_features(obs, option):
        score += WEIGHTS.get(feature, 0.0) * LEARNED_WEIGHT_SCALE

    your_index = (obs.get("current") or {}).get("yourIndex")
    if option.get("playerIndex") == your_index:
        score += 12.0

    target_area = option.get("inPlayArea")
    if option_type == 8:
        score += energy_attachment_bonus(obs, option)
    if option_type in (8, 9, 10):
        if target_area == 4:
            score += 24.0
        elif target_area == 5:
            score += 16.0

    select = obs.get("select") or {}
    if option_type == 14 and any(
        candidate.get("type") != 14 for candidate in select.get("option") or []
    ):
        score -= 500.0
    return score


def choose_action(obs):
    select = obs.get("select") if isinstance(obs, dict) else None
    if select is None:
        return DECK[:]

    options = select.get("option") or []
    min_count = int(select.get("minCount") or 0)
    max_count = int(select.get("maxCount") or 0)
    if not options or max_count <= 0:
        return []

    attack_indexes = [
        index for index, option in enumerate(options) if option.get("type") == 13
    ]
    if attack_indexes and min_count <= 1 <= max_count:
        return [attack_indexes[0]]

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
        minimum = int(select.get("minCount") or 0)
        return list(range(min(minimum, len(select.get("option") or []))))


def agent(obs):
    """Kaggle executes the final function defined in this file."""
    return safe_action(obs)
