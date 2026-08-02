#!/usr/bin/env python3
"""Counterfactual evaluation of an agent against every saved replay.

The local battle API does not expose Kaggle's replay seed or the submitted
opponent source.  This harness therefore preserves everything that is
reconstructable:

* the replay's replacement seat;
* the opponent's exact submitted 60-card deck;
* the opponent's recorded semantic action sequence whenever the new state
  still offers equivalent actions.

When the counterfactual trajectory diverges, the opponent falls back to the
project's legal generic attack-first policy.  Script/fallback counts are
reported so the fidelity limitation remains visible in every result.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "competition_data" / "sample_submission" / "sample_submission"
sys.path.insert(0, str(SAMPLE_DIR))

from cg.game import battle_finish, battle_select, battle_start  # noqa: E402


OUR_TEAMS = frozenset({"MUHAMMAD UMER FAROOQ", "ROASTERS"})
DECK_ACTION_SIZE = 60
RESULT_REASON = {
    1: "prizes",
    2: "deck_out",
    3: "no_active_pokemon",
    4: "card_effect",
}


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_agent(agent_dir: Path, module_name: str):
    return load_module(agent_dir / "main.py", module_name).agent


def read_deck(path: Path) -> list[int]:
    cards = [
        int(line.strip().split(",")[0])
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(cards) != DECK_ACTION_SIZE:
        raise ValueError(f"{path} has {len(cards)} cards; expected 60")
    return cards


def replay_files(corpus: Path) -> list[Path]:
    return sorted(
        path
        for path in corpus.glob("**/*.json")
        if path.name != "corpus_summary.json"
    )


def load_unique_replays(corpus: Path) -> list[tuple[int, Path, dict]]:
    unique: dict[int, tuple[Path, dict]] = {}
    for path in replay_files(corpus):
        replay = json.loads(path.read_text())
        episode_id = int((replay.get("info") or {}).get("EpisodeId") or path.stem)
        if episode_id in unique:
            raise ValueError(
                f"Duplicate replay episode {episode_id}: "
                f"{unique[episode_id][0]} and {path}"
            )
        unique[episode_id] = (path, replay)
    return [
        (episode_id, path, replay)
        for episode_id, (path, replay) in sorted(unique.items())
    ]


def replay_deck(replay: dict, player: int) -> list[int]:
    for step in replay.get("steps") or []:
        if player >= len(step):
            continue
        action = step[player].get("action")
        if isinstance(action, list) and len(action) == DECK_ACTION_SIZE:
            return [int(card) for card in action]
    raise ValueError(f"Replay has no 60-card deck action for player {player}")


def replacement_seat(
    replay: dict,
    team_aliases: set[str] | frozenset[str] | None = None,
    public_replacement: str = "loser",
) -> tuple[int, str]:
    aliases = OUR_TEAMS if team_aliases is None else team_aliases
    teams = (replay.get("info") or {}).get("TeamNames") or []
    for seat, team in enumerate(teams[:2]):
        if team in aliases:
            kind = "our_agent" if team in OUR_TEAMS else "configured_team"
            return seat, kind
    if public_replacement == "seat0":
        return 0, "public_seat0"
    if public_replacement == "seat1":
        return 1, "public_seat1"
    if public_replacement != "loser":
        raise ValueError(
            "public_replacement must be one of: loser, seat0, seat1"
        )
    rewards = replay.get("rewards") or []
    if len(rewards) >= 2 and rewards[0] != rewards[1]:
        return (0 if rewards[0] < rewards[1] else 1), "public_loser"
    return 0, "public_seat0"


def replay_first_player(replay: dict) -> int | None:
    """Return the first-player seat recorded by Kaggle, when observable."""
    for step in replay.get("steps") or []:
        for row in step[:2]:
            current = ((row.get("observation") or {}).get("current") or {})
            first_player = current.get("firstPlayer")
            if first_player in (0, 1):
                return int(first_player)
    return None


def card_id(card: Any) -> int | None:
    if isinstance(card, dict):
        value = card.get("id")
        return int(value) if isinstance(value, int) else value
    if isinstance(card, int):
        return card
    return None


def current_state(obs: dict) -> dict:
    return (obs or {}).get("current") or {}


def select_state(obs: dict) -> dict:
    return (obs or {}).get("select") or {}


def zone_cards(obs: dict, player: int, area: int | None) -> list:
    state = current_state(obs)
    select = select_state(obs)
    if area == 1:
        return select.get("deck") or []
    if area == 7:
        return state.get("stadium") or []
    if area == 12:
        return state.get("looking") or []
    players = state.get("players") or []
    if player not in (0, 1) or player >= len(players):
        return []
    zone = {
        2: "hand",
        3: "discard",
        4: "active",
        5: "bench",
        6: "prize",
    }.get(area)
    return players[player].get(zone) or [] if zone else []


def option_source_card(obs: dict, option: dict) -> Any:
    state = current_state(obs)
    player = option.get("playerIndex", state.get("yourIndex", 0))
    area = option.get("area")
    if area is None and option.get("type") == 7:
        area = 2
    index = option.get("index")
    cards = zone_cards(obs, player, area)
    if isinstance(index, int) and 0 <= index < len(cards):
        card = cards[index]
        if not isinstance(card, dict):
            return card
        option_type = option.get("type")
        if option_type == 4:
            tool_index = option.get("toolIndex")
            tools = card.get("tools") or []
            if isinstance(tool_index, int) and 0 <= tool_index < len(tools):
                return tools[tool_index]
        if option_type in (5, 6):
            energy_index = option.get("energyIndex")
            energies = card.get("energyCards") or []
            if isinstance(energy_index, int) and 0 <= energy_index < len(energies):
                return energies[energy_index]
        return card
    return None


def option_target_card(obs: dict, option: dict) -> Any:
    state = current_state(obs)
    player = option.get("playerIndex", state.get("yourIndex", 0))
    area = option.get("inPlayArea")
    index = option.get("inPlayIndex")
    cards = zone_cards(obs, player, area)
    if isinstance(index, int) and 0 <= index < len(cards):
        return cards[index]
    return None


def option_feature(obs: dict, option: dict) -> dict[str, Any]:
    source = option_source_card(obs, option)
    target = option_target_card(obs, option)
    return {
        "type": option.get("type"),
        "source_id": card_id(source),
        "source_serial": source.get("serial") if isinstance(source, dict) else None,
        "source_area": (
            2
            if option.get("area") is None and option.get("type") == 7
            else option.get("area")
        ),
        "target_id": card_id(target),
        "target_serial": target.get("serial") if isinstance(target, dict) else None,
        "target_area": option.get("inPlayArea"),
        "attack_id": option.get("attackId"),
        "energy_index": option.get("energyIndex"),
        "tool_index": option.get("toolIndex"),
        "number": option.get("number"),
        "card_id": option.get("cardId"),
        "special": option.get("specialConditionType"),
        "count": option.get("count"),
    }


def decision_signature(obs: dict) -> tuple[Any, ...]:
    select = select_state(obs)
    effect = select.get("effect")
    context_card = select.get("contextCard")
    return (
        select.get("context"),
        card_id(effect),
        card_id(context_card),
        select.get("minCount"),
        select.get("maxCount"),
    )


@dataclass
class RecordedDecision:
    signature: tuple[Any, ...]
    features: list[dict[str, Any]]
    turn: int


def recorded_decisions(replay: dict, player: int) -> list[RecordedDecision]:
    """Pair active observations with the same player's following-step action."""
    steps = replay.get("steps") or []
    decisions: list[RecordedDecision] = []
    for step_index in range(len(steps) - 1):
        if player >= len(steps[step_index]) or player >= len(steps[step_index + 1]):
            continue
        row = steps[step_index][player]
        if row.get("status") != "ACTIVE":
            continue
        obs = row.get("observation") or {}
        select = obs.get("select")
        action = steps[step_index + 1][player].get("action")
        if not isinstance(select, dict) or not isinstance(action, list):
            continue
        options = select.get("option") or []
        if not options:
            continue
        if any(not isinstance(index, int) or index < 0 or index >= len(options) for index in action):
            continue
        decisions.append(
            RecordedDecision(
                signature=decision_signature(obs),
                features=[option_feature(obs, options[index]) for index in action],
                turn=int((obs.get("current") or {}).get("turn") or 0),
            )
        )
    return decisions


