"""V10 Mega Lopunny / Dudunsparce state planner.

The policy is deliberately driven by visible cards and board state.  It does
not contain opponent names, replay identifiers, or episode-specific branches.
"""

import os


EXPECTED_DECK = [
    11, 11, 11, 11, 13, 14, 14, 14,
    66, 66, 66, 66, 174,
    305, 305, 305, 305,
    848, 848, 848, 848,
    849, 849, 849,
    1086, 1086, 1086, 1086,
    1121, 1121, 1121, 1121,
    1122, 1122, 1122, 1122,
    1152, 1152, 1152, 1152,
    1174, 1174, 1174, 1174,
    1182, 1182, 1182,
    1197,
    1225, 1225, 1225, 1225,
    1227, 1227, 1227, 1227,
    1229, 1229, 1229, 1229,
]


def load_deck():
    paths = [os.path.join("/kaggle_simulations/agent", "deck.csv")]
    source = globals().get("__file__", "")
    if source:
        paths.append(os.path.join(os.path.dirname(os.path.abspath(source)), "deck.csv"))
    paths.append(os.path.join(os.getcwd(), "deck.csv"))
    for path in paths:
        try:
            with open(path, encoding="utf-8-sig") as handle:
                candidate = [
                    int(line.strip().split(",")[0])
                    for line in handle
                    if line.strip()
                ]
        except (OSError, ValueError):
            continue
        if candidate == EXPECTED_DECK:
            return candidate
    return EXPECTED_DECK[:]


DECK = load_deck()

# Card IDs in V10.
DUDUNSPARCE = 66
FAN_ROTOM = 174
DUNSPARCE = 305
BUNEARY = 848
LOPUNNY = 849
MIST = 11
ENRICHING = 13
SPIKY = 14
POFFIN = 1086
ULTRA_BALL = 1121
POKEGEAR = 1122
POKE_PAD = 1152
AIR_BALLOON = 1174
BOSS = 1182
XEROSIC = 1197
HILDA = 1225
LILLIE = 1227
WALLY = 1229

ENERGY_IDS = {MIST, ENRICHING, SPIKY}
BASIC_IDS = {FAN_ROTOM, DUNSPARCE, BUNEARY}
EVOLUTION_IDS = {DUDUNSPARCE, LOPUNNY}
SUPPORTER_IDS = {BOSS, XEROSIC, HILDA, LILLIE, WALLY}

# Attack IDs from the official engine/card data.
GALE_THRUST = 1225
SPIKY_HOPPER = 1226
TRADING_PLACES = 230
RAM = 231
RUN_AROUND = 1223
KICK = 1224

# Known Pokémon ex and rule-box attackers.  This is card metadata, not an
# opponent identity list; it is used only for prize and damage-effect scoring.
EX_POKEMON = {
    24, 29, 30, 37, 40, 44, 46, 52, 63, 75, 79, 80, 83, 84, 96, 99,
    107, 108, 117, 121, 125, 130, 138, 139, 140, 141, 150, 153, 154,
    161, 176, 179, 184, 189, 190, 193, 198, 205, 207, 210, 223, 229,
    231, 232, 236, 239, 241, 243, 244, 246, 248, 249, 259, 269, 272,
    283, 293, 299, 302, 306, 313, 316, 320, 326, 328, 329, 331, 336,
    337, 340, 357, 369, 372, 381, 389, 404, 407, 424, 431, 447, 455,
    458, 471, 481, 509, 515, 525, 527, 547, 561, 573, 583, 598, 618,
    631, 641, 648, 652, 662, 678, 687, 695, 723, 737, 747, 754, 756,
    766, 772, 781, 790, 795, 806, 813, 828, 835, 849, 861, 868, 886,
    896, 904, 911, 919, 928, 932, 939, 944, 951, 954, 957, 962, 968,
    969, 975, 979, 984, 988, 990, 993, 997, 1002, 1006, 1022, 1026,
    1031, 1040, 1056, 1062, 1064, 1071,
}

# Attacks or Abilities that make ordinary damage unreliable.  Spiky Hopper's
# printed effect ignores those protections.  IDs are derived from card text.
DAMAGE_PROTECTION_POKEMON = {
    117, 118, 345, 357, 401, 428, 442, 504, 525, 569, 637, 742, 748,
    755, 799, 824, 834, 851, 858, 866, 901, 924, 970, 994, 1024,
}

# Visible opposing Active Pokémon whose attacks place counters or otherwise
# apply effects that Mist Energy can prevent.
MIST_THREATS = {
    29, 32, 56, 94, 104, 112, 121, 215, 219, 223, 245, 247, 432,
    455, 593, 648, 738, 743, 817, 864, 876, 880, 982, 1058,
}

