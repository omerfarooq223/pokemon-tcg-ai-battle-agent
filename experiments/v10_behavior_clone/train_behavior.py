#!/usr/bin/env python3
"""Train a compact visible-state behavior clone of the Top-5 Lopunny pilot.

The generated runtime contains no replay IDs, player names, or opponent
identity features.  Team names are used here only to select the twelve source
traces during offline training.  The fitted model sees public board state,
hand composition, turn flags, and the current legal-action menu.
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import random
import zipfile
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BASE_SOURCE = ROOT / "agents" / "v10_candidate" / "main.py"
OUTPUT = Path(__file__).resolve().parent / "main.py"
DEFAULT_ARCHIVE = Path("/Users/muhammadomerfarooq/Downloads/Top 5.zip")
SOURCE_TEAM = "Majkel1337"
POKEMON_IDS = (174, 305, 848, 66, 849)
ACTIVE_ID_MAP = {None: 0, 174: 1, 305: 2, 848: 3, 66: 4, 849: 5}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def action_key(base, obs: dict, option: dict) -> tuple:
    """Semantic action key; serial numbers and option indexes are excluded."""
    option_type = option.get("type")
    source_id = base.card_id(base.option_source(obs, option))
    target_id = base.card_id(base.option_target(obs, option))
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


def extract_rows(archive: Path, base):
    rows = []
    with zipfile.ZipFile(archive) as handle:
        for member in handle.namelist():
            if (
                not member.startswith("Top 5/")
                or not member.endswith(".json")
                or " (1)" in member
            ):
                continue
            replay = json.loads(handle.read(member))
            teams = replay.get("info", {}).get("TeamNames") or []
            if SOURCE_TEAM not in teams:
                continue
            seat = teams.index(SOURCE_TEAM)
            episode = int(Path(member).stem)
            steps = replay.get("steps") or []
            for step_index in range(1, len(steps) - 1):
                record = steps[step_index][seat]
                obs = record.get("observation") or {}
                select = obs.get("select")
                if record.get("status") != "ACTIVE" or not isinstance(select, dict):
                    continue
                actual = steps[step_index + 1][seat].get("action")
                options = select.get("option") or []
                if not isinstance(actual, list) or any(
                    not isinstance(index, int) or not 0 <= index < len(options)
                    for index in actual
                ):
                    continue
                rows.append(
                    {
                        "episode": episode,
                        "context": select.get("context"),
                        "obs": obs,
                        "options": options,
                        "actual": actual,
                    }
                )
    return rows


def feature_vector(base, obs: dict, action_space: list[tuple]) -> list[float]:
    state = base.current(obs)
    you = base.your_index(state)
    opponent = 1 - you
    ps = base.players(state)
    active = base.active(state, you)
    opponent_active = base.active(state, opponent)
    board_counts = base.board_counts(state, you)
    hand_counts = collections.Counter(base.hand_ids(state, you))
    options = base.selection(obs).get("option") or []
    values = [
        min(20, base.as_int(state.get("turn"), 0)),
        min(30, base.as_int(state.get("turnActionCount"), 0)),
        int(bool(state.get("energyAttached"))),
        int(bool(state.get("supporterPlayed"))),
        int(bool(state.get("retreated"))),
        ACTIVE_ID_MAP.get(base.card_id(active), 6),
        min(3, base.attached_count(active)),
        min(8, base.damage_on(active) // 30),
        min(10, base.hp(active) // 30),
        min(5, base.attached_count(opponent_active)),
        min(10, base.damage_on(opponent_active) // 30),
        min(12, base.hp(opponent_active) // 30),
        min(12, base.max_hp(opponent_active) // 30),
        len(base.bench(state, you)),
        len(base.bench(state, opponent)),
        min(15, len(base.hand(state, you))),
        min(
            15,
            base.as_int(ps[opponent].get("handCount"), 0)
            if opponent < len(ps)
            else 0,
        ),
        min(
            15,
            (base.as_int(ps[you].get("deckCount"), 0) // 3)
            if you < len(ps)
            else 0,
        ),
        base.prize_count(state, you),
        base.prize_count(state, opponent),
    ]
    for card in POKEMON_IDS:
        values.extend((board_counts.get(card, 0), hand_counts[card]))
    for card in sorted(set(base.EXPECTED_DECK)):
        if card not in POKEMON_IDS:
            values.append(hand_counts[card])
    available = collections.Counter(action_key(base, obs, option) for option in options)
    values.extend(min(2, available[action]) for action in action_space)
    return values


class Node:
    __slots__ = ("feature", "threshold", "left", "right", "counts")

    def __init__(
        self,
        *,
        feature=-1,
        threshold=0.0,
        left=None,
        right=None,
        counts=None,
    ):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.counts = counts


def fit_tree(
    x,
    y,
    indices,
    class_count,
    rng,
    *,
    depth=0,
    max_depth=13,
    minimum_leaf=2,
    feature_trials=16,
):
    counts = np.bincount(y[indices], minlength=class_count)
    if (
        depth >= max_depth
        or len(indices) < minimum_leaf * 2
        or np.count_nonzero(counts) <= 1
    ):
        return Node(counts=counts)

    parent_impurity = 1.0 - np.sum((counts / len(indices)) ** 2)
    best = None
    features = rng.sample(range(x.shape[1]), min(feature_trials, x.shape[1]))
    for feature in features:
        values = x[indices, feature]
        unique = np.unique(values)
        if len(unique) < 2:
            continue
        thresholds = (unique[:-1] + unique[1:]) / 2.0
        if len(thresholds) > 8:
            thresholds = thresholds[
                np.linspace(0, len(thresholds) - 1, 8).astype(int)
            ]
        for threshold in thresholds:
            left_mask = values <= threshold
            left_size = int(left_mask.sum())
            right_size = len(indices) - left_size
            if left_size < minimum_leaf or right_size < minimum_leaf:
                continue
            left_counts = np.bincount(
                y[indices[left_mask]], minlength=class_count
            )
            right_counts = counts - left_counts
            gain = parent_impurity
            gain -= (left_size / len(indices)) * (
                1.0 - np.sum((left_counts / left_size) ** 2)
            )
            gain -= (right_size / len(indices)) * (
                1.0 - np.sum((right_counts / right_size) ** 2)
            )
            if best is None or gain > best[0]:
                best = (
                    gain,
                    feature,
                    float(threshold),
                    indices[left_mask],
                    indices[~left_mask],
                )
    if best is None:
        return Node(counts=counts)
    _, feature, threshold, left_indices, right_indices = best
    return Node(
        feature=feature,
        threshold=threshold,
        left=fit_tree(
            x,
            y,
            left_indices,
            class_count,
            rng,
            depth=depth + 1,
            max_depth=max_depth,
            minimum_leaf=minimum_leaf,
            feature_trials=feature_trials,
        ),
        right=fit_tree(
            x,
            y,
            right_indices,
            class_count,
            rng,
            depth=depth + 1,
            max_depth=max_depth,
            minimum_leaf=minimum_leaf,
            feature_trials=feature_trials,
        ),
    )


def compact_tree(node: Node):
    if node.counts is not None:
        sparse = tuple(
            (index, int(value))
            for index, value in enumerate(node.counts)
            if value
        )
        return ("L", sparse)
    return (
        "N",
        node.feature,
        round(node.threshold, 4),
        compact_tree(node.left),
        compact_tree(node.right),
    )


RUNTIME = r'''

# ---------------------------------------------------------------------------
# Offline-fitted visible-state behavior clone.
# ---------------------------------------------------------------------------

_RULE_CHOOSE_ACTION = choose_action
_CLONE_POKEMON_IDS = (174, 305, 848, 66, 849)
_CLONE_ACTIVE_ID_MAP = {None: 0, 174: 1, 305: 2, 848: 3, 66: 4, 849: 5}
_CLONE_ACTIONS = __ACTIONS__
_CLONE_ACTION_INDEX = {action: index for index, action in enumerate(_CLONE_ACTIONS)}
_CLONE_TREES = __TREES__
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
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--trees", type=int, default=24)
    parser.add_argument("--seed", type=int, default=76123)
    args = parser.parse_args()

    base = load_module(BASE_SOURCE, "_v10_clone_training_base")
    rows = extract_rows(args.archive, base)
    episodes = sorted({row["episode"] for row in rows})
    main_rows = [row for row in rows if row["context"] == 0]
    action_space = sorted(
        {
            action_key(base, row["obs"], option)
            for row in main_rows
            for option in row["options"]
        },
        key=repr,
    )
    action_index = {action: index for index, action in enumerate(action_space)}
    x = np.asarray(
        [feature_vector(base, row["obs"], action_space) for row in main_rows],
        dtype=np.float32,
    )
    y = np.asarray(
        [
            action_index[
                action_key(base, row["obs"], row["options"][row["actual"][0]])
            ]
            for row in main_rows
        ],
        dtype=np.int32,
    )

    rng = random.Random(args.seed)
    indices = np.arange(len(main_rows))
    forest = []
    for _ in range(args.trees):
        bootstrap = np.asarray(
            [indices[rng.randrange(len(indices))] for _ in range(len(indices))]
        )
        forest.append(
            fit_tree(x, y, bootstrap, len(action_space), rng)
        )

    runtime = RUNTIME.replace("__ACTIONS__", repr(tuple(action_space)))
    runtime = runtime.replace(
        "__TREES__", repr(tuple(compact_tree(tree) for tree in forest))
    )
    base_text = BASE_SOURCE.read_text(encoding="utf-8")
    OUTPUT.write_text(base_text.rstrip() + "\n" + runtime, encoding="utf-8")
    print(
        f"episodes={len(episodes)} decisions={len(rows)} "
        f"main_decisions={len(main_rows)} classes={len(action_space)} "
        f"trees={len(forest)} output={OUTPUT}"
    )


if __name__ == "__main__":
    main()
