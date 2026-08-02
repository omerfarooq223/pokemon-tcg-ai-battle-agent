from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_v10():
    path = ROOT / "agents" / "v10_candidate" / "main.py"
    spec = importlib.util.spec_from_file_location("v10_test_agent", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def pokemon(card_id, serial, hp, *, max_hp=None, energies=(), tools=()):
    return {
        "id": card_id,
        "serial": serial,
        "hp": hp,
        "maxHp": hp if max_hp is None else max_hp,
        "energyCards": [
            {"id": energy_id, "serial": serial * 100 + index}
            for index, energy_id in enumerate(energies)
        ],
        "tools": [
            {"id": tool_id, "serial": serial * 1000 + index}
            for index, tool_id in enumerate(tools)
        ],
    }


def observation(*, hand=(), active=(), bench=(), opponent_active=(), select=None, **state):
    current = {
        "yourIndex": 0,
        "turn": 4,
        "turnActionCount": 1,
        "players": [
            {
                "hand": list(hand),
                "handCount": len(hand),
                "active": list(active),
                "bench": list(bench),
                "prize": [{"id": 1}] * 6,
            },
            {
                "hand": [],
                "handCount": 0,
                "active": list(opponent_active),
                "bench": [],
                "prize": [{"id": 1}] * 6,
            },
        ],
        **state,
    }
    return {"current": current, "select": select or {"minCount": 0, "maxCount": 1, "option": []}}


class V10SemanticTests(unittest.TestCase):
    def setUp(self):
        self.v10 = load_v10()

    def attachment_scores(self, opposing_id, opposing_hp):
        energy = {"id": self.v10.SPIKY, "serial": 900}
        active = pokemon(self.v10.LOPUNNY, 10, 330, energies=(self.v10.MIST,))
        backup = pokemon(self.v10.BUNEARY, 11, 70)
        opponent = pokemon(opposing_id, 20, opposing_hp)
        options = [
            {"type": 8, "area": 2, "index": 0, "inPlayArea": 4, "inPlayIndex": 0},
            {"type": 8, "area": 2, "index": 0, "inPlayArea": 5, "inPlayIndex": 0},
        ]
        obs = observation(
            hand=(energy,),
            active=(active,),
            bench=(backup,),
            opponent_active=(opponent,),
            select={"context": 0, "minCount": 0, "maxCount": 1, "option": options},
        )
        return [self.v10.attach_score(obs, option) for option in options]

    def test_second_energy_breaks_damage_protection(self):
        active_score, backup_score = self.attachment_scores(345, 170)
        self.assertGreater(active_score, backup_score + 4000)

    def test_pivot_knockout_spreads_energy_in_161_to_230_window(self):
        active_score, backup_score = self.attachment_scores(96, 210)
        self.assertGreater(backup_score, active_score)

    def test_active_wally_is_rejected(self):
        active = pokemon(self.v10.LOPUNNY, 10, 120, max_hp=330, energies=(self.v10.SPIKY,))
        backup = pokemon(self.v10.LOPUNNY, 11, 330, energies=(self.v10.SPIKY,))
        obs = observation(active=(active,), bench=(backup,))
        self.assertLess(self.v10.supporter_value(obs, self.v10.WALLY), 0)

    def test_active_dunsparce_cannot_evolve_away_switch_attack_without_ready_lopunny(self):
        active = pokemon(self.v10.DUNSPARCE, 10, 70, energies=(self.v10.MIST,))
        backup = pokemon(self.v10.BUNEARY, 11, 70)
        evolution = {"id": self.v10.DUDUNSPARCE, "serial": 30}
        option = {"type": 9, "area": 2, "index": 0, "inPlayArea": 4, "inPlayIndex": 0}
        obs = observation(
            hand=(evolution,),
            active=(active,),
            bench=(backup,),
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [option, {"type": 13, "attackId": 1}],
            },
        )
        self.assertLess(self.v10.evolution_score(obs, option), -10000)

    def test_active_run_away_draw_forces_ready_lopunny_promotion(self):
        active = pokemon(self.v10.DUDUNSPARCE, 10, 140)
        ability = {"type": 10, "area": 4, "index": 0}
        obs = observation(
            active=(active,),
            bench=(pokemon(self.v10.LOPUNNY, 11, 330, energies=(self.v10.SPIKY,)),),
            select={"context": 0, "minCount": 0, "maxCount": 1, "option": [ability]},
        )
        self.assertEqual(self.v10.safe_action(obs), [0])
        self.assertTrue(self.v10.FORCE_READY_PROMOTION)

        unready = pokemon(self.v10.BUNEARY, 12, 70)
        ready = pokemon(self.v10.LOPUNNY, 11, 330, energies=(self.v10.SPIKY,))
        promotion_options = [
            {"type": 3, "playerIndex": 0, "area": 5, "index": 0},
            {"type": 3, "playerIndex": 0, "area": 5, "index": 1},
        ]
        promote = observation(
            bench=(unready, ready),
            select={"context": 4, "minCount": 1, "maxCount": 1, "option": promotion_options},
        )
        self.assertEqual(self.v10.safe_action(promote), [1])
        self.assertFalse(self.v10.FORCE_READY_PROMOTION)

    def test_multi_basic_search_builds_complementary_lines(self):
        deck = [
            pokemon(self.v10.BUNEARY, 20, 70),
            pokemon(self.v10.BUNEARY, 21, 70),
            pokemon(self.v10.DUNSPARCE, 22, 70),
            pokemon(self.v10.DUNSPARCE, 23, 70),
        ]
        options = [
            {"type": 3, "playerIndex": 0, "area": 1, "index": index}
            for index in range(4)
        ]
        obs = observation(
            select={
                "context": 5,
                "minCount": 0,
                "maxCount": 2,
                "option": options,
                "deck": deck,
            }
        )
        action = self.v10.choose_action(obs)
        self.assertEqual({deck[index]["id"] for index in action}, {self.v10.BUNEARY, self.v10.DUNSPARCE})

    def test_prizes_are_counted_from_api_list(self):
        state = {"players": [{"prize": [{}, {}]}, {"prize": [{}]}]}
        self.assertEqual(self.v10.prize_count(state, 0), 2)
        self.assertEqual(self.v10.prize_count(state, 1), 1)

    def test_startup_returns_exact_deck(self):
        self.assertEqual(self.v10.agent({}), self.v10.EXPECTED_DECK)
        self.assertEqual(len(self.v10.EXPECTED_DECK), 60)


if __name__ == "__main__":
    unittest.main()
