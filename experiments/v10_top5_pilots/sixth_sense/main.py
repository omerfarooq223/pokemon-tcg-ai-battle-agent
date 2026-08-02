from pathlib import Path
import importlib.util


DECK = [
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 104, 104, 112, 112, 112, 112,
    646, 646, 646, 646, 647, 647, 647, 648, 648, 648, 860, 860, 1079,
    1079, 1079, 1080, 1086, 1086, 1086, 1086, 1097, 1097, 1097, 1122,
    1137, 1152, 1152, 1152, 1152, 1182, 1182, 1219, 1219, 1219, 1219,
    1227, 1227, 1227, 1227, 1231, 1259, 1259, 1259, 1259,
]


def _load_runner():
    source = Path(__file__).resolve().parents[1] / "_profile_runner.py"
    spec = importlib.util.spec_from_file_location("_v10_sixth_runner", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_POLICY = _load_runner().build("grimmsnarl_spread", DECK)


def agent(obs):
    return _POLICY.agent(obs)

