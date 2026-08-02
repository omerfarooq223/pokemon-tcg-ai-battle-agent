from pathlib import Path
import importlib.util


DECK = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    18, 18, 96, 96, 96, 96, 1094, 1094, 1094, 1094, 1118, 1118, 1119,
    1119, 1119, 1119, 1122, 1122, 1122, 1127, 1127, 1137, 1147, 1147,
    1159, 1182, 1182, 1182, 1201, 1213, 1213, 1213, 1213, 1221, 1223,
    1223, 1227, 1227, 1227, 1227, 1251, 1251,
]


def _load_runner():
    source = Path(__file__).resolve().parents[1] / "_profile_runner.py"
    spec = importlib.util.spec_from_file_location("_v10_rmy_runner", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_POLICY = _load_runner().build("ogerpon_engine", DECK)


def agent(obs):
    return _POLICY.agent(obs)