# Small amount of per-game memory is used only for loop protection and to
# recognize a same-turn Active change that enables Gale Thrust.
LAST_TURN = None
TURN_START_ACTIVE = None
SEEN_MENUS = set()
ATTACK_DEFERRALS = {}
FORCE_READY_PROMOTION = False
try:
    MAX_ATTACK_DEFERRALS = max(0, int(os.environ.get("V10_LOPUNNY_ATTACK_DEFERRALS", "12")))
except (TypeError, ValueError):
    MAX_ATTACK_DEFERRALS = 12


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def current(obs):
    return (obs or {}).get("current") or {}


def selection(obs):
    return (obs or {}).get("select") or {}


def players(state):
    value = state.get("players") or []
    return value if isinstance(value, list) else []


def your_index(state):
    value = state.get("yourIndex", 0)
    return value if value in (0, 1) else 0


def card_id(card):
    return card.get("id") if isinstance(card, dict) else None


def zone_cards(state, player, area, select=None):
    select = select or {}
    if area == 1:
        return select.get("deck") or []
    if area == 7:
        return state.get("stadium") or []
    if area == 12:
        return state.get("looking") or []
    ps = players(state)
    if player not in (0, 1) or player >= len(ps):
        return []
    key = {2: "hand", 3: "discard", 4: "active", 5: "bench", 6: "prize"}.get(area)
    return ps[player].get(key) or [] if key else []


def card_at(state, player, area, index, select=None):
    cards = zone_cards(state, player, area, select)
    if isinstance(index, int) and 0 <= index < len(cards):
        value = cards[index]
        return value if isinstance(value, dict) else None
    return None


def option_source(obs, option):
    state = current(obs)
    yi = your_index(state)
    owner = option.get("playerIndex", yi)
    area = option.get("area")
    if area is None and option.get("type") == 7:
        area = 2
    card = card_at(state, owner, area, option.get("index"), selection(obs))
    if not isinstance(card, dict):
        return card
    if option.get("type") in (5, 6):
        energies = card.get("energyCards") or []
        energy_index = option.get("energyIndex")
        if isinstance(energy_index, int) and 0 <= energy_index < len(energies):
            energy = energies[energy_index]
            return energy if isinstance(energy, dict) else None
    if option.get("type") == 4:
        tools = card.get("tools") or []
        tool_index = option.get("toolIndex")
        if isinstance(tool_index, int) and 0 <= tool_index < len(tools):
            tool = tools[tool_index]
            return tool if isinstance(tool, dict) else None
    return card


def option_target(obs, option):
    state = current(obs)
    yi = your_index(state)
    owner = option.get("playerIndex", yi)
    return card_at(
        state,
        owner,
        option.get("inPlayArea"),
        option.get("inPlayIndex"),
        selection(obs),
    )


def hand(state, player):
    return zone_cards(state, player, 2)


def hand_ids(state, player):
    return [card_id(card) for card in hand(state, player)]


def board(state, player):
    result = []
    for area in (4, 5):
        for index, card in enumerate(zone_cards(state, player, area)):
            if isinstance(card, dict):
                result.append((area, index, card))
    return result


def active(state, player):
    cards = zone_cards(state, player, 4)
    return cards[0] if cards and isinstance(cards[0], dict) else None


def bench(state, player):
    return [card for card in zone_cards(state, player, 5) if isinstance(card, dict)]


def attached_count(card):
    return len((card or {}).get("energyCards") or (card or {}).get("energies") or [])


def has_tool(card, tool_id=None):
    tools = (card or {}).get("tools") or []
    if tool_id is None:
        return bool(tools)
    return any(card_id(tool) == tool_id for tool in tools)


def hp(card):
    return as_int((card or {}).get("hp"), 0)


def max_hp(card):
    return as_int((card or {}).get("maxHp"), hp(card))


def damage_on(card):
    return max(0, max_hp(card) - hp(card))


def prize_count(state, player):
    ps = players(state)
    if player < len(ps) and isinstance(ps[player].get("prize"), list):
        return len(ps[player]["prize"])
    return 6


def bench_capacity(state, player):
    ps = players(state)
    if player >= len(ps):
        return 0
    limit = as_int(ps[player].get("benchMax"), 5)
    return max(0, limit - len(bench(state, player)))


def board_counts(state, player):
    counts = {}
    for _, _, card in board(state, player):
        cid = card_id(card)
        counts[cid] = counts.get(cid, 0) + 1
    return counts


def reset_turn_memory(state):
    global LAST_TURN, TURN_START_ACTIVE, SEEN_MENUS, ATTACK_DEFERRALS, FORCE_READY_PROMOTION
    turn = as_int(state.get("turn"), 0)
    yi = your_index(state)
    key = (turn, yi)
    active_card = active(state, yi)
    serial = active_card.get("serial") if isinstance(active_card, dict) else None
    if LAST_TURN != key:
        if LAST_TURN is None or turn <= LAST_TURN[0] or LAST_TURN[1] != yi:
            SEEN_MENUS = set()
        else:
            SEEN_MENUS = set()
        ATTACK_DEFERRALS = {}
        FORCE_READY_PROMOTION = False
        LAST_TURN = key
        TURN_START_ACTIVE = serial


