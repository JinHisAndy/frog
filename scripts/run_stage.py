from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def run(stage: str) -> dict[str, object]:
    if stage == "00":
        from frog.experiments.stage00_kernel.engine import GridEnvironment

        config = json.loads((ROOT / "configs/stages/stage00-kernel.json").read_text())
        return {
            "stage": "00",
            "trajectory": GridEnvironment(width=config["width"], height=config["height"]).run(
                seed=config["seed"], steps=config["steps"]
            ).to_dict(),
        }
    if stage == "01":
        from frog.experiments.stage01_lifecycle.engine import FoodEnvironment
        from frog.experiments.stage01_lifecycle.state import LifeAction

        environment = FoodEnvironment(width=3, height=1, foods={(1, 0)}, initial_energy=3, food_energy=5)
        state = environment.step(environment.initial_state(), LifeAction.RIGHT)
        return {
            "stage": "01",
            "state": {
                "x": state.x,
                "y": state.y,
                "energy": state.energy,
                "tick": state.tick,
                "alive": state.alive,
                "foods": sorted(state.foods),
            },
        }
    if stage == "02":
        from frog.experiments.stage02_evolution.engine import evolve_population

        result = evolve_population(seed=7, generations=8, population_size=12)
        return {"stage": "02", "initial_best": result.initial_best_fitness, "best": result.best_fitness}
    if stage == "03":
        from frog.experiments.stage03_sensor_action.engine import LocalSensorEnvironment

        environment = LocalSensorEnvironment(width=5, food=(2, 0), sensor_radius=3)
        action = environment.greedy_visible_policy(environment.observe(position=(0, 0)))
        return {"stage": "03", "action": action.value}
    if stage == "04":
        from frog.experiments.stage04_behavior.engine import AvoidHazardEnvironment

        environment = AvoidHazardEnvironment(width=5, hazard=2, sensor_radius=3)
        return {"stage": "04", "action": environment.avoid_policy(environment.observe(position=1)).value}
    if stage == "05":
        from frog.experiments.stage05_development.engine import develop
        from frog.experiments.stage05_development.model import SplitGene

        layout = develop(SplitGene(split=True, children=(SplitGene(), SplitGene())), max_depth=2)
        return {"stage": "05", "leaves": [leaf.__dict__ for leaf in layout.leaves]}
    if stage == "06":
        from frog.experiments.stage06_one_pixel_reflex.engine import train_one_pixel_reflex

        model = train_one_pixel_reflex(training=[(True, True), (False, False)])
        return {"stage": "06", "pixel_on_bite": model.act(True).bite, "pixel_off_bite": model.act(False).bite}
    if stage == "07":
        from frog.experiments.stage07_two_pixel_reflex.engine import evaluate, train_two_pixel_reflex

        model = train_two_pixel_reflex(training=[((False, True), True), ((True, True), False)])
        report = evaluate(model, [((False, True), True), ((True, True), False)])
        return {"stage": "07", "accuracy": report.accuracy, "confusion": report.__dict__}
    raise ValueError(f"unknown stage: {stage}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Frog incremental experiment stage.")
    parser.add_argument("stage", choices=[f"{number:02}" for number in range(8)])
    args = parser.parse_args()
    print(json.dumps(run(args.stage), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
