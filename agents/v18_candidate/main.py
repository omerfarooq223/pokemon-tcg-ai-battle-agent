"""V18 Grandmaster Agent for Kaggle Pokemon TCG AI Battle Challenge.

Architecture & Tactical Invariants:
1. Dynamic Universal Damage-Immunity Recognition:
   - Evaluates damage immunity from defensive Pokémon abilities (Crustle, Cornerstone, Mimikyu)
     AND ACE SPEC Stadiums (Neutralization Zone 1247 on non-Rule Box Pokémon).
   - When damage immunity is detected, immediately accelerates 2nd energy attachment and fires
     Spiky Hopper (1226, 160 dmg), which pierces and ignores all defensive effects.
2. Damaged High-Prize Bench Gusting & Lethal Closeouts:
   - Prioritizes Boss's Orders (1182) to drag damaged high-prize Pokémon (Mega ex = 3 prizes, ex = 2 prizes)
     from the bench to claim immediate knockouts, rather than hitting fresh undamaged targets.
   - Instantly triggers lethal gust closeouts whenever taking down a bench target wins the game.
3. Draw & Search Lifeline Preservation (Anti-Discard of Lillie/Hilda):
   - When active attacker has 0 Energy (or hand has no energy), strictly protects Lillie's Determination (1227)
     and Hilda (1225) from Ultra Ball discards, prioritizing them over Xerosic to guarantee continuous energy flow.
4. Active Pivot & Trapped Support Escape Invariant:
   - When an active support Pokémon (Dunsparce/Fan Rotom) has no Air Balloon and 0 Energy, prioritizing
     Air Balloon or 1 Energy attachment enables immediate retreat into a ready benched Lopunny,
     completely eliminating trapped-active stall turns.
5. Attacker Energy Attachment Priority & Turn-1 Enriching Optimization:
   - On Turn 1 (or when no attacker can strike this turn), Enriching Energy (13) on Dunsparce/Fan Rotom
     accelerates the hand with +4 cards.
   - On Turn 2+ when an attacker can strike, energy attachment strictly prioritizes powering the active/benched
     attacker to guarantee an attack every turn.
6. Deck-Thinning & Dudunsparce Engine Optimization:
   - Dudunsparce's Run Away Draw aggressively cycles the deck to find Wally's Compassion and Air Balloons,
     while safeguarding against deck-out (conserves draw when deck count <= 2).
7. Dynamic Gale Thrust Free-Retreat Pivot Engine:
   - Gale Thrust (1225) deals 60 + 170 = 230 DAMAGE for only 1 Colorless Energy when moving from Bench to Active.
   - Air Balloon (1174, retreat cost -2) enables free pivoting between Active support and Mega Lopunny ex.
8. Quad-Wally Heal & Recovery Loop:
   - Heals 120 HP on damaged 330 HP Mega Lopunny ex and safely recycles injured attackers before the opponent
     can claim prize cards.
9. 100% Crash-Proof Standard Library Architecture:
   - Verified on Kaggle loader without external dependencies or disk path assumptions.
"""

from __future__ import annotations

import os
from typing import Any

# Card IDs
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

# Stadium IDs
NEUTRALIZATION_ZONE = 1247

ENERGY_IDS = {MIST, ENRICHING, SPIKY}
BASIC_IDS = {FAN_ROTOM, DUNSPARCE, BUNEARY}
EVOLUTION_IDS = {DUDUNSPARCE, LOPUNNY}
SUPPORTER_IDS = {BOSS, XEROSIC, HILDA, LILLIE, WALLY}

# Attack IDs
GALE_THRUST = 1225
SPIKY_HOPPER = 1226
TRADING_PLACES = 230
RAM = 231
RUN_AROUND = 1223
KICK = 1224

# Rule box and special categories
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

MEGA_EX_POKEMON = {
    652, 662, 678, 687, 695, 723, 737, 747, 754, 756, 766, 772, 781,
    790, 828, 849, 861, 868, 886, 896, 904, 919, 928, 932, 939, 1006,
    1031, 1040, 1056, 1064,
}

DAMAGE_PROTECTION_POKEMON = {
    117, 118, 345, 357, 401, 428, 442, 504, 525, 569, 637, 742, 748,
    755, 799, 824, 834, 851, 858, 866, 901, 924, 970, 994, 1024,
}