def feature_similarity(recorded: dict[str, Any], live: dict[str, Any]) -> float:
    if recorded.get("type") != live.get("type"):
        return -1000.0
    score = 10.0
    weights = {
        "source_id": 18.0,
        "source_serial": 4.0,
        "target_id": 13.0,
        "target_serial": 3.0,
        "attack_id": 24.0,
        "source_area": 3.0,
        "target_area": 3.0,
        "number": 7.0,
        "card_id": 7.0,
        "special": 7.0,
        "count": 2.0,
        "tool_index": 1.0,
    }
    for key, weight in weights.items():
        expected = recorded.get(key)
        actual = live.get(key)
        if expected is None:
            continue
        score += weight if expected == actual else -weight * 0.8
    return score


def signature_similarity(recorded: tuple[Any, ...], live: tuple[Any, ...]) -> float:
    score = 0.0
    weights = (15.0, 24.0, 12.0, 3.0, 3.0)
    for expected, actual, weight in zip(recorded, live, weights):
        if expected is None:
            continue
        score += weight if expected == actual else -weight
    return score


class ReplayOpponent:
    """Replay-semantic opponent with a legal generic fallback."""

    def __init__(
        self,
        deck: list[int],
        decisions: list[RecordedDecision],
        fallback_module,
        mode: str,
    ):
        self.deck = deck
        self.decisions = decisions
        self.fallback_module = fallback_module
        self.mode = mode
        self.pointer = 0
        self.stats = Counter()

    def _fallback(self, obs: dict) -> list[int]:
        self.stats["fallback_decisions"] += 1
        return self.fallback_module.choose_action(obs)

    def _candidate_decisions(self, obs: dict) -> list[tuple[float, int, RecordedDecision]]:
        live_signature = decision_signature(obs)
        start = max(0, self.pointer - 3)
        stop = min(len(self.decisions), self.pointer + 32)
        candidates = []
        live_types = {
            option.get("type")
            for option in (select_state(obs).get("option") or [])
        }
        live_minimum = int(select_state(obs).get("minCount") or 0)
        live_turn = int(current_state(obs).get("turn") or 0)
        for index in range(start, stop):
            decision = self.decisions[index]
            # Only call an action replay-semantic when the selection contract
            # itself is identical. Similar menus from a diverged trajectory
            # belong to the state-driven fallback, not the fidelity count.
            if decision.signature != live_signature:
                continue
            if decision.features and not any(
                feature.get("type") in live_types
                for feature in decision.features
            ):
                continue
            if not decision.features and live_minimum != 0:
                continue
            score = signature_similarity(decision.signature, live_signature)
            score -= abs(decision.turn - live_turn) * 0.35
            score -= abs(index - self.pointer) * 0.25
            candidates.append((score, index, decision))
        return sorted(candidates, key=lambda item: (-item[0], item[1]))

    def _map_decision(
        self, obs: dict, decision: RecordedDecision
    ) -> tuple[list[int], float, bool]:
        select = select_state(obs)
        options = select.get("option") or []
        live_features = [option_feature(obs, option) for option in options]
        available = set(range(len(options)))
        mapped = []
        scores = []
        for recorded in decision.features:
            ranked = sorted(
                (
                    (feature_similarity(recorded, live_features[index]), index)
                    for index in available
                ),
                key=lambda item: (-item[0], item[1]),
            )
            if not ranked or ranked[0][0] < 8.0:
                continue
            score, index = ranked[0]
            mapped.append(index)
            scores.append(score)
            available.remove(index)
        minimum = int(select.get("minCount") or 0)
        maximum = int(select.get("maxCount") or 0)
        # Never turn a non-empty recorded action into an empty or partial live
        # action. The old minCount-only check accepted false scripted skips.
        if len(mapped) != len(decision.features):
            return [], -1000.0, False
        if len(mapped) < minimum or len(mapped) > maximum:
            return [], -1000.0, False
        # A recorded empty optional selection is exact after the signature
        # check. Non-empty actions must pass the semantic confidence gate.
        confidence = min(scores) if scores else 100.0
        return mapped, confidence, True

    def choose_action(self, obs: dict) -> list[int]:
        if not isinstance(obs, dict) or obs.get("select") is None:
            return self.deck[:]
        if self.mode == "generic" or not self.decisions:
            return self._fallback(obs)
        candidates = self._candidate_decisions(obs)
        for alignment_score, index, decision in candidates[:8]:
            if alignment_score < -12.0:
                break
            mapped, confidence, valid = self._map_decision(obs, decision)
            if valid and confidence >= 40.0:
                self.pointer = index + 1
                self.stats["scripted_decisions"] += 1
                self.stats["high_confidence_scripted"] += 1
                return mapped
        return self._fallback(obs)

    def __call__(self, obs: dict) -> list[int]:
        try:
            return self.choose_action(obs)
        except Exception:
            self.stats["opponent_exceptions"] += 1
            return self._fallback(obs)


