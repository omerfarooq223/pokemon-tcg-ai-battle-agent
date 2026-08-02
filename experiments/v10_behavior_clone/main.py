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
try:
    MAX_ATTACK_DEFERRALS = max(
        0, int(os.environ.get("V10_ATTACK_DEFERRALS", "2"))
    )
except (TypeError, ValueError):
    MAX_ATTACK_DEFERRALS = 2


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
    global LAST_TURN, TURN_START_ACTIVE, SEEN_MENUS, ATTACK_DEFERRALS
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
        balloon_available = AIR_BALLOON in hand_ids(state, yi)
        if cid in (DUNSPARCE, BUNEARY) and (
            has_tool(card, AIR_BALLOON) or energy >= 1 or balloon_available
        ):
            return 5600.0 if cid == DUNSPARCE else 5200.0
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
        # Dunsparce is the preferred opening pivot: it can evolve into the
        # draw engine before yielding the Active Spot, while Buneary remains
        # safe on the Bench until Mega Lopunny is available.
        return {DUNSPARCE: 5200.0, BUNEARY: 4200.0, FAN_ROTOM: 3400.0}.get(cid, 0.0)
    if cid == BUNEARY:
        return 4700.0 - counts.get(BUNEARY, 0) * 900.0 - counts.get(LOPUNNY, 0) * 350.0
    if cid == DUNSPARCE:
        return 4400.0 - counts.get(DUNSPARCE, 0) * 600.0 - counts.get(DUDUNSPARCE, 0) * 250.0
    if cid == FAN_ROTOM:
        first_turn = as_int(state.get("turn"), 0) <= 1
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
            return 6200.0 if counts.get(BUNEARY, 0) else 3000.0
        if cid == DUDUNSPARCE:
            return 4900.0 if counts.get(DUNSPARCE, 0) else 2200.0
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
            return 1800.0 if as_int(state.get("turn"), 0) <= 1 else 100.0
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
    damaged_bench = [
        c for c in bench(state, yi)
        if card_id(c) == LOPUNNY and damage_on(c) > 0
    ]
    active_card = active(state, yi)
    ready_bench = any(lopunny_ready(card) for card in bench(state, yi))
    active_can_pivot = (
        card_id(active_card) == LOPUNNY
        and ready_bench
        and (
            has_tool(active_card, AIR_BALLOON)
            or AIR_BALLOON in hand_ids(state, yi)
        )
    )
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
        # heal a damaged Bench attacker, or heal the Active only when a free
        # retreat into another powered Lopunny preserves this turn's attack.
        eligible = damaged_bench[:]
        if active_can_pivot and damage_on(active_card) > 0:
            eligible.append(active_card)
        largest = max((damage_on(card) for card in eligible), default=0)
        if not eligible:
            value = -4500.0
        else:
            value = 6500.0 + largest * 5.0 if largest >= 80 else 500.0 + largest
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
        return 3900.0 if not supporter_used else 1800.0
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
        score = 4300.0
        if area == 4 and not bool(state.get("retreated")):
            ready_bench = any(lopunny_ready(card) for card in bench(state, yi))
            score += 3600.0 if ready_bench else 900.0
        if target_id == LOPUNNY:
            score += 1400.0
        elif target_id in (DUNSPARCE, BUNEARY):
            score += 1100.0
        return score

    if cid not in ENERGY_IDS:
        return 200.0
    if bool(state.get("energyAttached")) and option.get("area") == 2:
        return -4000.0
    energy_count = attached_count(target)
    if target_id not in (BUNEARY, LOPUNNY):
        # Enriching Energy is also a draw-four engine.  The top line often
        # places it on Fan Rotom or a pivot when no Mega Lopunny is ready.
        if (
            cid == ENRICHING
            and target_id in (DUNSPARCE, FAN_ROTOM)
            and energy_count == 0
        ):
            stadium_live = bool(state.get("stadium"))
            return 7100.0 + (500.0 if target_id == FAN_ROTOM and stadium_live else 0.0)
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
    # Prefer establishing two independent attackers before stacking the second
    # Energy needed for Spiky Hopper.
    if energy_count == 1:
        other_unpowered = any(
            card_id(card) in (BUNEARY, LOPUNNY)
            and card.get("serial") != target.get("serial")
            and attached_count(card) == 0
            for _, _, card in board(state, yi)
        )
        if other_unpowered:
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
        return 7200.0 if area == 5 else 1200.0
    if cid == FAN_ROTOM:
        return 6800.0 if as_int(state.get("turn"), 0) <= 1 else 800.0
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
    return -500.0


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
            return choose_promotion_score(obs, card, context)
        if context == 17 and effect_id == WALLY:
            if cid != LOPUNNY:
                return -5000.0
            if area == 4:
                ready_bench = any(lopunny_ready(c) for c in bench(state, yi))
                if not ready_bench or not (
                    has_tool(card, AIR_BALLOON)
                    or AIR_BALLOON in hand_ids(state, yi)
                ):
                    return -4500.0
            return 3000.0 + damage_on(card) * 12.0 + attached_count(card) * 300.0
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
            or best[0] <= 0
            or best[0] <= best_attack[0] + 500.0
        ):
            return [best_attack[1]]
        ATTACK_DEFERRALS[turn_key] = deferred + 1
        return [best[1]]

    # Poffin/Fan Call-style multi-searches should establish complementary
    # Buneary and Dunsparce lines instead of taking duplicate copies merely
    # because their static scores tie.
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
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        options = select.get("option") or []
        minimum = as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(options))))


def agent(obs):
    return safe_action(obs)


# ---------------------------------------------------------------------------
# Offline-fitted visible-state behavior clone.
# ---------------------------------------------------------------------------