MIST_THREATS = {
    29, 32, 56, 94, 104, 112, 121, 215, 219, 223, 245, 247, 432,
    455, 593, 648, 738, 743, 817, 864, 876, 880, 982, 1058,
}

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

# Per-game tracking
LAST_TURN = None
TURN_START_ACTIVE = None
SEEN_MENUS: set[tuple[Any, ...]] = set()
ATTACK_DEFERRALS: dict[tuple[int, int], int] = {}
FORCE_READY_PROMOTION = False
WALLY_HEALED_SERIAL: int | None = None
WALLY_HEALED_WAS_ACTIVE = False
WALLY_RETREAT_WAS_AVAILABLE = False
MAX_ATTACK_DEFERRALS = 12


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def current(obs: dict[str, Any]) -> dict[str, Any]:
    return (obs or {}).get("current") or {}


def selection(obs: dict[str, Any]) -> dict[str, Any]:
    return (obs or {}).get("select") or {}


def players(state: dict[str, Any]) -> list[dict[str, Any]]:
    val = state.get("players") or []
    return val if isinstance(val, list) else []


def your_index(state: dict[str, Any]) -> int:
    val = state.get("yourIndex", 0)
    return val if val in (0, 1) else 0


def card_id(card: Any) -> int | None:
    if isinstance(card, dict):
        val = card.get("id")
        return int(val) if isinstance(val, int) else None
    if isinstance(card, int):
        return card
    return None


def zone_cards(state: dict[str, Any], player: int, area: int | None, select: dict[str, Any] | None = None) -> list[Any]:
    select = select or {}
    if area == 1:
        return select.get("deck") or []
    if area == 7:
        return state.get("stadium") or []
    if area == 12:
        return state.get("looking") or []
    pls = players(state)
    if player not in (0, 1) or player >= len(pls):
        return []
    key = {2: "hand", 3: "discard", 4: "active", 5: "bench", 6: "prize"}.get(area)
    return pls[player].get(key) or [] if key else []


def card_at(state: dict[str, Any], player: int, area: int | None, index: int | None, select: dict[str, Any] | None = None) -> dict[str, Any] | None:
    cards = zone_cards(state, player, area, select)
    if isinstance(index, int) and 0 <= index < len(cards):
        val = cards[index]
        return val if isinstance(val, dict) else None
    return None


def option_source(obs: dict[str, Any], option: dict[str, Any]) -> dict[str, Any] | None:
    st = current(obs)
    yi = your_index(st)
    owner = option.get("playerIndex", yi)
    area = option.get("area")
    if area is None and option.get("type") == 7:
        area = 2
    card = card_at(st, owner, area, option.get("index"), selection(obs))
    if not isinstance(card, dict):
        return card
    opt_type = option.get("type")
    if opt_type in (5, 6):
        energies = card.get("energyCards") or []
        e_idx = option.get("energyIndex")
        if isinstance(e_idx, int) and 0 <= e_idx < len(energies):
            energy = energies[e_idx]
            return energy if isinstance(energy, dict) else None
    if opt_type == 4:
        tools = card.get("tools") or []
        t_idx = option.get("toolIndex")
        if isinstance(t_idx, int) and 0 <= t_idx < len(tools):
            tool = tools[t_idx]
            return tool if isinstance(tool, dict) else None
    return card


def option_target(obs: dict[str, Any], option: dict[str, Any]) -> dict[str, Any] | None:
    st = current(obs)
    yi = your_index(st)
    owner = option.get("playerIndex", yi)
    return card_at(st, owner, option.get("inPlayArea"), option.get("inPlayIndex"), selection(obs))


def hand(state: dict[str, Any], player: int) -> list[Any]:
    return zone_cards(state, player, 2)


def hand_ids(state: dict[str, Any], player: int) -> list[int]:
    return [c for c in (card_id(card) for card in hand(state, player)) if c is not None]


def board(state: dict[str, Any], player: int) -> list[tuple[int, int, dict[str, Any]]]:
    result: list[tuple[int, int, dict[str, Any]]] = []
    for area in (4, 5):
        for index, card in enumerate(zone_cards(state, player, area)):
            if isinstance(card, dict):
                result.append((area, index, card))
    return result