def validate_action(obs: dict, action: Any) -> list[int]:
    select = select_state(obs)
    options = select.get("option") or []
    minimum = int(select.get("minCount") or 0)
    maximum = int(select.get("maxCount") or 0)
    if not isinstance(action, list):
        raise TypeError(f"Agent returned {type(action).__name__}, expected list")
    if len(action) < minimum or len(action) > maximum:
        raise ValueError(
            f"Invalid selection length {len(action)}; expected {minimum}..{maximum}"
        )
    if len(action) != len(set(action)):
        raise ValueError("Agent returned duplicate option indexes")
    if any(not isinstance(index, int) or index < 0 or index >= len(options) for index in action):
        raise IndexError("Agent returned an out-of-range option index")
    return action


def summarize_card(card: Any) -> dict | None:
    if not isinstance(card, dict):
        return None
    return {
        "id": card.get("id"),
        "hp": card.get("hp"),
        "maxHp": card.get("maxHp"),
        "energies": card.get("energies") or [],
        "tools": [card_id(tool) for tool in card.get("tools") or []],
    }


def summarize_state(obs: dict) -> dict:
    state = current_state(obs)
    summaries = []
    for player in state.get("players") or []:
        summaries.append(
            {
                "active": [summarize_card(card) for card in player.get("active") or []],
                "bench": [summarize_card(card) for card in player.get("bench") or []],
                "deckCount": player.get("deckCount"),
                "discard": [card_id(card) for card in player.get("discard") or []],
                "prizeCount": len(player.get("prize") or []),
                "handCount": player.get("handCount"),
            }
        )
    return {
        "turn": state.get("turn"),
        "yourIndex": state.get("yourIndex"),
        "firstPlayer": state.get("firstPlayer"),
        "result": state.get("result"),
        "players": summaries,
    }


