from pathlib import Path
import importlib.util


DECK = [
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    673, 673, 674, 674, 675, 675, 676, 676, 676,
    677, 677, 677, 677, 678, 678, 678, 678,
    1102, 1102, 1102, 1102, 1123, 1123,
    1141, 1141, 1141, 1141, 1142, 1142, 1142, 1142,
    1152, 1152, 1159, 1182, 1182, 1182,
    1192, 1192, 1192, 1192, 1227, 1227, 1227, 1227, 1252,
]


def _load_runner():
    source = Path(__file__).resolve().parents[1] / "v10_top5_pilots" / "_profile_runner.py"
    spec = importlib.util.spec_from_file_location("_v11_lucario_runner", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_POLICY = _load_runner().build("lucario_race", DECK)


def agent(obs):
    return _POLICY.agent(obs)