def active(state: dict[str, Any], player: int) -> dict[str, Any] | None:
    cards = zone_cards(state, player, 4)
    return cards[0] if cards and isinstance(cards[0], dict) else None


def bench(state: dict[str, Any], player: int) -> list[dict[str, Any]]:
    return [card for card in zone_cards(state, player, 5) if isinstance(card, dict)]


def attached_count(card: dict[str, Any] | None) -> int:
    return len((card or {}).get("energyCards") or (card or {}).get("energies") or [])


def has_tool(card: dict[str, Any] | None, tool_id: int | None = None) -> bool:
    tools = (card or {}).get("tools") or []
    if tool_id is None:
        return bool(tools)
    return any(card_id(t) == tool_id for t in tools)


def hp(card: dict[str, Any] | None) -> int:
    return as_int((card or {}).get("hp"), 0)


def max_hp(card: dict[str, Any] | None) -> int:
    return as_int((card or {}).get("maxHp"), hp(card))


def damage_on(card: dict[str, Any] | None) -> int:
    return max(0, max_hp(card) - hp(card))


def prize_count(state: dict[str, Any], player: int) -> int:
    pls = players(state)
    if player < len(pls) and isinstance(pls[player].get("prize"), list):
        return len(pls[player]["prize"])
    return 6


def prize_value(card: dict[str, Any] | None) -> int:
    cid = card_id(card)
    if cid in MEGA_EX_POKEMON:
        return 3
    if cid in EX_POKEMON:
        return 2
    return 1


def bench_capacity(state: dict[str, Any], player: int) -> int:
    pls = players(state)
    if player >= len(pls):
        return 0
    limit = as_int(pls[player].get("benchMax"), 5)
    return max(0, limit - len(bench(state, player)))


def board_counts(state: dict[str, Any], player: int) -> dict[int, int]:
    counts: dict[int, int] = {}
    for _, _, card in board(state, player):
        cid = card_id(card)
        if cid is not None:
            counts[cid] = counts.get(cid, 0) + 1
    return counts


def stadium_id_in_play(state: dict[str, Any]) -> int | None:
    stadiums = state.get("stadium") or []
    if stadiums and isinstance(stadiums[0], dict):
        return card_id(stadiums[0])
    return None


def is_damage_immune(state: dict[str, Any], defender: dict[str, Any] | None) -> bool:
    if not isinstance(defender, dict):
        return False
    def_id = card_id(defender)
    if def_id in DAMAGE_PROTECTION_POKEMON:
        return True
    st_id = stadium_id_in_play(state)
    if st_id == NEUTRALIZATION_ZONE and def_id not in EX_POKEMON:
        return True
    return False


def reset_game_memory():
    global LAST_TURN, TURN_START_ACTIVE, SEEN_MENUS, ATTACK_DEFERRALS
    global FORCE_READY_PROMOTION, WALLY_HEALED_SERIAL, WALLY_HEALED_WAS_ACTIVE
    global WALLY_RETREAT_WAS_AVAILABLE
    LAST_TURN = None
    TURN_START_ACTIVE = None
    SEEN_MENUS = set()
    ATTACK_DEFERRALS = {}
    FORCE_READY_PROMOTION = False
    WALLY_HEALED_SERIAL = None
    WALLY_HEALED_WAS_ACTIVE = False
    WALLY_RETREAT_WAS_AVAILABLE = False


def reset_turn_memory(state: dict[str, Any]):
    global LAST_TURN, TURN_START_ACTIVE, SEEN_MENUS, ATTACK_DEFERRALS
    global FORCE_READY_PROMOTION, WALLY_HEALED_SERIAL, WALLY_HEALED_WAS_ACTIVE
    global WALLY_RETREAT_WAS_AVAILABLE
    turn = as_int(state.get("turn"), 0)
    yi = your_index(state)
    key = (turn, yi)
    act_card = active(state, yi)
    serial = act_card.get("serial") if isinstance(act_card, dict) else None
    if LAST_TURN != key:
        SEEN_MENUS = set()
        ATTACK_DEFERRALS = {}
        FORCE_READY_PROMOTION = False
        WALLY_HEALED_SERIAL = None
        WALLY_HEALED_WAS_ACTIVE = False
        WALLY_RETREAT_WAS_AVAILABLE = False
        LAST_TURN = key
        TURN_START_ACTIVE = serial


