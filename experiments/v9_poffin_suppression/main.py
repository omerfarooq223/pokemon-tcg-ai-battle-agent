"""Local one-change screen: refuse provably empty Buddy-Buddy Poffin plays."""

from __future__ import annotations

import copy
import importlib.util
import os


_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "v9_discard_only",
    "main.py",
)
_SPEC = importlib.util.spec_from_file_location("v9_poffin_base", _BASE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Unable to load the discard-only V9 comparator")
_base = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_base)

DECK = _base.DECK
POFFIN_ID = 1086
DWEBBLE_ID = 344
DWEBBLE_COPIES = 4


def _visible_copy_count(state, player, wanted_id):
    players = _base.players(state)
    if player < 0 or player >= len(players):
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
        count = 1 if _base.card_id(card) == wanted_id else 0
        for prior in card.get("preEvolution") or []:
            count += count_card(prior)
        return count

    total = 0
    player_state = players[player]
    for zone in ("active", "bench", "hand", "discard", "prize"):
        for card in player_state.get(zone) or []:
            total += count_card(card)
    return total


def _poffin_can_progress(obs):
    state = _base.current_state(obs)
    yi = _base.your_index(state)
    players = _base.players(state)
    if yi >= len(players):
        return False
    player = players[yi]
    bench = player.get("bench") or []
    if len(bench) >= _base.as_int(player.get("benchMax"), 5):
        return False
    deck_count = player.get("deckCount")
    if deck_count is not None and _base.as_int(deck_count, 0) <= 0:
        return False
    visible_deck = player.get("deck")
    if isinstance(visible_deck, list) and visible_deck:
        return any(_base.card_id(card) == DWEBBLE_ID for card in visible_deck)
    return _visible_copy_count(state, yi, DWEBBLE_ID) < DWEBBLE_COPIES


def choose_action(obs):
    select = _base.select_state(obs)
    options = select.get("option") or []
    poffin_indexes = [
        index
        for index, option in enumerate(options)
        if option.get("type") == 7
        and _base.card_id(_base.option_card(obs, option)) == POFFIN_ID
    ]
    if not poffin_indexes or _poffin_can_progress(obs):
        return _base.choose_action(obs)

    kept_indexes = [
        index for index in range(len(options)) if index not in set(poffin_indexes)
    ]
    if len(kept_indexes) < _base.as_int(select.get("minCount"), 0):
        return _base.choose_action(obs)

    filtered = copy.deepcopy(obs)
    filtered["select"]["option"] = [options[index] for index in kept_indexes]
    chosen = _base.choose_action(filtered)
    return [kept_indexes[index] for index in chosen]


def safe_action(obs):
    try:
        return choose_action(obs)
    except Exception:
        select = obs.get("select") if isinstance(obs, dict) else None
        if select is None:
            return DECK[:]
        minimum = _base.as_int(select.get("minCount"), 0)
        return list(range(min(minimum, len(select.get("option") or []))))


def agent(obs):
    return safe_action(obs)