def selected_features(obs: dict, action: list[int]) -> list[dict[str, Any]]:
    options = select_state(obs).get("option") or []
    return [
        option_feature(obs, options[index])
        for index in action
        if 0 <= index < len(options)
    ]


def run_one(
    primary_agent,
    primary_deck: list[int],
    opponent: ReplayOpponent,
    opponent_deck: list[int],
    primary_seat: int,
    max_decisions: int,
    capture_trace: bool,
    forced_first_player: int | None = None,
) -> tuple[int | None, dict, list[dict]]:
    agents = (
        (primary_agent, opponent)
        if primary_seat == 0
        else (opponent, primary_agent)
    )
    decks = (
        (primary_deck, opponent_deck)
        if primary_seat == 0
        else (opponent_deck, primary_deck)
    )
    obs, start = battle_start(decks[0], decks[1])
    if obs is None:
        raise RuntimeError(
            f"Battle failed: player={start.errorPlayer} error={start.errorType}"
        )

    trace = []
    stats: dict[str, Any] = {
        "decisions": 0,
        "primary_decisions": 0,
        "opponent_decisions": 0,
        "primary_attack_menus": 0,
        "primary_attacks": 0,
        "primary_attack_turns": set(),
        "primary_attacked_turns": set(),
        "primary_first_attack_turn": None,
        "primary_selected_types": Counter(),
        "opponent_selected_types": Counter(),
        "result_reason": "unknown",
        "terminal_state": None,
        "timed_out": False,
        "forced_first_player_decisions": 0,
    }
    try:
        for decision_number in range(1, max_decisions + 1):
            state = current_state(obs)
            player = state.get("yourIndex")
            if player not in (0, 1):
                raise RuntimeError(f"Invalid selecting player: {player}")
            select = select_state(obs)
            options = select.get("option") or []
            action = validate_action(obs, agents[player](obs))
            if (
                forced_first_player in (0, 1)
                and select.get("context") == 41
                and player == 0
            ):
                desired_type = 1 if forced_first_player == 0 else 2
                forced = [
                    index
                    for index, option in enumerate(options)
                    if option.get("type") == desired_type
                ]
                if forced:
                    action = validate_action(obs, [forced[0]])
                    stats["forced_first_player_decisions"] += 1
            features = selected_features(obs, action)
            stats["decisions"] += 1
            role = "primary" if player == primary_seat else "opponent"
            stats[f"{role}_decisions"] += 1
            stats[f"{role}_selected_types"].update(
                feature.get("type") for feature in features
            )
            if player == primary_seat:
                attacks = [
                    index
                    for index, option in enumerate(options)
                    if option.get("type") == 13
                ]
                if attacks:
                    turn = state.get("turn")
                    stats["primary_attack_menus"] += 1
                    stats["primary_attack_turns"].add(turn)
                    if any(index in attacks for index in action):
                        stats["primary_attacks"] += 1
                        stats["primary_attacked_turns"].add(turn)
                        if stats["primary_first_attack_turn"] is None:
                            stats["primary_first_attack_turn"] = turn
            if capture_trace:
                trace.append(
                    {
                        "decision": decision_number,
                        "role": role,
                        "state": summarize_state(obs),
                        "select": {
                            "context": select.get("context"),
                            "effect": card_id(select.get("effect")),
                            "minCount": select.get("minCount"),
                            "maxCount": select.get("maxCount"),
                        },
                        "chosen": features,
                    }
                )

            obs = battle_select(action)
            for log in obs.get("logs") or []:
                if log.get("type") == 23:
                    stats["result_reason"] = RESULT_REASON.get(
                        log.get("reason"), f"reason_{log.get('reason')}"
                    )
            result = current_state(obs).get("result", -1)
            if result != -1:
                stats["terminal_state"] = summarize_state(obs)
                return result, stats, trace
    finally:
        battle_finish()

    stats["timed_out"] = True
    stats["terminal_state"] = summarize_state(obs)
    return None, stats, trace