def active_moved_this_turn(state: dict[str, Any]) -> bool:
    yi = your_index(state)
    card = active(state, yi)
    serial = card.get("serial") if isinstance(card, dict) else None
    return bool(state.get("retreated")) or (
        TURN_START_ACTIVE is not None and serial is not None and serial != TURN_START_ACTIVE
    )


def lopunny_ready(card: dict[str, Any] | None, two_energy: bool = False) -> bool:
    if card_id(card) != LOPUNNY:
        return False
    needed = 2 if two_energy else 1
    return attached_count(card) >= needed


def best_lopunny(state: dict[str, Any], player: int, exclude_serial: int | None = None) -> Any:
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


def effective_lopunny_damage(state: dict[str, Any], attack_id: int | None) -> int:
    if attack_id == SPIKY_HOPPER:
        return 160
    if attack_id == GALE_THRUST:
        return 230 if active_moved_this_turn(state) else 60
    return 0


def current_attack_ceiling(state: dict[str, Any]) -> int:
    yi = your_index(state)
    card = active(state, yi)
    if card_id(card) != LOPUNNY or attached_count(card) < 1:
        return 0
    damage = 230 if active_moved_this_turn(state) else 60
    if attached_count(card) >= 2:
        damage = max(damage, 160)
    return damage


def current_attack_damage_against(state: dict[str, Any], target: dict[str, Any] | None) -> int:
    yi = your_index(state)
    attacker = active(state, yi)
    if card_id(attacker) != LOPUNNY or attached_count(attacker) < 1:
        return 0
    if is_damage_immune(state, target):
        return 160 if attached_count(attacker) >= 2 else 0
    return current_attack_ceiling(state)


def opponent_target_value(obs: dict[str, Any], card: dict[str, Any] | None, area: int | None) -> float:
    if not isinstance(card, dict):
        return -10000.0
    state = current(obs)
    yi = your_index(state)
    target_hp = hp(card)
    damage = current_attack_damage_against(state, card)
    prizes = prize_value(card)
    
    value = damage_on(card) * 3.0 + attached_count(card) * 100.0 + prizes * 300.0
    value += 40.0 if area == 4 else 0.0
    
    if damage and 0 < target_hp <= damage:
        value += 3000.0 + (prizes * 1000.0)
        if prizes >= prize_count(state, yi):
            value += 20000.0
    elif target_hp:
        value -= target_hp * 0.25
    return value


def choose_promotion_score(obs: dict[str, Any], card: dict[str, Any] | None, context: int | None) -> float:
    state = current(obs)
    yi = your_index(state)
    cid = card_id(card)
    energy = attached_count(card)
    if context == 4:
        pivot_tool_available = AIR_BALLOON in hand_ids(state, yi)
        if cid in (DUNSPARCE, BUNEARY) and (has_tool(card, AIR_BALLOON) or energy >= 1 or pivot_tool_available):
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


def setup_card_score(state: dict[str, Any], cid: int | None, context: int | None) -> float:
    yi = your_index(state)
    counts = board_counts(state, yi)
    if context == 1:
        return {DUNSPARCE: 5200.0, BUNEARY: 4200.0, FAN_ROTOM: 3400.0}.get(cid, 0.0)
    if cid == BUNEARY:
        return 4700.0 - counts.get(BUNEARY, 0) * 900.0 - counts.get(LOPUNNY, 0) * 350.0
    if cid == DUNSPARCE:
        return 4400.0 - counts.get(DUNSPARCE, 0) * 600.0 - counts.get(DUDUNSPARCE, 0) * 250.0
    if cid == FAN_ROTOM:
        first_turn = as_int(state.get("turn"), 0) <= 2
        return 4300.0 if first_turn and counts.get(FAN_ROTOM, 0) == 0 else 500.0
    return 0.0