_RULE_CHOOSE_ACTION = choose_action
_CLONE_POKEMON_IDS = (174, 305, 848, 66, 849)
_CLONE_ACTIVE_ID_MAP = {None: 0, 174: 1, 305: 2, 848: 3, 66: 4, 849: 5}
_CLONE_ACTIONS = ((10, 1259, None, 7, None), (10, 174, None, 4, None), (10, 174, None, 5, None), (10, 66, None, 4, None), (10, 66, None, 5, None), (12, None, None, None, None), (13, 1223, None, None, None), (13, 1225, None, None, None), (13, 1226, None, None, None), (13, 230, None, None, None), (14, -14, None, None, None), (7, 1086, None, None, None), (7, 1121, None, None, None), (7, 1122, None, None, None), (7, 1152, None, None, None), (7, 1182, None, None, None), (7, 1197, None, None, None), (7, 1225, None, None, None), (7, 1227, None, None, None), (7, 1229, None, None, None), (7, 174, None, None, None), (7, 305, None, None, None), (7, 848, None, None, None), (8, 11, 174, 2, 4), (8, 11, 174, 2, 5), (8, 11, 305, 2, 4), (8, 11, 305, 2, 5), (8, 11, 66, 2, 4), (8, 11, 66, 2, 5), (8, 11, 848, 2, 4), (8, 11, 848, 2, 5), (8, 11, 849, 2, 4), (8, 11, 849, 2, 5), (8, 1174, 174, 2, 4), (8, 1174, 174, 2, 5), (8, 1174, 305, 2, 4), (8, 1174, 305, 2, 5), (8, 1174, 66, 2, 4), (8, 1174, 66, 2, 5), (8, 1174, 848, 2, 4), (8, 1174, 848, 2, 5), (8, 1174, 849, 2, 4), (8, 1174, 849, 2, 5), (8, 13, 174, 2, 4), (8, 13, 174, 2, 5), (8, 13, 305, 2, 4), (8, 13, 305, 2, 5), (8, 13, 66, 2, 4), (8, 13, 66, 2, 5), (8, 13, 848, 2, 5), (8, 13, 849, 2, 4), (8, 13, 849, 2, 5), (8, 14, 174, 2, 4), (8, 14, 174, 2, 5), (8, 14, 305, 2, 4), (8, 14, 305, 2, 5), (8, 14, 66, 2, 4), (8, 14, 66, 2, 5), (8, 14, 848, 2, 4), (8, 14, 848, 2, 5), (8, 14, 849, 2, 4), (8, 14, 849, 2, 5), (9, 66, 305, 2, 4), (9, 66, 305, 2, 5), (9, 849, 848, 2, 4), (9, 849, 848, 2, 5))
_CLONE_ACTION_INDEX = {action: index for index, action in enumerate(_CLONE_ACTIONS)}
_CLONE_TREES = (('N', 100, 0.5, ('N', 81, 0.5, ('N', 27, 0.5, ('N', 84, 0.5, ('N', 64, 0.5, ('N', 108, 0.5, ('N', 65, 0.5, ('N', 57, 0.5, ('N', 35, 0.5, ('N', 4, 0.5, ('N', 48, 0.5, ('N', 29, 0.5, ('N', 31, 0.5, ('L', ((2, 2), (10, 1), (11, 2), (12, 4), (17, 5), (18, 5), (32, 2), (35, 1), (60, 2))), ('L', ((3, 2), (49, 3), (50, 1)))), ('N', 69, 1.0, ('L', ((10, 6),)), ('L', ((18, 1), (35, 3))))), ('N', 6, 0.5, ('N', 14, 4.5, ('L', ((5, 7),)), ('L', ((5, 2), (32, 1)))), ('N', 1, 4.5, ('L', ((5, 2), (8, 5), (12, 3), (15, 6), (19, 4), (51, 1), (60, 5), (61, 2))), ('L', ((4, 6), (5, 11), (6, 2), (7, 3), (11, 1), (12, 5), (18, 3), (61, 1)))))), ('N', 29, 0.5, ('N', 32, 0.5, ('N', 3, 0.5, ('L', ((15, 3), (17, 3), (19, 1))), ('L', ((0, 1), (4, 3), (7, 2)))), ('L', ((7, 6),))), ('L', ((11, 3),)))), ('N', 9, 2.5, ('N', 22, 2.5, ('N', 16, 5.5, ('N', 14, 2.0, ('L', ((13, 1), (18, 1), (20, 1))), ('L', ((0, 1), (13, 3), (43, 1), (61, 1)))), ('N', 32, 0.5, ('L', ((1, 2), (12, 1))), ('L', ((20, 3),)))), ('L', ((13, 4),))), ('L', ((13, 6),)))), ('N', 17, 8.0, ('N', 11, 7.0, ('N', 1, 6.0, ('N', 83, 0.5, ('L', ((7, 1), (61, 1))), ('L', ((15, 2), (60, 1)))), ('N', 83, 1.5, ('L', ((8, 3), (13, 1))), ('L', ((8, 1), (11, 1))))), ('L', ((5, 3),))), ('N', 70, 0.5, ('N', 56, 1.5, ('N', 40, 1.5, ('N', 68, 1.5, ('L', ((0, 1), (14, 14), (17, 1), (60, 1))), ('L', ((59, 2),))), ('L', ((5, 2),))), ('L', ((13, 1), (29, 2)))), ('L', ((3, 3),))))), ('N', 28, 1.5, ('L', ((22, 11),)), ('N', 79, 0.5, ('N', 40, 1.5, ('L', ((5, 1), (7, 1))), ('L', ((5, 2),))), ('L', ((35, 3),))))), ('N', 22, 0.5, ('N', 1, 6.0, ('L', ((64, 1), (65, 1))), ('L', ((65, 4),))), ('L', ((65, 26),)))), ('N', 0, 10.0, ('N', 93, 0.5, ('N', 67, 0.5, ('N', 78, 1.5, ('N', 7, 4.0, ('N', 65, 0.5, ('N', 38, 2.5, ('N', 32, 0.5, ('L', ((21, 16),)), ('L', ((5, 1), (13, 1), (21, 8)))), ('L', ((11, 1), (21, 1)))), ('N', 12, 2.5, ('L', ((21, 1), (22, 2))), ('L', ((21, 2), (22, 1))))), ('N', 35, 0.5, ('L', ((19, 1), (61, 1))), ('L', ((13, 1), (19, 1))))), ('L', ((35, 2),))), ('N', 96, 1.0, ('L', ((22, 1), (30, 1))), ('L', ((21, 1), (22, 2))))), ('L', ((12, 1), (51, 1)))), ('N', 19, 1.5, ('L', ((21, 3),)), ('N', 48, 0.5, ('L', ((15, 4),)), ('L', ((5, 3),)))))), ('N', 74, 0.5, ('L', ((41, 7),)), ('L', ((41, 1), (59, 3))))), ('N', 105, 0.5, ('N', 23, 0.5, ('N', 1, 9.5, ('N', 41, 2.5, ('N', 22, 0.5, ('N', 3, 0.5, ('N', 0, 7.5, ('N', 67, 0.5, ('N', 24, 2.5, ('L', ((4, 1), (11, 1), (14, 1))), ('N', 13, 2.5, ('L', ((10, 1), (12, 2), (20, 1))), ('L', ((10, 1), (12, 1))))), ('L', ((19, 2),))), ('N', 83, 1.5, ('N', 8, 6.5, ('L', ((5, 3),)), ('L', ((17, 2),))), ('L', ((13, 1), (32, 1))))), ('N', 11, 6.5, ('N', 18, 2.5, ('L', ((8, 2),)), ('L', ((8, 2), (11, 1)))), ('N', 36, 0.5, ('L', ((7, 2), (61, 1))), ('L', ((11, 3),))))), ('N', 17, 12.5, ('N', 17, 0.5, ('L', ((7, 2), (8, 1), (61, 1))), ('N', 7, 6.5, ('N', 20, 0.5, ('N', 15, 8.5, ('L', ((60, 2), (63, 4))), ('L', ((8, 1), (63, 14)))), ('N', 84, 0.5, ('L', ((5, 3), (8, 1), (17, 1), (22, 2), (31, 1), (32, 1), (33, 1), (63, 15), (64, 1))), ('L', ((41, 2),)))), ('N', 14, 3.0, ('L', ((63, 3),)), ('N', 62, 0.5, ('L', ((61, 1), (63, 1))), ('L', ((19, 4),)))))), ('N', 32, 0.5, ('L', ((10, 3),)), ('L', ((2, 5), (49, 1)))))), ('N', 7, 5.0, ('N', 32, 1.5, ('N', 51, 0.5, ('L', ((19, 2),)), ('N', 17, 4.5, ('N', 1, 2.5, ('L', ((8, 2), (61, 1))), ('L', ((8, 4),))), ('N', 57, 0.5, ('L', ((8, 3),)), ('L', ((14, 1), (15, 1)))))), ('N', 61, 1.0, ('L', ((7, 3),)), ('N', 34, 2.0, ('L', ((11, 2),)), ('L', ((60, 2),))))), ('N', 19, 5.0, ('L', ((51, 3),)), ('N', 2, 0.5, ('L', ((32, 2), (61, 1), (65, 2))), ('L', ((5, 1), (19, 1), (41, 4))))))), ('N', 36, 0.5, ('N', 106, 0.5, ('N', 5, 3.5, ('N', 1, 20.0, ('L', ((10, 3),)), ('L', ((10, 1), (35, 1)))), ('N', 30, 1.5, ('N', 13, 3.5, ('L', ((7, 3),)), ('N', 14, 1.5, ('L', ((7, 2),)), ('N', 42, 0.5, ('L', ((0, 2), (3, 1), (11, 2), (16, 1))), ('L', ((8, 2), (10, 2), (22, 2)))))), ('N', 96, 1.0, ('N', 1, 11.5, ('N', 4, 0.5, ('L', ((3, 1), (61, 2))), ('L', ((16, 2), (60, 1)))), ('N', 20, 0.5, ('L', ((5, 1), (13, 2), (41, 1))), ('L', ((5, 2), (41, 1))))), ('L', ((59, 2),))))), ('N', 77, 1.0, ('N', 84, 1.0, ('L', ((63, 4),)), ('L', ((41, 2),))), ('L', ((50, 2),)))), ('N', 85, 1.0, ('N', 33, 0.5, ('N', 17, 10.5, ('N', 12, 8.5, ('N', 96, 1.0, ('L', ((14, 2),)), ('L', ((60, 3),))), ('L', ((14, 5),))), ('L', ((14, 7),))), ('L', ((11, 2),))), ('N', 58, 0.5, ('N', 11, 5.5, ('L', ((8, 2),)), ('L', ((63, 2),))), ('L', ((5, 2),)))))), ('N', 24, 0.5, ('N', 58, 0.5, ('N', 17, 4.5, ('L', ((7, 1), (31, 1))), ('N', 1, 11.0, ('L', ((0, 1), (5, 1))), ('L', ((7, 6),)))), ('N', 7, 3.5, ('L', ((11, 2),)), ('N', 2, 0.5, ('L', ((0, 1), (7, 1), (61, 3))), ('L', ((5, 1), (13, 2), (63, 1)))))), ('N', 79, 0.5, ('N', 23, 1.5, ('L', ((21, 14),)), ('N', 98, 1.0, ('L', ((11, 2), (21, 2))), ('L', ((58, 2),)))), ('N', 0, 6.0, ('N', 77, 0.5, ('L', ((7, 2),)), ('L', ((21, 3), (22, 1)))), ('L', ((63, 5),)))))), ('N', 24, 0.5, ('L', ((63, 2),)), ('L', ((62, 10),))))), ('N', 25, 0.5, ('L', ((4, 24),)), ('L', ((22, 2),)))), ('N', 34, 0.5, ('N', 47, 1.5, ('N', 0, 3.5, ('L', ((4, 1), (41, 2), (63, 1))), ('L', ((4, 4),))), ('L', ((4, 1), (17, 1), (64, 4)))), ('L', ((4, 8),)))), ('N', 64, 0.5, ('N', 48, 0.5, ('N', 8, 5.0, ('N', 26, 0.5, ('N', 62, 0.5, ('N', 106, 0.5, ('N', 35, 0.5, ('N', 54, 0.5, ('N', 61, 0.5, ('N', 5, 4.0, ('N', 40, 2.5, ('N', 78, 0.5, ('N', 16, 5.5, ('L', ((10, 4), (12, 1), (14, 1), (22, 2), (49, 1), (65, 1))), ('L', ((9, 1), (10, 13), (17, 1)))), ('N', 32, 0.5, ('L', ((10, 2), (14, 1), (22, 1))), ('L', ((35, 6), (65, 2))))), ('L', ((2, 2),))), ('N', 40, 0.5, ('L', ((12, 4), (15, 1))), ('L', ((8, 2),)))), ('N', 9, 0.5, ('L', ((18, 3),)), ('L', ((15, 1), (18, 1), (22, 2))))), ('N', 37, 0.5, ('N', 29, 0.5, ('N', 45, 0.5, ('L', ((11, 2), (61, 1))), ('L', ((2, 2),))), ('L', ((65, 2),))), ('L', ((11, 3),)))), ('N', 45, 0.5, ('N', 44, 0.5, ('N', 75, 1.0, ('N', 65, 0.5, ('N', 36, 0.5, ('N', 21, 0.5, ('L', ((13, 7), (46, 1))), ('L', ((20, 2),))), ('L', ((14, 4),))), ('L', ((22, 4),))), ('L', ((43, 2),))), ('L', ((1, 3),))), ('L', ((2, 5),)))), ('N', 105, 0.5, ('N', 13, 4.0, ('L', ((63, 2),)), ('L', ((65, 2),))), ('L', ((62, 6),)))), ('L', ((33, 4),))), ('N', 11, 6.5, ('N', 46, 0.5, ('L', ((4, 5),)), ('N', 22, 0.5, ('L', ((49, 2),)), ('N', 38, 0.5, ('L', ((18, 3),)), ('L', ((4, 1), (11, 1)))))), ('N', 55, 1.0, ('N', 2, 0.5, ('N', 65, 0.5, ('N', 104, 1.0, ('L', ((17, 4),)), ('L', ((59, 2),))), ('L', ((3, 1), (11, 1)))), ('N', 20, 0.5, ('L', ((3, 2), (22, 1))), ('L', ((3, 2),)))), ('L', ((32, 3),))))), ('N', 3, 0.5, ('N', 14, 4.5, ('N', 60, 0.5, ('L', ((7, 1), (8, 1), (65, 4))), ('N', 84, 0.5, ('N', 41, 1.5, ('N', 55, 0.5, ('N', 11, 5.5, ('L', ((7, 1), (17, 1))), ('L', ((17, 2),))), ('N', 1, 8.5, ('L', ((7, 1), (17, 2))), ('L', ((7, 2),)))), ('N', 60, 1.5, ('L', ((19, 3),)), ('N', 34, 1.5, ('L', ((31, 2),)), ('L', ((4, 1), (8, 1), (63, 1)))))), ('L', ((41, 4), (59, 1))))), ('L', ((0, 1), (16, 3)))), ('N', 2, 0.5, ('N', 65, 0.5, ('N', 30, 0.5, ('N', 36, 1.0, ('L', ((7, 1), (13, 2))), ('L', ((61, 2),))), ('N', 11, 6.5, ('L', ((60, 5),)), ('N', 50, 0.5, ('L', ((60, 2),)), ('L', ((61, 2),))))), ('L', ((7, 2),))), ('N', 106, 0.5, ('N', 30, 0.5, ('N', 55, 1.0, ('N', 39, 0.5, ('N', 40, 2.5, ('N', 19, 4.5, ('L', ((0, 2), (7, 1))), ('L', ((0, 2), (7, 1)))), ('L', ((4, 1), (7, 2)))), ('L', ((0, 2),))), ('L', ((12, 3), (41, 1)))), ('N', 34, 0.5, ('N', 33, 0.5, ('N', 9, 2.5, ('N', 29, 0.5, ('L', ((4, 1), (7, 1), (41, 1))), ('L', ((7, 2),))), ('N', 40, 1.5, ('L', ((7, 3), (8, 1))), ('L', ((7, 4),)))), ('L', ((11, 4),))), ('N', 1, 10.5, ('L', ((7, 2), (65, 1))), ('L', ((7, 8),))))), ('N', 20, 0.5, ('L', ((63, 3),)), ('L', ((7, 1), (8, 3)))))))), ('N', 47, 0.5, ('N', 107, 0.5, ('N', 54, 0.5, ('N', 108, 0.5, ('N', 69, 0.5, ('N', 0, 3.5, ('N', 57, 0.5, ('N', 25, 0.5, ('N', 3, 0.5, ('L', ((18, 4),)), ('N', 55, 0.5, ('N', 1, 14.0, ('L', ((13, 4),)), ('L', ((6, 1), (13, 1)))), ('N', 35, 0.5, ('L', ((0, 1), (5, 1), (9, 3))), ('L', ((0, 2),))))), ('N', 106, 1.0, ('L', ((22, 6),)), ('L', ((63, 3),)))), ('N', 40, 1.5, ('N', 5, 4.0, ('L', ((14, 3),)), ('L', ((14, 2), (60, 1)))), ('L', ((14, 1), (15, 1))))), ('N', 51, 0.5, ('N', 106, 0.5, ('N', 30, 1.5, ('N', 32, 1.5, ('N', 39, 0.5, ('L', ((5, 11), (12, 2), (18, 1), (19, 1), (61, 1))), ('L', ((7, 4), (14, 1), (15, 2), (41, 6), (61, 1)))), ('N', 96, 1.0, ('L', ((10, 1), (17, 1))), ('L', ((60, 6),)))), ('N', 16, 6.5, ('N', 15, 13.0, ('L', ((5, 7),)), ('L', ((14, 2),))), ('L', ((5, 8),)))), ('N', 6, 0.5, ('N', 10, 1.0, ('L', ((5, 3),)), ('L', ((60, 2),))), ('N', 14, 4.5, ('L', ((63, 9),)), ('L', ((19, 1), (41, 1), (51, 1)))))), ('N', 11, 5.5, ('N', 60, 1.5, ('N', 7, 4.5, ('N', 34, 3.0, ('L', ((8, 7),)), ('L', ((8, 1), (14, 1), (61, 1)))), ('N', 30, 0.5, ('L', ((63, 2),)), ('L', ((5, 1), (13, 1), (32, 2))))), ('L', ((15, 3),))), ('N', 17, 9.5, ('N', 32, 0.5, ('N', 35, 1.5, ('L', ((8, 1), (63, 10))), ('L', ((19, 2),))), ('L', ((15, 1), (19, 2)))), ('L', ((17, 3), (51, 1))))))), ('N', 18, 1.5, ('L', ((8, 3),)), ('N', 37, 0.5, ('N', 13, 2.5, ('L', ((63, 4),)), ('N', 34, 0.5, ('N', 15, 4.5, ('L', ((32, 2),)), ('N', 61, 0.5, ('L', ((61, 3), (63, 1))), ('L', ((5, 2), (19, 2))))), ('N', 40, 1.5, ('N', 7, 5.5, ('L', ((12, 2), (14, 2), (60, 1))), ('L', ((12, 3),))), ('L', ((31, 1), (59, 1)))))), ('N', 42, 0.5, ('N', 103, 1.5, ('N', 1, 6.5, ('N', 58, 0.5, ('L', ((60, 2),)), ('L', ((15, 1), (63, 1)))), ('L', ((18, 3),))), ('L', ((61, 3),))), ('N', 17, 8.5, ('L', ((61, 5),)), ('L', ((61, 1), (63, 1)))))))), ('L', ((65, 8),))), ('N', 79, 1.5, ('N', 1, 8.0, ('N', 1, 6.0, ('N', 58, 1.5, ('N', 24, 0.5, ('L', ((12, 2),)), ('L', ((8, 1), (41, 1), (63, 1)))), ('L', ((11, 2),))), ('N', 17, 9.5, ('L', ((65, 4),)), ('L', ((5, 2),)))), ('N', 40, 0.5, ('L', ((11, 6),)), ('N', 22, 1.5, ('L', ((11, 3), (41, 1))), ('L', ((22, 2),))))), ('N', 61, 0.5, ('N', 15, 11.5, ('L', ((63, 4),)), ('L', ((5, 1), (63, 1)))), ('N', 96, 1.5, ('N', 37, 3.5, ('N', 2, 0.5, ('N', 27, 1.5, ('N', 39, 0.5, ('L', ((15, 1), (17, 1))), ('L', ((8, 6),))), ('L', ((63, 2),))), ('L', ((8, 4),))), ('L', ((15, 2),))), ('L', ((61, 2),)))))), ('L', ((64, 4),))), ('N', 50, 0.5, ('L', ((17, 1), (63, 1))), ('N', 18, 3.5, ('N', 33, 0.5, ('L', ((4, 2), (18, 1))), ('L', ((4, 6),))), ('L', ((4, 31),)))))), ('N', 11, 2.5, ('N', 12, 8.5, ('N', 106, 0.5, ('N', 67, 0.5, ('N', 64, 1.5, ('N', 5, 1.5, ('L', ((11, 1), (21, 1))), ('N', 65, 0.5, ('L', ((21, 14),)), ('N', 13, 3.5, ('L', ((21, 2), (22, 1))), ('L', ((21, 2),))))), ('N', 13, 2.5, ('L', ((22, 2),)), ('L', ((21, 2),)))), ('L', ((22, 1), (30, 2)))), ('L', ((60, 1), (63, 1)))), ('N', 28, 2.5, ('L', ((8, 2), (21, 1))), ('L', ((5, 2), (8, 3))))), ('N', 29, 0.5, ('N', 7, 5.0, ('N', 92, 1.0, ('N', 33, 0.5, ('N', 10, 5.5, ('N', 68, 0.5, ('L', ((21, 13),)), ('L', ((21, 1), (22, 1)))), ('L', ((21, 1), (31, 1)))), ('N', 1, 12.5, ('N', 28, 1.5, ('N', 48, 0.5, ('L', ((58, 2),)), ('L', ((11, 1), (22, 3)))), ('N', 17, 7.5, ('L', ((0, 1), (7, 1))), ('L', ((5, 1), (7, 1))))), ('L', ((21, 3),)))), ('L', ((12, 2), (51, 1)))), ('N', 47, 0.5, ('N', 16, 5.5, ('N', 32, 0.5, ('L', ((19, 1), (22, 1))), ('N', 17, 5.5, ('L', ((5, 3),)), ('L', ((0, 1), (5, 3))))), ('N', 32, 1.5, ('N', 106, 1.0, ('L', ((13, 1), (19, 1), (61, 1))), ('L', ((63, 2),))), ('L', ((21, 2),)))), ('L', ((4, 4),)))), ('N', 17, 12.0, ('N', 13, 1.5, ('N', 50, 0.5, ('L', ((60, 2),)), ('N', 74, 0.5, ('L', ((7, 2),)), ('L', ((7, 1), (13, 1), (19, 1))))), ('N', 14, 5.0, ('N', 79, 0.5, ('L', ((65, 3),)), ('L', ((13, 1), (35, 1), (63, 1)))), ('L', ((15, 3),)))), ('L', ((44, 3),)))))), ('N', 64, 0.5, ('N', 71, 0.5, ('N', 106, 0.5, ('N', 48, 0.5, ('N', 50, 0.5, ('N', 108, 0.5, ('N', 54, 0.5, ('N', 1, 6.5, ('N', 98, 0.5, ('N', 26, 0.5, ('N', 5, 2.5, ('N', 59, 0.5, ('N', 73, 0.5, ('L', ((10, 2), (13, 2), (14, 4), (17, 1), (18, 5))), ('L', ((14, 4), (20, 2)))), ('N', 25, 0.5, ('L', ((13, 2),)), ('L', ((22, 2),)))), ('N', 60, 0.5, ('N', 9, 0.5, ('L', ((10, 2), (29, 1))), ('L', ((10, 1), (12, 2)))), ('L', ((29, 2),)))), ('N', 5, 2.5, ('L', ((4, 2),)), ('N', 75, 1.0, ('N', 11, 6.5, ('L', ((18, 1), (49, 1))), ('L', ((3, 2),))), ('L', ((3, 1), (32, 1)))))), ('N', 11, 8.5, ('L', ((49, 5),)), ('L', ((17, 2), (50, 1))))), ('N', 0, 2.5, ('L', ((10, 7),)), ('N', 55, 1.5, ('N', 78, 0.5, ('N', 8, 3.5, ('N', 17, 6.5, ('L', ((10, 2),)), ('L', ((10, 2), (43, 1)))), ('N', 8, 7.0, ('L', ((3, 1), (18, 1), (22, 1))), ('L', ((60, 2),)))), ('N', 11, 9.0, ('L', ((10, 1), (35, 2))), ('L', ((35, 5),)))), ('L', ((3, 2),))))), ('N', 40, 1.5, ('N', 36, 1.5, ('L', ((11, 7),)), ('L', ((2, 1), (11, 1)))), ('L', ((3, 2), (11, 1))))), ('L', ((65, 9),))), ('N', 31, 0.5, ('N', 6, 1.5, ('N', 55, 1.5, ('N', 16, 5.5, ('N', 84, 0.5, ('N', 29, 0.5, ('N', 74, 1.0, ('N', 34, 0.5, ('L', ((0, 1), (7, 22), (13, 1))), ('L', ((7, 6), (17, 1), (19, 1)))), ('L', ((19, 1), (61, 2)))), ('L', ((65, 2),))), ('L', ((41, 2),))), ('N', 32, 0.5, ('N', 41, 2.0, ('N', 17, 6.5, ('L', ((4, 3), (12, 1))), ('N', 20, 0.5, ('L', ((17, 1), (65, 1))), ('L', ((17, 2),)))), ('L', ((11, 2),))), ('N', 13, 2.5, ('N', 28, 1.5, ('L', ((60, 2),)), ('L', ((11, 1), (41, 1)))), ('N', 1, 6.5, ('L', ((7, 1), (65, 1))), ('L', ((7, 4),)))))), ('N', 77, 0.5, ('L', ((12, 3),)), ('L', ((7, 1), (14, 1), (41, 1))))), ('N', 47, 0.5, ('N', 19, 3.5, ('N', 54, 0.5, ('N', 11, 6.5, ('L', ((7, 2),)), ('L', ((7, 1), (14, 1), (17, 1)))), ('L', ((11, 2),))), ('N', 32, 2.0, ('N', 17, 3.5, ('L', ((8, 2),)), ('N', 14, 4.5, ('L', ((8, 2),)), ('L', ((12, 2),)))), ('L', ((8, 1), (13, 2))))), ('L', ((4, 3),)))), ('N', 81, 1.0, ('N', 1, 14.0, ('L', ((0, 2),)), ('L', ((14, 2),))), ('L', ((4, 2),))))), ('N', 58, 1.5, ('N', 26, 0.5, ('N', 89, 0.5, ('N', 7, 4.5, ('N', 6, 1.5, ('N', 75, 0.5, ('N', 96, 1.0, ('N', 108, 0.5, ('N', 17, 7.5, ('L', ((5, 11), (17, 1))), ('L', ((0, 2), (5, 4), (7, 1), (9, 1), (10, 3), (11, 1), (12, 3), (13, 5), (14, 7), (17, 1), (18, 2), (22, 3)))), ('L', ((65, 5),))), ('L', ((60, 3),))), ('N', 73, 1.5, ('N', 20, 0.5, ('L', ((32, 1), (59, 1), (61, 1))), ('N', 7, 3.5, ('L', ((32, 1), (60, 2))), ('L', ((60, 3),)))), ('L', ((50, 3),)))), ('N', 30, 1.5, ('N', 34, 1.5, ('N', 17, 11.5, ('N', 1, 11.0, ('L', ((11, 2), (17, 1))), ('L', ((8, 1), (13, 2), (14, 6)))), ('L', ((8, 1), (17, 2)))), ('N', 103, 1.5, ('N', 62, 1.0, ('L', ((0, 1), (8, 7), (14, 2), (41, 2))), ('L', ((15, 3),))), ('L', ((61, 3),)))), ('N', 28, 1.5, ('L', ((12, 1), (65, 3))), ('L', ((11, 1), (65, 1)))))), ('N', 17, 8.5, ('N', 98, 0.5, ('N', 17, 6.5, ('N', 58, 0.5, ('L', ((5, 6),)), ('N', 8, 2.0, ('L', ((19, 2),)), ('L', ((5, 3),)))), ('N', 55, 1.5, ('L', ((5, 2), (12, 1), (13, 1))), ('L', ((32, 3),)))), ('N', 12, 8.0, ('L', ((65, 2),)), ('N', 0, 10.5, ('L', ((19, 1), (61, 1))), ('L', ((61, 2),))))), ('N', 14, 4.5, ('L', ((5, 1), (41, 2))), ('L', ((19, 2), (41, 4)))))), ('L', ((51, 6),))), ('N', 5, 4.0, ('L', ((17, 1), (64, 3))), ('N', 15, 4.0, ('L', ((4, 1), (18, 3))), ('N', 37, 0.5, ('L', ((4, 12),)), ('N', 100, 1.0, ('L', ((4, 5),)), ('L', ((41, 2),))))))), ('N', 19, 2.5, ('L', ((13, 1), (18, 1))), ('N', 30, 3.5, ('N', 102, 0.5, ('L', ((5, 9),)), ('L', ((5, 3), (59, 1)))), ('L', ((11, 1), (12, 1))))))), ('N', 96, 1.5, ('N', 0, 16.5, ('N', 1, 2.5, ('N', 7, 6.5, ('N', 37, 3.0, ('N', 8, 3.5, ('N', 9, 1.5, ('N', 5, 2.0, ('N', 69, 1.0, ('N', 28, 0.5, ('L', ((65, 2),)), ('L', ((33, 1), (63, 1)))), ('L', ((32, 2),))), ('L', ((64, 2),))), ('L', ((62, 3),))), ('N', 94, 0.5, ('N', 106, 1.5, ('L', ((31, 2), (61, 1), (63, 1))), ('N', 8, 9.0, ('L', ((63, 9),)), ('N', 47, 0.5, ('L', ((63, 5),)), ('L', ((4, 2),))))), ('L', ((51, 2),)))), ('L', ((15, 3),))), ('N', 13, 3.5, ('L', ((19, 6),)), ('L', ((41, 1), (63, 1))))), ('N', 15, 2.5, ('L', ((62, 2),)), ('N', 16, 1.5, ('L', ((8, 2),)), ('N', 50, 0.5, ('N', 0, 4.0, ('L', ((63, 6),)), ('N', 41, 0.5, ('L', ((60, 3),)), ('L', ((22, 1), (62, 1))))), ('N', 8, 4.0, ('N', 57, 1.0, ('L', ((19, 1), (61, 1), (63, 3))), ('L', ((63, 2),))), ('N', 37, 0.5, ('L', ((63, 15),)), ('N', 85, 0.5, ('N', 27, 1.5, ('L', ((41, 1), (50, 1))), ('L', ((4, 1), (63, 4)))), ('N', 20, 0.5, ('L', ((60, 1), (63, 6))), ('L', ((22, 1), (63, 9))))))))))), ('N', 62, 1.5, ('N', 6, 1.5, ('L', ((5, 2), (7, 1))), ('L', ((8, 6),))), ('N', 1, 3.5, ('N', 67, 1.0, ('L', ((41, 2),)), ('L', ((32, 2), (65, 1)))), ('L', ((5, 2),))))), ('N', 56, 1.0, ('N', 47, 0.5, ('L', ((31, 2),)), ('L', ((4, 2),))), ('L', ((60, 3),))))), ('L', ((4, 16),))), ('N', 106, 1.5, ('N', 30, 1.5, ('N', 73, 1.5, ('N', 27, 1.5, ('N', 11, 2.5, ('N', 34, 1.5, ('N', 11, 1.5, ('L', ((8, 1), (21, 2))), ('N', 65, 0.5, ('L', ((21, 12),)), ('L', ((21, 3), (22, 1))))), ('L', ((5, 1), (8, 1)))), ('N', 13, 3.5, ('N', 74, 0.5, ('N', 98, 0.5, ('N', 17, 9.0, ('N', 16, 6.5, ('N', 37, 1.5, ('L', ((41, 1), (65, 2))), ('L', ((19, 1), (21, 1), (51, 1)))), ('L', ((7, 2),))), ('N', 0, 1.5, ('L', ((11, 1), (21, 1), (22, 2))), ('N', 61, 1.0, ('N', 40, 1.5, ('L', ((21, 4),)), ('L', ((21, 3), (22, 1)))), ('L', ((21, 2), (65, 1)))))), ('N', 41, 0.5, ('L', ((58, 2),)), ('L', ((13, 2), (61, 1))))), ('L', ((17, 2),))), ('N', 81, 0.5, ('N', 40, 2.5, ('N', 37, 1.5, ('N', 12, 3.5, ('L', ((5, 2), (44, 1))), ('L', ((13, 1), (21, 2)))), ('L', ((35, 5),))), ('L', ((17, 3),))), ('L', ((4, 4),))))), ('L', ((21, 11),))), ('N', 12, 4.5, ('L', ((30, 2),)), ('L', ((59, 4),)))), ('N', 27, 1.5, ('N', 60, 1.5, ('N', 54, 0.5, ('N', 34, 0.5, ('L', ((21, 2),)), ('N', 58, 0.5, ('L', ((21, 1), (22, 1))), ('L', ((5, 2), (15, 1))))), ('L', ((0, 2), (4, 1), (5, 5), (11, 2)))), ('L', ((19, 2),))), ('N', 16, 10.0, ('L', ((5, 1), (7, 3))), ('L', ((7, 1), (19, 1)))))), ('L', ((13, 5),)))), ('N', 23, 0.5, ('N', 106, 0.5, ('N', 47, 0.5, ('N', 29, 0.5, ('N', 8, 9.0, ('N', 48, 0.5, ('N', 15, 5.5, ('N', 73, 0.5, ('N', 22, 0.5, ('N', 21, 0.5, ('N', 0, 9.5, ('L', ((10, 4),)), ('L', ((12, 1), (15, 1)))), ('L', ((20, 2),))), ('N', 34, 0.5, ('L', ((10, 1), (18, 2))), ('N', 11, 4.5, ('L', ((12, 1), (49, 1))), ('L', ((3, 1), (22, 1)))))), ('L', ((32, 5), (62, 1)))), ('N', 54, 0.5, ('N', 31, 0.5, ('N', 11, 9.5, ('N', 102, 0.5, ('N', 60, 0.5, ('N', 32, 0.5, ('L', ((3, 1), (10, 1), (22, 1))), ('L', ((7, 1), (14, 1)))), ('N', 15, 11.0, ('L', ((17, 8), (22, 1))), ('L', ((8, 1), (13, 1))))), ('L', ((2, 1), (59, 2)))), ('N', 5, 3.0, ('N', 83, 1.5, ('L', ((35, 3),)), ('N', 22, 1.5, ('L', ((10, 2), (35, 3))), ('L', ((12, 1), (14, 1))))), ('L', ((17, 2), (59, 1))))), ('N', 19, 5.5, ('L', ((49, 5),)), ('L', ((3, 2), (43, 1))))), ('N', 45, 0.5, ('N', 9, 2.5, ('L', ((11, 8),)), ('N', 11, 9.0, ('L', ((22, 1), (49, 1))), ('L', ((11, 2),)))), ('L', ((2, 2),))))), ('N', 96, 0.5, ('N', 51, 0.5, ('N', 16, 3.5, ('N', 56, 0.5, ('N', 15, 4.5, ('L', ((12, 2),)), ('L', ((5, 1), (19, 1), (61, 1)))), ('N', 42, 0.5, ('L', ((13, 2),)), ('L', ((13, 2), (14, 1), (18, 1))))), ('N', 104, 0.5, ('N', 17, 7.0, ('N', 62, 0.5, ('L', ((5, 11),)), ('L', ((5, 2), (19, 1)))), ('N', 62, 0.5, ('N', 73, 1.0, ('L', ((5, 1), (10, 1), (14, 2))), ('L', ((5, 2),))), ('L', ((11, 1), (41, 2))))), ('N', 7, 3.0, ('L', ((59, 2), (62, 1))), ('L', ((61, 2),))))), ('N', 0, 8.5, ('N', 7, 5.0, ('L', ((8, 1), (11, 1), (17, 1))), ('N', 35, 0.5, ('L', ((5, 3),)), ('L', ((13, 1), (32, 1))))), ('N', 59, 0.5, ('N', 13, 3.5, ('L', ((8, 2), (14, 1))), ('L', ((8, 7),))), ('N', 16, 8.0, ('L', ((16, 3),)), ('L', ((8, 2), (19, 1))))))), ('N', 51, 0.5, ('N', 13, 3.5, ('N', 9, 2.5, ('L', ((60, 2),)), ('L', ((5, 1), (60, 1)))), ('L', ((60, 6),))), ('N', 57, 1.5, ('L', ((61, 4),)), ('L', ((8, 2),)))))), ('N', 51, 0.5, ('N', 62, 0.5, ('N', 96, 0.5, ('N', 2, 0.5, ('N', 16, 9.5, ('N', 13, 2.5, ('N', 56, 0.5, ('L', ((17, 1), (60, 2))), ('L', ((13, 3),))), ('N', 34, 1.5, ('N', 28, 1.5, ('L', ((14, 1), (15, 1), (22, 1))), ('L', ((5, 1), (32, 2), (50, 1)))), ('L', ((12, 2),)))), ('L', ((61, 2),))), ('N', 33, 0.5, ('N', 22, 2.5, ('N', 43, 0.5, ('N', 57, 0.5, ('L', ((5, 5), (7, 24), (12, 1), (41, 1))), ('L', ((7, 2), (14, 5)))), ('N', 22, 0.5, ('L', ((7, 2),)), ('L', ((0, 5),)))), ('N', 58, 1.0, ('N', 15, 11.5, ('L', ((17, 1), (41, 1))), ('L', ((7, 2),))), ('L', ((16, 2),)))), ('N', 0, 11.0, ('N', 12, 8.5, ('L', ((7, 1), (41, 2))), ('L', ((11, 5),))), ('L', ((5, 1), (7, 3)))))), ('N', 22, 1.0, ('L', ((11, 1), (60, 1), (61, 1))), ('L', ((60, 2),)))), ('N', 61, 0.5, ('L', ((19, 3),)), ('N', 22, 1.5, ('L', ((41, 2),)), ('L', ((17, 2),))))), ('N', 18, 5.5, ('N', 33, 0.5, ('L', ((8, 4),)), ('L', ((11, 3),))), ('N', 37, 1.5, ('N', 20, 0.5, ('N', 30, 0.5, ('L', ((17, 2),)), ('N', 17, 8.0, ('L', ((5, 2), (15, 1))), ('N', 15, 8.0, ('L', ((11, 1), (13, 1))), ('L', ((12, 2), (22, 1)))))), ('N', 11, 4.0, ('L', ((8, 1), (14, 1))), ('N', 27, 1.5, ('L', ((14, 4),)), ('L', ((7, 1), (13, 1)))))), ('L', ((41, 3),)))))), ('N', 19, 4.5, ('N', 33, 0.5, ('N', 75, 0.5, ('N', 38, 1.5, ('L', ((7, 2), (65, 1))), ('L', ((7, 5),))), ('N', 79, 1.5, ('L', ((51, 1), (60, 1), (65, 1))), ('L', ((35, 2),)))), ('N', 54, 1.5, ('L', ((11, 6),)), ('L', ((5, 2), (11, 1))))), ('N', 5, 3.5, ('N', 1, 14.0, ('N', 56, 0.5, ('N', 1, 2.5, ('L', ((65, 4),)), ('N', 39, 0.5, ('L', ((10, 1), (65, 2))), ('N', 1, 6.5, ('L', ((10, 2), (64, 1))), ('L', ((10, 3),))))), ('N', 14, 0.5, ('N', 40, 0.5, ('L', ((14, 3), (20, 1))), ('L', ((1, 2),))), ('N', 55, 0.5, ('N', 35, 1.5, ('N', 30, 1.0, ('L', ((13, 2), (46, 1))), ('L', ((13, 5),))), ('L', ((13, 2), (22, 1)))), ('L', ((2, 1), (13, 2)))))), ('L', ((9, 4),))), ('L', ((65, 16),))))), ('N', 26, 1.5, ('N', 102, 1.5, ('L', ((4, 30),)), ('N', 35, 1.5, ('L', ((4, 3),)), ('L', ((4, 1), (41, 1))))), ('N', 90, 0.5, ('N', 79, 1.0, ('N', 15, 3.5, ('L', ((18, 4),)), ('L', ((14, 1), (17, 1), (22, 1)))), ('L', ((4, 1), (22, 1)))), ('L', ((49, 5),))))), ('N', 81, 0.5, ('N', 15, 14.5, ('N', 105, 0.5, ('N', 108, 0.5, ('N', 17, 5.5, ('N', 62, 0.5, ('N', 98, 1.0, ('L', ((51, 1), (63, 2))), ('L', ((60, 1), (61, 1)))), ('L', ((19, 5),))), ('N', 76, 0.5, ('N', 0, 12.5, ('N', 100, 0.5, ('N', 65, 0.5, ('N', 1, 9.0, ('N', 32, 2.0, ('L', ((63, 32),)), ('L', ((5, 1), (63, 6)))), ('N', 32, 0.5, ('L', ((3, 1), (50, 1), (63, 1))), ('L', ((41, 1), (63, 3))))), ('N', 1, 5.0, ('L', ((63, 4),)), ('L', ((22, 1), (31, 3))))), ('N', 13, 4.5, ('L', ((63, 3),)), ('L', ((4, 2),)))), ('L', ((8, 2),))), ('L', ((33, 3),)))), ('N', 49, 0.5, ('L', ((8, 1), (65, 1))), ('L', ((64, 2),)))), ('N', 33, 0.5, ('L', ((62, 5),)), ('N', 22, 2.5, ('L', ((62, 2),)), ('L', ((63, 2),))))), ('N', 5, 4.0, ('L', ((5, 3),)), ('N', 13, 3.5, ('L', ((15, 1), (63, 1))), ('N', 32, 1.5, ('N', 74, 0.5, ('N', 7, 2.0, ('L', ((5, 1), (8, 2))), ('L', ((8, 6),))), ('N', 12, 7.5, ('L', ((8, 1), (65, 1))), ('L', ((61, 2),)))), ('N', 2, 0.5, ('L', ((60, 2), (63, 1))), ('L', ((7, 2),))))))), ('L', ((4, 5),)))), ('N', 38, 2.5, ('N', 12, 8.5, ('N', 101, 1.0, ('N', 79, 0.5, ('N', 20, 0.5, ('L', ((21, 13),)), ('N', 64, 0.5, ('L', ((12, 2),)), ('N', 40, 0.5, ('N', 25, 0.5, ('L', ((11, 1), (21, 1))), ('N', 54, 0.5, ('L', ((21, 1), (22, 1))), ('L', ((22, 2),)))), ('L', ((21, 9),))))), ('N', 69, 0.5, ('N', 83, 0.5, ('L', ((5, 1), (15, 2))), ('N', 79, 1.5, ('N', 18, 5.0, ('L', ((13, 1), (21, 1))), ('L', ((5, 2),))), ('N', 11, 2.5, ('L', ((60, 1), (63, 1))), ('L', ((35, 3),))))), ('N', 15, 7.5, ('L', ((59, 4),)), ('L', ((22, 4),))))), ('L', ((58, 3),))), ('N', 15, 8.5, ('N', 26, 0.5, ('N', 25, 0.5, ('N', 33, 0.5, ('L', ((21, 6),)), ('L', ((8, 1), (21, 1)))), ('L', ((22, 4),))), ('L', ((4, 3),))), ('N', 48, 0.5, ('N', 43, 0.5, ('N', 2, 0.5, ('L', ((7, 2), (41, 1))), ('L', ((7, 1), (11, 1), (21, 1)))), ('N', 34, 1.5, ('N', 15, 9.5, ('L', ((0, 2),)), ('L', ((0, 2), (7, 1)))), ('L', ((12, 2),)))), ('N', 17, 8.5, ('N', 102, 0.5, ('N', 54, 0.5, ('N', 41, 0.5, ('L', ((5, 5),)), ('L', ((5, 1), (22, 1)))), ('N', 34, 2.5, ('N', 1, 3.5, ('L', ((61, 2),)), ('L', ((5, 4),))), ('N', 2, 0.5, ('L', ((19, 2),)), ('L', ((21, 3),))))), ('L', ((21, 3),))), ('L', ((4, 3), (13, 1))))))), ('N', 43, 0.5, ('N', 27, 1.5, ('N', 9, 2.0, ('L', ((13, 2),)), ('L', ((13, 2), (17, 1)))), ('L', ((7, 1), (60, 1)))), ('N', 104, 0.5, ('L', ((13, 1), (63, 2))), ('L', ((4, 1), (63, 3))))))), ('N', 84, 0.5, ('N', 64, 0.5, ('N', 6, 0.5, ('N', 46, 0.5, ('N', 102, 0.5, ('N', 48, 0.5, ('N', 58, 0.5, ('N', 13, 0.5, ('L', ((11, 4),)), ('N', 43, 0.5, ('N', 60, 0.5, ('N', 56, 0.5, ('N', 73, 1.0, ('N', 36, 0.5, ('L', ((10, 21), (35, 1), (60, 1), (65, 2))), ('L', ((11, 1), (14, 3), (39, 1)))), ('L', ((29, 2),))), ('N', 63, 0.5, ('N', 25, 0.5, ('L', ((1, 1), (2, 2), (13, 3), (14, 2), (46, 1))), ('L', ((13, 2),))), ('L', ((20, 2),)))), ('N', 79, 1.0, ('N', 37, 0.5, ('N', 13, 3.5, ('L', ((22, 3), (29, 1))), ('L', ((11, 1), (18, 1)))), ('L', ((2, 2),))), ('L', ((33, 2),)))), ('N', 12, 2.5, ('L', ((4, 1), (43, 2))), ('L', ((62, 5),))))), ('N', 1, 4.5, ('N', 42, 1.0, ('N', 79, 0.5, ('L', ((12, 2),)), ('L', ((13, 1), (14, 1), (22, 1)))), ('N', 106, 1.0, ('L', ((4, 1), (65, 2))), ('L', ((65, 3),)))), ('L', ((17, 6),)))), ('N', 19, 2.5, ('N', 41, 0.5, ('L', ((60, 2),)), ('L', ((51, 2),))), ('N', 15, 5.5, ('L', ((5, 1), (32, 4))), ('L', ((5, 9),))))), ('N', 68, 1.5, ('N', 102, 1.5, ('N', 77, 0.5, ('N', 16, 6.5, ('L', ((49, 2),)), ('N', 28, 1.0, ('L', ((59, 2),)), ('L', ((35, 1), (50, 1))))), ('L', ((2, 3),))), ('N', 83, 1.5, ('N', 40, 0.5, ('L', ((35, 1), (49, 2))), ('L', ((61, 3), (65, 1)))), ('L', ((65, 6),)))), ('N', 27, 0.5, ('L', ((11, 1), (59, 4))), ('L', ((62, 6),))))), ('N', 67, 1.5, ('N', 1, 7.5, ('N', 17, 10.5, ('L', ((3, 8),)), ('N', 42, 0.5, ('L', ((49, 1), (63, 1))), ('N', 73, 0.5, ('L', ((3, 2),)), ('L', ((32, 1), (63, 1)))))), ('N', 55, 1.5, ('N', 83, 1.5, ('N', 15, 8.5, ('L', ((22, 2), (49, 1))), ('L', ((22, 3),))), ('N', 37, 2.0, ('L', ((3, 2),)), ('L', ((4, 1), (22, 1))))), ('L', ((11, 3),)))), ('L', ((59, 2), (65, 1))))), ('N', 47, 0.5, ('N', 48, 0.5, ('N', 54, 0.5, ('N', 2, 0.5, ('N', 51, 0.5, ('N', 42, 0.5, ('N', 22, 0.5, ('N', 14, 1.0, ('L', ((17, 1), (65, 1))), ('L', ((13, 3),))), ('L', ((60, 2),))), ('N', 0, 9.5, ('L', ((17, 1), (19, 1))), ('L', ((19, 2),)))), ('N', 15, 3.5, ('L', ((8, 1), (12, 2))), ('L', ((15, 2),)))), ('N', 60, 1.5, ('N', 108, 0.5, ('N', 6, 1.5, ('N', 32, 0.5, ('N', 18, 5.5, ('N', 4, 0.5, ('L', ((7, 2),)), ('L', ((0, 5), (7, 1), (19, 1)))), ('N', 34, 0.5, ('L', ((7, 4),)), ('L', ((7, 7), (19, 1))))), ('N', 59, 0.5, ('N', 35, 0.5, ('L', ((7, 12),)), ('L', ((7, 2), (12, 1)))), ('L', ((7, 1), (12, 1))))), ('N', 79, 1.0, ('L', ((7, 1), (8, 2))), ('L', ((7, 1), (8, 1))))), ('L', ((65, 2),))), ('N', 27, 1.0, ('N', 0, 5.0, ('L', ((17, 2),)), ('L', ((8, 1), (12, 1), (65, 1)))), ('L', ((0, 2),))))), ('L', ((11, 3),))), ('N', 108, 0.5, ('N', 106, 0.5, ('N', 65, 0.5, ('N', 56, 0.5, ('N', 40, 0.5, ('N', 62, 1.5, ('N', 58, 1.5, ('N', 1, 1.5, ('L', ((60, 2),)), ('L', ((0, 2), (7, 3), (8, 5), (9, 1), (14, 6), (19, 2), (51, 1), (61, 2)))), ('L', ((11, 2), (12, 2), (18, 2)))), ('L', ((18, 4),))), ('N', 34, 0.5, ('N', 9, 0.5, ('N', 3, 0.5, ('L', ((5, 1), (15, 1), (51, 1))), ('L', ((6, 1), (7, 3)))), ('N', 2, 0.5, ('L', ((5, 4), (14, 1), (15, 2), (17, 1), (19, 1), (61, 1))), ('L', ((5, 13),)))), ('N', 75, 0.5, ('N', 32, 0.5, ('L', ((0, 3), (5, 3), (8, 1), (11, 1), (12, 4), (14, 1), (17, 1))), ('L', ((8, 7), (10, 2), (15, 2), (60, 2), (61, 1)))), ('N', 38, 0.5, ('L', ((61, 4),)), ('L', ((15, 3), (60, 1))))))), ('N', 17, 6.5, ('N', 3, 0.5, ('L', ((5, 1), (16, 1), (61, 1))), ('L', ((8, 1), (14, 1)))), ('N', 28, 1.5, ('N', 21, 0.5, ('N', 57, 0.5, ('L', ((13, 3),)), ('L', ((13, 1), (14, 4)))), ('L', ((13, 2),))), ('N', 13, 4.0, ('N', 24, 0.5, ('L', ((13, 5),)), ('L', ((13, 1), (32, 1)))), ('L', ((0, 1), (13, 1))))))), ('N', 58, 0.5, ('N', 9, 2.0, ('L', ((22, 7),)), ('L', ((5, 1), (11, 1)))), ('L', ((15, 2),)))), ('N', 75, 0.5, ('N', 61, 1.5, ('N', 36, 0.5, ('L', ((63, 16),)), ('N', 77, 1.5, ('L', ((63, 2),)), ('L', ((22, 1), (63, 2))))), ('N', 16, 5.0, ('N', 102, 1.5, ('L', ((63, 8),)), ('L', ((31, 1), (63, 2)))), ('N', 2, 0.5, ('L', ((51, 1), (63, 1))), ('L', ((5, 1), (8, 2)))))), ('N', 15, 7.5, ('L', ((31, 3),)), ('N', 39, 0.5, ('L', ((8, 1), (19, 1), (61, 1))), ('L', ((63, 3),)))))), ('N', 28, 0.5, ('L', ((64, 5),)), ('N', 12, 3.5, ('L', ((8, 1), (65, 1))), ('L', ((65, 4),)))))), ('N', 101, 1.5, ('N', 43, 0.5, ('L', ((4, 35),)), ('N', 18, 4.0, ('L', ((18, 2),)), ('L', ((4, 6),)))), ('L', ((64, 2),))))), ('N', 18, 4.5, ('N', 13, 3.5, ('N', 4, 0.5, ('N', 57, 0.5, ('N', 60, 0.5, ('L', ((7, 3),)), ('N', 24, 0.5, ('N', 35, 0.5, ('N', 38, 1.5, ('L', ((22, 2),)), ('L', ((17, 5),))), ('L', ((13, 3),))), ('L', ((21, 2),)))), ('N', 48, 0.5, ('L', ((19, 1), (60, 3))), ('N', 18, 2.5, ('L', ((5, 4),)), ('L', ((0, 1), (5, 2)))))), ('N', 15, 10.0, ('L', ((7, 2), (11, 1))), ('L', ((7, 3),)))), ('L', ((13, 4),))), ('N', 108, 0.5, ('N', 93, 0.5, ('N', 65, 0.5, ('N', 79, 0.5, ('N', 14, 1.5, ('N', 73, 1.0, ('L', ((21, 7),)), ('L', ((30, 2),))), ('L', ((21, 18),))), ('N', 3, 0.5, ('N', 14, 2.5, ('L', ((17, 1), (59, 1))), ('L', ((13, 1), (63, 2)))), ('N', 77, 0.5, ('L', ((21, 4),)), ('L', ((5, 1), (35, 2)))))), ('N', 32, 1.5, ('N', 78, 0.5, ('L', ((22, 4),)), ('L', ((21, 1), (22, 3)))), ('L', ((21, 2),)))), ('N', 1, 9.0, ('L', ((12, 2),)), ('L', ((51, 3),)))), ('L', ((65, 4),))))), ('N', 57, 1.5, ('N', 75, 0.5, ('N', 19, 3.5, ('N', 69, 1.5, ('N', 23, 0.5, ('N', 27, 0.5, ('L', ((4, 2), (17, 1))), ('L', ((8, 1), (63, 2)))), ('L', ((21, 3),))), ('N', 27, 0.5, ('L', ((41, 3),)), ('L', ((63, 3),)))), ('N', 56, 1.5, ('L', ((41, 17),)), ('N', 13, 4.5, ('L', ((41, 2),)), ('L', ((8, 3),))))), ('N', 41, 2.0, ('L', ((59, 2),)), ('N', 1, 1.5, ('L', ((21, 1), (65, 1))), ('L', ((32, 1), (61, 3)))))), ('N', 81, 1.0, ('N', 102, 0.5, ('N', 22, 1.5, ('N', 62, 0.5, ('N', 37, 2.5, ('L', ((11, 2),)), ('L', ((7, 1), (8, 2)))), ('L', ((21, 2),))), ('L', ((8, 3), (63, 1)))), ('L', ((60, 3),))), ('L', ((4, 7),))))), ('N', 48, 0.5, ('N', 0, 5.5, ('N', 92, 0.5, ('N', 14, 1.5, ('N', 54, 0.5, ('N', 63, 0.5, ('N', 8, 6.0, ('N', 56, 0.5, ('N', 65, 0.5, ('N', 39, 0.5, ('N', 13, 3.0, ('N', 13, 1.5, ('L', ((59, 2),)), ('L', ((2, 2),))), ('N', 83, 1.0, ('L', ((10, 3),)), ('N', 16, 5.0, ('L', ((35, 1), (65, 2))), ('L', ((9, 1), (17, 1), (21, 2), (35, 1)))))), ('N', 16, 5.5, ('L', ((10, 6),)), ('L', ((10, 2), (17, 1))))), ('N', 37, 0.5, ('L', ((22, 2),)), ('L', ((21, 1), (22, 4))))), ('N', 57, 0.5, ('N', 30, 0.5, ('N', 60, 0.5, ('N', 25, 1.0, ('N', 42, 0.5, ('L', ((13, 1), (21, 5))), ('L', ((1, 1), (2, 1), (21, 2)))), ('L', ((22, 2),))), ('L', ((13, 2),))), ('L', ((13, 4),))), ('L', ((14, 3),)))), ('N', 83, 0.5, ('N', 32, 0.5, ('L', ((17, 3),)), ('L', ((7, 2),))), ('L', ((41, 2),)))), ('L', ((20, 5),))), ('N', 0, 1.5, ('L', ((58, 3),)), ('N', 19, 5.5, ('L', ((22, 2),)), ('L', ((11, 3),))))), ('N', 54, 0.5, ('N', 105, 0.5, ('N', 108, 0.5, ('N', 81, 1.0, ('N', 41, 0.5, ('N', 22, 0.5, ('L', ((32, 4),)), ('N', 40, 1.5, ('N', 3, 0.5, ('L', ((4, 1), (17, 3), (35, 1), (63, 2))), ('L', ((43, 1), (63, 1)))), ('L', ((0, 2), (12, 1))))), ('N', 65, 0.5, ('N', 17, 10.5, ('N', 9, 0.5, ('N', 17, 7.0, ('L', ((8, 2),)), ('L', ((3, 3),))), ('N', 11, 8.0, ('L', ((7, 1), (31, 1))), ('L', ((10, 2), (35, 1), (59, 1))))), ('N', 13, 3.5, ('N', 102, 0.5, ('L', ((14, 4), (17, 1), (21, 2))), ('L', ((59, 2),))), ('N', 16, 4.5, ('L', ((12, 3), (18, 2))), ('L', ((18, 2),))))), ('L', ((22, 3),)))), ('L', ((4, 3),))), ('L', ((65, 10),))), ('L', ((62, 6),))), ('N', 106, 1.5, ('N', 32, 1.5, ('N', 17, 10.5, ('L', ((11, 1), (63, 1))), ('N', 70, 1.0, ('L', ((11, 5),)), ('L', ((4, 1), (11, 3))))), ('L', ((61, 1), (65, 3)))), ('L', ((62, 3),))))), ('N', 29, 0.5, ('N', 9, 0.5, ('L', ((49, 2), (50, 1), (63, 1))), ('L', ((49, 4),))), ('L', ((44, 1), (65, 2))))), ('N', 26, 0.5, ('N', 28, 2.5, ('N', 33, 0.5, ('N', 36, 1.5, ('N', 64, 0.5, ('N', 58, 0.5, ('N', 106, 0.5, ('N', 2, 0.5, ('N', 34, 0.5, ('L', ((10, 3), (61, 1))), ('N', 18, 2.5, ('L', ((35, 1), (65, 1))), ('L', ((8, 1), (12, 1))))), ('N', 38, 2.5, ('N', 43, 0.5, ('N', 17, 10.5, ('L', ((7, 8), (41, 1))), ('L', ((7, 1), (14, 2), (41, 1)))), ('L', ((0, 1), (7, 1)))), ('L', ((0, 3), (7, 1), (14, 1))))), ('N', 41, 1.5, ('L', ((63, 2),)), ('N', 51, 0.5, ('L', ((33, 2),)), ('L', ((8, 1), (63, 2)))))), ('N', 108, 0.5, ('N', 75, 1.0, ('N', 27, 0.5, ('N', 28, 1.5, ('L', ((15, 1), (17, 1))), ('L', ((12, 2),))), ('L', ((16, 3),))), ('N', 77, 0.5, ('L', ((60, 3),)), ('L', ((17, 1), (19, 2))))), ('L', ((65, 5),)))), ('N', 2, 0.5, ('L', ((22, 1), (31, 1))), ('N', 59, 0.5, ('L', ((21, 5),)), ('L', ((15, 2),))))), ('L', ((14, 5), (41, 1)))), ('N', 4, 0.5, ('N', 27, 2.5, ('L', ((13, 1), (17, 1), (60, 1))), ('L', ((39, 1), (61, 1)))), ('N', 1, 9.5, ('L', ((11, 6),)), ('L', ((7, 1), (11, 2)))))), ('N', 1, 6.5, ('N', 104, 1.0, ('N', 3, 0.5, ('N', 11, 3.5, ('L', ((7, 2), (8, 1))), ('L', ((19, 4),))), ('L', ((13, 2),))), ('L', ((50, 2),))), ('N', 18, 5.5, ('N', 30, 0.5, ('N', 64, 0.5, ('L', ((0, 1), (7, 2))), ('L', ((7, 2), (41, 1)))), ('L', ((7, 8),))), ('N', 106, 0.5, ('L', ((7, 4), (17, 1))), ('L', ((63, 2),)))))), ('N', 104, 0.5, ('L', ((4, 5),)), ('L', ((3, 2),))))), ('N', 26, 0.5, ('N', 94, 0.5, ('N', 106, 0.5, ('N', 64, 0.5, ('N', 51, 0.5, ('N', 108, 0.5, ('N', 54, 0.5, ('N', 0, 2.5, ('N', 32, 1.5, ('N', 22, 1.5, ('L', ((14, 2),)), ('L', ((10, 1), (14, 1), (18, 1)))), ('L', ((6, 2), (13, 4), (22, 3)))), ('N', 39, 0.5, ('N', 7, 6.5, ('N', 38, 2.5, ('N', 19, 5.5, ('L', ((5, 13),)), ('L', ((5, 7), (17, 1), (32, 1), (41, 1), (60, 1), (61, 1)))), ('L', ((5, 1), (9, 1), (13, 1)))), ('N', 98, 1.0, ('L', ((5, 1), (15, 1))), ('N', 15, 6.5, ('L', ((61, 3),)), ('L', ((13, 1), (19, 1)))))), ('N', 77, 1.0, ('N', 9, 1.5, ('N', 5, 2.5, ('L', ((5, 2), (59, 1))), ('L', ((12, 2), (13, 1), (15, 1)))), ('N', 3, 0.5, ('L', ((19, 1), (41, 1), (60, 1))), ('L', ((7, 4), (14, 1), (61, 1))))), ('L', ((15, 1), (60, 2)))))), ('N', 27, 1.5, ('N', 1, 5.5, ('L', ((11, 1), (12, 2))), ('N', 83, 1.5, ('N', 25, 0.5, ('L', ((11, 6),)), ('N', 74, 0.5, ('L', ((11, 3),)), ('L', ((41, 2),)))), ('L', ((41, 2),)))), ('L', ((5, 3),)))), ('L', ((65, 6),))), ('N', 60, 1.5, ('N', 35, 0.5, ('N', 18, 4.5, ('N', 27, 2.5, ('L', ((8, 7),)), ('L', ((19, 2),))), ('N', 108, 1.0, ('N', 41, 1.5, ('N', 11, 7.5, ('N', 15, 6.5, ('L', ((7, 2),)), ('L', ((8, 1), (11, 1), (12, 2), (14, 1), (17, 1), (18, 1), (41, 1)))), ('L', ((5, 4),))), ('L', ((8, 2),))), ('L', ((65, 2),)))), ('N', 36, 0.5, ('N', 83, 1.5, ('N', 10, 0.5, ('N', 42, 0.5, ('L', ((13, 2),)), ('L', ((7, 2),))), ('L', ((13, 3), (41, 1)))), ('L', ((8, 1), (65, 1)))), ('N', 34, 1.5, ('L', ((14, 3),)), ('N', 75, 1.5, ('N', 67, 0.5, ('L', ((13, 1), (16, 2))), ('L', ((61, 2),))), ('L', ((32, 2),)))))), ('N', 54, 0.5, ('N', 1, 4.0, ('L', ((15, 2), (65, 1))), ('L', ((15, 5),))), ('L', ((8, 2), (15, 1)))))), ('N', 29, 0.5, ('N', 28, 2.5, ('N', 33, 0.5, ('N', 58, 1.5, ('N', 42, 1.5, ('L', ((21, 15),)), ('L', ((13, 1), (21, 2)))), ('L', ((5, 1), (61, 1)))), ('N', 12, 8.0, ('N', 36, 1.0, ('L', ((11, 2),)), ('L', ((11, 4), (22, 1)))), ('N', 51, 0.5, ('L', ((12, 1), (21, 1))), ('L', ((21, 5),))))), ('L', ((5, 5),))), ('N', 5, 3.5, ('L', ((5, 2),)), ('L', ((65, 3),))))), ('N', 15, 14.5, ('N', 108, 0.5, ('N', 40, 0.5, ('N', 7, 6.5, ('N', 23, 0.5, ('N', 7, 4.5, ('N', 13, 4.5, ('N', 34, 0.5, ('N', 25, 0.5, ('L', ((41, 1), (63, 4))), ('L', ((60, 1), (63, 1)))), ('L', ((8, 1), (22, 1), (41, 1)))), ('L', ((63, 3),))), ('L', ((63, 6),))), ('L', ((21, 2),))), ('N', 9, 1.5, ('L', ((19, 3),)), ('L', ((19, 1), (63, 1))))), ('N', 60, 1.5, ('L', ((63, 23),)), ('N', 37, 0.5, ('L', ((63, 6),)), ('L', ((41, 1), (63, 2)))))), ('N', 83, 0.5, ('L', ((8, 3),)), ('L', ((13, 2),)))), ('N', 62, 1.5, ('N', 50, 0.5, ('L', ((5, 3),)), ('N', 1, 1.5, ('N', 6, 1.5, ('L', ((60, 3),)), ('L', ((8, 2),))), ('N', 30, 1.0, ('N', 16, 5.5, ('L', ((8, 2),)), ('L', ((13, 1), (63, 1)))), ('L', ((8, 3),))))), ('N', 64, 0.5, ('N', 17, 5.0, ('N', 102, 0.5, ('N', 85, 0.5, ('L', ((5, 1), (8, 1), (65, 1))), ('L', ((19, 2), (32, 1)))), ('L', ((61, 3),))), ('L', ((63, 2),))), ('L', ((21, 2),)))))), ('N', 24, 1.5, ('L', ((51, 9),)), ('L', ((50, 1), (51, 2))))), ('N', 101, 0.5, ('N', 56, 1.5, ('N', 39, 0.5, ('L', ((4, 37),)), ('N', 42, 1.0, ('L', ((18, 2),)), ('L', ((4, 2),)))), ('L', ((4, 1), (41, 3)))), ('L', ((17, 1), (63, 2)))))), ('N', 47, 0.5, ('N', 64, 0.5, ('N', 5, 4.5, ('N', 29, 0.5, ('N', 56, 0.5, ('N', 106, 0.5, ('N', 54, 0.5, ('N', 4, 0.5, ('N', 32, 0.5, ('N', 34, 0.5, ('N', 60, 0.5, ('N', 15, 6.5, ('L', ((14, 2), (18, 1))), ('L', ((14, 4), (22, 1)))), ('L', ((14, 1), (17, 1)))), ('N', 15, 3.5, ('L', ((10, 1), (18, 4))), ('N', 65, 0.5, ('N', 30, 0.5, ('L', ((2, 1), (3, 1), (10, 1), (12, 2), (20, 2))), ('L', ((3, 1), (29, 3), (32, 1)))), ('N', 60, 0.5, ('L', ((22, 3),)), ('L', ((5, 1), (22, 1))))))), ('N', 92, 0.5, ('N', 83, 0.5, ('N', 55, 1.5, ('L', ((59, 4),)), ('L', ((17, 1), (59, 4)))), ('N', 41, 0.5, ('N', 77, 0.5, ('L', ((35, 4),)), ('L', ((5, 1), (17, 1), (35, 1)))), ('N', 68, 1.0, ('L', ((3, 4), (17, 1), (59, 1))), ('L', ((12, 1), (62, 1)))))), ('L', ((49, 3),)))), ('L', ((10, 6),))), ('N', 13, 3.5, ('L', ((11, 5),)), ('L', ((11, 1), (61, 1))))), ('N', 0, 6.5, ('N', 26, 0.5, ('N', 40, 0.5, ('N', 61, 1.0, ('L', ((63, 2),)), ('L', ((62, 2),))), ('L', ((62, 8),))), ('L', ((63, 3),))), ('N', 16, 3.5, ('L', ((5, 1), (32, 1))), ('L', ((5, 2), (39, 2)))))), ('N', 11, 7.5, ('N', 1, 5.0, ('N', 72, 0.5, ('L', ((13, 6),)), ('L', ((11, 1), (29, 1)))), ('N', 16, 4.0, ('L', ((14, 1), (18, 1))), ('L', ((0, 1), (13, 2))))), ('L', ((3, 1), (22, 1))))), ('N', 14, 1.5, ('N', 35, 0.5, ('N', 6, 0.5, ('N', 12, 4.5, ('L', ((10, 4),)), ('L', ((10, 1), (65, 1)))), ('N', 15, 8.0, ('L', ((6, 4),)), ('L', ((9, 2), (65, 1))))), ('L', ((1, 2), (2, 3), (13, 5), (14, 4), (20, 3), (22, 2), (46, 3)))), ('N', 30, 2.5, ('L', ((65, 16),)), ('L', ((35, 1), (65, 1)))))), ('N', 108, 0.5, ('N', 48, 0.5, ('N', 11, 8.5, ('N', 106, 0.5, ('N', 6, 1.5, ('N', 73, 1.5, ('N', 59, 0.5, ('N', 37, 0.5, ('N', 15, 5.0, ('N', 11, 6.0, ('L', ((0, 1), (12, 1))), ('L', ((13, 2),))), ('N', 7, 0.5, ('L', ((7, 2), (17, 1))), ('L', ((7, 4),)))), ('N', 14, 1.5, ('N', 67, 0.5, ('L', ((41, 6),)), ('L', ((59, 2),))), ('N', 43, 0.5, ('L', ((7, 2), (14, 2), (19, 2))), ('L', ((17, 2),))))), ('L', ((11, 1), (16, 3)))), ('L', ((17, 4),))), ('N', 16, 5.5, ('N', 3, 0.5, ('L', ((8, 2), (13, 1))), ('L', ((8, 2),))), ('N', 16, 7.5, ('L', ((11, 2),)), ('L', ((14, 2),))))), ('N', 62, 0.5, ('L', ((63, 3),)), ('L', ((19, 1), (63, 1))))), ('N', 41, 2.5, ('N', 40, 1.5, ('N', 22, 1.5, ('L', ((7, 9),)), ('N', 17, 6.5, ('L', ((16, 1), (63, 1))), ('L', ((7, 2),)))), ('N', 73, 1.0, ('N', 83, 1.5, ('L', ((7, 3),)), ('N', 27, 0.5, ('L', ((12, 2),)), ('N', 1, 24.0, ('L', ((0, 1), (12, 1))), ('L', ((7, 2),))))), ('L', ((50, 1), (61, 1))))), ('L', ((8, 2), (11, 1))))), ('N', 84, 0.5, ('N', 98, 0.5, ('N', 6, 1.5, ('N', 36, 0.5, ('N', 106, 0.5, ('N', 28, 2.5, ('N', 17, 7.5, ('L', ((5, 15),)), ('N', 0, 8.5, ('L', ((5, 5), (10, 2), (11, 2), (13, 2), (17, 1), (32, 1))), ('L', ((7, 1), (15, 2), (60, 2))))), ('N', 38, 0.5, ('L', ((18, 2),)), ('N', 7, 3.0, ('L', ((5, 1), (7, 1), (32, 1))), ('L', ((13, 1), (19, 2)))))), ('N', 17, 5.0, ('N', 14, 3.0, ('L', ((5, 3),)), ('L', ((19, 2), (51, 1)))), ('N', 8, 7.5, ('N', 30, 0.5, ('L', ((63, 2),)), ('L', ((31, 3),))), ('L', ((63, 5),))))), ('N', 43, 0.5, ('N', 9, 2.5, ('N', 58, 0.5, ('L', ((11, 1), (14, 1))), ('L', ((14, 2),))), ('N', 15, 13.5, ('L', ((5, 5),)), ('L', ((5, 1), (60, 1))))), ('N', 40, 1.0, ('L', ((0, 2),)), ('L', ((5, 8),))))), ('N', 85, 1.5, ('N', 57, 0.5, ('N', 41, 1.5, ('N', 10, 1.0, ('N', 3, 0.5, ('L', ((17, 2),)), ('L', ((0, 2), (5, 2), (7, 1), (8, 1), (11, 2), (22, 1), (51, 1)))), ('N', 30, 1.0, ('L', ((8, 5),)), ('L', ((8, 1), (18, 1))))), ('N', 55, 0.5, ('L', ((63, 4),)), ('L', ((22, 1), (63, 1))))), ('N', 1, 11.0, ('N', 10, 2.5, ('N', 58, 0.5, ('L', ((8, 4), (63, 1))), ('L', ((15, 3),))), ('L', ((14, 2), (16, 1)))), ('L', ((14, 6),)))), ('N', 34, 2.5, ('N', 16, 5.5, ('L', ((63, 2),)), ('L', ((11, 1), (22, 1), (63, 2)))), ('N', 39, 0.5, ('N', 75, 1.0, ('L', ((13, 5),)), ('L', ((32, 2),))), ('L', ((5, 3),)))))), ('N', 18, 2.5, ('N', 0, 14.0, ('L', ((8, 2), (15, 1))), ('N', 106, 1.0, ('L', ((8, 2),)), ('L', ((8, 3), (60, 1))))), ('N', 27, 0.5, ('N', 24, 1.5, ('N', 63, 0.5, ('N', 34, 0.5, ('N', 24, 0.5, ('L', ((61, 2),)), ('L', ((13, 1), (61, 1)))), ('N', 33, 0.5, ('L', ((60, 7), (61, 1))), ('L', ((61, 2),)))), ('L', ((12, 2),))), ('L', ((51, 3),))), ('N', 3, 0.5, ('N', 65, 0.5, ('N', 106, 0.5, ('L', ((5, 1), (17, 1))), ('L', ((63, 8),))), ('L', ((31, 1), (63, 1)))), ('N', 22, 1.5, ('L', ((60, 3),)), ('L', ((60, 2), (61, 1)))))))), ('N', 42, 1.5, ('N', 0, 10.5, ('L', ((41, 9),)), ('L', ((17, 1), (41, 1)))), ('N', 0, 8.5, ('L', ((41, 3),)), ('N', 8, 2.5, ('L', ((19, 3),)), ('N', 69, 1.0, ('N', 11, 3.5, ('L', ((63, 2),)), ('N', 1, 8.0, ('N', 61, 1.0, ('L', ((63, 3),)), ('L', ((8, 1), (15, 1)))), ('L', ((8, 1), (11, 1))))), ('L', ((61, 2),)))))))), ('N', 1, 2.5, ('L', ((8, 2),)), ('L', ((65, 13),))))), ('N', 54, 0.5, ('N', 79, 0.5, ('N', 12, 11.5, ('N', 15, 9.5, ('N', 13, 0.5, ('L', ((21, 2), (22, 1))), ('N', 73, 0.5, ('L', ((21, 20),)), ('L', ((21, 1), (30, 1))))), ('N', 0, 2.0, ('L', ((22, 2),)), ('L', ((21, 5),)))), ('L', ((7, 1), (17, 1)))), ('N', 61, 0.5, ('N', 17, 8.0, ('L', ((21, 5),)), ('N', 13, 3.5, ('L', ((22, 3),)), ('N', 73, 1.0, ('N', 36, 0.5, ('L', ((17, 3), (21, 1))), ('L', ((5, 1), (35, 1)))), ('L', ((59, 2),))))), ('N', 98, 0.5, ('N', 36, 0.5, ('L', ((13, 2), (15, 1))), ('L', ((19, 4),))), ('N', 38, 1.5, ('L', ((21, 1), (22, 1))), ('L', ((13, 1), (61, 2))))))), ('N', 36, 1.5, ('N', 28, 1.5, ('N', 3, 0.5, ('N', 7, 3.0, ('L', ((13, 2), (17, 2))), ('L', ((19, 6),))), ('N', 36, 0.5, ('N', 74, 1.0, ('L', ((65, 2),)), ('L', ((12, 2),))), ('L', ((60, 2),)))), ('N', 1, 6.5, ('N', 37, 1.5, ('N', 11, 2.0, ('L', ((8, 3),)), ('N', 17, 8.5, ('N', 1, 3.5, ('L', ((0, 1), (61, 1))), ('N', 19, 5.0, ('L', ((5, 2),)), ('L', ((5, 1), (65, 1))))), ('L', ((13, 1), (21, 1), (63, 1))))), ('L', ((21, 2),))), ('N', 65, 0.5, ('N', 11, 6.5, ('L', ((11, 5),)), ('N', 85, 1.0, ('L', ((5, 1), (7, 1))), ('L', ((51, 2),)))), ('N', 37, 0.5, ('L', ((7, 2),)), ('L', ((41, 2),)))))), ('N', 58, 0.5, ('L', ((58, 2),)), ('L', ((21, 7),)))))), ('N', 14, 1.5, ('N', 8, 4.0, ('N', 47, 1.5, ('L', ((4, 1), (63, 1))), ('L', ((17, 2), (64, 1)))), ('N', 37, 0.5, ('L', ((4, 4),)), ('L', ((41, 2),)))), ('N', 5, 4.5, ('N', 15, 4.5, ('L', ((14, 1), (49, 1))), ('N', 2, 0.5, ('L', ((4, 5),)), ('L', ((4, 1), (65, 1))))), ('N', 59, 0.5, ('L', ((4, 28),)), ('N', 51, 0.5, ('N', 12, 10.5, ('L', ((4, 1), (18, 1))), ('L', ((4, 2),))), ('L', ((4, 5),))))))), ('N', 71, 0.5, ('N', 81, 0.5, ('N', 106, 0.5, ('N', 104, 0.5, ('N', 5, 4.5, ('N', 23, 0.5, ('N', 5, 3.5, ('N', 28, 0.5, ('N', 63, 0.5, ('N', 36, 0.5, ('N', 45, 0.5, ('N', 17, 13.5, ('N', 37, 1.5, ('L', ((10, 12), (17, 1), (49, 1))), ('L', ((13, 2), (22, 1), (65, 3)))), ('N', 6, 0.5, ('L', ((1, 2), (10, 2), (12, 1), (13, 5), (17, 2), (18, 1), (22, 2), (46, 2), (49, 1))), ('L', ((12, 4),)))), ('L', ((2, 3),))), ('N', 102, 0.5, ('N', 35, 1.5, ('N', 98, 0.5, ('L', ((9, 1), (11, 1), (14, 8))), ('L', ((2, 1), (11, 1)))), ('N', 30, 0.5, ('L', ((13, 2),)), ('L', ((11, 1), (29, 2))))), ('L', ((59, 3), (65, 1))))), ('N', 6, 0.5, ('N', 32, 1.5, ('L', ((20, 4),)), ('L', ((65, 2),))), ('L', ((6, 1), (13, 2), (22, 1))))), ('N', 61, 0.5, ('N', 14, 4.5, ('N', 83, 0.5, ('N', 48, 0.5, ('L', ((4, 1), (65, 1))), ('L', ((5, 2),))), ('L', ((5, 5),))), ('N', 37, 1.5, ('L', ((10, 2),)), ('L', ((35, 2),)))), ('L', ((11, 2),)))), ('N', 69, 1.0, ('N', 41, 1.5, ('N', 2, 0.5, ('L', ((3, 1), (18, 1))), ('L', ((3, 9),))), ('L', ((14, 1), (22, 1), (49, 1)))), ('N', 61, 0.5, ('L', ((65, 3),)), ('L', ((17, 3),))))), ('N', 15, 6.5, ('L', ((21, 13),)), ('N', 40, 0.5, ('N', 25, 0.5, ('N', 79, 0.5, ('N', 1, 9.0, ('L', ((11, 1), (30, 1))), ('L', ((11, 1), (13, 1)))), ('L', ((59, 2),))), ('N', 73, 0.5, ('L', ((21, 1), (22, 1))), ('N', 0, 1.5, ('L', ((22, 2),)), ('L', ((21, 1), (22, 1)))))), ('N', 48, 0.5, ('N', 89, 0.5, ('L', ((21, 5),)), ('L', ((21, 1), (44, 2)))), ('L', ((5, 2),)))))), ('N', 48, 0.5, ('N', 108, 0.5, ('N', 2, 0.5, ('N', 8, 5.5, ('N', 9, 2.0, ('L', ((4, 4), (8, 1))), ('N', 36, 0.5, ('L', ((15, 3),)), ('L', ((19, 2),)))), ('N', 24, 0.5, ('N', 35, 0.5, ('N', 32, 0.5, ('N', 10, 4.0, ('L', ((7, 3), (17, 2))), ('L', ((17, 1), (31, 1)))), ('L', ((60, 2),))), ('L', ((13, 3),))), ('L', ((17, 6),)))), ('N', 55, 1.5, ('N', 10, 4.5, ('N', 9, 0.5, ('N', 64, 0.5, ('N', 3, 0.5, ('L', ((41, 2),)), ('L', ((4, 1), (7, 3), (11, 1)))), ('L', ((21, 3),))), ('N', 9, 1.5, ('N', 17, 4.5, ('L', ((11, 2),)), ('L', ((7, 3),))), ('N', 77, 1.5, ('L', ((0, 1), (7, 21), (14, 1), (17, 1), (41, 2))), ('L', ((7, 1), (19, 2)))))), ('N', 0, 8.0, ('L', ((0, 3), (7, 1))), ('N', 83, 0.5, ('N', 59, 0.5, ('L', ((7, 3), (11, 1))), ('L', ((0, 1), (11, 1), (16, 1)))), ('L', ((8, 2),))))), ('N', 6, 1.5, ('N', 0, 6.5, ('N', 33, 0.5, ('L', ((12, 2),)), ('L', ((12, 2), (41, 1)))), ('L', ((7, 1), (14, 1), (41, 2)))), ('L', ((8, 1), (15, 2), (21, 1)))))), ('L', ((65, 3),))), ('N', 79, 0.5, ('N', 23, 0.5, ('N', 33, 0.5, ('N', 8, 6.5, ('N', 0, 12.0, ('N', 47, 0.5, ('N', 41, 0.5, ('L', ((13, 2),)), ('L', ((5, 3), (19, 3)))), ('N', 2, 0.5, ('L', ((4, 2),)), ('L', ((4, 1), (18, 2))))), ('L', ((5, 3),))), ('N', 58, 0.5, ('N', 61, 1.5, ('N', 15, 8.5, ('L', ((4, 1), (5, 1), (7, 5), (14, 2), (32, 4), (51, 1), (60, 3), (65, 5))), ('L', ((5, 3), (8, 5), (12, 4), (14, 4), (22, 3)))), ('L', ((16, 2),))), ('N', 26, 0.5, ('L', ((15, 6),)), ('L', ((4, 2),))))), ('N', 100, 1.0, ('N', 7, 4.5, ('N', 1, 7.5, ('L', ((65, 2),)), ('N', 30, 0.5, ('L', ((11, 7),)), ('L', ((11, 3), (14, 1), (22, 1))))), ('N', 55, 0.5, ('L', ((5, 2),)), ('L', ((12, 1), (13, 1))))), ('L', ((4, 2),)))), ('N', 102, 1.5, ('N', 27, 0.5, ('N', 11, 1.5, ('L', ((5, 2),)), ('L', ((5, 1), (12, 1), (65, 1)))), ('N', 41, 1.5, ('N', 6, 1.5, ('L', ((5, 1), (7, 1))), ('L', ((21, 4),))), ('L', ((21, 11),)))), ('L', ((12, 2),)))), ('N', 35, 0.5, ('N', 84, 0.5, ('N', 12, 5.0, ('N', 11, 3.5, ('L', ((8, 3),)), ('N', 77, 0.5, ('L', ((8, 2), (15, 1))), ('L', ((10, 3),)))), ('N', 0, 5.5, ('L', ((5, 6),)), ('N', 64, 0.5, ('N', 26, 0.5, ('L', ((5, 2), (8, 2), (17, 2), (18, 1))), ('L', ((4, 2),))), ('L', ((19, 2), (21, 1)))))), ('N', 18, 4.0, ('L', ((8, 2), (17, 1))), ('L', ((41, 5),)))), ('N', 103, 0.5, ('N', 50, 0.5, ('L', ((5, 2),)), ('N', 10, 0.5, ('N', 57, 0.5, ('L', ((13, 2),)), ('L', ((14, 2),))), ('L', ((13, 6),)))), ('L', ((60, 1), (65, 2)))))))), ('N', 8, 6.5, ('N', 4, 0.5, ('N', 12, 10.5, ('N', 58, 1.5, ('N', 8, 1.0, ('L', ((19, 3),)), ('N', 98, 0.5, ('L', ((0, 1), (19, 1), (61, 4))), ('L', ((61, 10),)))), ('N', 1, 1.5, ('L', ((5, 2),)), ('N', 98, 0.5, ('L', ((35, 1), (59, 2))), ('N', 1, 5.0, ('L', ((13, 2),)), ('L', ((61, 2),)))))), ('N', 15, 13.5, ('N', 55, 0.5, ('N', 26, 0.5, ('L', ((62, 2),)), ('L', ((3, 2), (59, 1)))), ('L', ((12, 2), (65, 1)))), ('L', ((11, 2),)))), ('L', ((7, 4),))), ('N', 64, 0.5, ('N', 94, 0.5, ('N', 0, 11.5, ('N', 11, 8.0, ('L', ((60, 5),)), ('N', 73, 1.5, ('L', ((60, 5),)), ('N', 34, 0.5, ('L', ((19, 2), (61, 1))), ('L', ((61, 2),))))), ('N', 102, 0.5, ('N', 16, 6.5, ('L', ((8, 1), (15, 2))), ('L', ((8, 2),))), ('L', ((61, 2),)))), ('L', ((50, 2), (51, 1)))), ('N', 15, 12.5, ('L', ((21, 2),)), ('L', ((21, 1), (22, 1), (51, 1))))))), ('N', 35, 1.5, ('N', 100, 0.5, ('N', 105, 0.5, ('N', 17, 0.5, ('L', ((8, 2),)), ('N', 16, 2.0, ('N', 67, 0.5, ('L', ((8, 3),)), ('L', ((31, 2), (41, 1)))), ('N', 32, 2.5, ('N', 30, 2.5, ('N', 32, 0.5, ('N', 108, 1.5, ('N', 14, 1.5, ('L', ((15, 1), (63, 2))), ('L', ((19, 1), (22, 1), (63, 41)))), ('L', ((65, 2),))), ('N', 60, 0.5, ('L', ((60, 3),)), ('N', 17, 4.0, ('L', ((13, 2), (63, 1))), ('L', ((31, 1), (63, 10)))))), ('N', 62, 0.5, ('N', 8, 7.0, ('L', ((22, 1), (63, 1))), ('L', ((41, 1), (63, 1)))), ('L', ((19, 2),)))), ('N', 13, 4.5, ('L', ((41, 2), (63, 1))), ('L', ((5, 2), (33, 1), (63, 1))))))), ('N', 16, 4.5, ('L', ((62, 1), (63, 1))), ('L', ((62, 7),)))), ('L', ((4, 4),))), ('N', 73, 1.0, ('N', 85, 0.5, ('N', 77, 0.5, ('N', 42, 1.5, ('L', ((8, 2), (60, 1))), ('L', ((5, 2),))), ('L', ((8, 4),))), ('L', ((32, 1), (41, 1)))), ('L', ((21, 4),))))), ('N', 25, 0.5, ('N', 102, 1.5, ('L', ((4, 17),)), ('L', ((41, 4),))), ('L', ((22, 3),)))), ('L', ((4, 15),))), ('N', 47, 0.5, ('N', 106, 0.5, ('N', 62, 0.5, ('N', 29, 0.5, ('N', 84, 0.5, ('N', 55, 1.5, ('N', 104, 0.5, ('N', 4, 0.5, ('N', 64, 0.5, ('N', 36, 0.5, ('N', 50, 0.5, ('N', 41, 0.5, ('N', 27, 0.5, ('L', ((2, 2), (3, 1), (5, 1), (11, 1), (17, 1), (35, 1), (43, 1), (49, 2))), ('L', ((10, 7),))), ('N', 30, 1.0, ('L', ((5, 1), (12, 3), (18, 4), (49, 1))), ('L', ((10, 1), (11, 1))))), ('N', 10, 6.5, ('N', 8, 2.0, ('L', ((13, 1), (15, 2))), ('L', ((5, 15), (7, 3), (8, 1), (10, 1), (11, 2), (12, 1), (13, 1), (15, 1), (32, 1), (51, 1), (60, 1)))), ('N', 14, 6.0, ('L', ((13, 2),)), ('L', ((5, 1), (12, 2)))))), ('N', 2, 0.5, ('N', 13, 2.5, ('N', 32, 1.5, ('L', ((11, 1), (59, 3))), ('L', ((11, 3),))), ('N', 75, 0.5, ('L', ((14, 3), (22, 1), (49, 2), (60, 1))), ('L', ((3, 2), (5, 2))))), ('N', 20, 0.5, ('N', 12, 8.5, ('L', ((13, 1), (14, 3))), ('L', ((5, 2), (14, 2)))), ('L', ((14, 5),))))), ('N', 12, 11.5, ('N', 78, 0.5, ('N', 41, 0.5, ('N', 54, 0.5, ('L', ((21, 8), (22, 1))), ('L', ((5, 4), (58, 1)))), ('N', 8, 7.5, ('L', ((11, 1), (21, 2))), ('L', ((21, 9),)))), ('L', ((17, 1), (21, 1), (22, 2)))), ('L', ((7, 3), (17, 1))))), ('N', 2, 0.5, ('N', 0, 10.5, ('L', ((13, 5),)), ('N', 6, 0.5, ('L', ((10, 5),)), ('N', 40, 0.5, ('N', 38, 1.5, ('L', ((12, 2),)), ('L', ((15, 2),))), ('L', ((8, 3), (17, 1)))))), ('N', 9, 2.5, ('N', 16, 4.5, ('N', 18, 5.5, ('L', ((7, 3),)), ('L', ((7, 1), (17, 2)))), ('N', 36, 0.5, ('N', 33, 0.5, ('L', ((0, 4), (7, 6), (10, 1), (16, 1), (17, 1))), ('L', ((11, 3),))), ('N', 15, 5.5, ('L', ((14, 2),)), ('L', ((0, 2), (8, 1), (11, 1), (14, 2)))))), ('N', 42, 1.5, ('L', ((7, 14),)), ('L', ((7, 2), (17, 1))))))), ('N', 75, 0.5, ('L', ((61, 6),)), ('N', 56, 0.5, ('N', 65, 0.5, ('N', 60, 0.5, ('N', 30, 3.5, ('N', 43, 0.5, ('L', ((60, 4),)), ('L', ((50, 1), (60, 1), (61, 1)))), ('L', ((61, 2),))), ('N', 14, 4.5, ('N', 57, 0.5, ('L', ((51, 1), (61, 1))), ('L', ((0, 2), (61, 3)))), ('L', ((3, 1), (15, 1), (62, 1))))), ('L', ((35, 2),))), ('N', 19, 5.5, ('L', ((5, 2),)), ('L', ((13, 2),)))))), ('N', 8, 2.5, ('N', 1, 4.5, ('N', 13, 1.5, ('L', ((22, 3),)), ('N', 104, 1.0, ('N', 17, 14.5, ('L', ((13, 1), (62, 1))), ('L', ((10, 1), (12, 1)))), ('L', ((35, 1), (59, 2))))), ('L', ((17, 2),))), ('N', 33, 0.5, ('N', 9, 0.5, ('N', 18, 5.5, ('L', ((8, 3),)), ('L', ((3, 1), (12, 1), (22, 1)))), ('N', 40, 1.5, ('N', 11, 7.5, ('L', ((7, 1), (14, 1))), ('N', 18, 5.5, ('L', ((12, 1), (32, 1))), ('L', ((12, 2),)))), ('L', ((12, 6),)))), ('N', 64, 0.5, ('L', ((11, 11),)), ('L', ((12, 2), (21, 1), (51, 2))))))), ('N', 103, 0.5, ('N', 18, 3.5, ('N', 48, 0.5, ('L', ((41, 2),)), ('L', ((8, 3),))), ('L', ((41, 10),))), ('L', ((59, 2),)))), ('N', 0, 2.5, ('N', 56, 0.5, ('N', 3, 0.5, ('L', ((10, 5),)), ('N', 13, 3.0, ('L', ((10, 2),)), ('N', 52, 0.5, ('L', ((6, 1), (44, 1))), ('L', ((9, 1), (21, 3)))))), ('N', 64, 0.5, ('N', 44, 0.5, ('N', 13, 3.5, ('N', 24, 0.5, ('L', ((13, 4),)), ('N', 15, 7.0, ('L', ((2, 1), (14, 1), (20, 1))), ('L', ((20, 4), (22, 1))))), ('L', ((13, 10),))), ('L', ((1, 2),))), ('N', 25, 0.5, ('N', 38, 1.0, ('L', ((21, 1), (30, 1))), ('L', ((21, 2),))), ('N', 23, 1.5, ('L', ((21, 1), (22, 1))), ('L', ((22, 2),)))))), ('N', 0, 7.5, ('N', 29, 1.5, ('N', 16, 2.5, ('L', ((64, 2),)), ('L', ((65, 22),))), ('L', ((18, 1), (21, 1)))), ('N', 1, 6.5, ('N', 61, 0.5, ('L', ((65, 3),)), ('L', ((12, 3), (15, 1)))), ('N', 48, 0.5, ('N', 3, 0.5, ('L', ((13, 2), (17, 1))), ('L', ((7, 4),))), ('N', 15, 6.5, ('L', ((8, 2),)), ('N', 15, 7.5, ('L', ((14, 2), (21, 1))), ('L', ((5, 1), (11, 1)))))))))), ('N', 77, 0.5, ('N', 9, 1.5, ('N', 0, 14.0, ('N', 35, 0.5, ('L', ((15, 2), (60, 1))), ('L', ((13, 2),))), ('L', ((8, 2),))), ('N', 12, 5.5, ('L', ((17, 2),)), ('N', 12, 9.5, ('N', 41, 1.5, ('N', 56, 0.5, ('L', ((21, 2),)), ('N', 1, 2.5, ('L', ((5, 4),)), ('L', ((19, 2),)))), ('L', ((19, 5),))), ('N', 38, 2.5, ('N', 30, 0.5, ('N', 60, 0.5, ('L', ((18, 1), (19, 2), (41, 1))), ('L', ((19, 2),))), ('L', ((19, 8),))), ('L', ((19, 1), (61, 1))))))), ('N', 4, 0.5, ('N', 35, 0.5, ('N', 62, 1.5, ('N', 24, 0.5, ('L', ((5, 4),)), ('L', ((5, 1), (65, 1)))), ('L', ((15, 1), (17, 1), (60, 1)))), ('N', 96, 0.5, ('N', 9, 1.5, ('L', ((16, 3),)), ('L', ((13, 2),))), ('L', ((61, 3),)))), ('N', 84, 0.5, ('L', ((19, 3),)), ('L', ((41, 5),)))))), ('N', 14, 1.5, ('N', 6, 0.5, ('L', ((5, 5),)), ('N', 24, 1.5, ('N', 56, 0.5, ('N', 2, 0.5, ('N', 38, 1.5, ('L', ((60, 1), (63, 1))), ('L', ((15, 3),))), ('L', ((21, 2),))), ('N', 8, 5.0, ('L', ((19, 2), (41, 2))), ('N', 36, 0.5, ('L', ((8, 2), (61, 1))), ('N', 17, 3.5, ('L', ((8, 1), (60, 1))), ('L', ((7, 1), (19, 1))))))), ('L', ((63, 4),)))), ('N', 5, 3.5, ('N', 38, 1.5, ('N', 20, 0.5, ('L', ((62, 3),)), ('L', ((32, 1), (62, 1), (64, 1)))), ('L', ((63, 2), (65, 1)))), ('N', 64, 0.5, ('N', 56, 0.5, ('N', 58, 1.5, ('N', 16, 2.0, ('L', ((8, 2),)), ('N', 84, 1.0, ('N', 8, 6.0, ('L', ((63, 19),)), ('N', 98, 0.5, ('N', 79, 1.0, ('L', ((63, 16),)), ('N', 1, 9.0, ('L', ((22, 1), (63, 1))), ('L', ((63, 3),)))), ('L', ((31, 1), (60, 1), (63, 2))))), ('L', ((60, 1), (63, 2))))), ('L', ((19, 2), (63, 1)))), ('N', 48, 0.5, ('L', ((3, 2), (22, 1))), ('L', ((41, 2), (63, 2))))), ('N', 17, 7.5, ('L', ((13, 1), (63, 3))), ('N', 16, 3.0, ('L', ((8, 2),)), ('L', ((13, 2), (21, 1))))))))), ('N', 80, 1.0, ('N', 26, 1.5, ('N', 11, 9.5, ('N', 64, 0.5, ('L', ((4, 50),)), ('L', ((4, 1), (21, 1)))), ('N', 39, 0.5, ('L', ((4, 15),)), ('L', ((4, 1), (18, 3))))), ('N', 16, 5.5, ('L', ((14, 2), (18, 3), (21, 1), (22, 1), (65, 1))), ('N', 5, 3.5, ('L', ((17, 1), (64, 1))), ('L', ((4, 3),))))), ('L', ((22, 2),)))), ('N', 71, 0.5, ('N', 84, 0.5, ('N', 5, 4.5, ('N', 106, 0.5, ('N', 54, 0.5, ('N', 64, 0.5, ('N', 37, 1.5, ('N', 57, 0.5, ('N', 65, 0.5, ('N', 27, 0.5, ('N', 35, 0.5, ('N', 32, 1.5, ('N', 11, 2.5, ('L', ((9, 2), (10, 8), (17, 1), (65, 1))), ('L', ((3, 1), (17, 1), (18, 3), (49, 1), (51, 2), (64, 1)))), ('L', ((6, 3), (65, 1)))), ('N', 43, 0.5, ('N', 17, 14.5, ('L', ((13, 10), (18, 2))), ('L', ((1, 2), (2, 2), (46, 1)))), ('N', 69, 1.0, ('L', ((0, 2),)), ('L', ((43, 2),))))), ('N', 75, 1.0, ('N', 5, 3.5, ('N', 17, 13.5, ('L', ((10, 11),)), ('L', ((2, 1), (10, 3), (12, 1), (20, 1), (29, 1)))), ('L', ((3, 1), (65, 1)))), ('N', 32, 1.5, ('L', ((3, 1), (62, 1))), ('L', ((59, 2),))))), ('N', 40, 1.5, ('L', ((22, 6),)), ('N', 83, 1.5, ('L', ((5, 1), (35, 2), (59, 1))), ('L', ((12, 2),))))), ('N', 41, 0.5, ('N', 40, 0.5, ('L', ((14, 2),)), ('N', 20, 0.5, ('L', ((13, 1), (29, 2), (49, 1))), ('L', ((5, 2),)))), ('N', 13, 2.5, ('L', ((14, 3),)), ('N', 1, 6.5, ('L', ((14, 3),)), ('L', ((3, 1), (14, 1))))))), ('N', 26, 0.5, ('N', 85, 1.0, ('N', 30, 2.0, ('L', ((13, 1), (17, 2))), ('L', ((35, 3),))), ('L', ((35, 3),))), ('L', ((3, 2),)))), ('N', 19, 4.0, ('L', ((5, 2),)), ('N', 69, 0.5, ('N', 79, 0.5, ('N', 39, 0.5, ('N', 41, 1.5, ('L', ((21, 10),)), ('N', 17, 12.5, ('L', ((21, 2),)), ('L', ((21, 1), (65, 1))))), ('L', ((21, 1), (22, 1), (30, 1)))), ('N', 52, 0.5, ('N', 1, 6.5, ('L', ((22, 2),)), ('N', 1, 11.0, ('L', ((17, 1), (44, 1))), ('L', ((5, 2),)))), ('L', ((21, 2),)))), ('N', 25, 0.5, ('L', ((21, 1), (59, 1))), ('L', ((22, 2),)))))), ('N', 12, 5.0, ('L', ((11, 10),)), ('N', 45, 0.5, ('N', 60, 1.5, ('N', 30, 0.5, ('L', ((11, 1), (17, 1), (58, 1))), ('L', ((22, 1), (49, 1)))), ('L', ((3, 2),))), ('L', ((2, 2),))))), ('N', 32, 2.0, ('N', 0, 3.5, ('N', 27, 1.5, ('N', 1, 1.5, ('L', ((64, 1), (65, 2))), ('N', 61, 0.5, ('L', ((63, 5),)), ('L', ((62, 1), (63, 2))))), ('L', ((4, 2),))), ('N', 22, 1.5, ('L', ((22, 1), (63, 1))), ('L', ((62, 5),)))), ('L', ((5, 3), (33, 4))))), ('N', 81, 0.5, ('N', 79, 0.5, ('N', 3, 0.5, ('N', 7, 3.0, ('N', 7, 0.5, ('N', 26, 0.5, ('N', 103, 0.5, ('N', 19, 3.5, ('L', ((17, 4),)), ('N', 20, 0.5, ('N', 108, 0.5, ('L', ((7, 2), (12, 2), (15, 1), (16, 1), (19, 1))), ('L', ((65, 6),))), ('N', 62, 1.5, ('L', ((7, 2), (12, 1), (17, 1), (21, 1), (63, 2))), ('L', ((19, 3),))))), ('L', ((60, 4), (63, 1)))), ('L', ((4, 7),))), ('N', 15, 11.5, ('N', 55, 1.5, ('L', ((11, 1), (63, 2))), ('L', ((63, 2),))), ('L', ((11, 2), (65, 1))))), ('N', 0, 13.5, ('N', 36, 1.5, ('N', 106, 0.5, ('N', 11, 8.0, ('N', 103, 0.5, ('N', 40, 3.0, ('L', ((5, 7), (8, 1))), ('L', ((21, 3),))), ('N', 16, 6.0, ('L', ((0, 2), (5, 1), (7, 1), (61, 1), (65, 1))), ('L', ((61, 3),)))), ('N', 47, 0.5, ('N', 39, 0.5, ('L', ((12, 1), (13, 1), (15, 1), (19, 6))), ('L', ((12, 1), (14, 2), (15, 1), (17, 1), (60, 1), (61, 1)))), ('L', ((4, 3),)))), ('N', 17, 5.5, ('L', ((19, 3),)), ('L', ((63, 5),)))), ('N', 61, 0.5, ('L', ((13, 1), (32, 1))), ('L', ((13, 4),)))), ('N', 11, 3.5, ('N', 69, 0.5, ('N', 106, 0.5, ('L', ((5, 1), (8, 1))), ('L', ((8, 4),))), ('N', 12, 3.0, ('L', ((8, 3),)), ('L', ((31, 2),)))), ('N', 13, 3.5, ('N', 13, 0.5, ('L', ((15, 1), (22, 2))), ('L', ((15, 1), (19, 1), (21, 1)))), ('L', ((5, 2),)))))), ('N', 51, 0.5, ('N', 33, 0.5, ('N', 6, 0.5, ('N', 102, 1.0, ('L', ((31, 3), (60, 2))), ('L', ((50, 2),))), ('N', 48, 0.5, ('N', 36, 1.5, ('N', 15, 5.5, ('N', 16, 6.0, ('L', ((0, 2), (7, 6), (13, 1))), ('L', ((4, 1), (12, 1)))), ('N', 96, 0.5, ('L', ((7, 17), (63, 1))), ('L', ((7, 2), (61, 1))))), ('L', ((14, 2),))), ('N', 23, 0.5, ('N', 17, 9.5, ('N', 13, 4.5, ('L', ((5, 9), (14, 1), (63, 1))), ('L', ((5, 3), (12, 1), (32, 2)))), ('N', 11, 7.0, ('L', ((7, 3),)), ('L', ((0, 3),)))), ('L', ((21, 2),))))), ('N', 47, 0.5, ('N', 23, 0.5, ('N', 9, 1.5, ('N', 17, 7.0, ('L', ((11, 3),)), ('L', ((11, 1), (14, 1)))), ('L', ((7, 2),))), ('N', 7, 3.5, ('N', 15, 14.5, ('L', ((0, 1), (51, 2))), ('N', 30, 1.0, ('L', ((21, 1), (65, 1))), ('L', ((12, 2),)))), ('L', ((5, 2),)))), ('L', ((4, 5),)))), ('N', 57, 0.5, ('N', 83, 1.0, ('N', 64, 0.5, ('N', 11, 6.5, ('N', 27, 0.5, ('N', 55, 1.5, ('L', ((7, 1), (12, 1))), ('L', ((12, 1), (22, 1)))), ('N', 15, 9.5, ('L', ((8, 2),)), ('L', ((22, 2),)))), ('N', 30, 0.5, ('L', ((51, 3), (65, 1))), ('N', 15, 8.5, ('L', ((4, 4), (63, 1))), ('L', ((61, 2), (63, 4)))))), ('N', 15, 13.0, ('L', ((21, 4),)), ('L', ((7, 2),)))), ('L', ((21, 4),))), ('N', 37, 1.0, ('L', ((14, 3),)), ('L', ((8, 1), (14, 4))))))), ('N', 35, 0.5, ('N', 27, 0.5, ('N', 8, 9.0, ('N', 1, 1.5, ('N', 34, 1.5, ('L', ((15, 3),)), ('L', ((15, 2), (61, 1)))), ('N', 77, 0.5, ('N', 13, 4.5, ('L', ((8, 3),)), ('L', ((8, 2), (15, 2)))), ('L', ((17, 3),)))), ('N', 15, 10.5, ('N', 12, 4.0, ('L', ((5, 3),)), ('L', ((5, 3), (7, 1)))), ('N', 51, 0.5, ('N', 6, 0.5, ('L', ((21, 2),)), ('L', ((14, 1), (61, 1)))), ('L', ((11, 2),))))), ('N', 19, 5.5, ('N', 16, 8.0, ('N', 48, 0.5, ('N', 22, 2.5, ('L', ((11, 1), (63, 1))), ('L', ((0, 3), (16, 2)))), ('N', 40, 0.5, ('L', ((5, 2), (61, 1))), ('L', ((5, 1), (17, 1))))), ('L', ((5, 3),))), ('N', 8, 7.5, ('L', ((63, 9),)), ('N', 42, 0.5, ('L', ((0, 3),)), ('N', 9, 2.0, ('L', ((10, 1), (50, 1), (63, 1))), ('L', ((7, 2),))))))), ('N', 4, 0.5, ('N', 106, 1.5, ('N', 19, 5.5, ('L', ((13, 10),)), ('N', 17, 9.5, ('N', 74, 1.0, ('N', 37, 1.5, ('N', 18, 5.0, ('L', ((13, 4),)), ('L', ((7, 1), (13, 2)))), ('L', ((8, 1), (13, 1), (21, 1)))), ('N', 85, 1.0, ('L', ((65, 2),)), ('L', ((61, 2),)))), ('L', ((14, 2), (21, 1))))), ('N', 22, 1.5, ('L', ((13, 1), (63, 1))), ('L', ((63, 8),)))), ('N', 12, 9.0, ('L', ((13, 1), (15, 1))), ('L', ((12, 4),)))))), ('L', ((4, 11),)))), ('N', 19, 3.5, ('N', 47, 0.5, ('N', 1, 3.5, ('N', 13, 2.5, ('N', 37, 2.5, ('L', ((21, 2), (63, 1))), ('L', ((21, 3),))), ('N', 1, 1.5, ('L', ((17, 1), (60, 1))), ('L', ((19, 1), (21, 1), (63, 1))))), ('N', 1, 8.5, ('N', 7, 2.0, ('N', 11, 3.5, ('L', ((7, 1), (41, 1))), ('L', ((60, 1), (63, 1)))), ('N', 9, 2.5, ('L', ((8, 3),)), ('L', ((8, 1), (21, 1))))), ('L', ((8, 1), (11, 3))))), ('L', ((4, 7),))), ('N', 17, 5.0, ('N', 74, 0.5, ('N', 30, 1.5, ('L', ((41, 5),)), ('L', ((8, 3),))), ('N', 7, 6.0, ('L', ((21, 1), (61, 3))), ('L', ((61, 1), (65, 1))))), ('N', 35, 0.5, ('L', ((41, 19),)), ('N', 104, 0.5, ('L', ((41, 5),)), ('L', ((59, 2),))))))), ('L', ((4, 14),))), ('N', 71, 0.5, ('N', 51, 0.5, ('N', 65, 0.5, ('N', 8, 6.5, ('N', 106, 0.5, ('N', 35, 0.5, ('N', 108, 0.5, ('N', 31, 0.5, ('N', 6, 0.5, ('N', 15, 6.5, ('N', 16, 6.5, ('N', 22, 0.5, ('N', 39, 0.5, ('L', ((21, 2), (32, 2))), ('L', ((10, 6), (20, 2)))), ('N', 41, 0.5, ('L', ((3, 1), (5, 1), (10, 2), (62, 1))), ('L', ((10, 1), (12, 3), (14, 1), (18, 8))))), ('N', 23, 0.5, ('N', 12, 5.0, ('L', ((59, 2),)), ('L', ((10, 2),))), ('L', ((21, 5),)))), ('N', 60, 0.5, ('N', 13, 1.5, ('N', 14, 2.0, ('L', ((10, 1), (11, 2))), ('L', ((11, 3),))), ('N', 102, 0.5, ('L', ((3, 2), (5, 1), (10, 5), (11, 2), (14, 2), (35, 4))), ('L', ((35, 1), (59, 3))))), ('N', 63, 0.5, ('N', 15, 7.5, ('L', ((11, 1), (17, 5))), ('L', ((3, 1), (14, 1), (62, 1)))), ('L', ((61, 2),))))), ('N', 104, 0.5, ('N', 0, 3.0, ('N', 15, 5.0, ('L', ((10, 2), (14, 1))), ('N', 57, 1.5, ('L', ((6, 1), (9, 1), (21, 2))), ('L', ((11, 2), (21, 1))))), ('N', 61, 0.5, ('N', 36, 0.5, ('L', ((5, 2), (12, 2), (15, 1))), ('L', ((5, 9),))), ('N', 47, 0.5, ('L', ((12, 1), (19, 7))), ('L', ((4, 2), (18, 2)))))), ('N', 14, 4.5, ('N', 57, 0.5, ('L', ((5, 1), (61, 3))), ('L', ((61, 4),))), ('L', ((12, 2),))))), ('N', 77, 0.5, ('N', 3, 0.5, ('L', ((49, 5),)), ('L', ((3, 1), (21, 1), (49, 1)))), ('L', ((35, 3), (44, 1), (51, 4))))), ('N', 5, 2.5, ('L', ((65, 11),)), ('L', ((64, 1), (65, 1))))), ('N', 101, 0.5, ('N', 12, 9.0, ('N', 22, 0.5, ('N', 36, 0.5, ('L', ((5, 3),)), ('L', ((11, 2),))), ('N', 68, 0.5, ('N', 20, 0.5, ('N', 61, 0.5, ('N', 0, 1.5, ('L', ((13, 4), (14, 2), (46, 1))), ('L', ((13, 11), (29, 1)))), ('L', ((18, 2),))), ('N', 64, 0.5, ('N', 42, 1.5, ('L', ((13, 2),)), ('L', ((13, 1), (43, 1)))), ('L', ((21, 5),)))), ('L', ((2, 1), (20, 2), (30, 1))))), ('L', ((13, 11),))), ('N', 15, 5.5, ('L', ((17, 3),)), ('L', ((64, 2),))))), ('N', 6, 0.5, ('N', 34, 1.0, ('N', 85, 0.5, ('N', 28, 0.5, ('N', 5, 1.5, ('L', ((65, 2),)), ('L', ((62, 1), (63, 1)))), ('L', ((63, 2),))), ('L', ((3, 2),))), ('N', 76, 0.5, ('N', 41, 1.5, ('L', ((62, 2),)), ('L', ((5, 3),))), ('L', ((32, 1), (33, 1))))), ('N', 9, 0.5, ('N', 27, 2.5, ('L', ((4, 1), (63, 2))), ('L', ((63, 2),))), ('N', 17, 5.0, ('L', ((51, 1), (63, 1))), ('L', ((63, 10),)))))), ('N', 47, 0.5, ('N', 64, 0.5, ('N', 54, 0.5, ('N', 4, 0.5, ('N', 73, 0.5, ('N', 102, 1.5, ('N', 22, 0.5, ('N', 19, 5.5, ('N', 12, 11.0, ('L', ((12, 2),)), ('L', ((5, 1), (60, 2)))), ('L', ((7, 2),))), ('N', 74, 0.5, ('N', 16, 4.5, ('L', ((17, 1), (63, 2))), ('L', ((0, 1), (5, 18), (13, 2)))), ('L', ((15, 1), (32, 1))))), ('L', ((60, 4),))), ('N', 57, 0.5, ('N', 98, 0.5, ('L', ((12, 1), (63, 2))), ('N', 11, 10.5, ('L', ((31, 1), (50, 1), (61, 1))), ('L', ((17, 1), (65, 1))))), ('N', 102, 0.5, ('L', ((14, 4),)), ('L', ((14, 1), (63, 1)))))), ('N', 75, 1.0, ('N', 29, 0.5, ('N', 28, 1.5, ('N', 16, 7.0, ('L', ((12, 1), (17, 2), (41, 1))), ('L', ((60, 2),))), ('N', 32, 0.5, ('N', 56, 1.5, ('L', ((0, 3), (7, 8), (14, 2), (19, 3), (50, 1))), ('L', ((19, 3),))), ('N', 27, 1.5, ('L', ((0, 1), (7, 11), (12, 1), (41, 1))), ('L', ((14, 1), (16, 1)))))), ('N', 19, 5.0, ('L', ((7, 1), (65, 1))), ('L', ((65, 4),)))), ('N', 61, 1.0, ('N', 96, 0.5, ('L', ((17, 4),)), ('L', ((19, 1), (60, 1)))), ('L', ((60, 3),))))), ('N', 13, 3.5, ('L', ((11, 6),)), ('N', 12, 3.0, ('L', ((11, 2),)), ('N', 84, 0.5, ('L', ((7, 1), (63, 1))), ('L', ((41, 2), (60, 1))))))), ('N', 54, 0.5, ('N', 15, 10.0, ('L', ((7, 1), (21, 1))), ('L', ((21, 9),))), ('N', 1, 11.5, ('N', 83, 1.0, ('L', ((0, 3), (11, 1))), ('N', 57, 1.0, ('L', ((12, 1), (51, 1), (65, 1))), ('L', ((60, 2),)))), ('L', ((21, 3),))))), ('L', ((4, 7),)))), ('N', 104, 0.5, ('N', 9, 1.5, ('N', 96, 1.0, ('N', 84, 0.5, ('N', 78, 0.5, ('L', ((22, 18),)), ('L', ((21, 2), (22, 1)))), ('L', ((41, 2),))), ('N', 0, 2.0, ('L', ((58, 2),)), ('N', 100, 1.0, ('L', ((31, 2),)), ('L', ((4, 2),))))), ('N', 77, 0.5, ('N', 28, 1.5, ('N', 17, 2.5, ('L', ((7, 2),)), ('N', 2, 0.5, ('N', 106, 1.5, ('L', ((11, 1), (60, 1))), ('L', ((63, 2),))), ('L', ((4, 2),)))), ('N', 58, 0.5, ('L', ((5, 2),)), ('L', ((5, 2), (12, 1))))), ('N', 6, 0.5, ('L', ((21, 1), (22, 2))), ('L', ((41, 3),))))), ('N', 28, 1.5, ('N', 1, 4.0, ('L', ((3, 1), (62, 2))), ('L', ((12, 3),))), ('N', 98, 0.5, ('L', ((7, 2), (59, 1))), ('N', 15, 9.5, ('L', ((59, 2),)), ('L', ((22, 1), (35, 1)))))))), ('N', 41, 2.5, ('N', 64, 0.5, ('N', 94, 0.5, ('N', 81, 0.5, ('N', 47, 0.5, ('N', 106, 0.5, ('N', 33, 0.5, ('N', 58, 0.5, ('N', 18, 5.5, ('N', 11, 5.5, ('N', 15, 12.5, ('L', ((8, 7),)), ('L', ((8, 2), (13, 1)))), ('N', 85, 0.5, ('L', ((17, 2),)), ('L', ((8, 1), (17, 1))))), ('N', 36, 0.5, ('N', 14, 3.5, ('L', ((12, 1), (13, 1), (22, 4), (65, 5))), ('L', ((0, 1), (7, 4), (8, 5)))), ('L', ((14, 6),)))), ('N', 35, 0.5, ('N', 12, 7.0, ('L', ((15, 3),)), ('L', ((5, 1), (15, 1), (19, 1)))), ('N', 30, 1.5, ('L', ((13, 3),)), ('N', 1, 6.5, ('L', ((32, 1), (41, 1))), ('L', ((13, 3),)))))), ('N', 62, 1.0, ('N', 37, 1.0, ('L', ((5, 2), (11, 1))), ('L', ((11, 3),))), ('N', 85, 1.5, ('L', ((61, 2),)), ('L', ((8, 1), (19, 1)))))), ('N', 12, 10.5, ('N', 25, 0.5, ('N', 84, 1.5, ('L', ((63, 18),)), ('N', 3, 0.5, ('L', ((8, 1), (63, 3))), ('L', ((63, 4),)))), ('N', 15, 10.0, ('L', ((63, 2),)), ('L', ((22, 2), (63, 1))))), ('N', 0, 12.0, ('N', 74, 1.0, ('L', ((63, 3),)), ('L', ((19, 2),))), ('L', ((63, 2),))))), ('L', ((4, 4),))), ('L', ((4, 13),))), ('L', ((51, 4),))), ('N', 35, 0.5, ('N', 0, 19.0, ('L', ((21, 10),)), ('L', ((5, 1), (63, 1), (65, 2)))), ('L', ((5, 1), (8, 1), (13, 1))))), ('N', 73, 0.5, ('N', 13, 3.5, ('N', 12, 8.5, ('N', 16, 6.0, ('L', ((8, 1), (14, 1))), ('L', ((16, 2),))), ('L', ((5, 1), (15, 2)))), ('N', 10, 2.0, ('N', 32, 0.5, ('L', ((5, 1), (32, 1), (41, 1))), ('L', ((8, 4),))), ('L', ((8, 6),)))), ('N', 37, 1.5, ('L', ((21, 1), (61, 1), (65, 1))), ('L', ((61, 2),)))))), ('L', ((4, 17),))), ('N', 28, 0.5, ('N', 65, 0.5, ('N', 23, 0.5, ('N', 45, 0.5, ('N', 105, 0.5, ('N', 36, 0.5, ('N', 56, 0.5, ('N', 92, 0.5, ('N', 1, 6.5, ('N', 33, 0.5, ('N', 6, 0.5, ('N', 14, 1.5, ('N', 63, 0.5, ('L', ((10, 7), (12, 1), (17, 1))), ('L', ((20, 2),))), ('N', 15, 7.0, ('L', ((18, 1), (65, 1))), ('L', ((18, 2), (65, 1))))), ('N', 17, 13.5, ('L', ((64, 2),)), ('L', ((12, 2),)))), ('N', 9, 1.0, ('L', ((4, 3),)), ('L', ((11, 1), (17, 2))))), ('N', 79, 1.0, ('L', ((10, 10),)), ('L', ((10, 1), (65, 1))))), ('N', 106, 0.5, ('L', ((49, 5),)), ('L', ((63, 2),)))), ('N', 24, 1.5, ('L', ((1, 1), (20, 2), (46, 1))), ('N', 98, 1.0, ('N', 2, 0.5, ('L', ((17, 1), (64, 1))), ('N', 15, 5.5, ('L', ((13, 2), (18, 1))), ('L', ((13, 6),)))), ('L', ((49, 1), (63, 1)))))), ('N', 32, 1.5, ('N', 16, 4.0, ('N', 52, 0.5, ('N', 42, 0.5, ('L', ((11, 1), (14, 1), (59, 1))), ('L', ((13, 1), (29, 1)))), ('L', ((65, 2),))), ('N', 1, 12.0, ('L', ((14, 11),)), ('L', ((9, 1), (14, 2))))), ('L', ((11, 2),)))), ('L', ((62, 6),))), ('L', ((2, 5),))), ('N', 79, 0.5, ('N', 42, 0.5, ('N', 13, 1.5, ('L', ((21, 3),)), ('N', 17, 13.5, ('L', ((11, 1), (21, 1), (65, 1))), ('L', ((21, 2), (30, 1))))), ('L', ((21, 5),))), ('N', 98, 0.5, ('N', 3, 0.5, ('L', ((17, 2), (21, 1))), ('N', 78, 0.5, ('L', ((5, 1), (21, 1))), ('L', ((35, 1), (44, 1))))), ('L', ((59, 3),))))), ('N', 9, 3.0, ('N', 77, 0.5, ('N', 29, 0.5, ('L', ((22, 6),)), ('N', 1, 7.5, ('L', ((22, 4),)), ('L', ((21, 2), (22, 1))))), ('N', 1, 5.5, ('L', ((21, 2),)), ('L', ((22, 2),)))), ('L', ((4, 3), (63, 1))))), ('N', 108, 0.5, ('N', 26, 0.5, ('N', 23, 0.5, ('N', 2, 0.5, ('N', 106, 0.5, ('N', 78, 0.5, ('N', 31, 0.5, ('N', 55, 0.5, ('N', 42, 0.5, ('N', 43, 0.5, ('N', 84, 1.0, ('N', 57, 0.5, ('L', ((5, 4), (7, 3), (10, 1), (13, 2), (15, 1), (18, 2), (60, 2), (62, 1))), ('L', ((11, 1), (14, 3), (60, 1), (61, 1)))), ('L', ((41, 2),))), ('N', 57, 0.5, ('L', ((32, 1), (61, 4))), ('L', ((17, 1), (60, 1), (61, 1))))), ('N', 83, 1.5, ('N', 62, 0.5, ('L', ((17, 2), (61, 1))), ('N', 12, 9.0, ('L', ((5, 2), (19, 3))), ('L', ((5, 1), (19, 11))))), ('N', 43, 0.5, ('L', ((17, 3),)), ('L', ((17, 2), (41, 1)))))), ('N', 97, 0.5, ('N', 38, 0.5, ('N', 96, 0.5, ('L', ((62, 3),)), ('N', 25, 0.5, ('L', ((61, 3),)), ('L', ((5, 2), (60, 2))))), ('N', 17, 3.5, ('L', ((8, 4),)), ('N', 29, 0.5, ('L', ((5, 1), (11, 1), (12, 3), (15, 5), (32, 3))), ('L', ((11, 2), (12, 2)))))), ('L', ((59, 3),)))), ('N', 43, 0.5, ('L', ((51, 3),)), ('L', ((43, 3), (50, 1))))), ('N', 73, 1.5, ('L', ((35, 5),)), ('L', ((11, 2), (12, 2))))), ('N', 41, 1.5, ('N', 104, 0.5, ('N', 33, 0.5, ('N', 6, 0.5, ('L', ((60, 1), (62, 1), (63, 1))), ('L', ((63, 11),))), ('L', ((31, 1), (63, 1)))), ('L', ((60, 2), (62, 1)))), ('N', 30, 2.5, ('N', 28, 1.5, ('N', 62, 0.5, ('L', ((63, 3),)), ('L', ((31, 2),))), ('N', 34, 0.5, ('L', ((51, 2),)), ('N', 17, 3.5, ('N', 55, 1.5, ('L', ((5, 1), (15, 1), (39, 1))), ('L', ((8, 2), (60, 1)))), ('L', ((32, 2),))))), ('L', ((61, 2),))))), ('N', 34, 1.5, ('N', 60, 0.5, ('N', 4, 0.5, ('N', 10, 1.5, ('N', 1, 11.5, ('N', 42, 1.5, ('N', 24, 1.5, ('L', ((5, 11),)), ('L', ((5, 4), (35, 1)))), ('N', 16, 8.0, ('L', ((22, 2),)), ('N', 55, 0.5, ('L', ((63, 3),)), ('L', ((11, 3),))))), ('N', 84, 0.5, ('N', 6, 1.5, ('N', 54, 0.5, ('L', ((5, 4), (7, 1), (10, 1), (14, 2), (18, 2))), ('L', ((11, 2),))), ('N', 11, 3.0, ('L', ((8, 2), (14, 2))), ('L', ((7, 3), (13, 1), (14, 1))))), ('L', ((41, 2),)))), ('L', ((8, 5),))), ('N', 11, 11.5, ('N', 17, 5.5, ('N', 17, 4.5, ('N', 54, 1.5, ('N', 0, 9.0, ('L', ((7, 2), (63, 1))), ('L', ((7, 4), (11, 1)))), ('L', ((11, 2),))), ('N', 79, 1.0, ('L', ((8, 1), (16, 1))), ('L', ((0, 1), (11, 1))))), ('N', 84, 0.5, ('N', 6, 1.5, ('N', 19, 3.5, ('L', ((0, 2), (7, 2))), ('L', ((7, 16), (10, 1)))), ('L', ((14, 2), (63, 1)))), ('L', ((41, 5),)))), ('L', ((7, 1), (63, 3))))), ('N', 59, 0.5, ('N', 56, 0.5, ('N', 54, 0.5, ('N', 17, 8.5, ('N', 14, 2.5, ('L', ((12, 2), (17, 1))), ('L', ((5, 2),))), ('N', 27, 0.5, ('N', 12, 3.0, ('L', ((5, 1), (17, 1))), ('L', ((17, 8),))), ('L', ((15, 1), (63, 1))))), ('N', 37, 0.5, ('L', ((63, 2),)), ('L', ((41, 2),)))), ('L', ((7, 3),))), ('L', ((0, 1), (5, 3), (16, 3))))), ('N', 3, 0.5, ('N', 56, 0.5, ('N', 8, 5.0, ('N', 1, 7.0, ('L', ((5, 2), (33, 1))), ('L', ((5, 2),))), ('N', 40, 1.5, ('L', ((15, 3),)), ('L', ((8, 1), (63, 3))))), ('N', 41, 2.5, ('L', ((13, 4),)), ('N', 0, 17.0, ('N', 11, 7.0, ('L', ((8, 1), (16, 1))), ('L', ((19, 1), (41, 1)))), ('L', ((19, 1), (41, 2)))))), ('N', 7, 1.0, ('N', 15, 13.5, ('N', 0, 3.5, ('L', ((0, 1), (11, 1))), ('L', ((12, 3),))), ('N', 11, 7.0, ('L', ((7, 1), (14, 1))), ('L', ((5, 1), (8, 1))))), ('N', 40, 0.5, ('L', ((8, 4), (63, 1))), ('L', ((8, 4),))))))), ('N', 48, 0.5, ('N', 56, 0.5, ('N', 50, 0.5, ('L', ((31, 3), (60, 1))), ('N', 58, 0.5, ('N', 34, 1.0, ('L', ((7, 8),)), ('L', ((21, 1), (41, 1)))), ('L', ((11, 1), (19, 1), (22, 1))))), ('N', 16, 9.5, ('L', ((0, 1), (12, 1), (13, 1))), ('L', ((15, 1), (21, 2))))), ('N', 16, 5.5, ('N', 9, 1.5, ('N', 52, 0.5, ('L', ((21, 5),)), ('L', ((0, 1), (11, 1), (13, 1)))), ('N', 57, 1.5, ('N', 93, 0.5, ('N', 24, 1.0, ('N', 74, 1.0, ('L', ((5, 4),)), ('L', ((0, 1), (5, 1)))), ('L', ((5, 2), (19, 1)))), ('L', ((12, 3), (51, 1)))), ('L', ((60, 3),)))), ('N', 54, 0.5, ('N', 8, 6.5, ('N', 35, 0.5, ('L', ((61, 1), (63, 2))), ('L', ((5, 1), (13, 2)))), ('N', 19, 1.5, ('L', ((7, 3),)), ('N', 1, 2.0, ('N', 8, 9.0, ('L', ((13, 2),)), ('L', ((12, 1), (22, 1)))), ('N', 38, 0.5, ('L', ((5, 1), (21, 2))), ('L', ((21, 10),)))))), ('L', ((21, 7),)))))), ('N', 75, 0.5, ('N', 1, 9.5, ('N', 34, 1.5, ('N', 15, 3.5, ('N', 28, 2.5, ('L', ((4, 3),)), ('L', ((4, 1), (18, 1)))), ('L', ((4, 37),))), ('N', 47, 0.5, ('L', ((3, 2),)), ('L', ((4, 2),)))), ('N', 50, 0.5, ('L', ((3, 4),)), ('N', 51, 0.5, ('N', 17, 10.0, ('L', ((4, 4),)), ('L', ((4, 1), (41, 2)))), ('L', ((21, 2),))))), ('N', 15, 5.5, ('L', ((32, 2),)), ('N', 28, 1.5, ('N', 1, 7.5, ('L', ((3, 4),)), ('L', ((49, 2),))), ('L', ((4, 3),)))))), ('N', 28, 1.5, ('L', ((65, 16),)), ('N', 17, 8.0, ('L', ((65, 4),)), ('N', 9, 0.5, ('L', ((8, 3),)), ('N', 47, 0.5, ('L', ((63, 1), (65, 1))), ('L', ((4, 2),)))))))), ('N', 47, 0.5, ('N', 108, 0.5, ('N', 23, 0.5, ('N', 4, 0.5, ('N', 7, 4.5, ('N', 106, 0.5, ('N', 5, 4.5, ('N', 5, 3.5, ('N', 54, 0.5, ('N', 56, 0.5, ('N', 104, 1.5, ('N', 28, 0.5, ('N', 89, 0.5, ('L', ((2, 1), (6, 1), (10, 11), (12, 3), (14, 9), (18, 2), (22, 2), (29, 2), (59, 2))), ('L', ((49, 4),))), ('N', 42, 0.5, ('L', ((5, 4), (62, 1))), ('L', ((5, 2), (12, 4), (17, 2), (18, 2), (61, 1), (62, 2))))), ('L', ((35, 2),))), ('N', 1, 5.5, ('N', 0, 1.5, ('N', 20, 0.5, ('L', ((14, 2), (20, 4), (46, 2))), ('L', ((1, 2), (2, 3)))), ('N', 9, 2.5, ('L', ((13, 1), (22, 1), (29, 1))), ('L', ((13, 2),)))), ('L', ((13, 5),)))), ('N', 79, 1.5, ('N', 13, 1.5, ('L', ((11, 6),)), ('N', 12, 6.0, ('L', ((11, 2),)), ('L', ((2, 1), (11, 1))))), ('L', ((22, 3),)))), ('N', 28, 0.5, ('N', 13, 4.0, ('L', ((11, 1), (17, 1))), ('L', ((17, 4),))), ('N', 12, 4.0, ('N', 24, 1.5, ('L', ((3, 1), (18, 1))), ('L', ((3, 2), (11, 2)))), ('N', 13, 3.5, ('N', 15, 9.0, ('L', ((32, 1), (49, 1))), ('L', ((3, 2),))), ('N', 75, 1.0, ('L', ((3, 5),)), ('L', ((3, 1), (59, 1)))))))), ('N', 104, 0.5, ('N', 13, 0.5, ('L', ((7, 6),)), ('N', 65, 0.5, ('N', 17, 7.5, ('N', 7, 1.0, ('N', 1, 13.0, ('L', ((5, 13), (8, 1), (11, 1), (15, 1), (17, 5), (41, 1))), ('L', ((8, 3),))), ('L', ((8, 6),))), ('N', 34, 1.5, ('N', 30, 2.5, ('L', ((0, 1), (5, 5), (7, 5), (13, 1), (17, 2), (18, 4), (32, 2), (41, 2), (51, 1), (60, 1))), ('L', ((13, 3),))), ('N', 11, 4.0, ('L', ((11, 4), (41, 1))), ('L', ((8, 2), (11, 2), (12, 5)))))), ('N', 55, 0.5, ('L', ((11, 2), (41, 1))), ('N', 74, 0.5, ('N', 14, 2.5, ('L', ((15, 1), (22, 2))), ('L', ((22, 2),))), ('L', ((22, 2),)))))), ('N', 51, 0.5, ('N', 57, 0.5, ('N', 103, 1.5, ('N', 7, 1.5, ('L', ((50, 1), (60, 1))), ('L', ((15, 1), (60, 1)))), ('L', ((61, 2),))), ('L', ((60, 4),))), ('L', ((8, 1), (15, 1), (61, 3)))))), ('N', 105, 0.5, ('N', 34, 0.5, ('N', 30, 2.0, ('N', 0, 11.0, ('L', ((63, 11),)), ('N', 36, 0.5, ('L', ((60, 1), (63, 1))), ('L', ((60, 1), (63, 2))))), ('L', ((41, 1), (63, 1)))), ('N', 17, 5.0, ('L', ((8, 4),)), ('N', 14, 3.5, ('N', 73, 0.5, ('N', 22, 1.5, ('L', ((8, 1), (41, 1), (63, 1))), ('N', 77, 1.5, ('L', ((63, 4),)), ('L', ((22, 2),)))), ('N', 83, 0.5, ('L', ((31, 3),)), ('L', ((41, 1), (63, 1))))), ('L', ((5, 1), (32, 1), (33, 3)))))), ('N', 30, 2.5, ('L', ((62, 7),)), ('L', ((62, 1), (63, 1)))))), ('N', 62, 0.5, ('N', 1, 5.5, ('N', 9, 2.5, ('N', 106, 0.5, ('N', 28, 1.5, ('L', ((15, 3),)), ('N', 2, 0.5, ('L', ((12, 1), (61, 1))), ('L', ((14, 2),)))), ('L', ((63, 9),))), ('N', 102, 1.5, ('N', 8, 3.0, ('N', 35, 0.5, ('L', ((12, 1), (61, 1))), ('L', ((13, 2),))), ('L', ((5, 4),))), ('L', ((63, 2),)))), ('N', 27, 0.5, ('L', ((5, 7),)), ('L', ((5, 1), (63, 1))))), ('N', 57, 0.5, ('N', 37, 0.5, ('N', 35, 1.0, ('L', ((19, 9),)), ('L', ((5, 3),))), ('N', 39, 0.5, ('N', 18, 3.5, ('N', 67, 0.5, ('L', ((19, 3),)), ('L', ((61, 2),))), ('N', 9, 2.5, ('N', 15, 9.0, ('L', ((63, 2),)), ('L', ((13, 1), (63, 1)))), ('L', ((5, 2),)))), ('L', ((41, 3),)))), ('N', 40, 0.5, ('L', ((8, 1), (63, 1))), ('N', 13, 4.0, ('L', ((32, 4),)), ('L', ((5, 1), (32, 2), (63, 1)))))))), ('N', 6, 1.5, ('N', 84, 0.5, ('N', 55, 1.5, ('N', 42, 0.5, ('N', 5, 3.5, ('L', ((10, 2), (35, 1))), ('N', 15, 9.5, ('N', 9, 1.5, ('L', ((7, 1), (60, 1))), ('N', 28, 2.5, ('N', 41, 0.5, ('L', ((7, 6),)), ('L', ((7, 2), (17, 1)))), ('N', 13, 2.5, ('L', ((7, 2), (13, 2))), ('L', ((0, 1), (7, 8)))))), ('N', 54, 0.5, ('N', 0, 8.0, ('N', 13, 3.5, ('L', ((7, 2),)), ('L', ((0, 1), (7, 1), (63, 1)))), ('L', ((0, 1), (60, 1)))), ('L', ((11, 3),))))), ('N', 50, 0.5, ('L', ((9, 2), (10, 1))), ('N', 62, 0.5, ('N', 2, 0.5, ('L', ((17, 1), (50, 2))), ('N', 3, 0.5, ('L', ((12, 2), (17, 1))), ('L', ((7, 4),)))), ('L', ((19, 3),))))), ('N', 17, 5.0, ('L', ((19, 2),)), ('L', ((12, 2), (14, 1))))), ('N', 18, 4.5, ('L', ((7, 1), (41, 1))), ('L', ((41, 5),)))), ('N', 83, 0.5, ('N', 24, 0.5, ('N', 19, 3.5, ('L', ((11, 3),)), ('L', ((7, 1), (15, 1), (16, 2)))), ('L', ((7, 1), (8, 1), (14, 3)))), ('N', 15, 11.5, ('L', ((8, 5),)), ('N', 36, 0.5, ('L', ((8, 2),)), ('L', ((8, 1), (11, 1)))))))), ('N', 28, 1.5, ('N', 62, 0.5, ('N', 54, 0.5, ('N', 24, 0.5, ('N', 11, 5.5, ('L', ((21, 3),)), ('N', 5, 3.5, ('L', ((5, 2),)), ('L', ((15, 3), (22, 1))))), ('N', 27, 0.5, ('N', 15, 6.5, ('L', ((21, 3),)), ('N', 1, 3.5, ('L', ((22, 2),)), ('N', 39, 0.5, ('N', 22, 1.5, ('L', ((21, 3),)), ('N', 17, 12.5, ('L', ((5, 1), (21, 4), (22, 1), (35, 1))), ('L', ((17, 1), (44, 1))))), ('L', ((22, 1), (30, 1)))))), ('L', ((21, 20),)))), ('N', 22, 0.5, ('L', ((13, 1), (17, 1), (60, 1))), ('L', ((11, 1), (22, 1))))), ('L', ((19, 4),))), ('N', 17, 6.5, ('N', 34, 0.5, ('N', 37, 1.5, ('N', 15, 9.5, ('L', ((7, 1), (17, 2))), ('L', ((7, 5),))), ('N', 15, 10.5, ('L', ((0, 2), (7, 1))), ('N', 57, 0.5, ('N', 79, 1.0, ('L', ((21, 2),)), ('L', ((63, 5),))), ('N', 32, 0.5, ('L', ((19, 1), (21, 1))), ('L', ((13, 1), (61, 1))))))), ('L', ((21, 5),))), ('N', 11, 1.5, ('L', ((5, 4), (8, 1))), ('N', 27, 0.5, ('N', 4, 0.5, ('N', 0, 8.0, ('N', 56, 0.5, ('L', ((9, 2), (22, 1))), ('N', 1, 11.5, ('L', ((11, 2), (51, 1))), ('N', 52, 0.5, ('L', ((5, 1), (21, 1))), ('L', ((0, 1), (13, 1)))))), ('L', ((13, 2),))), ('N', 1, 16.5, ('L', ((41, 3),)), ('L', ((12, 3),)))), ('N', 48, 0.5, ('L', ((0, 5), (7, 1), (11, 1))), ('N', 43, 0.5, ('L', ((21, 1), (61, 1))), ('L', ((0, 2), (5, 1)))))))))), ('N', 39, 0.5, ('L', ((65, 20),)), ('N', 14, 3.0, ('L', ((13, 1), (64, 1), (65, 1))), ('L', ((65, 4),))))), ('N', 5, 4.5, ('N', 41, 1.5, ('N', 26, 1.5, ('L', ((4, 4),)), ('L', ((4, 1), (17, 1), (22, 1)))), ('N', 64, 0.5, ('L', ((18, 1), (22, 1), (49, 1))), ('L', ((21, 3), (65, 1))))), ('N', 42, 0.5, ('N', 16, 4.5, ('N', 39, 0.5, ('L', ((4, 3),)), ('L', ((18, 3),))), ('N', 33, 0.5, ('L', ((4, 9),)), ('N', 15, 7.5, ('L', ((4, 2),)), ('L', ((41, 2),))))), ('N', 17, 5.5, ('N', 61, 0.5, ('L', ((4, 1), (21, 1))), ('L', ((4, 2),))), ('L', ((4, 24),)))))), ('N', 26, 0.5, ('N', 8, 9.0, ('N', 65, 0.5, ('N', 50, 0.5, ('N', 36, 0.5, ('N', 35, 0.5, ('N', 73, 0.5, ('N', 88, 0.5, ('N', 0, 3.5, ('N', 1, 3.5, ('N', 55, 0.5, ('N', 33, 0.5, ('L', ((21, 1), (63, 1), (65, 1))), ('L', ((63, 3),))), ('N', 97, 0.5, ('L', ((10, 1), (11, 1))), ('L', ((11, 2),)))), ('N', 60, 0.5, ('N', 1, 16.0, ('N', 17, 14.5, ('L', ((6, 1), (10, 14))), ('L', ((10, 1), (21, 1)))), ('L', ((9, 3),))), ('L', ((17, 3),)))), ('N', 83, 1.5, ('N', 76, 0.5, ('N', 49, 0.5, ('N', 60, 0.5, ('L', ((10, 1), (35, 1), (59, 2), (62, 1))), ('L', ((5, 2), (61, 2)))), ('L', ((12, 1), (64, 2)))), ('L', ((33, 3),))), ('N', 1, 7.0, ('L', ((17, 5),)), ('L', ((35, 2),))))), ('N', 69, 1.0, ('N', 32, 0.5, ('L', ((44, 2), (62, 1))), ('L', ((49, 6),))), ('L', ((51, 3),)))), ('N', 0, 4.0, ('N', 73, 1.5, ('L', ((2, 2), (65, 1))), ('L', ((59, 2),))), ('N', 55, 0.5, ('L', ((62, 5),)), ('L', ((31, 1), (62, 2)))))), ('N', 73, 1.0, ('N', 15, 9.5, ('N', 23, 0.5, ('N', 2, 0.5, ('L', ((13, 1), (46, 1), (63, 1))), ('N', 45, 0.5, ('N', 48, 0.5, ('L', ((13, 10),)), ('L', ((13, 2), (18, 1)))), ('L', ((2, 2),)))), ('L', ((21, 4),))), ('L', ((0, 3), (13, 1), (43, 1)))), ('N', 1, 4.0, ('L', ((49, 3),)), ('L', ((30, 3),))))), ('N', 1, 7.5, ('N', 49, 0.5, ('N', 66, 0.5, ('N', 57, 1.5, ('N', 2, 0.5, ('N', 1, 2.0, ('L', ((11, 1), (14, 2))), ('N', 14, 2.5, ('L', ((29, 1), (49, 1))), ('L', ((11, 1), (59, 1))))), ('L', ((14, 3),))), ('L', ((11, 3),))), ('L', ((65, 2),))), ('L', ((13, 4), (14, 1)))), ('N', 40, 1.5, ('L', ((14, 7), (21, 2))), ('L', ((21, 2), (35, 1)))))), ('N', 7, 5.5, ('N', 51, 0.5, ('N', 103, 0.5, ('N', 15, 5.5, ('L', ((31, 2),)), ('N', 37, 0.5, ('L', ((63, 3),)), ('N', 17, 9.5, ('N', 79, 1.0, ('L', ((11, 2), (65, 1))), ('L', ((10, 1), (17, 1)))), ('L', ((41, 2),))))), ('N', 85, 0.5, ('N', 69, 0.5, ('L', ((60, 3),)), ('N', 102, 1.0, ('L', ((15, 1), (60, 2))), ('L', ((63, 2),)))), ('L', ((60, 9),)))), ('N', 93, 0.5, ('N', 23, 0.5, ('N', 54, 0.5, ('N', 69, 1.0, ('N', 36, 0.5, ('N', 34, 0.5, ('N', 2, 0.5, ('L', ((17, 2),)), ('L', ((8, 3),))), ('L', ((8, 5),))), ('N', 4, 0.5, ('N', 10, 2.5, ('L', ((8, 3), (15, 1), (17, 1), (63, 3))), ('L', ((14, 1), (63, 1)))), ('N', 35, 0.5, ('L', ((8, 3),)), ('L', ((13, 2),))))), ('L', ((61, 2),))), ('N', 30, 0.5, ('N', 61, 1.5, ('L', ((8, 8),)), ('N', 96, 0.5, ('L', ((8, 2),)), ('N', 16, 6.5, ('L', ((15, 2),)), ('L', ((8, 2),))))), ('L', ((5, 1), (11, 1))))), ('N', 17, 7.0, ('L', ((21, 5),)), ('L', ((8, 1), (13, 4))))), ('L', ((51, 3),)))), ('N', 103, 0.5, ('N', 106, 0.5, ('N', 35, 0.5, ('N', 61, 1.5, ('N', 30, 0.5, ('N', 12, 10.5, ('N', 9, 2.5, ('N', 22, 0.5, ('L', ((21, 2),)), ('L', ((5, 2), (14, 1), (19, 2), (41, 2)))), ('L', ((15, 2),))), ('N', 58, 0.5, ('L', ((12, 3),)), ('L', ((12, 1), (15, 1))))), ('L', ((5, 7),))), ('N', 32, 1.0, ('N', 64, 0.5, ('L', ((19, 4),)), ('L', ((19, 2), (21, 1)))), ('L', ((5, 1), (21, 2))))), ('N', 85, 1.0, ('L', ((5, 1), (19, 1))), ('N', 30, 1.5, ('L', ((13, 4),)), ('N', 34, 2.0, ('L', ((13, 3),)), ('L', ((32, 2),)))))), ('N', 13, 2.5, ('L', ((13, 1), (51, 1), (63, 1))), ('N', 20, 0.5, ('L', ((63, 7),)), ('L', ((5, 1), (32, 1), (41, 1)))))), ('N', 39, 0.5, ('N', 35, 0.5, ('N', 9, 2.5, ('L', ((61, 7),)), ('L', ((5, 1), (19, 1), (61, 1)))), ('N', 48, 0.5, ('L', ((7, 2),)), ('N', 27, 0.5, ('L', ((13, 2),)), ('L', ((63, 4),))))), ('N', 98, 1.5, ('L', ((63, 3),)), ('L', ((5, 3), (12, 1)))))))), ('N', 17, 11.5, ('N', 15, 13.5, ('N', 15, 7.0, ('N', 27, 1.5, ('L', ((19, 3),)), ('L', ((22, 4),))), ('N', 108, 0.5, ('N', 35, 0.5, ('N', 85, 0.5, ('L', ((62, 4),)), ('L', ((22, 1), (35, 2)))), ('N', 6, 1.5, ('L', ((5, 4),)), ('L', ((8, 2),)))), ('L', ((65, 4),)))), ('L', ((11, 4),))), ('L', ((22, 12),)))), ('N', 57, 0.5, ('N', 4, 0.5, ('N', 106, 0.5, ('N', 108, 0.5, ('N', 23, 0.5, ('N', 84, 1.0, ('N', 11, 3.5, ('N', 33, 0.5, ('L', ((0, 2), (22, 1))), ('L', ((11, 2),))), ('N', 10, 3.5, ('N', 32, 0.5, ('N', 43, 0.5, ('L', ((7, 6),)), ('L', ((12, 2), (18, 1)))), ('N', 42, 0.5, ('N', 92, 0.5, ('L', ((15, 1), (17, 1), (61, 1))), ('L', ((50, 2),))), ('L', ((5, 2),)))), ('L', ((32, 3),)))), ('L', ((41, 3),))), ('N', 48, 0.5, ('N', 17, 4.5, ('L', ((31, 2),)), ('L', ((7, 1), (13, 1)))), ('N', 43, 0.5, ('L', ((21, 11),)), ('L', ((12, 2),))))), ('L', ((65, 9),))), ('N', 77, 0.5, ('N', 64, 0.5, ('N', 14, 2.5, ('N', 67, 0.5, ('L', ((63, 3),)), ('L', ((31, 2),))), ('N', 12, 10.5, ('L', ((63, 6),)), ('L', ((60, 1), (63, 2))))), ('L', ((21, 2),))), ('L', ((5, 2),)))), ('N', 58, 0.5, ('N', 23, 0.5, ('N', 33, 0.5, ('N', 106, 0.5, ('N', 3, 0.5, ('L', ((7, 2), (41, 1), (59, 1))), ('N', 30, 3.5, ('L', ((7, 20),)), ('L', ((7, 2), (41, 1))))), ('L', ((8, 1), (63, 1)))), ('N', 83, 1.0, ('L', ((7, 2),)), ('L', ((41, 2),)))), ('L', ((0, 2), (7, 1), (21, 1)))), ('N', 41, 1.0, ('N', 29, 0.5, ('N', 22, 0.5, ('L', ((19, 2),)), ('N', 42, 1.0, ('L', ((17, 2), (60, 1))), ('L', ((12, 1), (17, 1))))), ('L', ((65, 4),))), ('N', 6, 1.5, ('L', ((0, 1), (11, 1), (16, 2))), ('L', ((16, 2),)))))), ('N', 6, 0.5, ('N', 1, 5.5, ('L', ((41, 1), (60, 2))), ('N', 16, 5.5, ('L', ((21, 2),)), ('L', ((5, 6),)))), ('N', 40, 3.5, ('N', 84, 0.5, ('N', 0, 8.5, ('N', 12, 9.0, ('N', 33, 0.5, ('N', 28, 1.5, ('N', 60, 1.0, ('L', ((14, 4),)), ('L', ((15, 1), (21, 1)))), ('L', ((7, 1), (8, 1)))), ('N', 48, 0.5, ('L', ((11, 3),)), ('L', ((11, 1), (22, 1))))), ('N', 27, 0.5, ('L', ((0, 1), (12, 1), (14, 1))), ('L', ((14, 7),)))), ('N', 58, 0.5, ('N', 27, 1.5, ('L', ((7, 5),)), ('L', ((7, 1), (8, 1)))), ('N', 17, 6.5, ('L', ((17, 1), (21, 1))), ('L', ((11, 2),))))), ('N', 48, 0.5, ('N', 11, 3.5, ('L', ((7, 1), (41, 1))), ('L', ((41, 4),))), ('L', ((11, 1), (63, 1))))), ('L', ((5, 5), (7, 1))))))), ('N', 47, 0.5, ('N', 13, 3.5, ('N', 24, 1.5, ('N', 2, 0.5, ('L', ((32, 1), (49, 1), (63, 1))), ('L', ((22, 2),))), ('L', ((11, 1), (17, 3)))), ('N', 73, 1.0, ('N', 13, 4.5, ('L', ((3, 2), (11, 1))), ('N', 55, 1.0, ('L', ((3, 1), (18, 1))), ('L', ((3, 7),)))), ('L', ((3, 1), (63, 1))))), ('N', 43, 0.5, ('N', 17, 10.5, ('L', ((4, 34),)), ('N', 101, 0.5, ('L', ((4, 12),)), ('L', ((17, 1), (63, 1), (64, 1))))), ('N', 57, 0.5, ('N', 26, 1.5, ('N', 16, 5.5, ('L', ((4, 11),)), ('N', 1, 9.5, ('L', ((4, 4),)), ('L', ((4, 1), (21, 1))))), ('N', 25, 0.5, ('L', ((18, 2),)), ('L', ((22, 2),)))), ('L', ((14, 4),)))))), ('N', 23, 0.5, ('N', 6, 0.5, ('N', 85, 0.5, ('N', 108, 0.5, ('N', 105, 0.5, ('N', 92, 0.5, ('N', 45, 0.5, ('N', 20, 0.5, ('N', 33, 0.5, ('N', 80, 0.5, ('N', 25, 0.5, ('N', 56, 0.5, ('N', 75, 1.0, ('L', ((5, 1), (10, 6), (12, 2), (14, 2), (17, 1), (18, 2), (35, 2), (59, 5))), ('L', ((32, 3),))), ('N', 63, 0.5, ('L', ((13, 4), (14, 1), (46, 1))), ('L', ((20, 4),)))), ('N', 0, 3.5, ('L', ((22, 6),)), ('N', 40, 1.0, ('L', ((60, 2),)), ('L', ((3, 1), (12, 1)))))), ('L', ((17, 3),))), ('N', 1, 6.0, ('N', 27, 2.0, ('N', 9, 0.5, ('N', 0, 3.5, ('L', ((11, 3),)), ('L', ((11, 2), (61, 2)))), ('L', ((11, 5),))), ('L', ((14, 2),))), ('L', ((10, 2),)))), ('N', 14, 2.5, ('N', 34, 0.5, ('N', 42, 1.5, ('N', 33, 0.5, ('L', ((1, 2),)), ('L', ((17, 2),))), ('L', ((10, 2),))), ('L', ((10, 8),))), ('N', 9, 0.5, ('L', ((12, 1), (18, 1), (35, 1))), ('L', ((43, 1), (63, 1)))))), ('L', ((2, 5),))), ('N', 75, 1.0, ('L', ((49, 3),)), ('L', ((50, 3),)))), ('L', ((62, 7),))), ('L', ((65, 13),))), ('N', 17, 6.0, ('L', ((5, 3),)), ('N', 26, 1.5, ('N', 80, 0.5, ('L', ((5, 2), (32, 1), (35, 3))), ('N', 73, 1.0, ('N', 17, 9.5, ('L', ((3, 3),)), ('L', ((3, 1), (11, 1)))), ('L', ((59, 2),)))), ('L', ((4, 3),))))), ('N', 71, 0.5, ('N', 108, 0.5, ('N', 106, 0.5, ('N', 57, 0.5, ('N', 84, 0.5, ('N', 62, 0.5, ('N', 26, 0.5, ('N', 48, 0.5, ('N', 16, 4.5, ('N', 1, 9.0, ('L', ((7, 1), (13, 1))), ('L', ((7, 9),))), ('N', 33, 0.5, ('N', 73, 1.0, ('L', ((0, 2), (7, 8), (12, 6), (15, 3), (16, 1), (17, 5), (60, 3))), ('L', ((61, 4),))), ('L', ((11, 5),)))), ('N', 7, 4.5, ('N', 14, 1.5, ('N', 65, 0.5, ('L', ((6, 1), (13, 7), (18, 3))), ('L', ((22, 4),))), ('N', 104, 1.5, ('L', ((0, 2), (5, 9), (7, 4), (8, 6), (11, 3), (12, 4), (13, 2), (15, 3), (17, 1), (18, 1), (22, 1), (32, 1), (51, 2), (60, 3))), ('L', ((61, 4),)))), ('N', 33, 0.5, ('L', ((5, 7),)), ('L', ((5, 1), (12, 1), (13, 1)))))), ('N', 32, 0.5, ('L', ((4, 10),)), ('L', ((4, 2), (17, 1))))), ('N', 26, 0.5, ('N', 12, 9.0, ('N', 20, 0.5, ('L', ((5, 4),)), ('N', 1, 11.0, ('L', ((13, 2), (17, 1), (61, 1))), ('L', ((19, 2),)))), ('N', 61, 0.5, ('L', ((19, 5),)), ('N', 18, 4.0, ('L', ((19, 4),)), ('N', 9, 3.5, ('L', ((18, 1), (19, 1))), ('L', ((19, 2),)))))), ('L', ((4, 6),)))), ('N', 102, 0.5, ('L', ((41, 10),)), ('L', ((59, 2),)))), ('N', 104, 0.5, ('N', 103, 1.0, ('N', 37, 0.5, ('N', 0, 9.5, ('N', 33, 0.5, ('N', 17, 13.5, ('L', ((14, 9),)), ('L', ((13, 1), (14, 1)))), ('N', 74, 0.5, ('L', ((11, 2),)), ('L', ((14, 2),)))), ('L', ((5, 1), (7, 1)))), ('N', 47, 0.5, ('N', 6, 1.5, ('N', 59, 0.5, ('N', 11, 4.0, ('L', ((5, 3), (7, 2), (17, 1))), ('L', ((0, 1), (14, 4), (17, 1)))), ('L', ((19, 4), (41, 1)))), ('N', 19, 5.5, ('L', ((8, 7),)), ('N', 33, 0.5, ('L', ((5, 1), (8, 9), (13, 3), (14, 4), (32, 1))), ('L', ((11, 2),))))), ('L', ((4, 5),)))), ('N', 37, 0.5, ('L', ((4, 4),)), ('L', ((41, 3), (60, 1))))), ('N', 74, 0.5, ('N', 102, 1.5, ('N', 1, 1.5, ('L', ((15, 1), (61, 4))), ('L', ((61, 5),))), ('L', ((60, 2),))), ('L', ((60, 3),))))), ('N', 0, 13.0, ('N', 89, 0.5, ('N', 104, 0.5, ('N', 26, 0.5, ('N', 12, 10.5, ('N', 84, 0.5, ('N', 25, 0.5, ('L', ((63, 33),)), ('N', 51, 0.5, ('L', ((63, 6),)), ('L', ((22, 1), (63, 1))))), ('L', ((41, 1), (63, 2)))), ('N', 2, 0.5, ('L', ((19, 2),)), ('L', ((63, 4),)))), ('N', 28, 0.5, ('L', ((4, 1), (63, 1))), ('L', ((4, 2),)))), ('L', ((61, 2),))), ('L', ((50, 4), (51, 1)))), ('N', 84, 0.5, ('N', 62, 0.5, ('N', 41, 1.5, ('L', ((8, 2), (63, 1))), ('L', ((7, 2),))), ('N', 7, 5.5, ('L', ((8, 1), (19, 1), (60, 1))), ('N', 77, 0.5, ('L', ((5, 1), (19, 2))), ('L', ((19, 3),))))), ('N', 41, 1.5, ('L', ((63, 3),)), ('N', 41, 2.5, ('N', 57, 1.0, ('L', ((8, 3),)), ('L', ((8, 1), (15, 1)))), ('L', ((8, 2), (32, 1), (41, 2)))))))), ('N', 107, 0.5, ('N', 106, 0.5, ('L', ((65, 16),)), ('L', ((8, 2),))), ('L', ((64, 3),)))), ('L', ((4, 8),)))), ('N', 30, 1.5, ('N', 0, 6.0, ('N', 15, 7.5, ('N', 1, 6.5, ('L', ((21, 2), (65, 1))), ('L', ((21, 10),))), ('N', 40, 0.5, ('L', ((22, 2), (58, 1))), ('N', 64, 0.5, ('L', ((5, 1), (7, 1), (12, 2))), ('N', 92, 1.0, ('N', 78, 1.5, ('N', 15, 8.5, ('L', ((21, 1), (22, 1))), ('L', ((21, 11),))), ('L', ((35, 2),))), ('N', 16, 5.5, ('L', ((21, 1), (51, 1))), ('L', ((44, 2),))))))), ('N', 79, 0.5, ('N', 10, 7.5, ('N', 10, 2.0, ('N', 85, 1.5, ('N', 42, 0.5, ('L', ((21, 2),)), ('N', 60, 1.5, ('L', ((13, 1), (17, 1))), ('L', ((4, 1), (7, 1))))), ('L', ((5, 2),))), ('N', 15, 11.5, ('L', ((8, 1), (21, 3))), ('L', ((21, 8),)))), ('N', 17, 4.5, ('L', ((7, 3),)), ('L', ((17, 2),)))), ('N', 56, 0.5, ('N', 0, 14.5, ('N', 79, 1.5, ('L', ((21, 3),)), ('L', ((19, 2), (21, 1)))), ('L', ((21, 1), (63, 3)))), ('N', 11, 9.5, ('L', ((13, 9),)), ('N', 13, 3.5, ('L', ((13, 4),)), ('L', ((4, 1), (63, 1)))))))), ('N', 1, 8.5, ('N', 0, 11.5, ('N', 34, 3.5, ('N', 8, 7.5, ('N', 10, 4.0, ('N', 13, 2.5, ('L', ((5, 2),)), ('L', ((4, 1), (5, 1)))), ('L', ((0, 2), (5, 1)))), ('N', 83, 0.5, ('L', ((15, 1), (21, 1), (22, 1))), ('L', ((21, 2),)))), ('L', ((19, 2),))), ('N', 16, 9.0, ('L', ((7, 1), (31, 1))), ('L', ((60, 3),)))), ('N', 8, 6.0, ('L', ((0, 2), (9, 1), (11, 1), (13, 1))), ('N', 41, 0.5, ('L', ((0, 1), (7, 2))), ('L', ((7, 6),))))))), ('N', 106, 0.5, ('N', 64, 0.5, ('N', 81, 0.5, ('N', 47, 0.5, ('N', 8, 4.5, ('N', 48, 0.5, ('N', 57, 0.5, ('N', 31, 0.5, ('N', 108, 0.5, ('N', 56, 0.5, ('N', 2, 0.5, ('N', 65, 0.5, ('N', 41, 0.5, ('L', ((2, 2), (3, 1), (10, 4), (11, 1), (12, 2), (15, 1), (17, 1), (20, 1), (29, 5), (32, 2), (35, 1), (62, 2))), ('L', ((17, 3), (18, 3), (59, 1), (61, 1)))), ('N', 17, 13.0, ('L', ((3, 1), (11, 2), (12, 1), (35, 2))), ('L', ((22, 5),)))), ('N', 54, 0.5, ('N', 61, 0.5, ('L', ((3, 2), (10, 13), (17, 2), (35, 1))), ('L', ((18, 2),))), ('L', ((11, 3),)))), ('N', 20, 0.5, ('L', ((13, 2), (20, 1))), ('N', 55, 0.5, ('L', ((13, 6),)), ('L', ((2, 1), (13, 2)))))), ('L', ((65, 7),))), ('N', 1, 9.0, ('N', 29, 0.5, ('L', ((3, 1), (49, 2))), ('L', ((35, 1), (46, 1)))), ('L', ((43, 3),)))), ('N', 75, 0.5, ('N', 33, 0.5, ('L', ((14, 1), (59, 3))), ('N', 41, 0.5, ('N', 13, 1.0, ('L', ((11, 4),)), ('L', ((2, 1), (14, 2)))), ('L', ((11, 3),)))), ('L', ((3, 2),)))), ('N', 15, 2.5, ('L', ((64, 2),)), ('N', 0, 3.5, ('N', 57, 0.5, ('N', 1, 14.0, ('L', ((13, 3),)), ('L', ((6, 1), (9, 1), (13, 1)))), ('L', ((13, 1), (14, 1)))), ('N', 73, 0.5, ('N', 34, 1.5, ('N', 13, 3.5, ('N', 34, 0.5, ('N', 58, 0.5, ('L', ((5, 4),)), ('L', ((5, 1), (15, 2), (19, 1)))), ('N', 8, 1.5, ('L', ((12, 1), (13, 1))), ('L', ((11, 1), (12, 1))))), ('L', ((5, 6),))), ('L', ((5, 1), (13, 3), (51, 1)))), ('N', 11, 11.0, ('L', ((13, 1), (19, 1), (65, 1))), ('L', ((59, 2),))))))), ('N', 84, 0.5, ('N', 37, 0.5, ('N', 34, 1.5, ('N', 4, 0.5, ('N', 102, 0.5, ('N', 108, 1.0, ('N', 17, 6.5, ('N', 48, 0.5, ('L', ((7, 2), (60, 1))), ('L', ((5, 4),))), ('N', 6, 0.5, ('L', ((32, 2),)), ('L', ((5, 1), (7, 1), (8, 1), (11, 2), (12, 1), (14, 4), (15, 4), (17, 2), (19, 1), (22, 2), (61, 1))))), ('L', ((65, 2),))), ('L', ((50, 2), (51, 3)))), ('N', 27, 0.5, ('N', 58, 0.5, ('N', 30, 2.5, ('N', 28, 2.5, ('L', ((7, 6),)), ('L', ((0, 2), (7, 1), (13, 1)))), ('N', 1, 9.5, ('L', ((7, 1), (11, 1))), ('L', ((11, 2),)))), ('N', 40, 0.5, ('L', ((7, 1), (65, 2))), ('L', ((12, 1), (17, 2), (65, 1))))), ('N', 73, 1.0, ('L', ((7, 12),)), ('L', ((65, 2),))))), ('N', 54, 0.5, ('N', 13, 3.0, ('L', ((12, 4),)), ('L', ((12, 1), (22, 2)))), ('L', ((11, 2),)))), ('N', 36, 0.5, ('N', 51, 0.5, ('N', 58, 1.5, ('N', 1, 2.0, ('L', ((15, 3),)), ('N', 75, 1.5, ('N', 61, 1.5, ('L', ((5, 12), (7, 3), (10, 1), (13, 2), (65, 1))), ('L', ((17, 4),))), ('L', ((61, 4),)))), ('N', 42, 0.5, ('L', ((0, 2),)), ('L', ((19, 3),)))), ('N', 79, 1.5, ('N', 35, 0.5, ('L', ((18, 5),)), ('L', ((13, 2),))), ('N', 14, 3.5, ('L', ((7, 1), (65, 1))), ('L', ((8, 4), (11, 1)))))), ('N', 1, 13.5, ('N', 48, 0.5, ('N', 11, 7.5, ('L', ((8, 1), (13, 1), (19, 3))), ('L', ((0, 2),))), ('N', 41, 1.5, ('N', 1, 11.5, ('N', 19, 5.5, ('L', ((5, 2),)), ('L', ((17, 2), (60, 1)))), ('L', ((11, 3),))), ('N', 58, 0.5, ('N', 18, 3.5, ('L', ((8, 1), (61, 1))), ('L', ((8, 4), (14, 1)))), ('N', 51, 0.5, ('L', ((14, 2), (60, 2))), ('L', ((15, 3),)))))), ('N', 1, 14.5, ('L', ((5, 1), (8, 1), (60, 1))), ('N', 16, 5.5, ('L', ((7, 3), (14, 3))), ('N', 6, 1.5, ('L', ((14, 6),)), ('L', ((8, 1), (14, 3))))))))), ('N', 16, 9.5, ('N', 79, 0.5, ('L', ((41, 1), (59, 1))), ('L', ((41, 20),))), ('N', 2, 0.5, ('L', ((8, 1), (61, 1))), ('L', ((7, 1), (11, 1), (41, 2))))))), ('N', 11, 3.5, ('N', 6, 0.5, ('N', 31, 0.5, ('L', ((14, 1), (18, 1), (22, 3))), ('L', ((49, 2),))), ('L', ((4, 3),))), ('N', 0, 3.5, ('L', ((4, 4), (64, 1))), ('N', 7, 5.5, ('L', ((4, 18),)), ('N', 16, 4.5, ('L', ((4, 1), (18, 1))), ('L', ((4, 7),))))))), ('N', 25, 0.5, ('N', 35, 1.5, ('L', ((4, 16),)), ('L', ((41, 2),))), ('L', ((22, 2),)))), ('N', 58, 1.5, ('N', 13, 0.5, ('N', 21, 0.5, ('L', ((22, 2),)), ('N', 32, 1.5, ('L', ((7, 4),)), ('L', ((60, 2),)))), ('N', 25, 0.5, ('N', 24, 0.5, ('N', 40, 0.5, ('N', 41, 0.5, ('L', ((4, 3),)), ('N', 30, 1.5, ('L', ((7, 2),)), ('L', ((11, 2), (21, 1))))), ('N', 43, 0.5, ('N', 17, 6.5, ('N', 11, 4.5, ('L', ((21, 2),)), ('L', ((5, 1), (15, 1)))), ('N', 8, 7.0, ('L', ((5, 2), (61, 1))), ('L', ((11, 2),)))), ('N', 8, 7.5, ('N', 10, 3.5, ('L', ((5, 1), (21, 1))), ('L', ((0, 2),))), ('L', ((0, 2),))))), ('N', 40, 1.5, ('N', 17, 13.5, ('L', ((21, 19),)), ('N', 48, 0.5, ('N', 15, 6.5, ('L', ((21, 2),)), ('L', ((21, 1), (30, 1)))), ('L', ((21, 3),)))), ('N', 77, 1.5, ('N', 7, 5.0, ('N', 28, 1.5, ('N', 20, 0.5, ('L', ((65, 2),)), ('L', ((5, 1), (44, 1)))), ('N', 3, 0.5, ('L', ((4, 1), (13, 2), (21, 1))), ('L', ((21, 3), (51, 1))))), ('L', ((19, 2),))), ('L', ((35, 3),))))), ('N', 55, 1.5, ('N', 27, 0.5, ('N', 1, 6.5, ('L', ((22, 5),)), ('L', ((21, 1), (22, 2)))), ('L', ((21, 1), (22, 1), (58, 1)))), ('L', ((7, 1), (65, 2)))))), ('N', 41, 0.5, ('L', ((4, 1), (7, 1))), ('N', 35, 0.5, ('N', 36, 0.5, ('L', ((17, 1), (21, 1))), ('N', 19, 3.0, ('L', ((19, 2),)), ('N', 102, 0.5, ('L', ((19, 3),)), ('L', ((61, 2),))))), ('L', ((13, 4),)))))), ('N', 71, 0.5, ('N', 14, 1.5, ('N', 84, 1.5, ('N', 18, 3.5, ('N', 30, 1.5, ('N', 79, 0.5, ('L', ((5, 1), (7, 1), (19, 1))), ('L', ((19, 1), (41, 1)))), ('N', 62, 0.5, ('L', ((5, 2), (8, 1))), ('L', ((8, 6),)))), ('L', ((8, 4),))), ('N', 64, 0.5, ('N', 36, 1.0, ('L', ((41, 2), (61, 1))), ('N', 61, 1.0, ('L', ((63, 3),)), ('L', ((8, 1), (15, 1))))), ('L', ((60, 3),)))), ('N', 5, 3.5, ('N', 105, 0.5, ('L', ((5, 1), (63, 1), (65, 4))), ('N', 17, 12.0, ('L', ((62, 5),)), ('L', ((62, 1), (63, 1))))), ('N', 89, 0.5, ('N', 81, 0.5, ('N', 0, 10.5, ('N', 102, 1.5, ('N', 17, 9.5, ('N', 85, 1.0, ('L', ((63, 23),)), ('N', 34, 1.5, ('L', ((22, 1), (63, 1))), ('L', ((63, 3),)))), ('N', 21, 0.5, ('N', 79, 0.5, ('L', ((63, 6),)), ('L', ((41, 1), (63, 1)))), ('L', ((21, 2),)))), ('N', 40, 1.5, ('L', ((63, 2),)), ('L', ((31, 2),)))), ('N', 32, 0.5, ('N', 1, 2.0, ('N', 37, 0.5, ('N', 33, 0.5, ('L', ((19, 2), (63, 1))), ('L', ((8, 2),))), ('N', 42, 0.5, ('L', ((41, 2),)), ('L', ((13, 2),)))), ('L', ((63, 9),))), ('N', 1, 3.5, ('L', ((61, 2),)), ('L', ((60, 3),))))), ('L', ((4, 2),))), ('L', ((51, 2),))))), ('L', ((4, 6),)))), ('N', 47, 0.5, ('N', 51, 0.5, ('N', 62, 0.5, ('N', 105, 0.5, ('N', 106, 1.5, ('N', 84, 0.5, ('N', 5, 4.5, ('N', 108, 1.0, ('N', 97, 0.5, ('N', 8, 3.5, ('N', 65, 0.5, ('N', 57, 0.5, ('N', 23, 0.5, ('L', ((1, 1), (2, 2), (5, 2), (10, 16), (11, 2), (13, 8), (17, 1), (18, 5), (20, 5), (35, 1), (43, 1), (46, 1))), ('L', ((0, 2), (5, 1), (11, 1), (21, 6)))), ('N', 1, 14.0, ('L', ((11, 4), (13, 1), (14, 10), (29, 2), (35, 2))), ('L', ((9, 4),)))), ('N', 56, 0.5, ('N', 42, 0.5, ('L', ((22, 4),)), ('L', ((5, 1), (21, 1)))), ('L', ((22, 7),)))), ('N', 85, 0.5, ('N', 30, 0.5, ('L', ((3, 3),)), ('N', 40, 0.5, ('L', ((32, 2),)), ('L', ((3, 3), (17, 1))))), ('L', ((3, 1), (11, 1), (49, 1))))), ('N', 92, 0.5, ('N', 22, 1.5, ('N', 33, 0.5, ('L', ((5, 1), (21, 1), (59, 1))), ('L', ((11, 3),))), ('N', 14, 2.5, ('N', 83, 0.5, ('L', ((59, 4),)), ('L', ((22, 1), (59, 3)))), ('L', ((59, 1), (61, 1))))), ('L', ((49, 4),)))), ('N', 0, 5.0, ('L', ((65, 5),)), ('L', ((64, 1), (65, 1))))), ('N', 29, 0.5, ('N', 85, 0.5, ('N', 64, 0.5, ('N', 2, 0.5, ('N', 50, 0.5, ('N', 87, 0.5, ('L', ((32, 1), (50, 1), (60, 3))), ('L', ((50, 4),))), ('N', 106, 0.5, ('L', ((5, 5), (7, 2), (11, 1), (12, 5), (13, 3), (14, 3), (15, 3), (17, 2), (22, 2), (32, 1), (60, 4), (61, 7))), ('L', ((31, 5), (50, 1), (51, 2), (63, 1))))), ('N', 50, 0.5, ('L', ((5, 3),)), ('N', 28, 2.5, ('L', ((5, 7), (7, 25), (11, 4), (12, 6), (13, 1), (14, 4), (16, 2), (17, 1))), ('L', ((0, 6), (5, 2), (7, 7), (14, 4)))))), ('N', 35, 0.5, ('N', 24, 0.5, ('N', 34, 0.5, ('L', ((0, 2), (5, 2), (7, 1), (11, 1), (21, 9), (22, 1), (61, 2))), ('L', ((22, 2),))), ('L', ((21, 7),))), ('N', 77, 0.5, ('L', ((12, 1), (13, 2))), ('L', ((7, 2),))))), ('N', 32, 1.5, ('N', 27, 0.5, ('L', ((5, 1), (21, 1), (51, 1))), ('L', ((5, 7),))), ('L', ((10, 1), (61, 1))))), ('N', 108, 0.5, ('N', 54, 0.5, ('N', 34, 0.5, ('N', 39, 0.5, ('L', ((7, 2),)), ('N', 8, 6.5, ('L', ((5, 1), (63, 1))), ('L', ((60, 2),)))), ('L', ((12, 2),))), ('N', 64, 0.5, ('L', ((11, 7),)), ('L', ((7, 1), (60, 1))))), ('L', ((65, 14),))))), ('N', 32, 0.5, ('L', ((41, 12),)), ('N', 55, 0.5, ('L', ((41, 2),)), ('L', ((7, 2), (61, 1)))))), ('N', 84, 1.0, ('N', 24, 1.5, ('N', 18, 4.0, ('L', ((7, 1), (63, 2))), ('L', ((63, 9),))), ('N', 29, 0.5, ('L', ((63, 5),)), ('L', ((64, 1), (65, 2))))), ('L', ((41, 2),)))), ('N', 3, 0.5, ('L', ((62, 14),)), ('L', ((62, 1), (63, 1))))), ('N', 96, 1.5, ('N', 85, 0.5, ('N', 32, 1.5, ('N', 42, 1.5, ('N', 98, 0.5, ('N', 2, 0.5, ('N', 56, 1.0, ('L', ((19, 7),)), ('L', ((5, 1), (19, 3)))), ('L', ((19, 1), (41, 1)))), ('L', ((19, 2), (61, 1)))), ('L', ((18, 1), (19, 2)))), ('N', 37, 0.5, ('L', ((5, 1), (63, 3))), ('L', ((41, 1), (65, 1))))), ('N', 37, 2.5, ('N', 74, 0.5, ('N', 12, 7.0, ('N', 50, 0.5, ('L', ((5, 1), (32, 1))), ('L', ((17, 4),))), ('L', ((41, 2),))), ('L', ((60, 2),))), ('L', ((39, 3),)))), ('N', 58, 0.5, ('L', ((13, 3), (60, 1))), ('L', ((21, 1), (60, 2)))))), ('N', 106, 0.5, ('N', 8, 9.0, ('N', 73, 0.5, ('N', 96, 0.5, ('N', 58, 0.5, ('N', 27, 0.5, ('N', 33, 0.5, ('L', ((8, 8),)), ('L', ((5, 1), (8, 2)))), ('N', 12, 6.0, ('L', ((8, 2),)), ('N', 34, 2.5, ('L', ((5, 1), (17, 1))), ('N', 1, 5.0, ('L', ((14, 1), (16, 1))), ('L', ((8, 1), (21, 1))))))), ('N', 23, 0.5, ('L', ((5, 1), (8, 1), (19, 1))), ('L', ((21, 2),)))), ('N', 57, 1.5, ('L', ((61, 3),)), ('L', ((8, 1), (15, 1))))), ('L', ((19, 1), (61, 2)))), ('N', 57, 0.5, ('N', 4, 0.5, ('N', 79, 1.5, ('N', 11, 3.5, ('N', 13, 3.5, ('L', ((13, 1), (21, 1))), ('L', ((8, 3),))), ('N', 61, 0.5, ('L', ((12, 1), (22, 1), (65, 1))), ('L', ((15, 1), (51, 1))))), ('N', 34, 1.5, ('N', 69, 1.0, ('L', ((7, 5),)), ('L', ((41, 2),))), ('L', ((41, 2),)))), ('N', 16, 10.5, ('L', ((7, 9),)), ('L', ((16, 2),)))), ('N', 30, 2.0, ('N', 23, 0.5, ('N', 15, 11.5, ('N', 13, 2.5, ('L', ((11, 2), (14, 2))), ('L', ((14, 2),))), ('L', ((15, 2),))), ('L', ((21, 3),))), ('L', ((8, 2),))))), ('N', 0, 12.5, ('N', 21, 0.5, ('L', ((63, 23),)), ('L', ((21, 1), (63, 1)))), ('N', 57, 0.5, ('N', 0, 15.0, ('N', 84, 0.5, ('L', ((19, 4),)), ('L', ((8, 2), (41, 1)))), ('N', 106, 1.5, ('N', 33, 0.5, ('L', ((8, 2), (61, 1))), ('L', ((8, 3),))), ('L', ((8, 2),)))), ('N', 12, 7.5, ('N', 73, 1.0, ('N', 2, 0.5, ('L', ((8, 1), (32, 1))), ('N', 30, 1.5, ('L', ((5, 2), (8, 1), (41, 2))), ('L', ((8, 2),)))), ('L', ((65, 2),))), ('N', 83, 1.5, ('L', ((13, 1), (63, 1))), ('L', ((63, 3),)))))))), ('N', 17, 8.5, ('L', ((4, 39),)), ('N', 46, 0.5, ('N', 96, 0.5, ('N', 7, 5.0, ('L', ((4, 9),)), ('N', 2, 0.5, ('L', ((4, 2),)), ('L', ((18, 2),)))), ('N', 83, 0.5, ('N', 24, 1.5, ('L', ((4, 2),)), ('L', ((17, 2), (63, 1), (64, 1)))), ('L', ((41, 3),)))), ('N', 57, 0.5, ('N', 81, 1.0, ('L', ((18, 1), (22, 1), (49, 1))), ('L', ((22, 2),))), ('L', ((21, 3),)))))), ('N', 108, 0.5, ('N', 48, 0.5, ('N', 12, 4.5, ('N', 26, 0.5, ('N', 106, 0.5, ('N', 73, 0.5, ('N', 22, 2.5, ('N', 64, 0.5, ('N', 14, 0.5, ('L', ((1, 2), (2, 4), (11, 1), (14, 4), (49, 1))), ('N', 39, 0.5, ('N', 1, 17.0, ('N', 11, 3.0, ('L', ((11, 2),)), ('L', ((8, 2),))), ('L', ((7, 1), (8, 1)))), ('L', ((10, 3), (46, 1))))), ('N', 24, 1.5, ('N', 56, 0.5, ('N', 15, 8.5, ('L', ((21, 1), (22, 1))), ('L', ((21, 3),))), ('L', ((22, 6),))), ('N', 79, 0.5, ('L', ((21, 7),)), ('L', ((21, 3), (44, 1)))))), ('N', 35, 0.5, ('N', 30, 0.5, ('N', 2, 0.5, ('L', ((10, 3),)), ('L', ((9, 1), (10, 3)))), ('N', 79, 1.0, ('L', ((7, 1), (17, 1), (18, 1))), ('L', ((14, 2), (22, 1))))), ('L', ((13, 3),)))), ('N', 17, 14.5, ('N', 35, 0.5, ('L', ((29, 2), (59, 1))), ('L', ((29, 1), (30, 2)))), ('L', ((20, 3),)))), ('N', 85, 0.5, ('N', 42, 0.5, ('L', ((62, 3), (63, 1))), ('L', ((63, 8),))), ('L', ((32, 2),)))), ('N', 14, 3.5, ('L', ((4, 5),)), ('N', 13, 4.5, ('L', ((14, 1), (22, 1), (63, 1))), ('L', ((4, 2),))))), ('N', 105, 0.5, ('N', 5, 4.5, ('N', 17, 10.0, ('N', 26, 0.5, ('L', ((10, 2), (11, 1))), ('N', 16, 8.5, ('L', ((3, 5),)), ('L', ((3, 1), (22, 1))))), ('N', 75, 1.0, ('N', 25, 0.5, ('N', 15, 5.5, ('N', 41, 0.5, ('L', ((10, 4),)), ('L', ((18, 3),))), ('N', 96, 0.5, ('N', 24, 0.5, ('L', ((11, 3),)), ('N', 85, 0.5, ('N', 64, 0.5, ('L', ((10, 1), (11, 1), (12, 1), (13, 2), (14, 2), (17, 2), (49, 1), (61, 2))), ('L', ((21, 2),))), ('L', ((35, 2),)))), ('N', 33, 0.5, ('L', ((2, 2),)), ('L', ((2, 1), (49, 1)))))), ('N', 33, 1.5, ('N', 64, 1.0, ('L', ((22, 6),)), ('L', ((21, 1), (58, 1)))), ('L', ((4, 1), (10, 1), (11, 2), (63, 2))))), ('L', ((32, 4), (49, 1))))), ('N', 75, 0.5, ('N', 61, 0.5, ('N', 84, 0.5, ('N', 47, 0.5, ('N', 17, 10.5, ('N', 8, 6.5, ('N', 1, 4.5, ('L', ((12, 2), (15, 1))), ('L', ((8, 1), (21, 1)))), ('N', 10, 6.5, ('N', 11, 11.5, ('L', ((0, 2), (7, 32), (11, 1), (13, 1), (14, 2), (19, 1), (63, 1))), ('L', ((63, 2),))), ('N', 3, 0.5, ('L', ((11, 1), (21, 1))), ('L', ((8, 3),))))), ('N', 39, 0.5, ('N', 15, 3.5, ('L', ((17, 3),)), ('N', 13, 1.5, ('L', ((60, 1), (63, 1))), ('L', ((14, 2),)))), ('L', ((12, 2),)))), ('L', ((4, 4),))), ('N', 17, 5.5, ('L', ((7, 1), (8, 1), (61, 1))), ('L', ((41, 5),)))), ('N', 62, 0.5, ('N', 56, 0.5, ('N', 33, 0.5, ('N', 6, 1.5, ('L', ((16, 2),)), ('L', ((15, 1), (16, 3)))), ('L', ((11, 3), (17, 1)))), ('L', ((13, 3),))), ('N', 22, 1.5, ('N', 6, 1.5, ('L', ((19, 1), (41, 2))), ('L', ((8, 1), (19, 1)))), ('L', ((19, 2),))))), ('N', 104, 0.5, ('L', ((17, 4), (31, 1))), ('N', 17, 5.5, ('L', ((60, 5),)), ('N', 14, 3.5, ('N', 75, 1.5, ('L', ((59, 2),)), ('N', 30, 1.5, ('L', ((60, 2),)), ('L', ((7, 1), (50, 1))))), ('L', ((61, 3),))))))), ('L', ((62, 8),)))), ('N', 51, 0.5, ('N', 84, 0.5, ('N', 38, 2.5, ('N', 58, 1.5, ('N', 47, 0.5, ('N', 28, 1.5, ('N', 57, 0.5, ('N', 38, 0.5, ('N', 15, 4.5, ('N', 35, 0.5, ('L', ((10, 2), (60, 1))), ('L', ((18, 2),))), ('L', ((63, 14),))), ('N', 15, 14.0, ('N', 42, 1.5, ('N', 42, 0.5, ('L', ((5, 2), (13, 1), (15, 3), (21, 2), (60, 1), (62, 2), (63, 2))), ('L', ((31, 2),))), ('N', 32, 0.5, ('L', ((11, 2), (12, 1))), ('L', ((5, 2), (11, 2))))), ('L', ((12, 4),)))), ('N', 0, 1.5, ('L', ((11, 1), (14, 2), (21, 3))), ('N', 61, 0.5, ('L', ((14, 1), (61, 1))), ('L', ((14, 4),))))), ('N', 75, 0.5, ('N', 40, 0.5, ('N', 38, 0.5, ('L', ((12, 1), (18, 4))), ('N', 23, 0.5, ('N', 17, 8.0, ('L', ((5, 6), (63, 2))), ('L', ((7, 1), (14, 2), (19, 1), (63, 2)))), ('N', 27, 0.5, ('L', ((21, 3),)), ('L', ((7, 3),))))), ('N', 1, 9.0, ('N', 11, 10.5, ('N', 58, 0.5, ('L', ((5, 14),)), ('L', ((5, 1), (60, 1)))), ('L', ((12, 1), (13, 1)))), ('N', 60, 1.0, ('N', 79, 1.0, ('L', ((5, 1), (51, 1))), ('L', ((10, 3),))), ('L', ((17, 2),))))), ('N', 79, 1.5, ('N', 30, 2.5, ('N', 27, 1.5, ('N', 73, 1.5, ('L', ((19, 2), (31, 1), (32, 2), (59, 1), (60, 1))), ('L', ((50, 2),))), ('L', ((5, 2),))), ('N', 43, 0.5, ('L', ((61, 2),)), ('L', ((0, 3),)))), ('L', ((21, 4), (60, 1)))))), ('N', 49, 0.5, ('N', 18, 4.0, ('L', ((4, 1), (18, 1))), ('L', ((4, 12),))), ('L', ((17, 1), (63, 1))))), ('N', 63, 0.5, ('N', 39, 0.5, ('L', ((5, 7),)), ('L', ((5, 1), (59, 1)))), ('L', ((11, 1), (12, 1))))), ('N', 62, 0.5, ('N', 89, 0.5, ('N', 33, 0.5, ('N', 31, 0.5, ('N', 36, 0.5, ('N', 56, 0.5, ('L', ((4, 1), (9, 1), (63, 1))), ('N', 58, 1.0, ('L', ((13, 2),)), ('L', ((13, 2), (63, 1))))), ('L', ((13, 2),))), ('L', ((5, 1), (21, 3)))), ('N', 19, 5.0, ('L', ((21, 2),)), ('L', ((11, 2),)))), ('L', ((51, 3),))), ('L', ((61, 2),)))), ('N', 17, 5.5, ('L', ((17, 1), (60, 2))), ('L', ((41, 13),)))), ('N', 23, 0.5, ('N', 26, 0.5, ('N', 12, 4.5, ('N', 32, 1.5, ('N', 14, 3.5, ('L', ((8, 5),)), ('N', 17, 9.5, ('N', 58, 0.5, ('N', 8, 9.0, ('L', ((8, 4),)), ('L', ((0, 1), (8, 2)))), ('L', ((15, 2),))), ('L', ((11, 1), (41, 2))))), ('N', 55, 1.5, ('N', 38, 0.5, ('L', ((8, 1), (14, 1), (22, 1))), ('L', ((15, 2), (63, 1)))), ('L', ((15, 2),)))), ('N', 98, 0.5, ('N', 7, 5.5, ('N', 15, 8.5, ('N', 9, 1.0, ('L', ((7, 4), (13, 2), (14, 1))), ('N', 60, 0.5, ('N', 0, 10.5, ('N', 54, 0.5, ('L', ((5, 1), (8, 2), (13, 2), (14, 1), (18, 2), (41, 1))), ('L', ((11, 2),))), ('L', ((51, 2),))), ('L', ((17, 2),)))), ('N', 0, 5.0, ('L', ((12, 3), (22, 1))), ('N', 79, 1.0, ('N', 12, 8.5, ('L', ((8, 2), (15, 1), (16, 1))), ('L', ((15, 2),))), ('N', 17, 8.5, ('N', 37, 1.5, ('L', ((8, 1), (63, 2))), ('L', ((8, 7),))), ('L', ((63, 3),)))))), ('N', 37, 1.5, ('N', 42, 1.5, ('L', ((19, 3),)), ('N', 28, 2.5, ('L', ((19, 2),)), ('L', ((5, 3), (41, 1))))), ('N', 13, 3.5, ('N', 39, 0.5, ('L', ((13, 6), (32, 1))), ('L', ((5, 3), (8, 1)))), ('L', ((63, 3),))))), ('N', 56, 0.5, ('L', ((51, 1), (61, 3))), ('L', ((61, 3),))))), ('L', ((4, 16),))), ('N', 74, 1.5, ('N', 2, 0.5, ('N', 37, 2.0, ('L', ((5, 1), (21, 1))), ('L', ((21, 2),))), ('L', ((21, 14),))), ('L', ((5, 1), (19, 1))))))), ('N', 33, 0.5, ('N', 15, 4.5, ('L', ((64, 1), (65, 2))), ('L', ((65, 17),))), ('N', 16, 3.0, ('L', ((8, 2),)), ('N', 81, 0.5, ('N', 34, 1.5, ('L', ((63, 4),)), ('L', ((65, 2),))), ('L', ((4, 3),)))))), ('N', 108, 0.5, ('N', 64, 0.5, ('N', 47, 0.5, ('N', 7, 1.5, ('N', 106, 0.5, ('N', 57, 0.5, ('N', 56, 0.5, ('N', 24, 1.5, ('N', 50, 0.5, ('N', 15, 3.5, ('N', 9, 1.5, ('N', 61, 0.5, ('L', ((10, 3),)), ('L', ((18, 2),))), ('L', ((3, 4),))), ('N', 102, 0.5, ('N', 11, 7.0, ('N', 14, 4.0, ('L', ((9, 1), (10, 1), (12, 1), (17, 1), (18, 1))), ('L', ((32, 2), (51, 1)))), ('N', 73, 0.5, ('L', ((5, 5), (60, 1))), ('L', ((49, 1), (62, 1))))), ('N', 77, 0.5, ('N', 85, 0.5, ('L', ((3, 1), (49, 2), (50, 1), (59, 2))), ('L', ((35, 3),))), ('L', ((2, 2),))))), ('N', 60, 0.5, ('N', 48, 0.5, ('N', 55, 0.5, ('N', 33, 1.0, ('L', ((0, 1), (7, 15), (41, 1), (60, 1))), ('L', ((11, 3),))), ('N', 32, 0.5, ('L', ((7, 6),)), ('L', ((7, 2), (12, 1))))), ('N', 20, 0.5, ('N', 17, 9.5, ('L', ((5, 8), (61, 1))), ('L', ((18, 2),))), ('N', 14, 2.5, ('L', ((22, 2),)), ('L', ((32, 2),))))), ('N', 22, 1.5, ('N', 19, 4.5, ('N', 59, 0.5, ('L', ((17, 2),)), ('L', ((11, 1), (17, 1)))), ('N', 16, 5.5, ('L', ((19, 2),)), ('L', ((5, 1), (17, 1))))), ('N', 59, 0.5, ('N', 9, 2.5, ('L', ((12, 2), (15, 1))), ('L', ((12, 2),))), ('L', ((0, 1), (5, 1), (7, 1))))))), ('N', 17, 11.5, ('N', 84, 0.5, ('N', 54, 0.5, ('N', 75, 1.0, ('N', 3, 0.5, ('L', ((17, 3), (18, 2))), ('L', ((0, 1), (3, 3), (5, 1), (8, 2), (10, 3), (12, 1), (22, 2), (35, 1)))), ('L', ((50, 3),))), ('N', 9, 4.5, ('N', 38, 0.5, ('L', ((11, 3), (61, 1))), ('L', ((11, 4),))), ('L', ((3, 2), (11, 1))))), ('L', ((41, 5),))), ('N', 1, 4.5, ('N', 25, 0.5, ('N', 42, 0.5, ('N', 38, 0.5, ('L', ((18, 1), (20, 1))), ('L', ((12, 3), (15, 1)))), ('L', ((12, 1), (29, 1)))), ('L', ((22, 4),))), ('N', 48, 0.5, ('L', ((10, 8),)), ('L', ((7, 2),)))))), ('N', 33, 0.5, ('N', 24, 1.5, ('N', 15, 4.5, ('L', ((13, 4),)), ('N', 44, 0.5, ('N', 17, 12.5, ('N', 1, 9.5, ('L', ((12, 2), (13, 1), (19, 2), (41, 2), (59, 1))), ('L', ((7, 4), (13, 1), (43, 1)))), ('N', 15, 6.5, ('L', ((2, 1), (20, 1))), ('L', ((2, 2),)))), ('L', ((1, 3),)))), ('N', 41, 0.5, ('L', ((13, 3),)), ('N', 1, 11.0, ('L', ((13, 1), (18, 1))), ('L', ((13, 3),))))), ('L', ((13, 1), (22, 5), (49, 1))))), ('N', 33, 0.5, ('N', 17, 7.0, ('N', 0, 7.5, ('L', ((0, 4), (12, 1), (14, 1))), ('N', 37, 0.5, ('N', 1, 7.5, ('L', ((5, 1), (7, 1))), ('L', ((7, 3),))), ('N', 4, 0.5, ('L', ((8, 2),)), ('L', ((14, 1), (17, 1), (41, 1)))))), ('N', 60, 1.5, ('N', 42, 1.5, ('N', 98, 1.0, ('N', 60, 0.5, ('N', 17, 14.5, ('L', ((14, 19),)), ('L', ((14, 3), (59, 1)))), ('N', 15, 5.5, ('L', ((13, 1), (14, 2))), ('L', ((14, 1), (29, 1))))), ('L', ((49, 1), (60, 1)))), ('L', ((7, 1), (9, 2)))), ('N', 15, 7.5, ('L', ((17, 3),)), ('L', ((15, 2), (41, 1)))))), ('N', 54, 0.5, ('N', 56, 0.5, ('L', ((14, 6),)), ('L', ((12, 2), (41, 1)))), ('N', 13, 2.5, ('L', ((11, 8),)), ('N', 17, 7.5, ('N', 51, 0.5, ('L', ((7, 1), (17, 1))), ('L', ((11, 2),))), ('L', ((22, 1), (41, 2)))))))), ('N', 87, 0.5, ('N', 96, 1.5, ('N', 105, 0.5, ('N', 34, 1.5, ('N', 80, 0.5, ('N', 11, 10.5, ('N', 57, 0.5, ('L', ((63, 16),)), ('L', ((60, 1), (63, 4)))), ('N', 79, 1.5, ('L', ((63, 3),)), ('L', ((41, 2),)))), ('L', ((3, 2),))), ('L', ((7, 1), (8, 1), (39, 1)))), ('N', 3, 0.5, ('L', ((62, 5),)), ('L', ((63, 2),)))), ('L', ((31, 2),))), ('L', ((50, 3),)))), ('N', 38, 1.5, ('N', 96, 0.5, ('N', 35, 0.5, ('N', 106, 0.5, ('N', 69, 1.0, ('N', 7, 5.0, ('N', 51, 0.5, ('N', 3, 0.5, ('L', ((11, 2), (17, 1))), ('L', ((10, 2),))), ('N', 13, 3.5, ('L', ((8, 1), (11, 1), (51, 1))), ('N', 40, 1.5, ('L', ((8, 3),)), ('L', ((8, 2), (15, 1)))))), ('N', 28, 2.5, ('N', 48, 0.5, ('L', ((8, 1), (12, 1))), ('N', 10, 0.5, ('L', ((5, 1), (8, 1))), ('L', ((5, 4), (19, 1))))), ('N', 79, 0.5, ('N', 1, 2.5, ('L', ((5, 1), (19, 1))), ('L', ((14, 1), (19, 1)))), ('L', ((41, 3),))))), ('L', ((19, 3),))), ('N', 18, 1.5, ('L', ((8, 2),)), ('N', 8, 4.0, ('L', ((19, 1), (33, 1), (63, 1))), ('N', 6, 1.5, ('L', ((41, 2), (63, 5))), ('L', ((63, 14),)))))), ('N', 84, 0.5, ('N', 0, 9.0, ('N', 57, 1.5, ('L', ((13, 6),)), ('L', ((13, 3), (32, 1)))), ('N', 24, 0.5, ('L', ((5, 2), (8, 1))), ('N', 59, 0.5, ('L', ((8, 2),)), ('L', ((16, 3),))))), ('N', 69, 1.0, ('L', ((41, 3),)), ('L', ((32, 2),))))), ('N', 7, 3.5, ('N', 13, 4.5, ('N', 38, 0.5, ('L', ((8, 3),)), ('L', ((15, 5),))), ('N', 32, 2.5, ('L', ((31, 2),)), ('L', ((60, 2),)))), ('N', 61, 0.5, ('N', 79, 1.0, ('L', ((7, 1), (60, 1))), ('L', ((60, 2),))), ('N', 34, 3.5, ('N', 83, 1.5, ('L', ((61, 1), (63, 1))), ('L', ((63, 2),))), ('L', ((61, 3),)))))), ('N', 106, 0.5, ('N', 42, 0.5, ('L', ((5, 6),)), ('L', ((5, 1), (8, 1)))), ('L', ((15, 1), (19, 1), (61, 1)))))), ('N', 50, 0.5, ('N', 92, 0.5, ('N', 65, 0.5, ('N', 35, 0.5, ('N', 41, 1.5, ('L', ((4, 5),)), ('L', ((14, 2),))), ('L', ((17, 2), (63, 3)))), ('L', ((22, 4),))), ('L', ((49, 4),))), ('L', ((4, 40),)))), ('N', 11, 5.5, ('N', 18, 1.5, ('L', ((5, 1), (8, 3))), ('N', 104, 0.5, ('N', 73, 0.5, ('N', 16, 5.5, ('N', 24, 0.5, ('N', 14, 3.5, ('L', ((11, 1), (21, 1))), ('L', ((11, 1), (21, 3)))), ('L', ((21, 16),))), ('N', 11, 2.5, ('N', 79, 0.5, ('L', ((21, 8),)), ('L', ((21, 3), (63, 1)))), ('N', 15, 8.5, ('L', ((22, 3), (31, 1))), ('L', ((4, 1), (13, 1), (21, 4)))))), ('L', ((22, 2), (30, 2)))), ('N', 37, 2.0, ('N', 11, 4.5, ('N', 7, 6.5, ('L', ((5, 1), (7, 1))), ('L', ((0, 1), (61, 1)))), ('L', ((21, 3),))), ('L', ((60, 4),))))), ('N', 100, 0.5, ('N', 13, 3.5, ('N', 58, 1.5, ('N', 34, 2.5, ('N', 33, 0.5, ('N', 17, 8.5, ('N', 48, 0.5, ('L', ((22, 2),)), ('L', ((21, 1), (22, 1)))), ('L', ((21, 3),))), ('N', 0, 5.0, ('L', ((11, 2), (22, 1), (58, 1))), ('N', 32, 0.5, ('L', ((7, 3),)), ('L', ((5, 1), (7, 1)))))), ('N', 33, 0.5, ('L', ((15, 2),)), ('N', 58, 0.5, ('L', ((12, 2),)), ('L', ((19, 2),))))), ('N', 74, 0.5, ('L', ((13, 2), (19, 1))), ('N', 56, 0.5, ('L', ((17, 2),)), ('L', ((13, 3),))))), ('N', 16, 7.5, ('L', ((21, 5),)), ('L', ((21, 2), (59, 1))))), ('L', ((4, 5),))))), ('N', 107, 0.5, ('N', 36, 0.5, ('N', 1, 3.0, ('L', ((8, 1), (65, 1))), ('L', ((65, 21),))), ('N', 41, 0.5, ('L', ((4, 1), (63, 2))), ('L', ((65, 3),)))), ('L', ((64, 3),)))), ('N', 108, 0.5, ('N', 81, 0.5, ('N', 106, 0.5, ('N', 47, 0.5, ('N', 104, 1.5, ('N', 35, 0.5, ('N', 33, 0.5, ('N', 26, 0.5, ('N', 23, 0.5, ('N', 0, 1.5, ('N', 1, 4.5, ('L', ((10, 3), (49, 1))), ('L', ((10, 5),))), ('N', 0, 7.5, ('N', 60, 0.5, ('N', 61, 0.5, ('L', ((0, 5), (2, 1), (5, 9), (6, 1), (7, 12), (8, 4), (9, 1), (10, 5), (12, 2), (14, 5), (19, 2), (22, 5), (32, 3), (35, 1), (49, 1), (62, 2))), ('L', ((18, 6),))), ('N', 78, 0.5, ('L', ((5, 4), (8, 1), (12, 1), (15, 1), (17, 17), (18, 1), (19, 1), (41, 1), (49, 2), (51, 1), (60, 2))), ('L', ((2, 2), (12, 3))))), ('N', 3, 0.5, ('N', 8, 6.0, ('L', ((5, 7), (12, 2), (15, 3), (19, 3))), ('L', ((7, 1), (8, 1), (15, 8), (16, 2), (60, 2)))), ('N', 10, 6.5, ('L', ((5, 1), (7, 10), (8, 1), (10, 2), (51, 1), (61, 1))), ('L', ((5, 1), (8, 5), (12, 3), (60, 2))))))), ('N', 4, 0.5, ('N', 22, 1.5, ('N', 10, 4.0, ('N', 7, 3.0, ('L', ((21, 9),)), ('L', ((22, 2), (61, 1)))), ('L', ((17, 2),))), ('N', 15, 9.0, ('N', 73, 0.5, ('L', ((17, 1), (21, 1))), ('L', ((22, 1), (59, 1)))), ('L', ((5, 3), (35, 1))))), ('L', ((21, 6),)))), ('N', 11, 2.5, ('L', ((18, 2),)), ('N', 12, 10.5, ('L', ((3, 9),)), ('N', 27, 0.5, ('L', ((17, 1), (49, 1))), ('L', ((3, 2),)))))), ('N', 54, 0.5, ('N', 60, 0.5, ('N', 79, 0.5, ('N', 11, 4.5, ('L', ((14, 2),)), ('L', ((7, 1), (14, 1)))), ('L', ((35, 1), (41, 2)))), ('N', 40, 1.5, ('L', ((12, 1), (17, 2))), ('L', ((17, 2),)))), ('N', 36, 0.5, ('N', 16, 3.5, ('N', 13, 3.5, ('L', ((12, 1), (21, 1))), ('L', ((5, 1), (7, 1)))), ('N', 23, 0.5, ('N', 37, 2.5, ('N', 34, 0.5, ('L', ((5, 1), (11, 7), (41, 2))), ('L', ((11, 13),))), ('L', ((11, 1), (41, 2)))), ('L', ((7, 2),)))), ('N', 30, 1.5, ('N', 15, 12.5, ('N', 28, 2.5, ('N', 60, 0.5, ('L', ((11, 4), (22, 3), (58, 1))), ('L', ((17, 2),))), ('L', ((7, 1), (41, 2)))), ('N', 50, 0.5, ('L', ((5, 1), (41, 1))), ('N', 17, 5.5, ('L', ((8, 5),)), ('L', ((8, 3), (15, 1)))))), ('N', 40, 0.5, ('L', ((11, 1), (19, 1), (60, 1))), ('N', 48, 0.5, ('L', ((7, 1), (11, 1))), ('L', ((5, 5),)))))))), ('N', 64, 0.5, ('N', 43, 0.5, ('N', 98, 0.5, ('N', 74, 0.5, ('N', 13, 2.5, ('N', 5, 1.5, ('L', ((1, 2),)), ('N', 38, 1.5, ('L', ((2, 1), (5, 1), (11, 3), (13, 3), (14, 8), (19, 1), (20, 2), (46, 1))), ('L', ((13, 2),)))), ('N', 35, 1.5, ('N', 42, 0.5, ('L', ((7, 2), (13, 2), (22, 1))), ('L', ((8, 1), (13, 8)))), ('N', 57, 0.5, ('L', ((13, 1), (22, 1))), ('L', ((13, 1), (14, 3)))))), ('N', 7, 4.5, ('L', ((13, 1), (61, 1))), ('L', ((5, 3), (17, 3))))), ('N', 15, 10.0, ('L', ((49, 3), (60, 1))), ('L', ((61, 4),)))), ('N', 75, 1.0, ('N', 52, 0.5, ('N', 4, 0.5, ('L', ((5, 1), (12, 1))), ('L', ((12, 3), (41, 1)))), ('L', ((0, 3),))), ('L', ((43, 2),)))), ('N', 24, 1.5, ('N', 14, 2.0, ('L', ((22, 8),)), ('N', 34, 2.5, ('N', 96, 0.5, ('N', 7, 5.0, ('L', ((8, 1), (11, 1))), ('L', ((5, 1), (13, 1)))), ('N', 1, 2.0, ('L', ((5, 3),)), ('L', ((7, 2),)))), ('L', ((15, 2),)))), ('N', 9, 1.5, ('L', ((21, 9),)), ('N', 62, 0.5, ('N', 85, 1.0, ('L', ((12, 2),)), ('L', ((21, 1), (51, 1)))), ('L', ((19, 3),))))))), ('N', 22, 0.5, ('N', 0, 10.5, ('L', ((7, 1), (60, 2))), ('L', ((0, 6), (61, 1)))), ('N', 23, 0.5, ('N', 97, 0.5, ('N', 32, 1.5, ('N', 102, 0.5, ('L', ((41, 1), (61, 1))), ('L', ((50, 1), (61, 1)))), ('L', ((61, 9),))), ('N', 37, 0.5, ('L', ((61, 2),)), ('L', ((35, 2),)))), ('N', 13, 3.5, ('L', ((22, 2),)), ('L', ((13, 1), (21, 3))))))), ('N', 17, 12.5, ('N', 18, 3.5, ('N', 28, 2.5, ('L', ((4, 4),)), ('L', ((4, 1), (18, 2)))), ('N', 60, 0.5, ('L', ((4, 23),)), ('N', 0, 3.5, ('L', ((4, 1), (17, 2))), ('L', ((4, 8),))))), ('N', 8, 3.0, ('L', ((4, 2),)), ('L', ((14, 2), (21, 1), (22, 1)))))), ('N', 68, 1.0, ('N', 6, 0.5, ('N', 17, 8.5, ('N', 0, 10.5, ('L', ((5, 1), (32, 1), (33, 1))), ('N', 39, 0.5, ('L', ((5, 1), (60, 1))), ('L', ((5, 2),)))), ('N', 5, 3.0, ('N', 9, 1.5, ('L', ((62, 2), (63, 1))), ('L', ((62, 4),))), ('N', 46, 0.5, ('L', ((31, 2),)), ('L', ((3, 2), (22, 1)))))), ('N', 61, 1.5, ('N', 93, 0.5, ('N', 79, 1.5, ('N', 84, 0.5, ('N', 10, 1.0, ('N', 17, 6.5, ('L', ((7, 1), (63, 1))), ('N', 33, 0.5, ('L', ((63, 7),)), ('N', 15, 5.5, ('L', ((4, 1), (63, 1))), ('L', ((63, 3),))))), ('L', ((8, 1), (19, 2), (63, 2)))), ('N', 30, 1.5, ('L', ((21, 1), (41, 1))), ('L', ((8, 2),)))), ('N', 9, 1.5, ('L', ((41, 1), (63, 1))), ('N', 24, 0.5, ('N', 58, 1.0, ('L', ((22, 1), (63, 1))), ('L', ((63, 3),))), ('L', ((63, 19),))))), ('L', ((50, 2),))), ('N', 32, 1.5, ('N', 79, 1.5, ('N', 62, 0.5, ('L', ((63, 2),)), ('N', 11, 7.0, ('L', ((8, 3), (19, 1))), ('L', ((19, 3),)))), ('N', 27, 2.5, ('N', 34, 0.5, ('L', ((13, 2), (51, 1))), ('L', ((15, 1), (61, 1)))), ('N', 51, 0.5, ('L', ((60, 2),)), ('L', ((21, 2),))))), ('N', 7, 1.0, ('L', ((4, 1), (63, 1))), ('N', 15, 11.5, ('L', ((63, 4),)), ('L', ((41, 1), (63, 1)))))))), ('L', ((62, 3),)))), ('N', 17, 10.5, ('L', ((4, 27),)), ('L', ((4, 2), (22, 1))))), ('N', 106, 0.5, ('N', 56, 0.5, ('L', ((65, 18),)), ('N', 15, 9.5, ('L', ((64, 1), (65, 1))), ('L', ((65, 3),)))), ('N', 36, 0.5, ('L', ((8, 2), (64, 1))), ('L', ((13, 2), (63, 2)))))), ('N', 8, 9.0, ('N', 64, 0.5, ('N', 26, 0.5, ('N', 108, 0.5, ('N', 28, 0.5, ('N', 65, 0.5, ('N', 45, 0.5, ('N', 36, 0.5, ('N', 31, 0.5, ('N', 98, 1.0, ('N', 22, 2.5, ('N', 27, 1.5, ('N', 39, 0.5, ('L', ((6, 1), (11, 1), (18, 2), (62, 1))), ('L', ((10, 1), (13, 2), (20, 4)))), ('L', ((12, 2),))), ('N', 29, 0.5, ('L', ((10, 3),)), ('N', 35, 0.5, ('L', ((10, 4), (18, 1))), ('L', ((13, 2),))))), ('L', ((63, 2),))), ('N', 102, 0.5, ('L', ((46, 2),)), ('L', ((49, 4),)))), ('N', 34, 0.5, ('N', 22, 0.5, ('L', ((11, 3),)), ('N', 41, 0.5, ('L', ((14, 2),)), ('N', 102, 0.5, ('L', ((14, 3),)), ('L', ((59, 2),))))), ('N', 22, 1.5, ('L', ((14, 2),)), ('L', ((9, 1), (14, 2)))))), ('L', ((2, 6),))), ('N', 24, 1.5, ('L', ((22, 3),)), ('N', 0, 3.0, ('L', ((22, 5),)), ('L', ((22, 1), (62, 1)))))), ('N', 78, 0.5, ('N', 105, 0.5, ('N', 84, 0.5, ('N', 8, 6.5, ('N', 98, 0.5, ('N', 4, 0.5, ('N', 106, 0.5, ('N', 63, 0.5, ('L', ((0, 2), (5, 18), (9, 1), (12, 2), (13, 5), (14, 1), (15, 2), (17, 2), (18, 1), (19, 4), (43, 1))), ('L', ((11, 5),))), ('N', 18, 2.5, ('L', ((5, 2),)), ('L', ((19, 4), (33, 1), (51, 1), (63, 10))))), ('N', 24, 0.5, ('N', 30, 1.0, ('L', ((8, 2), (15, 1))), ('L', ((7, 2),))), ('L', ((10, 5),)))), ('N', 9, 4.0, ('N', 67, 0.5, ('N', 55, 1.5, ('L', ((5, 1), (13, 1), (19, 1), (61, 10), (63, 1))), ('L', ((32, 2),))), ('L', ((63, 3),))), ('L', ((59, 3),)))), ('N', 2, 0.5, ('N', 104, 0.5, ('L', ((31, 3),)), ('N', 75, 0.5, ('L', ((8, 1), (60, 2))), ('L', ((60, 2),)))), ('N', 18, 4.5, ('N', 42, 1.5, ('L', ((8, 4),)), ('L', ((8, 1), (15, 1)))), ('N', 16, 6.5, ('N', 6, 1.5, ('L', ((10, 2), (63, 2))), ('L', ((5, 1), (8, 4), (11, 1), (13, 1), (14, 2), (22, 1), (63, 2)))), ('L', ((16, 3),)))))), ('N', 102, 0.5, ('N', 33, 0.5, ('N', 16, 6.0, ('L', ((41, 5),)), ('L', ((8, 1), (32, 1), (41, 3)))), ('N', 9, 1.5, ('L', ((15, 1), (41, 2))), ('N', 27, 2.5, ('L', ((8, 1), (63, 2))), ('L', ((8, 4),))))), ('L', ((61, 5),)))), ('L', ((62, 7),))), ('N', 102, 1.5, ('L', ((35, 8),)), ('N', 11, 11.0, ('L', ((35, 2),)), ('L', ((12, 3),)))))), ('N', 54, 0.5, ('N', 61, 1.5, ('L', ((65, 9),)), ('L', ((64, 1), (65, 1)))), ('L', ((8, 1), (65, 1))))), ('N', 18, 5.5, ('N', 51, 0.5, ('N', 7, 3.5, ('L', ((3, 1), (4, 1))), ('L', ((4, 3),))), ('L', ((4, 11),))), ('N', 7, 3.0, ('N', 2, 0.5, ('N', 38, 1.5, ('N', 29, 0.5, ('N', 17, 8.5, ('L', ((3, 2),)), ('N', 60, 0.5, ('N', 73, 1.0, ('N', 22, 0.5, ('L', ((49, 2),)), ('L', ((18, 1), (63, 1)))), ('L', ((49, 1), (59, 1)))), ('N', 106, 0.5, ('N', 69, 1.0, ('L', ((4, 2), (17, 1))), ('L', ((17, 2),))), ('L', ((63, 4),))))), ('L', ((65, 4),))), ('L', ((4, 3),))), ('N', 15, 5.5, ('L', ((14, 1), (18, 1))), ('N', 12, 4.0, ('L', ((3, 1), (22, 1))), ('L', ((3, 6),))))), ('L', ((4, 9),))))), ('N', 7, 5.5, ('N', 65, 0.5, ('N', 92, 1.0, ('N', 17, 0.5, ('L', ((21, 1), (60, 2))), ('N', 108, 0.5, ('N', 69, 0.5, ('N', 98, 1.0, ('N', 77, 0.5, ('N', 36, 1.5, ('L', ((21, 12),)), ('N', 50, 0.5, ('L', ((11, 1), (21, 1))), ('L', ((21, 2),)))), ('N', 40, 0.5, ('L', ((21, 2),)), ('L', ((5, 1), (17, 1), (35, 1))))), ('L', ((13, 2), (21, 2)))), ('L', ((21, 1), (59, 2)))), ('N', 48, 0.5, ('L', ((65, 2),)), ('L', ((4, 1), (13, 1), (63, 1)))))), ('L', ((21, 1), (44, 4)))), ('N', 22, 1.5, ('N', 29, 0.5, ('L', ((21, 3),)), ('L', ((22, 2), (65, 1)))), ('L', ((22, 5),)))), ('N', 58, 1.5, ('N', 19, 3.5, ('L', ((21, 2), (22, 1))), ('N', 19, 5.0, ('N', 32, 0.5, ('L', ((5, 2),)), ('L', ((0, 1), (5, 2)))), ('L', ((5, 2), (19, 1))))), ('N', 35, 0.5, ('N', 103, 0.5, ('L', ((4, 1), (19, 1))), ('L', ((61, 3),))), ('N', 38, 2.5, ('L', ((7, 2),)), ('N', 17, 5.5, ('L', ((13, 5),)), ('L', ((4, 1), (63, 1))))))))), ('N', 26, 0.5, ('N', 106, 0.5, ('N', 84, 0.5, ('N', 23, 0.5, ('N', 54, 0.5, ('N', 51, 0.5, ('N', 108, 0.5, ('N', 34, 1.5, ('N', 48, 0.5, ('N', 58, 0.5, ('N', 75, 1.0, ('N', 36, 0.5, ('L', ((7, 23), (19, 1))), ('L', ((0, 1), (7, 2), (14, 2), (17, 1)))), ('L', ((60, 2), (61, 1)))), ('N', 35, 1.0, ('N', 98, 0.5, ('L', ((0, 1), (7, 4), (12, 1), (16, 1), (17, 4))), ('L', ((60, 2),))), ('L', ((19, 3),)))), ('N', 98, 1.0, ('N', 93, 0.5, ('N', 75, 1.0, ('L', ((0, 3), (5, 8), (7, 2), (14, 1))), ('L', ((32, 2),))), ('L', ((50, 2),))), ('L', ((61, 3),)))), ('N', 57, 0.5, ('L', ((12, 4),)), ('L', ((12, 2), (19, 1))))), ('L', ((65, 4),))), ('N', 1, 14.5, ('N', 83, 0.5, ('N', 57, 0.5, ('N', 30, 0.5, ('L', ((17, 3),)), ('N', 48, 0.5, ('L', ((7, 3),)), ('N', 56, 0.5, ('L', ((5, 1), (7, 1), (15, 1), (22, 1), (51, 1), (65, 2))), ('L', ((13, 2),))))), ('N', 16, 6.5, ('L', ((14, 2), (15, 1))), ('L', ((14, 3),)))), ('L', ((8, 3),))), ('N', 14, 1.5, ('L', ((7, 3),)), ('N', 0, 4.0, ('N', 9, 0.5, ('L', ((0, 1), (8, 2))), ('L', ((8, 3), (22, 1)))), ('L', ((8, 3),)))))), ('N', 57, 1.5, ('N', 12, 9.5, ('N', 17, 9.5, ('L', ((11, 3),)), ('L', ((7, 1), (22, 1)))), ('L', ((11, 4),))), ('L', ((5, 3), (11, 1))))), ('N', 14, 5.5, ('N', 1, 20.5, ('N', 37, 2.5, ('N', 62, 0.5, ('N', 16, 6.5, ('L', ((21, 7),)), ('N', 83, 1.0, ('N', 51, 0.5, ('L', ((5, 1), (7, 2))), ('L', ((21, 3),))), ('L', ((21, 5),)))), ('L', ((7, 2),))), ('N', 1, 11.0, ('L', ((12, 1), (65, 2))), ('L', ((5, 1), (21, 1))))), ('L', ((0, 2),))), ('N', 61, 1.0, ('N', 1, 3.5, ('L', ((60, 2),)), ('L', ((7, 6),))), ('L', ((17, 2),))))), ('N', 84, 1.5, ('L', ((41, 8),)), ('N', 1, 4.5, ('L', ((17, 1), (61, 1))), ('N', 6, 0.5, ('L', ((41, 4),)), ('N', 14, 3.0, ('L', ((7, 1), (11, 2))), ('L', ((41, 4),))))))), ('N', 92, 0.5, ('N', 34, 2.5, ('N', 21, 0.5, ('N', 11, 8.5, ('L', ((63, 15),)), ('N', 37, 1.5, ('L', ((60, 1), (63, 2))), ('L', ((41, 1), (63, 1))))), ('L', ((21, 3),))), ('N', 1, 6.0, ('L', ((5, 2),)), ('N', 79, 0.5, ('L', ((7, 2),)), ('L', ((8, 2),))))), ('L', ((50, 5),)))), ('N', 35, 1.5, ('N', 77, 1.0, ('L', ((4, 21),)), ('L', ((4, 1), (21, 1)))), ('L', ((4, 2), (41, 1)))))), ('N', 71, 0.5, ('N', 108, 0.5, ('N', 2, 0.5, ('N', 23, 0.5, ('N', 103, 0.5, ('N', 5, 4.5, ('N', 4, 0.5, ('N', 32, 0.5, ('N', 106, 0.5, ('N', 41, 1.5, ('N', 57, 0.5, ('N', 9, 1.5, ('N', 65, 0.5, ('L', ((1, 2), (10, 2), (11, 1), (13, 1), (17, 1), (20, 1), (29, 1), (43, 1), (49, 1))), ('L', ((22, 2),))), ('L', ((3, 1), (32, 2)))), ('L', ((14, 4),))), ('L', ((49, 4),))), ('N', 15, 3.5, ('L', ((62, 3),)), ('N', 17, 11.5, ('L', ((39, 1), (62, 1))), ('N', 42, 1.0, ('L', ((62, 1), (63, 1))), ('L', ((63, 3),)))))), ('N', 102, 0.5, ('N', 30, 0.5, ('L', ((2, 1), (5, 1))), ('N', 36, 0.5, ('L', ((11, 1), (63, 1))), ('L', ((11, 2),)))), ('N', 104, 1.5, ('N', 20, 0.5, ('N', 60, 0.5, ('N', 22, 1.5, ('L', ((59, 2),)), ('L', ((49, 1), (59, 1)))), ('N', 75, 1.0, ('L', ((11, 1), (62, 1))), ('L', ((3, 2), (12, 1))))), ('N', 61, 0.5, ('L', ((4, 1), (63, 1))), ('L', ((17, 2), (63, 1))))), ('L', ((59, 8),))))), ('L', ((10, 7),))), ('N', 106, 0.5, ('N', 15, 2.5, ('L', ((4, 7),)), ('N', 28, 2.5, ('N', 7, 7.5, ('N', 51, 0.5, ('N', 62, 0.5, ('N', 0, 4.0, ('L', ((11, 1), (14, 1), (32, 1), (41, 1))), ('L', ((4, 1), (5, 7), (17, 2), (41, 1)))), ('L', ((19, 3),))), ('N', 84, 1.0, ('N', 16, 3.0, ('L', ((17, 1), (51, 1))), ('L', ((8, 5), (11, 2), (12, 1), (13, 1), (14, 1), (15, 1)))), ('L', ((4, 2),)))), ('N', 17, 3.5, ('L', ((19, 2),)), ('L', ((32, 3),)))), ('N', 35, 0.5, ('N', 75, 1.0, ('L', ((12, 1), (41, 1))), ('L', ((19, 2),))), ('N', 34, 0.5, ('N', 60, 0.5, ('L', ((13, 4),)), ('L', ((5, 1), (19, 1)))), ('L', ((13, 3),)))))), ('N', 61, 1.5, ('N', 47, 0.5, ('N', 13, 2.5, ('L', ((19, 1), (63, 2))), ('L', ((63, 13),))), ('L', ((4, 2),))), ('N', 19, 2.5, ('L', ((63, 2),)), ('L', ((19, 1), (51, 2))))))), ('N', 106, 1.5, ('N', 63, 0.5, ('N', 104, 0.5, ('N', 32, 1.5, ('L', ((60, 5),)), ('N', 69, 0.5, ('L', ((4, 1), (11, 1), (60, 3))), ('L', ((31, 2),)))), ('N', 58, 0.5, ('N', 11, 1.5, ('L', ((8, 3),)), ('N', 65, 0.5, ('N', 94, 0.5, ('N', 38, 0.5, ('L', ((8, 1), (19, 1), (60, 3), (61, 4))), ('L', ((61, 5),))), ('L', ((50, 2), (51, 1)))), ('L', ((5, 1), (59, 3))))), ('N', 11, 8.0, ('L', ((15, 4),)), ('N', 30, 0.5, ('L', ((41, 2),)), ('N', 18, 4.5, ('N', 60, 1.0, ('L', ((19, 2),)), ('L', ((5, 1), (19, 1)))), ('L', ((60, 3),))))))), ('N', 75, 1.0, ('L', ((17, 4),)), ('N', 13, 1.5, ('L', ((11, 3),)), ('L', ((12, 2), (63, 1)))))), ('N', 75, 1.5, ('N', 19, 5.5, ('L', ((60, 1), (63, 1))), ('L', ((63, 7),))), ('L', ((8, 1), (60, 3), (61, 1)))))), ('N', 25, 0.5, ('N', 9, 1.5, ('N', 8, 9.0, ('N', 62, 1.0, ('L', ((21, 7),)), ('L', ((13, 1), (21, 1)))), ('L', ((12, 2),))), ('N', 37, 0.5, ('N', 7, 3.5, ('L', ((31, 3),)), ('L', ((0, 2),))), ('N', 39, 0.5, ('N', 62, 1.0, ('N', 50, 0.5, ('L', ((51, 1), (60, 1))), ('N', 74, 1.5, ('N', 56, 0.5, ('L', ((17, 2),)), ('N', 17, 5.5, ('L', ((13, 2),)), ('L', ((13, 2), (63, 1))))), ('L', ((5, 1), (7, 1))))), ('L', ((19, 2),))), ('L', ((21, 2), (60, 1)))))), ('N', 54, 0.5, ('N', 23, 1.5, ('L', ((22, 6),)), ('N', 40, 2.0, ('L', ((21, 1), (22, 2))), ('L', ((21, 2),)))), ('N', 37, 0.5, ('L', ((5, 1), (7, 1), (58, 1))), ('L', ((5, 1), (41, 1))))))), ('N', 47, 0.5, ('N', 5, 4.5, ('N', 64, 0.5, ('N', 80, 0.5, ('N', 37, 1.5, ('N', 0, 5.5, ('N', 57, 0.5, ('N', 60, 0.5, ('N', 31, 0.5, ('N', 22, 2.5, ('L', ((0, 1), (2, 2), (3, 1), (9, 2), (10, 3), (13, 6), (20, 1), (22, 2))), ('L', ((10, 8), (13, 1), (22, 1)))), ('L', ((62, 2),))), ('N', 55, 1.0, ('L', ((11, 1), (18, 2))), ('L', ((17, 2), (22, 1))))), ('N', 60, 0.5, ('L', ((14, 10),)), ('L', ((5, 1), (13, 1))))), ('N', 30, 0.5, ('L', ((5, 1), (33, 1))), ('L', ((5, 2),)))), ('N', 0, 4.5, ('L', ((17, 1), (35, 1))), ('L', ((35, 3),)))), ('N', 80, 1.5, ('L', ((3, 3),)), ('N', 13, 4.5, ('L', ((11, 2),)), ('L', ((3, 2),))))), ('N', 24, 1.5, ('N', 9, 0.5, ('L', ((22, 2),)), ('L', ((11, 2),))), ('N', 77, 1.5, ('L', ((21, 13),)), ('L', ((35, 2),))))), ('N', 106, 0.5, ('N', 8, 9.0, ('N', 7, 5.0, ('N', 12, 5.5, ('N', 0, 8.0, ('L', ((13, 2),)), ('L', ((8, 6),))), ('N', 23, 0.5, ('N', 79, 1.0, ('N', 54, 0.5, ('L', ((8, 1), (15, 1))), ('L', ((11, 2),))), ('N', 83, 1.0, ('L', ((8, 1), (17, 1))), ('L', ((8, 2),)))), ('L', ((21, 4),)))), ('N', 35, 0.5, ('N', 11, 7.5, ('N', 30, 0.5, ('L', ((5, 1), (21, 1))), ('L', ((5, 5),))), ('L', ((5, 1), (14, 2)))), ('L', ((13, 3),)))), ('N', 15, 7.5, ('N', 41, 0.5, ('N', 3, 0.5, ('N', 60, 1.5, ('L', ((7, 2), (17, 2))), ('L', ((17, 3),))), ('N', 16, 6.5, ('L', ((7, 4),)), ('L', ((7, 1), (21, 1))))), ('N', 1, 17.0, ('N', 43, 0.5, ('N', 11, 8.5, ('N', 12, 8.5, ('L', ((7, 1), (41, 1))), ('L', ((7, 4),))), ('N', 4, 0.5, ('L', ((5, 3), (14, 1))), ('L', ((7, 2),)))), ('N', 17, 11.0, ('N', 4, 0.5, ('L', ((0, 2), (5, 1), (21, 1))), ('L', ((0, 3),))), ('L', ((12, 1), (18, 1))))), ('N', 35, 1.5, ('N', 28, 2.5, ('L', ((7, 5),)), ('L', ((7, 3), (21, 1)))), ('L', ((13, 2), (14, 1)))))), ('N', 33, 0.5, ('N', 4, 0.5, ('N', 22, 1.5, ('N', 3, 0.5, ('N', 15, 12.5, ('L', ((15, 2),)), ('L', ((21, 2),))), ('N', 6, 1.5, ('L', ((14, 1), (21, 1))), ('L', ((14, 3),)))), ('N', 11, 8.5, ('N', 21, 0.5, ('L', ((0, 1), (8, 4), (14, 1))), ('L', ((22, 3),))), ('L', ((5, 5),)))), ('N', 61, 1.5, ('N', 3, 0.5, ('N', 19, 5.0, ('L', ((15, 1), (21, 1))), ('L', ((7, 1), (41, 4)))), ('N', 57, 0.5, ('L', ((0, 1), (7, 14), (21, 1), (41, 2))), ('L', ((0, 2), (7, 2), (8, 1), (14, 3))))), ('N', 1, 12.0, ('L', ((0, 1), (16, 2))), ('L', ((16, 2),))))), ('N', 50, 0.5, ('N', 9, 2.5, ('L', ((21, 3),)), ('L', ((5, 1), (41, 1)))), ('N', 77, 0.5, ('N', 37, 2.5, ('N', 23, 0.5, ('L', ((11, 9),)), ('L', ((0, 2), (7, 2), (11, 3)))), ('L', ((7, 1), (41, 1)))), ('L', ((41, 2),))))))), ('N', 38, 0.5, ('N', 35, 1.0, ('N', 1, 4.0, ('L', ((8, 1), (63, 1))), ('L', ((63, 2),))), ('N', 4, 0.5, ('N', 28, 2.5, ('L', ((5, 2), (41, 1))), ('L', ((5, 2), (41, 1)))), ('L', ((7, 1), (8, 3))))), ('N', 54, 0.5, ('N', 65, 0.5, ('L', ((63, 8),)), ('L', ((22, 1), (63, 1)))), ('L', ((21, 2),)))))), ('N', 25, 0.5, ('N', 43, 0.5, ('L', ((4, 14),)), ('N', 13, 4.5, ('N', 9, 1.0, ('N', 61, 1.0, ('L', ((21, 2),)), ('L', ((14, 1), (21, 2)))), ('L', ((4, 1), (18, 1)))), ('L', ((4, 7),)))), ('N', 46, 0.5, ('L', ((4, 2),)), ('L', ((22, 2),)))))), ('N', 107, 0.5, ('N', 6, 1.5, ('L', ((65, 23),)), ('N', 33, 0.5, ('L', ((65, 3),)), ('N', 36, 0.5, ('L', ((8, 2),)), ('N', 1, 3.5, ('L', ((13, 1), (63, 3))), ('L', ((4, 1), (65, 1))))))), ('L', ((64, 3),)))), ('L', ((4, 19),))), ('N', 71, 0.5, ('N', 48, 0.5, ('N', 62, 0.5, ('N', 18, 4.5, ('N', 23, 0.5, ('N', 12, 7.5, ('N', 1, 5.5, ('L', ((17, 1), (61, 1))), ('N', 77, 0.5, ('L', ((7, 10),)), ('N', 55, 1.5, ('L', ((41, 2),)), ('L', ((7, 2),))))), ('N', 67, 1.0, ('N', 11, 9.5, ('N', 30, 1.0, ('N', 8, 1.5, ('L', ((12, 1), (15, 1))), ('L', ((7, 1), (10, 1)))), ('L', ((8, 5),))), ('L', ((7, 5),))), ('N', 60, 1.5, ('L', ((35, 1), (60, 1), (61, 2))), ('L', ((17, 2),))))), ('N', 54, 0.5, ('N', 20, 0.5, ('N', 8, 2.0, ('L', ((21, 3),)), ('L', ((21, 2), (22, 1)))), ('L', ((7, 1), (15, 1), (21, 1)))), ('N', 17, 5.5, ('L', ((7, 2),)), ('N', 43, 0.5, ('L', ((13, 1), (17, 1))), ('L', ((0, 2),)))))), ('N', 84, 0.5, ('N', 65, 0.5, ('N', 54, 0.5, ('N', 106, 0.5, ('N', 105, 0.5, ('N', 92, 0.5, ('N', 29, 0.5, ('N', 27, 0.5, ('N', 60, 0.5, ('L', ((3, 3), (4, 2), (7, 7), (8, 2), (10, 1), (12, 7), (13, 4), (14, 1), (15, 1), (18, 1), (32, 2), (35, 2), (43, 1), (59, 1))), ('L', ((2, 1), (4, 3), (7, 1), (14, 5), (17, 10), (18, 3), (29, 3), (60, 3)))), ('N', 40, 1.5, ('L', ((2, 2), (3, 1), (10, 10), (14, 11), (20, 2), (21, 3), (29, 1), (35, 1), (59, 1))), ('L', ((0, 3), (7, 2), (10, 1), (17, 3))))), ('N', 108, 0.5, ('N', 59, 0.5, ('L', ((2, 1), (9, 1), (10, 5), (13, 3), (14, 2), (18, 1), (20, 2), (21, 4), (30, 1), (46, 1))), ('L', ((16, 4), (60, 3)))), ('L', ((65, 13),)))), ('N', 22, 1.5, ('L', ((49, 4),)), ('N', 57, 0.5, ('L', ((44, 1), (50, 1))), ('L', ((49, 2),))))), ('L', ((62, 4),))), ('N', 50, 0.5, ('N', 37, 0.5, ('N', 41, 0.5, ('L', ((63, 2), (65, 1))), ('L', ((62, 3),))), ('L', ((3, 2), (62, 1)))), ('L', ((63, 7),)))), ('N', 97, 1.5, ('N', 77, 1.0, ('N', 12, 8.5, ('L', ((11, 14),)), ('L', ((7, 1), (11, 3)))), ('L', ((11, 1), (21, 1), (63, 1)))), ('L', ((49, 1), (61, 2), (65, 3))))), ('N', 0, 5.5, ('N', 42, 0.5, ('L', ((22, 12),)), ('L', ((21, 1), (22, 1)))), ('N', 26, 0.5, ('L', ((11, 1), (12, 1), (65, 1))), ('L', ((3, 2),))))), ('L', ((41, 8),)))), ('N', 9, 2.5, ('N', 18, 5.5, ('N', 76, 0.5, ('N', 79, 0.5, ('L', ((8, 1), (63, 1))), ('N', 1, 8.0, ('L', ((8, 1), (13, 1))), ('L', ((8, 2),)))), ('L', ((32, 1), (33, 2)))), ('L', ((19, 2), (41, 3)))), ('L', ((19, 7),)))), ('N', 87, 0.5, ('N', 98, 0.5, ('N', 27, 0.5, ('N', 22, 1.5, ('N', 51, 0.5, ('N', 101, 0.5, ('N', 29, 0.5, ('N', 77, 0.5, ('N', 83, 1.0, ('N', 42, 2.5, ('N', 37, 0.5, ('L', ((0, 2), (4, 6), (5, 12), (7, 1), (14, 1), (18, 3), (19, 1), (21, 3), (32, 1), (60, 1))), ('L', ((41, 2),))), ('L', ((11, 3),))), ('N', 62, 0.5, ('N', 38, 1.5, ('L', ((12, 1), (51, 1))), ('L', ((21, 2),))), ('L', ((19, 3),)))), ('L', ((5, 6),))), ('N', 74, 0.5, ('L', ((65, 4),)), ('L', ((11, 1), (65, 1))))), ('L', ((17, 2),))), ('N', 47, 0.5, ('N', 73, 1.0, ('N', 85, 1.0, ('L', ((8, 1), (18, 1))), ('L', ((5, 2), (13, 2)))), ('L', ((19, 2),))), ('L', ((4, 12),)))), ('N', 12, 8.5, ('N', 62, 0.5, ('N', 15, 10.5, ('N', 25, 0.5, ('N', 34, 1.5, ('N', 85, 0.5, ('N', 28, 2.5, ('L', ((5, 2), (7, 1), (12, 1), (13, 1), (65, 3))), ('L', ((15, 2),))), ('L', ((5, 3),))), ('L', ((12, 2),))), ('N', 65, 0.5, ('L', ((4, 3),)), ('L', ((22, 2),)))), ('L', ((9, 3),))), ('L', ((17, 4),))), ('L', ((5, 16),)))), ('N', 64, 0.5, ('N', 26, 0.5, ('N', 51, 0.5, ('N', 40, 0.5, ('N', 9, 1.5, ('N', 28, 1.5, ('N', 50, 0.5, ('L', ((14, 2),)), ('N', 37, 1.5, ('L', ((11, 1), (63, 1))), ('L', ((13, 1), (14, 1))))), ('L', ((41, 2),))), ('N', 1, 2.5, ('L', ((19, 1), (63, 2))), ('L', ((63, 3),)))), ('N', 3, 0.5, ('N', 56, 0.5, ('N', 32, 0.5, ('L', ((15, 1), (63, 2))), ('N', 62, 0.5, ('L', ((5, 1), (14, 1), (62, 2))), ('L', ((5, 3),)))), ('L', ((51, 3),))), ('L', ((5, 7),)))), ('N', 14, 1.5, ('N', 16, 9.0, ('N', 77, 0.5, ('L', ((8, 3),)), ('N', 56, 1.5, ('L', ((7, 2),)), ('N', 8, 5.0, ('L', ((19, 1), (32, 1), (41, 2), (65, 1))), ('L', ((8, 1), (13, 1), (14, 1)))))), ('N', 1, 1.5, ('L', ((15, 3),)), ('N', 79, 1.0, ('L', ((8, 2),)), ('L', ((19, 2), (63, 1)))))), ('N', 9, 1.5, ('N', 43, 0.5, ('N', 17, 9.5, ('N', 61, 1.0, ('L', ((8, 5),)), ('L', ((16, 1), (19, 1), (61, 1)))), ('N', 11, 1.5, ('L', ((8, 1), (22, 2))), ('L', ((8, 1), (63, 1))))), ('L', ((0, 1), (11, 2)))), ('N', 13, 3.5, ('N', 33, 0.5, ('N', 56, 1.5, ('L', ((5, 1), (14, 1), (17, 1), (63, 2))), ('L', ((32, 2),))), ('N', 84, 1.0, ('L', ((11, 3),)), ('L', ((11, 1), (63, 1))))), ('N', 16, 2.0, ('L', ((5, 2),)), ('N', 16, 7.5, ('L', ((22, 1), (63, 8))), ('L', ((8, 2), (63, 3))))))))), ('L', ((4, 7),))), ('N', 16, 5.5, ('N', 8, 6.0, ('N', 103, 0.5, ('L', ((5, 3),)), ('L', ((5, 1), (61, 1)))), ('L', ((13, 2), (21, 1), (63, 2)))), ('N', 30, 0.5, ('N', 12, 8.0, ('N', 23, 1.5, ('L', ((21, 3),)), ('L', ((11, 1), (21, 1), (22, 1)))), ('L', ((21, 6),))), ('L', ((7, 2), (21, 1))))))), ('N', 1, 4.5, ('N', 28, 1.5, ('N', 106, 0.5, ('L', ((4, 1), (61, 2), (65, 1))), ('N', 56, 0.5, ('N', 101, 0.5, ('L', ((63, 3),)), ('L', ((4, 1), (63, 1), (64, 1)))), ('L', ((63, 7),)))), ('N', 0, 12.5, ('N', 14, 4.5, ('N', 15, 5.5, ('L', ((61, 2),)), ('N', 79, 1.5, ('N', 37, 0.5, ('L', ((13, 2), (19, 1), (51, 1))), ('L', ((13, 1), (41, 1), (63, 1)))), ('N', 57, 0.5, ('L', ((21, 1), (22, 1), (61, 1))), ('N', 0, 10.0, ('L', ((60, 2),)), ('L', ((60, 1), (61, 1))))))), ('N', 106, 0.5, ('L', ((4, 1), (15, 1))), ('L', ((63, 3),)))), ('N', 62, 1.5, ('N', 106, 1.0, ('L', ((8, 3),)), ('L', ((8, 1), (60, 1)))), ('L', ((15, 2),))))), ('N', 14, 2.5, ('N', 36, 1.0, ('L', ((31, 2),)), ('L', ((60, 2),))), ('N', 40, 2.0, ('N', 29, 0.5, ('L', ((61, 3),)), ('L', ((65, 3),))), ('L', ((13, 4),)))))), ('N', 41, 0.5, ('L', ((50, 1), (51, 1), (65, 1))), ('L', ((51, 4),))))), ('L', ((4, 16),))), ('N', 47, 0.5, ('N', 106, 0.5, ('N', 4, 0.5, ('N', 25, 0.5, ('N', 64, 0.5, ('N', 103, 0.5, ('N', 57, 0.5, ('N', 14, 1.5, ('N', 35, 0.5, ('N', 12, 5.5, ('L', ((10, 7),)), ('N', 58, 0.5, ('N', 19, 5.5, ('L', ((35, 1), (65, 2))), ('N', 83, 0.5, ('L', ((10, 4), (17, 1), (20, 2))), ('L', ((2, 1), (10, 1))))), ('L', ((17, 3),)))), ('N', 89, 0.5, ('N', 55, 0.5, ('N', 60, 0.5, ('N', 16, 5.5, ('L', ((13, 3),)), ('L', ((1, 1), (7, 1), (13, 1)))), ('L', ((18, 2),))), ('N', 63, 0.5, ('N', 13, 2.5, ('L', ((2, 1), (13, 1))), ('L', ((2, 2),))), ('L', ((20, 2),)))), ('L', ((46, 3),)))), ('N', 108, 0.5, ('N', 35, 0.5, ('N', 73, 0.5, ('N', 12, 5.5, ('N', 24, 2.5, ('L', ((7, 4), (9, 1), (15, 1), (17, 1), (18, 1), (41, 2))), ('L', ((12, 3),))), ('N', 1, 4.5, ('L', ((3, 1), (5, 3), (15, 1), (17, 2), (19, 3), (35, 1), (59, 1))), ('L', ((3, 1), (5, 18), (7, 1), (18, 3), (19, 1), (51, 1))))), ('N', 9, 1.0, ('N', 73, 1.5, ('L', ((32, 3),)), ('L', ((12, 1), (29, 2)))), ('N', 26, 0.5, ('L', ((62, 2),)), ('L', ((3, 3),))))), ('N', 50, 0.5, ('L', ((0, 2), (43, 1))), ('N', 13, 2.5, ('L', ((5, 1), (13, 1), (41, 1))), ('L', ((13, 7),))))), ('L', ((65, 12),)))), ('N', 18, 5.5, ('N', 35, 0.5, ('N', 15, 8.5, ('N', 59, 0.5, ('L', ((0, 1), (17, 2))), ('L', ((14, 2),))), ('N', 61, 1.5, ('N', 17, 8.5, ('N', 51, 0.5, ('L', ((5, 1), (41, 1))), ('L', ((8, 10),))), ('L', ((11, 2),))), ('N', 40, 0.5, ('L', ((19, 3),)), ('L', ((8, 2), (15, 2)))))), ('N', 67, 1.0, ('N', 50, 0.5, ('L', ((5, 3),)), ('L', ((13, 1), (16, 1)))), ('L', ((32, 3),)))), ('N', 50, 0.5, ('N', 40, 1.5, ('N', 56, 1.5, ('N', 16, 2.5, ('L', ((11, 1), (59, 1))), ('N', 54, 0.5, ('L', ((14, 7), (49, 1))), ('L', ((2, 1), (11, 1))))), ('L', ((11, 1), (13, 1), (29, 1)))), ('L', ((5, 1), (61, 1)))), ('L', ((14, 8),))))), ('N', 94, 0.5, ('N', 19, 4.5, ('N', 8, 4.0, ('L', ((11, 1), (12, 2))), ('N', 79, 0.5, ('N', 104, 1.5, ('L', ((14, 1), (61, 2))), ('L', ((61, 3),))), ('N', 43, 0.5, ('L', ((61, 2),)), ('L', ((41, 2),))))), ('N', 28, 2.5, ('N', 11, 5.0, ('N', 17, 6.5, ('L', ((8, 1), (60, 1), (61, 1))), ('L', ((60, 5),))), ('N', 36, 0.5, ('N', 6, 1.5, ('N', 11, 8.0, ('L', ((15, 2),)), ('L', ((5, 1), (61, 2)))), ('L', ((19, 3),))), ('N', 61, 1.0, ('L', ((11, 1), (60, 1))), ('L', ((60, 2),))))), ('L', ((13, 2), (19, 4), (61, 1))))), ('N', 6, 1.0, ('L', ((50, 7),)), ('L', ((51, 2),))))), ('N', 40, 1.5, ('N', 38, 2.5, ('N', 96, 0.5, ('N', 17, 7.5, ('N', 7, 2.0, ('L', ((5, 1), (21, 1), (31, 1))), ('N', 12, 9.5, ('L', ((21, 6),)), ('L', ((21, 2), (61, 1))))), ('L', ((21, 23),))), ('L', ((59, 2),))), ('N', 60, 0.5, ('N', 8, 7.5, ('L', ((11, 1), (19, 1))), ('L', ((7, 3),))), ('L', ((13, 1), (17, 2))))), ('N', 35, 0.5, ('N', 1, 6.5, ('L', ((21, 3),)), ('N', 104, 0.5, ('N', 78, 1.5, ('L', ((19, 1), (44, 1))), ('L', ((35, 2),))), ('L', ((61, 4),)))), ('N', 24, 1.5, ('L', ((13, 3),)), ('L', ((21, 1), (65, 1))))))), ('N', 61, 0.5, ('N', 32, 0.5, ('L', ((22, 14),)), ('N', 9, 2.5, ('N', 5, 2.5, ('N', 65, 0.5, ('L', ((10, 2),)), ('N', 59, 0.5, ('N', 64, 1.5, ('L', ((21, 2), (22, 1))), ('L', ((21, 3),))), ('L', ((22, 3),)))), ('N', 14, 1.5, ('L', ((22, 4), (58, 1))), ('N', 22, 1.5, ('L', ((14, 1), (21, 1))), ('L', ((22, 2),))))), ('N', 19, 5.5, ('N', 83, 1.5, ('L', ((35, 2),)), ('N', 2, 0.5, ('N', 104, 1.5, ('L', ((65, 5),)), ('L', ((59, 2),))), ('L', ((3, 1), (22, 1), (41, 1))))), ('L', ((60, 3),))))), ('N', 9, 3.5, ('N', 32, 0.5, ('L', ((5, 6),)), ('L', ((5, 3), (22, 1)))), ('N', 69, 1.0, ('L', ((11, 3),)), ('L', ((3, 1), (12, 1), (17, 1))))))), ('N', 43, 0.5, ('N', 58, 0.5, ('N', 84, 0.5, ('N', 108, 0.5, ('N', 6, 0.5, ('L', ((10, 4),)), ('N', 7, 3.0, ('N', 35, 0.5, ('N', 6, 1.5, ('N', 42, 1.5, ('N', 9, 1.5, ('L', ((7, 2), (11, 1))), ('L', ((7, 18),))), ('N', 36, 1.5, ('L', ((7, 4), (9, 1), (21, 2))), ('L', ((14, 2),)))), ('N', 33, 0.5, ('L', ((7, 2), (21, 1))), ('L', ((11, 4),)))), ('N', 11, 6.0, ('L', ((13, 1), (21, 1))), ('L', ((13, 2),)))), ('L', ((8, 3),)))), ('L', ((65, 2),))), ('L', ((41, 4),))), ('N', 17, 5.5, ('N', 56, 0.5, ('N', 79, 1.0, ('L', ((15, 1), (16, 2), (60, 1))), ('L', ((16, 2),))), ('L', ((15, 2),))), ('N', 65, 0.5, ('N', 6, 1.5, ('N', 40, 1.5, ('N', 22, 1.5, ('L', ((7, 1), (11, 1), (19, 1), (60, 1))), ('L', ((21, 2),))), ('L', ((65, 2),))), ('L', ((17, 2),))), ('L', ((12, 2),))))), ('N', 96, 0.5, ('N', 11, 3.5, ('N', 13, 3.5, ('L', ((8, 4),)), ('N', 1, 17.0, ('L', ((11, 1), (17, 1))), ('L', ((8, 3),)))), ('N', 37, 1.5, ('L', ((0, 1), (7, 1))), ('N', 1, 20.0, ('L', ((0, 2), (12, 1))), ('L', ((0, 4),))))), ('N', 13, 2.5, ('L', ((7, 2),)), ('L', ((19, 1), (60, 1), (61, 1))))))), ('N', 0, 12.5, ('N', 50, 0.5, ('N', 41, 0.5, ('N', 30, 1.5, ('N', 28, 0.5, ('L', ((63, 1), (65, 1))), ('L', ((63, 3),))), ('L', ((62, 1), (63, 1)))), ('N', 48, 0.5, ('N', 98, 1.5, ('N', 41, 1.5, ('L', ((62, 5),)), ('L', ((22, 1), (62, 1)))), ('L', ((31, 1), (32, 1)))), ('L', ((64, 2),)))), ('N', 103, 1.5, ('N', 6, 1.5, ('N', 36, 0.5, ('N', 42, 0.5, ('N', 38, 2.0, ('N', 59, 0.5, ('L', ((41, 1), (63, 2))), ('L', ((63, 2),))), ('N', 83, 1.0, ('L', ((13, 1), (51, 1))), ('L', ((63, 2),)))), ('L', ((63, 4),))), ('L', ((60, 2),))), ('N', 75, 1.0, ('L', ((63, 27),)), ('N', 13, 4.5, ('L', ((61, 1), (63, 1))), ('L', ((63, 2),))))), ('L', ((31, 2), (63, 1))))), ('N', 98, 0.5, ('N', 42, 0.5, ('N', 1, 1.5, ('L', ((8, 4),)), ('N', 75, 0.5, ('L', ((63, 3),)), ('L', ((31, 2),)))), ('N', 1, 5.5, ('N', 41, 2.5, ('N', 56, 0.5, ('N', 1, 2.5, ('L', ((15, 1), (19, 1), (21, 1))), ('N', 16, 7.0, ('L', ((8, 1), (63, 1))), ('L', ((63, 2),)))), ('L', ((13, 2),))), ('N', 75, 1.0, ('N', 1, 3.5, ('L', ((19, 1), (41, 1))), ('L', ((5, 3),))), ('L', ((65, 2),)))), ('L', ((19, 3),)))), ('N', 6, 1.5, ('L', ((60, 5),)), ('N', 11, 7.0, ('N', 1, 1.5, ('L', ((8, 1), (21, 1))), ('L', ((61, 3),))), ('L', ((61, 5),))))))), ('N', 101, 1.5, ('N', 12, 3.5, ('N', 14, 3.5, ('L', ((4, 14),)), ('N', 57, 0.5, ('N', 13, 4.5, ('N', 65, 0.5, ('L', ((18, 1), (49, 1))), ('L', ((22, 3),))), ('L', ((4, 2),))), ('L', ((14, 2), (65, 1))))), ('N', 106, 0.5, ('L', ((4, 38),)), ('L', ((4, 2), (63, 1))))), ('L', ((64, 2),)))))
try:
    _CLONE_MAX_SAFE_DEFERRALS = max(
        0, int(os.environ.get("V10_CLONE_DEFERRALS", "0"))
    )
