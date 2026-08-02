import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_v11(tag):
    path = ROOT / "agents" / "v11_candidate" / "main.py"
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


class V11CandidateTests(unittest.TestCase):
    def setUp(self):
        self.v11 = load_v11(self.id().replace(".", "_"))

    def test_prize_helpers_read_real_prize_zones(self):
        obs = {
            "current": {
                "yourIndex": 0,
                "players": [
                    {"prize": [{}, {}]},
                    {"prize": [{}]},
                ],
            }
        }
        self.assertEqual(self.v11.our_prize_count(obs), 2)
        self.assertEqual(self.v11.opponent_prize_count(obs), 1)

    def test_attack_menu_first_builds_missing_backup_line(self):
        active = pokemon(345, 10, 150, energies=(1, 0, 0))
        obs = {
            "current": {
                "yourIndex": 0,
                "turn": 5,
                "players": [
                    {
                        "active": [active],
                        "bench": [],
                        "hand": [pokemon(344, 20, 70)],
                        "prize": [{}, {}, {}, {}, {}, {}],
                        "deckCount": 30,
                    },
                    {
                        "active": [pokemon(678, 30, 310)],
                        "bench": [],
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
        self.assertEqual(self.v11.agent(obs), [0])

    def test_ready_attack_is_taken_when_backup_exists(self):
        obs = {
            "current": {
                "yourIndex": 0,
                "turn": 6,
                "players": [
                    {
                        "active": [pokemon(345, 10, 150, energies=(1, 0, 0))],
                        "bench": [pokemon(344, 20, 70)],
                        "hand": [],
                        "prize": [{}, {}, {}, {}, {}, {}],
                        "deckCount": 30,
                    },
                    {
                        "active": [pokemon(678, 30, 310)],
                        "bench": [],
                        "hand": [],
                        "prize": [{}, {}, {}, {}, {}, {}],
                    },
                ],
            },
            "select": {
                "minCount": 1,
                "maxCount": 1,
                "option": [{"type": 13, "attackId": 479}],
            },
        }
        self.assertEqual(self.v11.agent(obs), [0])

    def test_missing_observation_returns_exact_embedded_deck(self):
        self.assertEqual(self.v11.agent({}), self.v11.EXPECTED_DECK)
        self.assertEqual(len(self.v11.EXPECTED_DECK), 60)


if __name__ == "__main__":
    unittest.main()