def active_moved_this_turn(state):
    yi = your_index(state)
    card = active(state, yi)
    serial = card.get("serial") if isinstance(card, dict) else None
    return bool(state.get("retreated")) or (
        TURN_START_ACTIVE is not None and serial is not None and serial != TURN_START_ACTIVE
    )


def lopunny_ready(card, two_energy=False):
    if card_id(card) != LOPUNNY:
        return False
    needed = 2 if two_energy else 1
    return attached_count(card) >= needed


def best_lopunny(state, player, exclude_serial=None):
    choices = []
    for area, index, card in board(state, player):
        if card_id(card) != LOPUNNY:
            continue
        if exclude_serial is not None and card.get("serial") == exclude_serial:
            continue
        choices.append(
            (
                attached_count(card) >= 1,
                attached_count(card) >= 2,
                hp(card),
                -damage_on(card),
                area,
                index,
                card,
            )
        )
    return max(choices, default=None)


def effective_lopunny_damage(state, attack_id):
    if attack_id == SPIKY_HOPPER:
        return 160
    if attack_id == GALE_THRUST:
        return 230 if active_moved_this_turn(state) else 60
    return 0


def current_attack_ceiling(state):
    yi = your_index(state)
    card = active(state, yi)
    if card_id(card) != LOPUNNY or attached_count(card) < 1:
        return 0
    damage = 230 if active_moved_this_turn(state) else 60
    if attached_count(card) >= 2:
        damage = max(damage, 160)
    return damage


def opponent_target_value(obs, card, area):
    if not isinstance(card, dict):
        return -10000.0
    state = current(obs)
    target_hp = hp(card)
    target_id = card_id(card)
    damage = current_attack_ceiling(state)
    value = (max_hp(card) - target_hp) * 2.0
    value += attached_count(card) * 90.0
    value += 260.0 if target_id in EX_POKEMON else 40.0
    value += 40.0 if area == 4 else 0.0
    if damage and 0 < target_hp <= damage:
        value += 2600.0
        if target_id in EX_POKEMON:
            value += 1000.0
    elif target_hp:
        value += max(0, damage - target_hp) * 0.2
        value -= target_hp * 0.25
    return value


def choose_promotion_score(obs, card, context):
    state = current(obs)
    yi = your_index(state)
    cid = card_id(card)
    energy = attached_count(card)
    if context == 4:
        # After a KO, a free pivot lets a Benched Lopunny move Active during
        # our turn and unlock Gale Thrust's 230 damage.
        pivot_tool_available = AIR_BALLOON in hand_ids(state, yi)
        if cid in (DUNSPARCE, BUNEARY) and (
            has_tool(card, AIR_BALLOON) or energy >= 1 or pivot_tool_available
        ):
            return 5200.0
        if cid == LOPUNNY and energy >= 1:
            return 4300.0 + hp(card)
        if cid == FAN_ROTOM and (has_tool(card, AIR_BALLOON) or energy >= 1):
            return 3600.0
    if cid == LOPUNNY:
        return 5000.0 + energy * 600.0 + hp(card)
    if cid in (DUNSPARCE, BUNEARY):
        return 2400.0 + (800.0 if has_tool(card, AIR_BALLOON) else 0.0) + energy * 500.0
    if cid == FAN_ROTOM:
        return 1700.0 + energy * 400.0
    if cid == DUDUNSPARCE:
        return 800.0 + energy * 300.0
    return 0.0


def setup_card_score(state, cid, context):
    yi = your_index(state)
    counts = board_counts(state, yi)
    if context == 1:
        # Dunsparce is the best opening pivot: it can use Trading Places and
        # later become a draw-three Dudunsparce without exposing Buneary.
        return {DUNSPARCE: 5200.0, BUNEARY: 4200.0, FAN_ROTOM: 3400.0}.get(cid, 0.0)
    if cid == BUNEARY:
        return 4700.0 - counts.get(BUNEARY, 0) * 900.0 - counts.get(LOPUNNY, 0) * 350.0
    if cid == DUNSPARCE:
        return 4400.0 - counts.get(DUNSPARCE, 0) * 600.0 - counts.get(DUDUNSPARCE, 0) * 250.0
    if cid == FAN_ROTOM:
        # Global turn 1 is the first player's opening turn and global turn 2 is
        # the second player's opening turn.  Fan Call is live in either seat.
        first_turn = as_int(state.get("turn"), 0) <= 2
        return (4300.0 if first_turn and counts.get(FAN_ROTOM, 0) == 0 else 500.0)
    return 0.0