except (TypeError, ValueError):
    _CLONE_MAX_SAFE_DEFERRALS = 0


def _clone_action_key(obs, option):
    option_type = option.get("type")
    source_id = card_id(option_source(obs, option))
    target_id = card_id(option_target(obs, option))
    if option_type == 13:
        source_id = option.get("attackId")
    elif option_type == 14:
        source_id = -14
    elif option_type == 0:
        source_id = option.get("number")
    return (
        option_type,
        source_id,
        target_id,
        option.get("area"),
        option.get("inPlayArea"),
    )


def _clone_features(obs):
    state = current(obs)
    you = your_index(state)
    opponent = 1 - you
    ps = players(state)
    active_card = active(state, you)
    opponent_active = active(state, opponent)
    counts = board_counts(state, you)
    held = hand_ids(state, you)
    hand_counts = {}
    for cid in held:
        hand_counts[cid] = hand_counts.get(cid, 0) + 1
    values = [
        min(20, as_int(state.get("turn"), 0)),
        min(30, as_int(state.get("turnActionCount"), 0)),
        int(bool(state.get("energyAttached"))),
        int(bool(state.get("supporterPlayed"))),
        int(bool(state.get("retreated"))),
        _CLONE_ACTIVE_ID_MAP.get(card_id(active_card), 6),
        min(3, attached_count(active_card)),
        min(8, damage_on(active_card) // 30),
        min(10, hp(active_card) // 30),
        min(5, attached_count(opponent_active)),
        min(10, damage_on(opponent_active) // 30),
        min(12, hp(opponent_active) // 30),
        min(12, max_hp(opponent_active) // 30),
        len(bench(state, you)),
        len(bench(state, opponent)),
        min(15, len(held)),
        min(
            15,
            as_int(ps[opponent].get("handCount"), 0)
            if opponent < len(ps)
            else 0,
        ),
        min(
            15,
            (as_int(ps[you].get("deckCount"), 0) // 3)
            if you < len(ps)
            else 0,
        ),
        prize_count(state, you),
        prize_count(state, opponent),
    ]
    for cid in _CLONE_POKEMON_IDS:
        values.extend((counts.get(cid, 0), hand_counts.get(cid, 0)))
    for cid in sorted(set(EXPECTED_DECK)):
        if cid not in _CLONE_POKEMON_IDS:
            values.append(hand_counts.get(cid, 0))
    available = {}
    for option in selection(obs).get("option") or []:
        key = _clone_action_key(obs, option)
        available[key] = available.get(key, 0) + 1
    values.extend(min(2, available.get(action, 0)) for action in _CLONE_ACTIONS)
    return values


def _clone_votes(features):
    votes = [0.0] * len(_CLONE_ACTIONS)
    for tree in _CLONE_TREES:
        node = tree
        while node[0] == "N":
            node = node[3] if features[node[1]] <= node[2] else node[4]
        total = sum(count for _, count in node[1])
        if total:
            for class_index, count in node[1]:
                votes[class_index] += count / total
    return votes


def _clone_model_choice(obs, options):
    votes = _clone_votes(_clone_features(obs))
    by_class = {}
    for index, option in enumerate(options):
        class_index = _CLONE_ACTION_INDEX.get(_clone_action_key(obs, option))
        if class_index is None:
            continue
        previous = by_class.get(class_index)
        candidate = (score_option(obs, option), -index, index)
        if previous is None or candidate > previous:
            by_class[class_index] = candidate
    if not by_class:
        return None
    best_class = max(
        by_class,
        key=lambda class_index: (
            votes[class_index],
            by_class[class_index][0],
            -class_index,
        ),
    )
    return by_class[best_class][2]


def _clone_safe_before_attack(obs, option):
    state = current(obs)
    you = your_index(state)
    option_type = option.get("type")
    source = option_source(obs, option)
    source_id = card_id(source)
    target = option_target(obs, option)
    target_id = card_id(target)
    target_area = option.get("inPlayArea")

    if option_type == 13:
        return True
    if option_type == 14:
        return False
    if option_type == 9:
        if target_area != 4:
            return True
        return (
            source_id == LOPUNNY
            and target_id == BUNEARY
            and attached_count(target) >= 1
        )
    if option_type == 10:
        return not (source_id == DUDUNSPARCE and option.get("area") == 4)
    if option_type == 12:
        active_card = active(state, you)
        serial = active_card.get("serial") if isinstance(active_card, dict) else None
        replacement = best_lopunny(state, you, exclude_serial=serial)
        return bool(replacement and replacement[0])
    if option_type == 7 and source_id == WALLY:
        return any(
            card_id(card) == LOPUNNY and damage_on(card) > 0
            for card in bench(state, you)
        )
    return option_type in (7, 8, 9, 10, 12)


def _clone_best_attack(obs, options):
    attacks = [
        (score_option(obs, option), -index, index)
        for index, option in enumerate(options)
        if option.get("type") == 13
    ]
    return max(attacks)[2] if attacks else None


def choose_action(obs):
    if not isinstance(obs, dict) or obs.get("select") is None:
        return DECK[:]
    select = selection(obs)
    options = select.get("option") or []
    if select.get("context") != 0 or not options:
        # Search, discard, promotion and effect targeting retain the robust
        # deterministic card-semantic rules from the base planner.
        return _RULE_CHOOSE_ACTION(obs)

    state = current(obs)
    reset_turn_memory(state)
    choice = _clone_model_choice(obs, options)
    if choice is None:
        return _RULE_CHOOSE_ACTION(obs)

    attack_index = _clone_best_attack(obs, options)
    if attack_index is not None:
        turn_key = LAST_TURN
        deferred = ATTACK_DEFERRALS.get(turn_key, 0)
        selected = options[choice]
        if selected.get("type") == 13:
            # The fitted model chooses when to attack; printed card mechanics
            # choose the safest of two simultaneously legal attacks.
            return [attack_index]
        if (
            deferred >= _CLONE_MAX_SAFE_DEFERRALS
            or as_int(state.get("turnActionCount"), 0) >= 28
            or not _clone_safe_before_attack(obs, selected)
        ):
            return [attack_index]
        ATTACK_DEFERRALS[turn_key] = deferred + 1
    return [choice]


def safe_action(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        options = select.get("option") or []
        minimum = as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(options))))


def agent(obs):
    return safe_action(obs)
