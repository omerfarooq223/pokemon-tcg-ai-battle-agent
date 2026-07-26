import argparse
import ast
import os
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ["main.py", "deck.csv"]
OPTIONAL_FILES = ["policy.json"]


def validate_kaggle_loader(agent_dir: Path, deck: list[int]) -> None:
    source = (agent_dir / "main.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    if not functions or functions[-1] != "agent":
        raise ValueError("The final function in main.py must be agent")

    original_cwd = Path.cwd()
    environment = {"__builtins__": __builtins__}
    try:
        os.chdir(agent_dir)
        exec(compile(source, "main.py", "exec"), environment)
    finally:
        os.chdir(original_cwd)
    if "__file__" in environment:
        raise RuntimeError("Loader validation unexpectedly defined __file__")
    if environment["agent"]({"select": None}) != deck:
        raise RuntimeError("Agent did not return the packaged deck at startup")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-dir", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "submission.tar.gz")
    args = parser.parse_args()
    agent_dir = args.agent_dir.resolve()
    output = args.output.resolve()

    for name in REQUIRED_FILES:
        path = agent_dir / name
        if not path.exists():
            raise FileNotFoundError(path)

    deck = [
        int(line.strip().split(",")[0])
        for line in (agent_dir / "deck.csv").read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(deck) != 60:
        raise ValueError(f"deck.csv must contain exactly 60 cards, got {len(deck)}")

    validate_kaggle_loader(agent_dir, deck)

    files = REQUIRED_FILES + [
        name for name in OPTIONAL_FILES if (agent_dir / name).exists()
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, "w:gz") as tar:
        for name in files:
            tar.add(agent_dir / name, arcname=name)

    print(output)


if __name__ == "__main__":
    main()
