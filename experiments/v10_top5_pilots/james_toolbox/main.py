from pathlib import Path
import importlib.util


DECK = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 5, 6, 6, 63, 63,
    96, 96, 96, 108, 140, 184, 184, 272, 756, 756, 756, 978, 1071,
    1071, 1071, 1088, 1097, 1097, 1098, 1098, 1116, 1116, 1116, 1116,
    1121, 1121, 1121, 1121, 1182, 1182, 1197, 1197, 1198, 1198, 1198,
    1198, 1205, 1205, 1250, 1250, 1250, 1250,
]


def _load_runner():
    source = Path(__file__).resolve().parents[1] / "_profile_runner.py"
    spec = importlib.util.spec_from_file_location("_v10_james_runner", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_POLICY = _load_runner().build("area_zero_toolbox", DECK)


def agent(obs):
    return _POLICY.agent(obs)

