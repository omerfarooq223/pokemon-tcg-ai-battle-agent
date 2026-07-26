import os


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


BASE = {
    13: 5000.0,
    10: 900.0,
    8: 840.0,
    9: 820.0,
    7: 700.0,
    3: 420.0,
    5: 350.0,
    12: 80.0,
    14: -1000.0,
}

ENERGY = {1, 2, 3, 4, 5, 6, 7, 11, 14, 15, 18, 19, 20}
BASIC_PRIORITY = {
    756: 120,
    678: 115,
    431: 110,
    743: 105,
    96: 100,
    63: 95,
    184: 90,
    677: 85,
    742: 80,
    401: 75,
    1071: 70,
}


def zone_cards(state, player, area, select):
    players = state.get("players") or []
    if area == 1:
        return select.get("deck") or []
    if area == 12:
        return state.get("looking") or []
    if not isinstance(player, int) or player < 0 or player >= len(players):
        return []
    name = {2: "hand", 3: "discard", 4: "active", 5: "bench"}.get(area)
    return players[player].get(name) or [] if name else []


def card_at(state, player, area, index, select):
    cards = zone_cards(state, player, area, select)
    if not isinstance(index, int) or index < 0 or index >= len(cards):
        return None
    card = cards[index]
    return card if isinstance(card, dict) else None


def cid(card):
    return card.get("id") if isinstance(card, dict) else None


def attached(card):
    return len((card or {}).get("energies") or [])


def target_score(card, active=False):
    if not isinstance(card, dict):
        return 0.0
    score = BASIC_PRIORITY.get(card.get("id"), 45.0)
    score += attached(card) * 65.0
    score += min(int(card.get("hp") or 0), 350) / 8.0
    if active:
        score += 120.0
    return score


def score_option(obs, option):
    state = obs.get("current") or {}
    select = obs.get("select") or {}
    yi = state.get("yourIndex", 0)
    typ = option.get("type")
    score = BASE.get(typ, 0.0)

    if typ == 13:
        return score
    if typ == 14 and any((o or {}).get("type") != 14 for o in select.get("option") or []):
        return -2000.0

    area = option.get("area")
    if area is None and typ == 7:
        area = 2
    source = card_at(state, option.get("playerIndex", yi), area, option.get("index"), select)
    source_id = cid(source)
    if source_id in ENERGY:
        score += 120.0
    else:
        score += BASIC_PRIORITY.get(source_id, 0.0)

    target_area = option.get("inPlayArea")
    target_index = option.get("inPlayIndex")
    if isinstance(target_area, int) and isinstance(target_index, int):
        target = card_at(state, option.get("playerIndex", yi), target_area, target_index, select)
        score += target_score(target, active=target_area == 4)
        if source_id in ENERGY and target_area == 4:
            score += 160.0

    if typ == 3:
        card = card_at(state, option.get("playerIndex", yi), option.get("area"), option.get("index"), select)
        if option.get("playerIndex") == yi:
            score += target_score(card, active=option.get("area") == 4)
        else:
            score += 80.0 + attached(card) * 50.0

    if typ == 10 and option.get("area") == 4:
        score += 140.0
    return score


def choose_action(obs):
    if not isinstance(obs, dict) or obs.get("select") is None:
        return DECK[:]
    select = obs.get("select") or {}
    options = select.get("option") or []
    min_count = int(select.get("minCount") or 0)
    max_count = int(select.get("maxCount") or 0)
    if not options or max_count <= 0:
        return []

    attacks = [i for i, option in enumerate(options) if option.get("type") == 13]
    if attacks and min_count <= 1 <= max_count:
        return [attacks[0]]

    ranked = sorted(
        ((score_option(obs, option), i) for i, option in enumerate(options)),
        key=lambda item: (-item[0], item[1]),
    )
    chosen = [i for _, i in ranked[:min_count]]
    for score, i in ranked[min_count:max_count]:
        if score <= 0:
            break
        chosen.append(i)
    return chosen


def agent(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        return list(range(min(int(select.get("minCount") or 0), len(select.get("option") or []))))