def discard_keep_value(obs: dict[str, Any], card: dict[str, Any] | None, option: dict[str, Any]) -> float:
    state = current(obs)
    yi = your_index(state)
    cid = card_id(card)
    hand_now = hand_ids(state, yi)
    counts = board_counts(state, yi)
    index = option.get("index")
    duplicate_rank = sum(1 for val in hand_now[:index] if val == cid) if isinstance(index, int) else 0
    value = 100.0
    
    # Check if we need energy / draw lifeline
    active_unpowered = attached_count(active(state, yi)) == 0
    has_energy_in_hand = any(c in ENERGY_IDS for c in hand_now)
    need_draw_lifeline = active_unpowered or not has_energy_in_hand

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
        value = 1400.0 if need_draw_lifeline else (760.0 if counts.get(BUNEARY, 0) else 220.0)
    elif cid == LILLIE:
        value = 1350.0 if need_draw_lifeline else 420.0
    elif cid == WALLY:
        lopunny_lines = counts.get(BUNEARY, 0) + counts.get(LOPUNNY, 0)
        damaged_lopunny = any(damage_on(c) >= 80 for _, _, c in board(state, yi) if card_id(c) == LOPUNNY)
        value = 1100.0 if damaged_lopunny else (760.0 if lopunny_lines else 180.0)
    elif cid == BOSS:
        value = 520.0
    elif cid == XEROSIC:
        opp = 1 - yi
        ps = players(state)
        opp_hand = as_int(ps[opp].get("handCount"), 0) if opp < len(ps) else 0
        value = 250.0 if need_draw_lifeline else (680.0 if opp_hand >= 6 else 100.0)
    elif cid in (POFFIN, POKE_PAD, ULTRA_BALL):
        value = 380.0 if bench_capacity(state, yi) else 60.0
    elif cid == POKEGEAR:
        value = 220.0
    if duplicate_rank:
        value -= duplicate_rank * 140.0
    return value


def search_card_score(obs: dict[str, Any], cid: int | None, effect_id: int | None, context: int | None) -> float:
    state = current(obs)
    yi = your_index(state)
    counts = board_counts(state, yi)
    held = hand_ids(state, yi)

    if effect_id == FAN_ROTOM or effect_id == POFFIN:
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
        return supporter_value(obs, cid, from_search=True)
    if cid in EVOLUTION_IDS:
        return 3000.0
    if cid in ENERGY_IDS:
        return 2400.0
    if cid in BASIC_IDS:
        return setup_card_score(state, cid, 2)
    return 200.0


def energy_available_after_wally(state: dict[str, Any], target: dict[str, Any] | None) -> bool:
    yi = your_index(state)
    return attached_count(target) > 0 or any(cid in ENERGY_IDS for cid in hand_ids(state, yi))


def wally_target_value(state: dict[str, Any], card: dict[str, Any] | None, area: int | None, retreat_available: bool = False) -> float:
    if card_id(card) != LOPUNNY:
        return -12000.0
    damage = damage_on(card)
    if damage < 80:
        return -5000.0

    yi = your_index(state)
    if area == 5:
        return 6500.0 + damage * 12.0 + attached_count(card) * 250.0

    if area != 4:
        return -12000.0

    ready_bench = any(lopunny_ready(c) for c in bench(state, yi))
    spiky_ready_bench = any(lopunny_ready(c, two_energy=True) for c in bench(state, yi))
    bench_lopunny = any(card_id(c) == LOPUNNY for c in bench(state, yi))
    can_attach = not bool(state.get("energyAttached"))
    energy_after = energy_available_after_wally(state, card)
    free_retreat = has_tool(card, AIR_BALLOON)
    can_retreat = not bool(state.get("retreated"))
    protection_break_needed = is_damage_immune(state, active(state, 1 - yi))

    if protection_break_needed:
        coherent = retreat_available and can_retreat and free_retreat and spiky_ready_bench
    else:
        coherent = (
            (can_attach and energy_after)
            or (retreat_available and can_retreat and free_retreat and ready_bench)
            or (retreat_available and can_retreat and free_retreat and can_attach and energy_after and bench_lopunny)
        )
    if not coherent:
        return -9000.0
    return 6800.0 + damage * 13.0 + attached_count(card) * 180.0


