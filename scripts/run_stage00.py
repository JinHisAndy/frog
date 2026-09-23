import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from frog.experiments.stage00_kernel.engine import GridEnvironment


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Frog Stage 00 deterministic grid kernel.")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/stages/stage00-kernel.json")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    trajectory = GridEnvironment(width=config["width"], height=config["height"]).run(
        seed=config["seed"],
        steps=config["steps"],
    )
    print(json.dumps(trajectory.to_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