def discard_keep_value(obs, card, option):
    state = current(obs)
    yi = your_index(state)
    cid = card_id(card)
    hand_now = hand_ids(state, yi)
    counts = board_counts(state, yi)
    index = option.get("index")
    duplicate_rank = 0
    if isinstance(index, int):
        duplicate_rank = sum(1 for value in hand_now[:index] if value == cid)
    value = 100.0
    if cid == LOPUNNY:
        unevolved = counts.get(BUNEARY, 0)
        value = 1100.0 if duplicate_rank < unevolved else 250.0
    elif cid == DUDUNSPARCE:
        unevolved = counts.get(DUNSPARCE, 0)
        value = 850.0 if duplicate_rank < unevolved else 180.0
    elif cid == BUNEARY:
        value = 700.0 if counts.get(BUNEARY, 0) + counts.get(LOPUNNY, 0) < 2 else 100.0
    elif cid == DUNSPARCE:
        value = 500.0 if counts.get(DUNSPARCE, 0) + counts.get(DUDUNSPARCE, 0) < 2 else 80.0
    elif cid == AIR_BALLOON:
        value = 820.0 if not any(has_tool(c, AIR_BALLOON) for _, _, c in board(state, yi)) else 180.0
    elif cid == ENRICHING:
        value = 950.0
    elif cid in (SPIKY, MIST):
        unready = sum(1 for _, _, c in board(state, yi) if card_id(c) in (BUNEARY, LOPUNNY) and attached_count(c) < 2)
        value = 650.0 if unready else 100.0
    elif cid == HILDA:
        value = 760.0 if counts.get(BUNEARY, 0) else 220.0
    elif cid == WALLY:
        value = 800.0 if any(damage_on(c) >= 80 for _, _, c in board(state, yi) if card_id(c) == LOPUNNY) else 140.0
    elif cid == BOSS:
        value = 520.0
    elif cid == XEROSIC:
        opp = 1 - yi
        ps = players(state)
        opp_hand = as_int(ps[opp].get("handCount"), 0) if opp < len(ps) else 0
        value = 680.0 if opp_hand >= 6 else 100.0
    elif cid == LILLIE:
        value = 420.0
    elif cid in (POFFIN, POKE_PAD, ULTRA_BALL):
        value = 380.0 if bench_capacity(state, yi) else 60.0
    elif cid == POKEGEAR:
        value = 220.0
    if duplicate_rank:
        value -= duplicate_rank * 140.0
    return value


def search_card_score(obs, cid, effect_id, context):
    state = current(obs)
    yi = your_index(state)
    counts = board_counts(state, yi)
    held = hand_ids(state, yi)

    if effect_id == FAN_ROTOM:
        return setup_card_score(state, cid, 2)
    if effect_id == POFFIN:
        return setup_card_score(state, cid, 2)
    if effect_id == HILDA:
        if cid == LOPUNNY:
            return 6200.0 if counts.get(BUNEARY, 0) > held.count(LOPUNNY) else 3500.0
        if cid == DUDUNSPARCE:
            return 4200.0 if counts.get(DUNSPARCE, 0) > held.count(DUDUNSPARCE) else 2200.0
        if cid == ENRICHING:
            return 5800.0
        if cid == SPIKY:
            return 5200.0
        if cid == MIST:
            opponent = active(state, 1 - yi)
            return 5400.0 if card_id(opponent) in MIST_THREATS else 4700.0
    if effect_id == ULTRA_BALL:
        if cid == LOPUNNY:
            missing = counts.get(BUNEARY, 0) > held.count(LOPUNNY)
            return 6200.0 if missing else 2300.0
        if cid == DUDUNSPARCE:
            return 4900.0 if counts.get(DUNSPARCE, 0) else 2200.0
        if cid in BASIC_IDS and len(board(state, yi)) <= 1:
            # Do not leave a lone evolving attacker as the entire board.  Once
            # its Lopunny is secured, the next broad search must establish a
            # second Basic before consuming more evolution pieces.
            return 7200.0 + setup_card_score(state, cid, 2) * 0.1
        return setup_card_score(state, cid, 2)
    if effect_id == POKE_PAD:
        if cid == DUDUNSPARCE:
            needed = counts.get(DUNSPARCE, 0) - held.count(DUDUNSPARCE)
            return 6000.0 if needed > 0 else 2500.0
        if cid == DUNSPARCE:
            return 4200.0 if counts.get(DUNSPARCE, 0) + counts.get(DUDUNSPARCE, 0) < 3 else 1000.0
        if cid == BUNEARY:
            return 4400.0 if counts.get(BUNEARY, 0) + counts.get(LOPUNNY, 0) < 2 else 900.0
        if cid == FAN_ROTOM:
            return 1800.0 if as_int(state.get("turn"), 0) <= 2 else 100.0
    if effect_id == POKEGEAR:
        # A Supporter is selected from the top seven.
        return supporter_value(obs, cid, from_search=True)
    if cid in EVOLUTION_IDS:
        return 3000.0
    if cid in ENERGY_IDS:
        return 2400.0
    if cid in BASIC_IDS:
        return setup_card_score(state, cid, 2)
    return 200.0