def supporter_value(obs: dict[str, Any], cid: int | None, from_search: bool = False) -> float:
    state = current(obs)
    yi = your_index(state)
    opp = 1 - yi
    ps = players(state)
    opp_hand = as_int(ps[opp].get("handCount"), 0) if opp < len(ps) else 0
    counts = board_counts(state, yi)
    cards_in_hand = len(hand(state, yi))
    opponent_bench = bench(state, opp)
    
    boss_targets = [c for c in opponent_bench if 0 < hp(c) <= current_attack_damage_against(state, c)]
    boss_ko = bool(boss_targets)

    if cid == BOSS:
        if boss_ko:
            best_prizes = max(prize_value(c) for c in boss_targets)
            best_dmg = max(damage_on(c) for c in boss_targets)
            value = 6500.0 + best_prizes * 800.0 + best_dmg * 6.0
            if best_prizes >= prize_count(state, yi):
                value += 20000.0
        elif opponent_bench:
            value = 3200.0
        else:
            value = 200.0
    elif cid == WALLY:
        retreat_available = any(option.get("type") == 12 for option in selection(obs).get("option") or [])
        values = [wally_target_value(state, card, area, retreat_available) for area, _, card in board(state, yi)]
        value = max(values, default=-9000.0)
    elif cid == HILDA:
        missing_lopunny = counts.get(BUNEARY, 0) > hand_ids(state, yi).count(LOPUNNY)
        unpowered = any(card_id(card) in (BUNEARY, LOPUNNY) and attached_count(card) < 1 for _, _, card in board(state, yi))
        value = 5800.0 if (missing_lopunny or unpowered) else 1200.0
    elif cid == XEROSIC:
        value = 900.0 + max(0, opp_hand - 3) * 500.0
        if opp_hand <= 4:
            value = 150.0
    elif cid == LILLIE:
        own_prizes = prize_count(state, yi)
        draw_to = 8 if own_prizes == 6 else 6
        value = 3200.0 + max(0, draw_to - cards_in_hand) * 600.0
        if cards_in_hand > draw_to + 2:
            value = 200.0
    else:
        value = 100.0
    return value + (250.0 if from_search else 0.0)


def main_play_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
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


def attach_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
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
            ready_bench = any(lopunny_ready(c) for c in bench(state, yi))
            score += 3500.0 if ready_bench else 500.0
        if target_id == LOPUNNY:
            score += 900.0
        elif target_id in (DUNSPARCE, BUNEARY):
            score += 700.0
        return score

    if cid not in ENERGY_IDS:
        return 200.0
    if bool(state.get("energyAttached")) and option.get("area") == 2:
        return -4000.0
        
    our_active = active(state, yi)
    opposing_active = active(state, 1 - yi)
    protection_break_needed = is_damage_immune(state, opposing_active)
    energy_count = attached_count(target)
    turn_num = as_int(state.get("turn"), 0)

    # Core Invariant 1: Trapped Active Support Escape Rule
    # If active is Dunsparce/Fan Rotom with 0E and NO Balloon, and bench has ready/readying Lopunny:
    # Attaching 1 energy to active lets it pay 1-retreat cost to promote the attacker!
    if area == 4 and target_id in (DUNSPARCE, FAN_ROTOM) and energy_count == 0:
        bench_has_ready_lopunny = any(lopunny_ready(c) for c in bench(state, yi))
        if bench_has_ready_lopunny and not has_tool(our_active, AIR_BALLOON) and not bool(state.get("retreated")):
            return 6800.0 # Enable retreat!

    # Core Invariant 2: Enriching Energy on Turn 1 (or when no attacker can strike this turn) gives draw acceleration!
    attacker_can_strike = turn_num >= 2 and any(
        (card_id(c) == LOPUNNY or (card_id(c) == BUNEARY and LOPUNNY in hand_ids(state, yi)))
        for _, _, c in board(state, yi)
    )

    if target_id not in (BUNEARY, LOPUNNY):
        if cid == ENRICHING and target_id in (DUNSPARCE, FAN_ROTOM) and energy_count == 0:
            if attacker_can_strike and card_id(our_active) in (BUNEARY, LOPUNNY) and attached_count(our_active) == 0:
                return -2000.0 # Force attacker power on Turn 2+!
            stadium_live = bool(state.get("stadium"))
            return 7100.0 + (500.0 if target_id == FAN_ROTOM and stadium_live else 0.0)
        return 500.0 if target_id in (DUNSPARCE, FAN_ROTOM) else -800.0

    if energy_count >= 2:
        return -2500.0

    score = 3900.0
    if cid == ENRICHING:
        score += 1800.0
    elif cid == MIST:
        threat = card_id(opposing_active) in MIST_THREATS
        score += 1500.0 if threat else 350.0
    elif cid == SPIKY:
        score += 900.0
        
    if energy_count == 0:
        score += 1800.0
    else:
        score += 650.0
        
    if area == 4:
        score += 450.0

    target_serial = target.get("serial") if isinstance(target, dict) else None
    active_serial = our_active.get("serial") if isinstance(our_active, dict) else None
    
    if WALLY_HEALED_SERIAL is not None:
        if WALLY_HEALED_WAS_ACTIVE and active_serial == WALLY_HEALED_SERIAL:
            ready_bench = any(lopunny_ready(card) for card in bench(state, yi))
            if (
                has_tool(our_active, AIR_BALLOON)
                and not bool(state.get("retreated"))
                and any(candidate.get("type") == 12 for candidate in selection(obs).get("option") or [])
                and area == 5
                and target_id == LOPUNNY
                and energy_count == 0
            ):
                score += 9000.0
            elif area == 4 and target_serial == WALLY_HEALED_SERIAL:
                score += 5200.0 if ready_bench else 7200.0
        elif not WALLY_HEALED_WAS_ACTIVE and target_serial == WALLY_HEALED_SERIAL and area == 5:
            score += 4200.0

    pivot_ko_window = not protection_break_needed and 160 < hp(opposing_active) <= 230
    if area == 4 and target_id == LOPUNNY and energy_count == 1:
        if protection_break_needed:
            score += 6800.0
        elif not pivot_ko_window:
            score += 2800.0
            
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