def original_outcome(replay: dict, seat: int) -> str:
    rewards = replay.get("rewards") or []
    if seat >= len(rewards):
        return "unknown"
    if rewards[seat] > 0:
        return "win"
    if rewards[seat] < 0:
        return "loss"
    return "draw"


def flatten_trial_stats(stats: dict) -> dict[str, Any]:
    attack_turns = stats["primary_attack_turns"]
    attacked_turns = stats["primary_attacked_turns"]
    terminal = stats.get("terminal_state") or {}
    return {
        "decisions": stats["decisions"],
        "primary_decisions": stats["primary_decisions"],
        "opponent_decisions": stats["opponent_decisions"],
        "primary_attack_menus": stats["primary_attack_menus"],
        "primary_attacks": stats["primary_attacks"],
        "primary_attack_turns": len(attack_turns),
        "primary_attacked_turns": len(attacked_turns),
        "primary_abandoned_attack_turns": len(attack_turns - attacked_turns),
        "primary_first_attack_turn": stats["primary_first_attack_turn"],
        "result_reason": stats["result_reason"],
        "timed_out": int(stats["timed_out"]),
        "forced_first_player_decisions": stats[
            "forced_first_player_decisions"
        ],
        "terminal_turn": terminal.get("turn"),
        "terminal_state": terminal,
        "primary_selected_types": dict(stats["primary_selected_types"]),
        "opponent_selected_types": dict(stats["opponent_selected_types"]),
    }