def supporter_value(obs, cid, from_search=False):
    state = current(obs)
    yi = your_index(state)
    opp = 1 - yi
    ps = players(state)
    opponent_hand = as_int(ps[opp].get("handCount"), 0) if opp < len(ps) else 0
    counts = board_counts(state, yi)
    cards_in_hand = len(hand(state, yi))
    damaged = [c for _, _, c in board(state, yi) if card_id(c) == LOPUNNY and damage_on(c) > 0]
    damaged_bench = [c for c in bench(state, yi) if card_id(c) == LOPUNNY and damage_on(c) > 0]
    our_active = active(state, yi)
    ready_bench_lopunny = any(lopunny_ready(c) for c in bench(state, yi))
    opponent_bench = bench(state, opp)
    ceiling = current_attack_ceiling(state)
    boss_ko = any(0 < hp(c) <= ceiling for c in opponent_bench) if ceiling else False

    if cid == BOSS:
        if boss_ko:
            value = 6100.0
        elif opponent_bench:
            value = 3000.0
        else:
            value = 300.0
    elif cid == WALLY:
        # Healing returns every attached Energy. Prefer the proven pivot loop:
        # retreat the damaged attacker, then heal it safely on the Bench.
        # Do not turn an attack-ready Active into an unpowered Active.
        largest = max((damage_on(card) for card in damaged_bench), default=0)
        active_damage = (
            damage_on(our_active) if card_id(our_active) == LOPUNNY else 0
        )
        if active_damage > 0:
            # Wally's target prompt can include the Active even when a damaged
            # Bench target exists.  If healing the Active would strand it with
            # zero Energy, do not open that irreversible prompt at all.
            value = -5000.0
        elif largest >= 80:
            value = 6500.0 + largest * 5.0
        else:
            value = -5000.0
    elif cid == HILDA:
        missing_lopunny = counts.get(BUNEARY, 0) > hand_ids(state, yi).count(LOPUNNY)
        unpowered = any(
            card_id(card) in (BUNEARY, LOPUNNY) and attached_count(card) < 1
            for _, _, card in board(state, yi)
        )
        value = 5600.0 if missing_lopunny else (4200.0 if unpowered else 1200.0)
    elif cid == XEROSIC:
        value = 900.0 + max(0, opponent_hand - 3) * 500.0
        if opponent_hand <= 4:
            value = 150.0
    elif cid == LILLIE:
        own_prizes = prize_count(state, yi)
        draw_to = 8 if own_prizes == 6 else 6
        value = 2200.0 + max(0, draw_to - cards_in_hand) * 520.0
        if cards_in_hand > draw_to + 2:
            value = 200.0
    else:
        value = 100.0
    return value + (250.0 if from_search else 0.0)


def main_play_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    card = option_source(obs, option)
    cid = card_id(card)
    capacity = bench_capacity(state, yi)
    counts = board_counts(state, yi)
    supporter_used = bool(state.get("supporterPlayed"))

    if cid in SUPPORTER_IDS:
        if supporter_used:
            return -5000.0
        return supporter_value(obs, cid)
    if cid == POKEGEAR:
        return 4700.0 if not supporter_used else 2600.0
    if cid == POFFIN:
        if capacity <= 0:
            return -1000.0
        wanted = counts.get(BUNEARY, 0) + counts.get(LOPUNNY, 0) < 2 or counts.get(DUNSPARCE, 0) + counts.get(DUDUNSPARCE, 0) < 2
        return 5000.0 if wanted else 1800.0
    if cid == ULTRA_BALL:
        need_evolution = counts.get(BUNEARY, 0) > hand_ids(state, yi).count(LOPUNNY)
        return 4800.0 if need_evolution else 2100.0
    if cid == POKE_PAD:
        need_draw_line = counts.get(DUNSPARCE, 0) > hand_ids(state, yi).count(DUDUNSPARCE)
        need_basic = counts.get(BUNEARY, 0) + counts.get(LOPUNNY, 0) < 2
        return 4550.0 if (need_draw_line or need_basic) else 1700.0
    if cid in BASIC_IDS:
        if capacity <= 0:
            return -2000.0
        return setup_card_score(state, cid, 2)
    return 300.0


