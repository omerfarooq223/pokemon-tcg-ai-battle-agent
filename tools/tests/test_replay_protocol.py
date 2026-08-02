from __future__ import annotations

import unittest
from types import SimpleNamespace

from tools.evaluate_replay_suite import (
    RecordedDecision,
    ReplayOpponent,
    decision_signature,
    recorded_decisions,
    replacement_seat,
    replay_first_player,
)


def row(*, status="INACTIVE", observation=None, action=None):
    return {
        "status": status,
        "observation": observation or {},
        "action": action,
    }


class ReplacementSeatTests(unittest.TestCase):
    def test_roasters_win_replaces_our_winning_seat(self):
        replay = {
            "info": {"TeamNames": ["ROASTERS", "Opponent"]},
            "rewards": [1, -1],
        }
        self.assertEqual(replacement_seat(replay), (0, "our_agent"))

    def test_roasters_loss_replaces_our_losing_seat(self):
        replay = {
            "info": {"TeamNames": ["Opponent", "ROASTERS"]},
            "rewards": [1, -1],
        }
        self.assertEqual(replacement_seat(replay), (1, "our_agent"))

    def test_public_replay_still_replaces_loser(self):
        replay = {
            "info": {"TeamNames": ["Public winner", "Public loser"]},
            "rewards": [1, -1],
        }
        self.assertEqual(replacement_seat(replay), (1, "public_loser"))

    def test_custom_top_team_reports_configured_origin(self):
        replay = {
            "info": {"TeamNames": ["flg", "Opponent"]},
            "rewards": [1, -1],
        }
        self.assertEqual(
            replacement_seat(replay, team_aliases=frozenset({"flg"})),
            (0, "configured_team"),
        )


class RecordedActionTests(unittest.TestCase):
    def setUp(self):
        self.observation = {
            "current": {"turn": 4, "yourIndex": 1, "players": [{}, {}]},
            "select": {
                "context": 43,
                "effect": {"id": 100},
                "contextCard": None,
                "minCount": 0,
                "maxCount": 1,
                "option": [{"type": 1}],
            },
        }

    def test_optional_choose_nothing_is_recorded(self):
        replay = {
            "steps": [
                [row(), row(status="ACTIVE", observation=self.observation)],
                [row(), row(action=[])],
            ]
        }
        decisions = recorded_decisions(replay, 1)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0].features, [])

    def test_optional_choose_nothing_is_replayed(self):
        decision = RecordedDecision(
            signature=decision_signature(self.observation),
            features=[],
            turn=4,
        )
        fallback = SimpleNamespace(choose_action=lambda obs: [0])
        opponent = ReplayOpponent([1] * 60, [decision], fallback, "scripted")
        self.assertEqual(opponent.choose_action(self.observation), [])
        self.assertEqual(opponent.stats["scripted_decisions"], 1)
        self.assertEqual(opponent.stats["fallback_decisions"], 0)

    def test_nonempty_recording_cannot_map_to_optional_empty_action(self):
        decision = RecordedDecision(
            signature=decision_signature(self.observation),
            features=[{"type": 7, "source_id": 999}],
            turn=4,
        )
        fallback = SimpleNamespace(choose_action=lambda obs: [0])
        opponent = ReplayOpponent([1] * 60, [decision], fallback, "scripted")
        self.assertEqual(opponent.choose_action(self.observation), [0])
        self.assertEqual(opponent.stats["scripted_decisions"], 0)
        self.assertEqual(opponent.stats["fallback_decisions"], 1)

    def test_signature_mismatch_uses_fallback(self):
        mismatched = dict(self.observation)
        mismatched["select"] = dict(self.observation["select"], context=8)
        decision = RecordedDecision(
            signature=decision_signature(self.observation),
            features=[],
            turn=4,
        )
        fallback = SimpleNamespace(choose_action=lambda obs: [0])
        opponent = ReplayOpponent([1] * 60, [decision], fallback, "scripted")
        self.assertEqual(opponent.choose_action(mismatched), [0])
        self.assertEqual(opponent.stats["scripted_decisions"], 0)
        self.assertEqual(opponent.stats["fallback_decisions"], 1)

    def test_first_player_is_recovered(self):
        replay = {
            "steps": [
                [
                    row(observation={"current": {"firstPlayer": -1}}),
                    row(),
                ],
                [
                    row(observation={"current": {"firstPlayer": 1}}),
                    row(),
                ],
            ]
        }
        self.assertEqual(replay_first_player(replay), 1)


if __name__ == "__main__":
    unittest.main()