def evaluate_replay(
    episode_id: int,
    path: Path,
    replay: dict,
    primary_agent,
    primary_deck: list[int],
    fallback_module,
    trials: int,
    max_decisions: int,
    opponent_mode: str,
    trace_dir: Path | None,
    team_aliases: set[str] | frozenset[str] | None = None,
    public_replacement: str = "loser",
    force_first_player: bool = False,
) -> tuple[dict, list[dict]]:
    seat, replacement_kind = replacement_seat(
        replay,
        team_aliases=team_aliases,
        public_replacement=public_replacement,
    )
    opponent_seat = 1 - seat
    teams = (replay.get("info") or {}).get("TeamNames") or ["unknown", "unknown"]
    opponent_deck = replay_deck(replay, opponent_seat)
    script = recorded_decisions(replay, opponent_seat)
    kaggle_seed_metadata = int(
        (replay.get("configuration") or {}).get("seed") or 0
    )
    original_first_player = replay_first_player(replay)

    wins = losses = draws = timeouts = 0
    scripted = fallback = high_confidence = opponent_exceptions = 0
    attack_menus = attacks = attack_turns = attacked_turns = abandoned = 0
    forced_first_player_decisions = 0
    first_player_preserved_trials = 0
    observed_first_players = Counter()
    first_attacks = []
    reasons = Counter()
    trial_rows = []
    loss_traces = []
    for trial in range(trials):
        opponent = ReplayOpponent(
            opponent_deck,
            script,
            fallback_module,
            opponent_mode,
        )
        result, stats, trace = run_one(
            primary_agent,
            primary_deck,
            opponent,
            opponent_deck,
            seat,
            max_decisions,
            capture_trace=trace_dir is not None,
            forced_first_player=(
                original_first_player if force_first_player else None
            ),
        )
        flat = flatten_trial_stats(stats)
        if flat["timed_out"]:
            outcome = "timeout"
            timeouts += 1
        elif result == seat:
            outcome = "win"
            wins += 1
        elif result in (0, 1):
            outcome = "loss"
            losses += 1
        else:
            outcome = "draw"
            draws += 1
        scripted += opponent.stats["scripted_decisions"]
        fallback += opponent.stats["fallback_decisions"]
        high_confidence += opponent.stats["high_confidence_scripted"]
        opponent_exceptions += opponent.stats["opponent_exceptions"]
        attack_menus += flat["primary_attack_menus"]
        attacks += flat["primary_attacks"]
        attack_turns += flat["primary_attack_turns"]
        attacked_turns += flat["primary_attacked_turns"]
        abandoned += flat["primary_abandoned_attack_turns"]
        forced_first_player_decisions += flat[
            "forced_first_player_decisions"
        ]
        observed_first_player = (
            (flat.get("terminal_state") or {}).get("firstPlayer")
        )
        observed_first_players[observed_first_player] += 1
        if (
            original_first_player in (0, 1)
            and observed_first_player == original_first_player
        ):
            first_player_preserved_trials += 1
        if flat["primary_first_attack_turn"] is not None:
            first_attacks.append(flat["primary_first_attack_turn"])
        reasons[flat["result_reason"]] += 1
        trial_row = {
            "trial": trial + 1,
            "outcome": outcome,
            "winner": result,
            **flat,
            "opponent_scripted_decisions": opponent.stats["scripted_decisions"],
            "opponent_fallback_decisions": opponent.stats["fallback_decisions"],
            "opponent_high_confidence_scripted": opponent.stats[
                "high_confidence_scripted"
            ],
        }
        trial_rows.append(trial_row)
        if outcome == "loss" and trace_dir is not None:
            loss_traces.append({"trial": trial + 1, "summary": trial_row, "trace": trace})

    if loss_traces and trace_dir is not None:
        trace_dir.mkdir(parents=True, exist_ok=True)
        (trace_dir / f"{episode_id}.json").write_text(
            json.dumps(loss_traces, indent=2, sort_keys=True)
        )

    decisive = wins + losses
    result_label = "win" if wins > losses else "loss" if losses > wins else "draw"
    row = {
        "episode_id": episode_id,
        "path": (
            str(path.relative_to(ROOT))
            if path.is_relative_to(ROOT)
            else str(path)
        ),
        "replacement_kind": replacement_kind,
        "replacement_seat": seat,
        "replacement_team": teams[seat] if seat < len(teams) else "unknown",
        "opponent_team": teams[opponent_seat] if opponent_seat < len(teams) else "unknown",
        "original_outcome": original_outcome(replay, seat),
        "replay_module_version": replay.get("module_version"),
        "replay_schema_version": replay.get("schema_version"),
        "replay_statuses": json.dumps(replay.get("statuses") or []),
        "replay_steps": len(replay.get("steps") or []),
        "kaggle_seed_metadata": kaggle_seed_metadata,
        "local_engine_seed_applied": 0,
        "original_first_player": original_first_player,
        "first_player_forced": int(
            force_first_player and original_first_player in (0, 1)
        ),
        "forced_first_player_decisions": forced_first_player_decisions,
        "first_player_preserved_trials": first_player_preserved_trials,
        "observed_first_players": json.dumps(
            {
                str(key): value
                for key, value in observed_first_players.items()
            },
            sort_keys=True,
        ),
        "opponent_script_decisions": len(script),
        "trials": trials,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "result": result_label,
        "win_rate": round(wins / trials, 6),
        "decisive_win_rate": round(wins / decisive, 6) if decisive else 0.0,
        "timeouts": timeouts,
        "opponent_scripted_decisions": scripted,
        "opponent_high_confidence_scripted": high_confidence,
        "opponent_fallback_decisions": fallback,
        "opponent_exceptions": opponent_exceptions,
        "scripted_fraction": round(
            scripted / (scripted + fallback), 6
        ) if scripted + fallback else 0.0,
        "primary_attack_menus": attack_menus,
        "primary_attacks": attacks,
        "primary_attack_turns": attack_turns,
        "primary_attacked_turns": attacked_turns,
        "primary_abandoned_attack_turns": abandoned,
        "avg_first_attack_turn": round(sum(first_attacks) / len(first_attacks), 3)
        if first_attacks
        else "",
        "result_reasons": json.dumps(dict(reasons), sort_keys=True),
    }
    return row, trial_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=ROOT / "scouting_replays")
    parser.add_argument(
        "--agent-dir", type=Path, default=ROOT / "agents" / "v5_candidate"
    )
    parser.add_argument("--agent-deck", type=Path)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--max-decisions", type=int, default=5000)
    parser.add_argument(
        "--opponent-mode", choices=("scripted", "generic"), default="scripted"
    )
    parser.add_argument(
        "--team-alias",
        action="append",
        help=(
            "Team name whose original seat should be replaced. May be repeated; "
            "defaults to MUHAMMAD UMER FAROOQ and ROASTERS."
        ),
    )
    parser.add_argument(
        "--public-replacement",
        choices=("loser", "seat0", "seat1"),
        default="loser",
        help="Seat policy when no configured team alias is present.",
    )
    parser.add_argument(
        "--force-first-player",
        action=argparse.BooleanOptionalAction,
        default=False,
        help=(
            "Force the original first-player seat. This preserves a recoverable "
            "condition but bypasses the replacement agent's IsFirst choice."
        ),
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--episodes",
        help="Comma-separated episode IDs; omitted means the full unique corpus.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "artifacts" / "v5_replay_suite.csv",
    )
    parser.add_argument("--trace-dir", type=Path)
    args = parser.parse_args()

    if args.trials < 1:
        parser.error("--trials must be positive")
    corpus = args.corpus.resolve()
    agent_dir = args.agent_dir.resolve()
    primary_agent = load_agent(agent_dir, "replay_suite_primary")
    primary_deck = read_deck(
        (args.agent_deck or agent_dir / "deck.csv").resolve()
    )
    fallback_module = load_module(
        ROOT / "agents" / "generic_attack_first" / "main.py",
        "replay_suite_fallback",
    )
    replays = load_unique_replays(corpus)
    if args.episodes:
        requested = {
            int(value.strip())
            for value in args.episodes.split(",")
            if value.strip()
        }
        replays = [row for row in replays if row[0] in requested]
        missing = requested - {row[0] for row in replays}
        if missing:
            parser.error(f"Unknown episodes: {sorted(missing)}")
    if args.limit:
        replays = replays[: args.limit]

    rows = []
    details = {}
    for index, (episode_id, path, replay) in enumerate(replays, 1):
        row, trial_rows = evaluate_replay(
            episode_id,
            path,
            replay,
            primary_agent,
            primary_deck,
            fallback_module,
            args.trials,
            args.max_decisions,
            args.opponent_mode,
            args.trace_dir.resolve() if args.trace_dir else None,
            team_aliases=(
                frozenset(args.team_alias) if args.team_alias else None
            ),
            public_replacement=args.public_replacement,
            force_first_player=args.force_first_player,
        )
        rows.append(row)
        details[str(episode_id)] = trial_rows
        print(
            f"{index}/{len(replays)} episode={episode_id} "
            f"result={row['wins']}-{row['losses']}-{row['draws']} "
            f"scripted={row['scripted_fraction']:.1%} "
            f"attacks={row['primary_attacked_turns']}/"
            f"{row['primary_attack_turns']}",
            flush=True,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()) if rows else []
        )
        writer.writeheader()
        writer.writerows(rows)
    detail_path = args.output.with_suffix(".json")
    detail_path.write_text(json.dumps(details, indent=2, sort_keys=True))
    total_wins = sum(row["wins"] for row in rows)
    total_losses = sum(row["losses"] for row in rows)
    total_draws = sum(row["draws"] for row in rows)
    total_timeouts = sum(row["timeouts"] for row in rows)
    print(
        f"summary replays={len(rows)} matches={total_wins + total_losses + total_draws} "
        f"wins={total_wins} losses={total_losses} draws={total_draws} "
        f"timeouts={total_timeouts} "
        f"win_rate={total_wins / max(1, total_wins + total_losses + total_draws):.3%}"
    )
    print(args.output)
    print(detail_path)


if __name__ == "__main__":
    main()