def attach_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    moving = option_source(obs, option)
    target = option_target(obs, option)
    cid = card_id(moving)
    target_id = card_id(target)
    area = option.get("inPlayArea")

    if cid == AIR_BALLOON:
        if has_tool(target):
            return -4000.0
        score = 2900.0
        if area == 4 and not bool(state.get("retreated")):
            ready_bench = any(lopunny_ready(card) for card in bench(state, yi))
            score += 2400.0 if ready_bench else 500.0
        if target_id == LOPUNNY:
            score += 900.0
        elif target_id in (DUNSPARCE, BUNEARY):
            score += 700.0
        return score

    if cid not in ENERGY_IDS:
        return 200.0
    if bool(state.get("energyAttached")) and option.get("area") == 2:
        return -4000.0
    energy_count = attached_count(target)
    if target_id not in (BUNEARY, LOPUNNY):
        # Enriching is also a draw-four engine.  When no Lopunny line is ready,
        # a first attachment to the Active pivot accelerates the whole setup.
        if (
            cid == ENRICHING
            and target_id in (DUNSPARCE, FAN_ROTOM)
            and energy_count == 0
        ):
            stadium_live = bool(state.get("stadium"))
            return 7100.0 + (
                500.0 if target_id == FAN_ROTOM and stadium_live else 0.0
            )
        return 500.0 if target_id in (DUNSPARCE, FAN_ROTOM) else -800.0
    if energy_count >= 2:
        return -2500.0
    score = 3900.0
    if cid == ENRICHING:
        score += 1800.0
    elif cid == MIST:
        threat = card_id(active(state, 1 - yi)) in MIST_THREATS
        score += 1500.0 if threat else 350.0
    elif cid == SPIKY:
        score += 900.0
    if energy_count == 0:
        score += 1500.0
    else:
        score += 650.0
    if area == 4:
        score += 350.0
    opposing_active = active(state, 1 - yi)
    protection_break_needed = card_id(opposing_active) in DAMAGE_PROTECTION_POKEMON
    pivot_ko_window = (
        not protection_break_needed and 160 < hp(opposing_active) <= 230
    )
    # Two Energy turns on Spiky Hopper.  It is the deck's defining answer to
    # effects that stop ordinary attack damage, and also the stable 160 line
    # when Gale Thrust has not been activated by a pivot.  The old planner
    # spread one Energy across several attackers and then looped harmless Gale
    # Thrusts into Crustle/Cornerstone.
    if area == 4 and target_id == LOPUNNY and energy_count == 1:
        if protection_break_needed:
            score += 6500.0
        elif not pivot_ko_window:
            score += 2800.0
    # Prefer establishing two independent attackers before stacking the second
    # Energy needed for Spiky Hopper.
    if energy_count == 1:
        other_unpowered = any(
            card_id(card) in (BUNEARY, LOPUNNY)
            and card.get("serial") != target.get("serial")
            and attached_count(card) == 0
            for _, _, card in board(state, yi)
        )
        if other_unpowered and not protection_break_needed and area != 4:
            score -= 900.0
    return score


def evolution_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    counts = board_counts(state, yi)
    moving = option_source(obs, option)
    target = option_target(obs, option)
    cid = card_id(moving)
    if cid == DUDUNSPARCE and card_id(target) == DUNSPARCE:
        attack_available = any(
            choice.get("type") == 13
            for choice in selection(obs).get("option") or []
        )
        if (
            option.get("inPlayArea") == 4
            and attack_available
            and not any(lopunny_ready(card) for card in bench(state, yi))
        ):
            # Evolving the Active removes Dunsparce's one-Energy switching
            # attack; Dudunsparce then needs three Energy.  Without a ready
            # Lopunny to promote after Run Away Draw this abandons the turn.
            return -12000.0
        return 7000.0
    if cid == LOPUNNY and card_id(target) == BUNEARY:
        score = 7600.0 + attached_count(target) * 600.0
        if counts.get(LOPUNNY, 0) >= 2:
            score -= 900.0
        if option.get("inPlayArea") == 4:
            score += 350.0
        return score
    return 1000.0


def ability_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    source = option_source(obs, option)
    cid = card_id(source)
    area = option.get("area")
    if cid == DUDUNSPARCE:
        # Run Away Draw removes the Pokémon. Retreat it first when Active.
        if area == 5:
            switching_active = card_id(active(state, yi)) in (DUNSPARCE, BUNEARY)
            attack_available = any(
                choice.get("type") == 13
                for choice in selection(obs).get("option") or []
            )
            if switching_active and attack_available and len(bench(state, yi)) <= 1:
                # Trading Places/Run Around needs a Bench target.  Shuffling
                # away the last Benched Dudunsparce deletes the legal attack.
                return -12000.0
            return 7200.0
        if any(lopunny_ready(card) for card in bench(state, yi)):
            return 7400.0
        return -12000.0
    if cid == FAN_ROTOM:
        # If the engine offers Fan Call, it is the user's first turn and the
        # draw/search value should always outrank ordinary setup.
        return 6800.0
    # Unknown once-per-turn abilities are usually useful, but do not outrank
    # the deck's proven draw/setup engine.
    return 1800.0


