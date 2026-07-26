DECK = [
    431, 431,
    400, 400, 400, 400,
    401, 401, 401, 401,
    434, 434,
    414, 1217,
    1152, 1152, 1152, 1218, 1152,
    1094, 1094,
    1134, 1134, 1134, 1134,
    1216, 1159,
    1, 414, 1094,
    1257, 1257, 1257,
    434,
    1216, 1216, 1216,
    1220, 1220, 1220, 1220,
    1227, 1227, 1227,
    1218, 1218,
    1175,
    1121, 1121,
    15, 15, 15, 15,
    1, 1, 1, 1, 1, 1,
    1086,
]


OPTION_TYPE_SCORE = {
    13: 1000.0,  # attack
    10: 760.0,   # ability / active board action
    9: 720.0,    # evolution-like in-play action
    8: 680.0,    # attach / move card to in-play target
    7: 610.0,    # play card from hand
    6: 520.0,    # pay energy / cost selection
    5: 410.0,
    4: 380.0,
    3: 320.0,    # choose a card or target
    15: 260.0,
    12: 80.0,    # pass / resolve / non-terminal utility
    14: -900.0,  # end / decline; keep this as last resort
}


def _safe_agent(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if not select:
            return DECK[:]
        min_count = int(select.get("minCount") or 0)
        return list(range(min(min_count, len(select.get("option") or []))))


def choose_action(obs):
    select = obs.get("select") if isinstance(obs, dict) else None
    if select is None:
        return DECK[:]

    options = select.get("option") or []
    if not options:
        return []

    min_count = int(select.get("minCount") or 0)
    max_count = int(select.get("maxCount") or min_count or 1)
    if max_count <= 0:
        return []

    scored = []
    for idx, option in enumerate(options):
        scored.append((score_option(option, select, obs), idx))
    scored.sort(key=lambda item: (-item[0], item[1]))

    chosen = []
    for score, idx in scored:
        if len(chosen) >= max_count:
            break
        if len(chosen) >= min_count and score <= 0:
            continue
        chosen.append(idx)

    if len(chosen) < min_count:
        chosen = [idx for _, idx in scored[:min_count]]

    return sorted(set(chosen), key=chosen.index)


def score_option(option, select, obs):
    option_type = option.get("type")
    score = OPTION_TYPE_SCORE.get(option_type, 0.0)

    current = obs.get("current") or {}
    players = current.get("players") or []
    your_index = current.get("yourIndex")

    if option_type == 13:
        score += attack_bonus(option)
    elif option_type in (8, 9, 10):
        score += board_action_bonus(option, your_index)
    elif option_type == 7:
        score += play_from_hand_bonus(option, current)
    elif option_type == 3:
        score += target_bonus(option, select, players, your_index)

    if option.get("playerIndex") == your_index:
        score += 12.0

    if option_type == 14 and has_non_terminal_option(select):
        score -= 500.0

    return score


def attack_bonus(option):
    attack_id = int(option.get("attackId") or 0)
    return 50.0 + (attack_id % 17) * 0.1


def board_action_bonus(option, your_index):
    score = 0.0
    in_play_area = option.get("inPlayArea")
    if in_play_area == 4:
        score += 24.0
    elif in_play_area == 5:
        score += 16.0
    if option.get("playerIndex") == your_index:
        score += 12.0
    return score


def play_from_hand_bonus(option, current):
    score = 0.0
    if not current.get("supporterPlayed"):
        score += 18.0
    if not current.get("energyAttached"):
        score += 14.0
    return score


def target_bonus(option, select, players, your_index):
    score = 0.0
    player_index = option.get("playerIndex")
    area = option.get("area")

    if player_index == your_index:
        score += 8.0
    elif player_index is not None:
        score += 16.0

    if area == 4:
        score += 18.0
    elif area == 5:
        score += 10.0
    elif area == 3:
        score += 6.0
    elif area == 1:
        score += deck_search_bonus(option, select)

    return score


def deck_search_bonus(option, select):
    deck = select.get("deck") or []
    idx = option.get("index")
    if not isinstance(idx, int) or idx < 0 or idx >= len(deck):
        return 0.0

    card_id = deck[idx].get("id")
    if card_id in (400, 401, 431, 434):
        return 30.0
    if card_id in (1121, 1122, 1152, 1216, 1218, 1220, 1227):
        return 22.0
    if card_id in (1, 7, 15):
        return 10.0
    return 14.0


def has_non_terminal_option(select):
    for option in select.get("option") or []:
        if option.get("type") != 14:
            return True
    return False


def agent(obs):
    """Kaggle executes the last function defined in this file."""
    return _safe_agent(obs)