def evolution_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    state = current(obs)
    yi = your_index(state)
    counts = board_counts(state, yi)
    moving = option_source(obs, option)
    target = option_target(obs, option)
    cid = card_id(moving)
    if cid == DUDUNSPARCE and card_id(target) == DUNSPARCE:
        attack_available = any(choice.get("type") == 13 for choice in selection(obs).get("option") or [])
        if option.get("inPlayArea") == 4 and attack_available and not any(lopunny_ready(card) for card in bench(state, yi)):
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


def ability_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    state = current(obs)
    yi = your_index(state)
    source = option_source(obs, option)
    cid = card_id(source)
    area = option.get("area")
    
    if cid == DUDUNSPARCE:
        pls = players(state)
        deck_count = as_int(pls[yi].get("deckCount"), 20) if yi < len(pls) else 20
        if deck_count <= 2:
            return -10000.0 # Anti-deck-out safeguard
            
        if area == 5:
            switching_active = card_id(active(state, yi)) in (DUNSPARCE, BUNEARY)
            attack_available = any(choice.get("type") == 13 for choice in selection(obs).get("option") or [])
            if switching_active and attack_available and len(bench(state, yi)) <= 1:
                return -12000.0
            return 7200.0
        if any(lopunny_ready(card) for card in bench(state, yi)):
            return 7400.0
        return -12000.0
    if cid == FAN_ROTOM:
        return 6800.0
    return 1800.0


def retreat_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    state = current(obs)
    yi = your_index(state)
    if bool(state.get("retreated")):
        return -5000.0
    act_card = active(state, yi)
    active_serial = act_card.get("serial") if isinstance(act_card, dict) else None
    best = best_lopunny(state, yi, exclude_serial=active_serial)
    opposing_active = active(state, 1 - yi)
    protection_break_needed = is_damage_immune(state, opposing_active)
    
    if best and best[0]:
        if protection_break_needed and not best[1]:
            return -12000.0
        score = 7600.0
        if card_id(act_card) == LOPUNNY:
            score += damage_on(act_card) * 3.0
        return score
    if card_id(act_card) != LOPUNNY:
        any_ready = best_lopunny(state, yi)
        if any_ready and any_ready[0]:
            return 7000.0
    return -12000.0