def retreat_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    if bool(state.get("retreated")):
        return -5000.0
    active_card = active(state, yi)
    active_serial = active_card.get("serial") if isinstance(active_card, dict) else None
    best = best_lopunny(state, yi, exclude_serial=active_serial)
    if best and best[0]:
        opposing_active = active(state, 1 - yi)
        if card_id(opposing_active) in DAMAGE_PROTECTION_POKEMON:
            # Gale Thrust cannot solve this board.  Only pivot if the incoming
            # Lopunny already has the two Energy required for Spiky Hopper.
            if not best[1]:
                return -12000.0
        # Moving a powered Lopunny Active enables 230 damage; moving away from a
        # damaged one also sets up a later Wally heal.
        score = 7600.0
        if card_id(active_card) == LOPUNNY:
            score += damage_on(active_card) * 3.0
        return score
    if card_id(active_card) != LOPUNNY:
        any_ready = best_lopunny(state, yi)
        if any_ready and any_ready[0]:
            return 7000.0
    # A retreat without a powered Lopunny destination removes the current
    # attack and can end an otherwise productive turn.  Make it strictly worse
    # than both attacking and explicitly ending the turn.
    return -12000.0


def attack_score(obs, option):
    state = current(obs)
    yi = your_index(state)
    our_active = active(state, yi)
    attack_id = option.get("attackId")
    opponent = active(state, 1 - yi)
    opponent_id = card_id(opponent)
    opponent_hp = hp(opponent)

    if card_id(our_active) == LOPUNNY:
        damage = effective_lopunny_damage(state, attack_id)
        score = 4300.0 + damage * 9.0
        if opponent_id in DAMAGE_PROTECTION_POKEMON:
            if attack_id == SPIKY_HOPPER:
                score += 4300.0
            else:
                score -= 4800.0
        if 0 < opponent_hp <= damage:
            score += 6200.0
            if opponent_id in EX_POKEMON:
                score += 2200.0
        if attack_id == GALE_THRUST and not active_moved_this_turn(state):
            score -= 1600.0
        if attack_id == SPIKY_HOPPER and attached_count(our_active) >= 2:
            score += 500.0
        return score
    if attack_id in (TRADING_PLACES, RUN_AROUND):
        return 3300.0 if any(lopunny_ready(card) for card in bench(state, yi)) else 900.0
    if attack_id in (RAM, KICK):
        return 1800.0
    return 1300.0


def target_selection_score(obs, option):
    state = current(obs)
    select = selection(obs)
    yi = your_index(state)
    context = select.get("context")
    owner = option.get("playerIndex", yi)
    area = option.get("area")
    card = option_source(obs, option)
    cid = card_id(card)
    effect_id = card_id(select.get("effect"))

    # Mandatory discard from our hand. Lower keep value must rank higher.
    if context in (8, 29) and owner == yi and area == 2:
        return 5000.0 - discard_keep_value(obs, card, option)

    if owner != yi and area in (4, 5):
        return opponent_target_value(obs, card, area)

    if owner == yi and area in (4, 5):
        if context in (3, 4, 43):
            if context == 4 and FORCE_READY_PROMOTION:
                if cid == LOPUNNY and attached_count(card) >= 1:
                    return 12000.0 + attached_count(card) * 500.0 + hp(card)
                return -2000.0 + attached_count(card) * 100.0
            return choose_promotion_score(obs, card, context)
        if context == 17 and effect_id == WALLY:
            if cid != LOPUNNY:
                return -5000.0
            if area == 4:
                return -5000.0
            score = 3000.0 + damage_on(card) * 12.0 + attached_count(card) * 300.0
            if area == 5:
                score += 250.0
            return score
        return 1000.0 + (attached_count(card) * 300.0) + hp(card)

    if area in (1, 2, 3, 12):
        return search_card_score(obs, cid, effect_id, context)
    return 0.0


def energy_discard_score(obs, option):
    energy = option_source(obs, option)
    cid = card_id(energy)
    # Enriching's draw trigger has already been consumed once attached, while
    # Mist and Spiky retain defensive effects.
    return {ENRICHING: 5200.0, SPIKY: 4300.0, MIST: 3500.0}.get(cid, 2500.0)


