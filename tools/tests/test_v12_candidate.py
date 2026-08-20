import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_v12(tag):
    path = ROOT / "agents" / "v12_candidate" / "main.py"
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


class V12CandidateTests(unittest.TestCase):
    def setUp(self):
        self.v12 = load_v12(self.id().replace(".", "_"))

    def base_obs(self, *, pressure, third_line=False):
        board = [
            pokemon(345, 10, 150, energies=(1, 0, 0)),
            pokemon(344, 20, 70),
        ]
        if third_line:
            board.append(pokemon(117, 30, 210, energies=(6, 0, 0)))
        return {
            "current": {
                "yourIndex": 0,
                "turn": 5,
                "players": [
                    {
                        "active": [board[0]],
                        "bench": board[1:],
                        "hand": [] if third_line else [pokemon(344, 40, 70)],
                        "prize": [{}, {}, {}, {}, {}, {}],
                        "deckCount": 30,
                    },
                    {
                        "active": [pokemon(pressure, 50, 140)],
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

    def test_counter_pressure_builds_third_line_before_attack(self):
        obs = self.base_obs(pressure=743)
        self.assertEqual(self.v12.required_line_count(obs), 3)
        self.assertEqual(self.v12.agent(obs), [0])

    def test_counter_pressure_attacks_after_three_lines(self):
        obs = self.base_obs(pressure=743, third_line=True)
        self.assertEqual(self.v12.required_line_count(obs), 3)
        self.assertEqual(self.v12.agent(obs), [1])

    def test_normal_board_keeps_two_line_requirement(self):
        obs = self.base_obs(pressure=678)
        self.assertEqual(self.v12.required_line_count(obs), 2)
        self.assertEqual(self.v12.agent(obs), [1])

    def test_v12_deck_matches_embedded_deck(self):
        deck = [
            int(line.strip().split(",")[0])
            for line in (ROOT / "agents" / "v12_candidate" / "deck.csv")
            .read_text()
            .splitlines()
            if line.strip()
        ]
        self.assertEqual(deck, self.v12.EXPECTED_DECK)
        self.assertEqual(len(deck), 60)


if __name__ == "__main__":
    unittest.main()
