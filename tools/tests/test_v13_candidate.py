import importlib.util
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_v13(tag):
    path = ROOT / "agents" / "v13_candidate" / "main.py"
    spec = importlib.util.spec_from_file_location(tag, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pokemon(card_id, serial, hp, energies=()):
    return {
        "id": card_id,
        "serial": serial,
        "hp": hp,
        "maxHp": hp,
        "energies": list(energies),
    }


class V13CandidateTests(unittest.TestCase):
    def setUp(self):
        self.v13 = load_v13(self.id().replace(".", "_"))

    def base_obs(self, *, active_threat=678, bench_threat=None, deck_count=30):
        our_player = {
            "active": [pokemon(345, 10, 150, energies=(1, 0, 0))],
            "bench": [pokemon(344, 20, 70)],
            "hand": [pokemon(344, 40, 70)],
            "prize": [{}, {}, {}, {}, {}, {}],
        }
        if deck_count is not ...:
            our_player["deckCount"] = deck_count
        opponent_bench = (
            [] if bench_threat is None else [pokemon(bench_threat, 60, 320)]
        )
        return {
            "current": {
                "yourIndex": 0,
                "turn": 5,
                "players": [
                    our_player,
                    {
                        "active": [pokemon(active_threat, 50, 140)],
                        "bench": opponent_bench,
                        "hand": [],
                        "prize": [{}, {}, {}, {}, {}, {}],
                    },
                ],
            },
            "select": {
                "minCount": 1,
                "maxCount": 1,
                "option": [
                    {"type": 7, "playerIndex": 0, "area": 2, "index": 0},
                    {"type": 13, "attackId": 479},
                ],
            },
        }

    def test_visible_bench_spread_threat_requires_third_line(self):
        obs = self.base_obs(bench_threat=121)
        self.assertEqual(self.v13.required_line_count(obs), 3)
        self.assertEqual(self.v13.agent(obs), [0])

    def test_visible_munkidori_requires_third_line(self):
        obs = self.base_obs(bench_threat=112)
        self.assertEqual(self.v13.required_line_count(obs), 3)

    def test_missing_deck_count_does_not_mean_empty_deck(self):
        obs = self.base_obs(active_threat=743, deck_count=...)
        self.assertEqual(self.v13.agent(obs), [0])

    def test_actual_empty_deck_attacks_immediately(self):
        obs = self.base_obs(active_threat=743, deck_count=0)
        self.assertEqual(self.v13.agent(obs), [1])

    def test_exception_fallback_prefers_attack(self):
        obs = self.base_obs()
        with mock.patch.object(
            self.v13, "choose_action", side_effect=RuntimeError("test")
        ):
            self.assertEqual(self.v13.agent(obs), [1])

    def test_deck_matches_embedded_deck(self):
        deck = [
            int(line.strip().split(",")[0])
            for line in (ROOT / "agents" / "v13_candidate" / "deck.csv")
            .read_text()
            .splitlines()
            if line.strip()
        ]
        self.assertEqual(deck, self.v13.EXPECTED_DECK)
        self.assertEqual(len(deck), 60)

    def test_four_bounded_setup_actions(self):
        self.assertEqual(self.v13.MAX_ATTACK_DEFERRALS, 4)


if __name__ == "__main__":
    unittest.main()