def menu_signature(obs):
    state = current(obs)
    select = selection(obs)
    yi = your_index(state)
    active_card = active(state, yi)
    return (
        as_int(state.get("turn"), 0),
        as_int(state.get("turnActionCount"), 0),
        bool(state.get("supporterPlayed")),
        bool(state.get("energyAttached")),
        card_id(active_card),
        active_card.get("serial") if isinstance(active_card, dict) else None,
        tuple(
            (
                option.get("type"), option.get("area"), option.get("index"),
                option.get("inPlayArea"), option.get("inPlayIndex"),
                option.get("attackId"), option.get("energyIndex"),
            )
            for option in select.get("option") or []
        ),
    )


def score_option(obs, option):
    state = current(obs)
    context = selection(obs).get("context")
    option_type = option.get("type")

    if option_type == 0 and context == 38:
        return as_int(option.get("number"), 0) * 1000.0
    if option_type in (1, 2) and context == 41:
        return 5000.0 if option_type == 1 else 1000.0
    if option_type == 3:
        return target_selection_score(obs, option)
    if option_type == 6 and context == 30:
        return energy_discard_score(obs, option)
    if option_type == 7:
        return main_play_score(obs, option)
    if option_type == 8:
        return attach_score(obs, option)
    if option_type == 9:
        return evolution_score(obs, option)
    if option_type == 10:
        return ability_score(obs, option)
    if option_type == 12:
        return retreat_score(obs, option)
    if option_type == 13:
        return attack_score(obs, option)
    if option_type == 14:
        attacks = any(o.get("type") == 13 for o in selection(obs).get("option") or [])
        return -9000.0 if attacks else -1000.0
    if option_type == 15:
        return 1000.0
    return 0.0


def choose_action(obs):
    if not isinstance(obs, dict) or obs.get("select") is None:
        return DECK[:]
    select = selection(obs)
    options = select.get("option") or []
    minimum = as_int(select.get("minCount"), 0)
    maximum = as_int(select.get("maxCount"), 0)
    if not options or maximum <= 0:
        return []

    state = current(obs)
    reset_turn_memory(state)
    ranked = sorted(
        ((score_option(obs, option), index) for index, option in enumerate(options)),
        key=lambda item: (-item[0], item[1]),
    )

    attacks = [(score, index) for score, index in ranked if options[index].get("type") == 13]
    signature = menu_signature(obs)
    repeated = signature in SEEN_MENUS
    SEEN_MENUS.add(signature)
    if attacks and minimum <= 1 <= maximum:
        best_attack = attacks[0]
        best = ranked[0]
        # Attack is a hard fallback on repeated state or after a generous setup
        # budget. Otherwise allow only a materially more valuable setup action.
        turn_key = LAST_TURN
        deferred = ATTACK_DEFERRALS.get(turn_key, 0)
        if (
            repeated
            or deferred >= MAX_ATTACK_DEFERRALS
            or as_int(state.get("turnActionCount"), 0) >= 24
        ):
            return [best_attack[1]]
        if (
            options[best[1]].get("type") == 13
            or best[0] < 1000.0
            or best[0] <= best_attack[0] + 500.0
        ):
            return [best_attack[1]]
        ATTACK_DEFERRALS[turn_key] = deferred + 1
        return [best[1]]

    # Multi-Pokémon searches build complementary attacker and draw lines.  A
    # static sort otherwise takes duplicate Buneary copies before a Dunsparce,
    # weakening both the pivot plan and the Run Away Draw engine.
    if selection(obs).get("context") == 5 and maximum > 1:
        chosen = []
        chosen_ids = {}
        remaining = set(range(len(options)))
        while len(chosen) < maximum and remaining:
            dynamic = []
            for index in remaining:
                source_id = card_id(option_source(obs, options[index]))
                score = score_option(obs, options[index])
                score -= chosen_ids.get(source_id, 0) * 1200.0
                dynamic.append((score, index, source_id))
            score, index, source_id = max(dynamic, key=lambda item: (item[0], -item[1]))
            if len(chosen) >= minimum and score <= 0:
                break
            chosen.append(index)
            chosen_ids[source_id] = chosen_ids.get(source_id, 0) + 1
            remaining.remove(index)
        return chosen

    chosen = [index for _, index in ranked[:minimum]]
    for score, index in ranked[minimum:maximum]:
        if score <= 0:
            break
        chosen.append(index)
    return chosen


def safe_action(obs):
    global FORCE_READY_PROMOTION
    try:
        action = choose_action(obs)
        select = selection(obs)
        options = select.get("option") or []
        if select.get("context") == 4 and FORCE_READY_PROMOTION:
            FORCE_READY_PROMOTION = False
        for index in action:
            if not isinstance(index, int) or not 0 <= index < len(options):
                continue
            option = options[index]
            if (
                option.get("type") == 10
                and option.get("area") == 4
                and card_id(option_source(obs, option)) == DUDUNSPARCE
            ):
                FORCE_READY_PROMOTION = True
        return action
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        options = select.get("option") or []
        minimum = as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(options))))


def agent(obs):
    return safe_action(obs)