def attack_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    state = current(obs)
    yi = your_index(state)
    our_active = active(state, yi)
    attack_id = option.get("attackId")
    opponent = active(state, 1 - yi)
    opponent_hp = hp(opponent)
    opponent_immune = is_damage_immune(state, opponent)

    if card_id(our_active) == LOPUNNY:
        damage = effective_lopunny_damage(state, attack_id)
        score = 4300.0 + damage * 9.0
        
        if opponent_immune:
            if attack_id == SPIKY_HOPPER:
                score += 5500.0
            else:
                score -= 6500.0 # Gale Thrust deals 0 damage against protected targets
                
        if not opponent_immune and 0 < opponent_hp <= damage:
            score += 6200.0
            prizes = prize_value(opponent)
            score += prizes * 1100.0
            if prizes >= prize_count(state, yi):
                score += 15000.0
        if attack_id == GALE_THRUST and not active_moved_this_turn(state):
            score -= 1600.0
        if attack_id == SPIKY_HOPPER and attached_count(our_active) >= 2:
            score += 500.0
        return score
    if attack_id in (TRADING_PLACES, RUN_AROUND):
        return 3300.0 if any(lopunny_ready(c) for c in bench(state, yi)) else 900.0
    if attack_id in (RAM, KICK):
        return 1800.0
    return 1300.0


def target_selection_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    state = current(obs)
    select = selection(obs)
    yi = your_index(state)
    context = select.get("context")
    owner = option.get("playerIndex", yi)
    area = option.get("area")
    card = option_source(obs, option)
    cid = card_id(card)
    effect_id = card_id(select.get("effect"))

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
            return wally_target_value(state, card, area, WALLY_RETREAT_WAS_AVAILABLE)
        return 1000.0 + (attached_count(card) * 300.0) + hp(card)

    if area in (1, 2, 3, 12):
        return search_card_score(obs, cid, effect_id, context)
    return 0.0


def energy_discard_score(obs: dict[str, Any], option: dict[str, Any]) -> float:
    energy = option_source(obs, option)
    cid = card_id(energy)
    return {ENRICHING: 5200.0, SPIKY: 4300.0, MIST: 3500.0}.get(cid, 2500.0)


def menu_signature(obs: dict[str, Any]) -> tuple[Any, ...]:
    state = current(obs)
    select = selection(obs)
    yi = your_index(state)
    act_card = active(state, yi)
    return (
        as_int(state.get("turn"), 0),
        as_int(state.get("turnActionCount"), 0),
        bool(state.get("supporterPlayed")),
        bool(state.get("energyAttached")),
        card_id(act_card),
        act_card.get("serial") if isinstance(act_card, dict) else None,
        tuple(
            (
                option.get("type"), option.get("area"), option.get("index"),
                option.get("inPlayArea"), option.get("inPlayIndex"),
                option.get("attackId"), option.get("energyIndex"),
            )
            for option in select.get("option") or []
        ),
    )


def score_option(obs: dict[str, Any], option: dict[str, Any]) -> float:
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


def choose_action(obs: dict[str, Any]) -> list[int]:
    if not isinstance(obs, dict) or obs.get("select") is None:
        reset_game_memory()
        return EXPECTED_DECK[:]
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

    if selection(obs).get("context") == 5 and maximum > 1:
        chosen: list[int] = []
        chosen_ids: dict[int | None, int] = {}
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


def safe_action(obs: dict[str, Any]) -> list[int]:
    global FORCE_READY_PROMOTION, WALLY_HEALED_SERIAL, WALLY_HEALED_WAS_ACTIVE
    global WALLY_RETREAT_WAS_AVAILABLE
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
            if option.get("type") == 7 and card_id(option_source(obs, option)) == WALLY:
                WALLY_RETREAT_WAS_AVAILABLE = any(candidate.get("type") == 12 for candidate in options)
            if select.get("context") == 17:
                target = option_source(obs, option)
                if card_id(target) == LOPUNNY:
                    WALLY_HEALED_SERIAL = target.get("serial") if isinstance(target, dict) else None
                    WALLY_HEALED_WAS_ACTIVE = option.get("area") == 4
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
            return EXPECTED_DECK[:]
        options = select.get("option") or []
        minimum = as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(options))))


def agent(obs: dict[str, Any], proc: Any = None) -> list[int]:
    return safe_action(obs)
