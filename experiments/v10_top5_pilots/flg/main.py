from pathlib import Path
import importlib.util


DECK = [
    1, 1, 11, 11, 11, 11, 14, 14, 14, 14, 18, 18, 18, 18, 20, 20,
    117, 344, 344, 344, 344, 345, 345, 345, 756, 756, 1086, 1086, 1121,
    1121, 1122, 1122, 1122, 1122, 1123, 1137, 1147, 1147, 1147, 1147,
    1159, 1182, 1182, 1182, 1182, 1194, 1194, 1197, 1219, 1219, 1219,
    1219, 1225, 1225, 1227, 1227, 1227, 1227, 1257, 1264,
]


def _load_runner():
    source = Path(__file__).resolve().parents[1] / "_profile_runner.py"
    spec = importlib.util.spec_from_file_location("_v10_flg_runner", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_POLICY = _load_runner().build("crustle_control", DECK)


def agent(obs):
    return _POLICY.agent(obs)

