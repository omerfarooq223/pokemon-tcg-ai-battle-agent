from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_final(tag="v10_final_test"):
    path = ROOT / "agents" / "v10_final_candidate" / "main.py"
    spec = importlib.util.spec_from_file_location(tag, path)
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
        "turn": 7,
        "turnActionCount": 1,
        "energyAttached": False,
        "supporterPlayed": False,
        "retreated": False,
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
    return {
        "current": current,
        "select": select or {"context": 0, "minCount": 0, "maxCount": 1, "option": []},
    }


def source_card_id(obs, option):
    state = obs["current"]
    player = option.get("playerIndex", state.get("yourIndex", 0))
    area = option.get("area")
    if area is None and option.get("type") == 7:
        area = 2
    zone = {2: "hand", 4: "active", 5: "bench"}.get(area)
    cards = state["players"][player].get(zone, []) if zone else []
    index = option.get("index")
    return cards[index]["id"] if isinstance(index, int) and 0 <= index < len(cards) else None


class V10FinalWallyTests(unittest.TestCase):
    def setUp(self):
        self.v10 = load_final(self.id().replace(".", "_"))

    def test_complete_active_wally_pivot_sequence(self):
        v10 = self.v10
        damaged = pokemon(
            v10.LOPUNNY,
            10,
            10,
            max_hp=330,
            energies=(v10.SPIKY,),
            tools=(v10.AIR_BALLOON,),
        )
        incoming = pokemon(v10.LOPUNNY, 11, 330)
        wally = {"id": v10.WALLY, "serial": 90}
        hilda = {"id": v10.HILDA, "serial": 91}

        main = observation(
            hand=(wally, hilda),
            active=(damaged,),
            bench=(incoming,),
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 7, "index": 0},
                    {"type": 7, "index": 1},
                ],
            },
        )
        self.assertEqual(v10.agent(main), [0])

        target = observation(
            active=(damaged,),
            bench=(incoming,),
            supporterPlayed=True,
            select={
                "context": 17,
                "effect": {"id": v10.WALLY},
                "minCount": 1,
                "maxCount": 1,
                "option": [
                    {"type": 3, "playerIndex": 0, "area": 4, "index": 0},
                    {"type": 3, "playerIndex": 0, "area": 5, "index": 0},
                ],
            },
        )
        self.assertEqual(v10.agent(target), [0])
        self.assertEqual(v10.WALLY_HEALED_SERIAL, 10)
        self.assertTrue(v10.WALLY_HEALED_WAS_ACTIVE)

        healed = pokemon(
            v10.LOPUNNY,
            10,
            330,
            tools=(v10.AIR_BALLOON,),
        )
        energy = {"id": v10.SPIKY, "serial": 92}
        attach = observation(
            hand=(energy,),
            active=(healed,),
            bench=(incoming,),
            supporterPlayed=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 4, "inPlayIndex": 0},
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 5, "inPlayIndex": 0},
                    {"type": 12},
                ],
            },
        )
        self.assertEqual(v10.agent(attach), [1])

        powered_incoming = pokemon(v10.LOPUNNY, 11, 330, energies=(v10.SPIKY,))
        retreat = observation(
            active=(healed,),
            bench=(powered_incoming,),
            supporterPlayed=True,
            energyAttached=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [{"type": 12}, {"type": 14}],
            },
        )
        self.assertEqual(v10.agent(retreat), [0])

        promote = observation(
            active=(healed,),
            bench=(powered_incoming,),
            supporterPlayed=True,
            energyAttached=True,
            retreated=True,
            select={
                "context": 3,
                "minCount": 1,
                "maxCount": 1,
                "option": [
                    {"type": 3, "playerIndex": 0, "area": 5, "index": 0}
                ],
            },
        )
        self.assertEqual(v10.agent(promote), [0])

        attack = observation(
            active=(powered_incoming,),
            bench=(healed,),
            opponent_active=(pokemon(381, 20, 230),),
            supporterPlayed=True,
            energyAttached=True,
            retreated=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 13, "attackId": v10.GALE_THRUST},
                    {"type": 14},
                ],
            },
        )
        self.assertEqual(v10.agent(attack), [0])

    def test_active_wally_is_rejected_only_when_it_strands_attacker(self):
        v10 = self.v10
        active = pokemon(v10.LOPUNNY, 10, 100, max_hp=330, energies=(v10.SPIKY,))
        obs = observation(
            active=(active,),
            energyAttached=True,
        )
        self.assertLess(v10.supporter_value(obs, v10.WALLY), 0)

    def test_active_wally_without_bench_can_heal_and_reattach(self):
        v10 = self.v10
        active = pokemon(v10.LOPUNNY, 10, 100, max_hp=330, energies=(v10.SPIKY,))
        obs = observation(active=(active,))
        self.assertGreater(v10.supporter_value(obs, v10.WALLY), 6000)

    def test_active_wally_never_removes_a_live_spiky_attack_into_protection(self):
        v10 = self.v10
        active = pokemon(
            v10.LOPUNNY,
            10,
            30,
            max_hp=330,
            energies=(v10.SPIKY, v10.MIST),
            tools=(v10.AIR_BALLOON,),
        )
        one_energy_bench = pokemon(
            v10.LOPUNNY,
            11,
            330,
            energies=(v10.SPIKY,),
        )
        protected = pokemon(next(iter(v10.DAMAGE_PROTECTION_POKEMON)), 20, 200)
        obs = observation(
            hand=({"id": v10.WALLY, "serial": 90},),
            active=(active,),
            bench=(one_energy_bench,),
            opponent_active=(protected,),
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 7, "index": 0},
                    {"type": 13, "attackId": v10.SPIKY_HOPPER},
                    {"type": 14},
                ],
            },
        )
        self.assertEqual(v10.agent(obs), [1])

    def test_wally_targets_bench_after_retreat_and_attachment_are_spent(self):
        v10 = self.v10
        active = pokemon(
            v10.LOPUNNY,
            10,
            150,
            max_hp=330,
            energies=(v10.SPIKY, v10.MIST),
            tools=(v10.AIR_BALLOON,),
        )
        ready_bench = pokemon(
            v10.LOPUNNY,
            11,
            250,
            max_hp=330,
            energies=(v10.SPIKY,),
        )
        obs = observation(
            hand=({"id": v10.WALLY, "serial": 90},),
            active=(active,),
            bench=(ready_bench,),
            opponent_active=(pokemon(381, 20, 250),),
            energyAttached=True,
            retreated=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 7, "index": 0},
                    {"type": 13, "attackId": v10.SPIKY_HOPPER},
                    {"type": 14},
                ],
            },
        )
        self.assertEqual(v10.agent(obs), [0])
        target_obs = observation(
            active=(active,),
            bench=(ready_bench,),
            opponent_active=(pokemon(381, 20, 250),),
            energyAttached=True,
            retreated=True,
            supporterPlayed=True,
            select={
                "context": 17,
                "effect": {"id": v10.WALLY},
                "minCount": 1,
                "maxCount": 1,
                "option": [
                    {"type": 3, "playerIndex": 0, "area": 4, "index": 0},
                    {"type": 3, "playerIndex": 0, "area": 5, "index": 0},
                ],
            },
        )
        self.assertEqual(v10.agent(target_obs), [1])

    def test_wally_reattaches_active_when_retreat_is_already_spent(self):
        v10 = self.v10
        damaged = pokemon(
            v10.LOPUNNY,
            10,
            170,
            max_hp=330,
            energies=(v10.SPIKY,),
            tools=(v10.AIR_BALLOON,),
        )
        empty_bench = pokemon(v10.LOPUNNY, 11, 250, max_hp=330)
        target_obs = observation(
            active=(damaged,),
            bench=(empty_bench,),
            retreated=True,
            supporterPlayed=True,
            select={
                "context": 17,
                "effect": {"id": v10.WALLY},
                "minCount": 1,
                "maxCount": 1,
                "option": [
                    {"type": 3, "playerIndex": 0, "area": 4, "index": 0},
                    {"type": 3, "playerIndex": 0, "area": 5, "index": 0},
                ],
            },
        )
        self.assertEqual(v10.agent(target_obs), [0])

        healed = pokemon(
            v10.LOPUNNY,
            10,
            330,
            tools=(v10.AIR_BALLOON,),
        )
        attach_obs = observation(
            hand=({"id": v10.SPIKY, "serial": 90},),
            active=(healed,),
            bench=(empty_bench,),
            retreated=True,
            supporterPlayed=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 4, "inPlayIndex": 0},
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 5, "inPlayIndex": 0},
                ],
            },
        )
        self.assertEqual(v10.agent(attach_obs), [0])

    def test_wally_reattaches_active_when_effect_removes_retreat_option(self):
        v10 = self.v10
        healed = pokemon(
            v10.LOPUNNY,
            10,
            330,
            tools=(v10.AIR_BALLOON,),
        )
        empty_bench = pokemon(v10.LOPUNNY, 11, 330)
        v10.WALLY_HEALED_SERIAL = 10
        v10.WALLY_HEALED_WAS_ACTIVE = True
        attach_obs = observation(
            hand=({"id": v10.SPIKY, "serial": 90},),
            active=(healed,),
            bench=(empty_bench,),
            supporterPlayed=True,
            select={
                "context": 0,
                "minCount": 0,
                "maxCount": 1,
                "option": [
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 4, "inPlayIndex": 0},
                    {"type": 8, "area": 2, "index": 0, "inPlayArea": 5, "inPlayIndex": 0},
                    {"type": 14},
                ],
            },
        )
        self.assertEqual(v10.agent(attach_obs), [0])

    def test_startup_resets_all_cross_game_memory(self):
        v10 = self.v10
        v10.LAST_TURN = (99, 1)
        v10.SEEN_MENUS.add(("stale",))
        v10.FORCE_READY_PROMOTION = True
        v10.WALLY_HEALED_SERIAL = 123
        self.assertEqual(v10.agent({}), v10.EXPECTED_DECK)
        self.assertIsNone(v10.LAST_TURN)
        self.assertEqual(v10.SEEN_MENUS, set())
        self.assertFalse(v10.FORCE_READY_PROMOTION)
        self.assertIsNone(v10.WALLY_HEALED_SERIAL)

    def test_mega_rule_box_is_three_prizes(self):
        v10 = self.v10
        self.assertEqual(v10.prize_value({"id": v10.LOPUNNY}), 3)
        self.assertEqual(v10.prize_value({"id": 121}), 2)
        self.assertEqual(v10.prize_value({"id": 345}), 1)

    def test_every_high_impact_live_wally_state_now_plays_wally(self):
        v10 = self.v10
        episodes = {
            89371815: 11,
            89374507: 7,
            89376120: 7,
            89377182: 13,
        }
        for episode, turn in episodes.items():
            path = ROOT / "scouting_replays" / "our_agent_v10" / "losses" / f"{episode}.json"
            replay = json.loads(path.read_text())
            seat = replay["info"]["TeamNames"].index("ROASTERS")
            found = False
            for index in range(1, len(replay["steps"])):
                previous = replay["steps"][index - 1][seat]
                if previous.get("status") != "ACTIVE":
                    continue
                obs = previous.get("observation") or {}
                state = obs.get("current") or {}
                select = obs.get("select") or {}
                if state.get("turn") != turn or select.get("context") != 0:
                    continue
                options = select.get("option") or []
                wally_indexes = [
                    option_index
                    for option_index, option in enumerate(options)
                    if option.get("type") == 7
                    and source_card_id(obs, option) == v10.WALLY
                ]
                if not wally_indexes:
                    continue
                module = load_final(f"live_{episode}_{turn}")
                action = module.agent(obs)
                self.assertEqual(
                    action,
                    [wally_indexes[0]],
                    f"episode {episode} turn {turn}",
                )
                found = True
                break
            self.assertTrue(found, f"missing live state {episode} turn {turn}")


if __name__ == "__main__":
    unittest.main()
