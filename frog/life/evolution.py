from __future__ import annotations

import random
from dataclasses import dataclass

from .controller import LinearPolicy


@dataclass(frozen=True)
class EvolutionResult:
    initial_best_score: float
    best_score: float
    best_policy: LinearPolicy


def _score(policy: LinearPolicy) -> float:
    """Transparent proxy: favor food attraction while penalizing hazard attraction."""
    return policy.food_weight + policy.hazard_weight


def evolve_policies(*, seed: int, generations: int, population_size: int) -> EvolutionResult:
    if generations < 0 or population_size < 2:
        raise ValueError("invalid evolution budget")
    rng = random.Random(seed)
    population = [LinearPolicy(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(population_size)]
    initial = max(_score(policy) for policy in population)
    for _ in range(generations):
        parent = max(population, key=_score)
        population = [parent]
        for _ in range(population_size - 1):
            population.append(
                LinearPolicy(
                    food_weight=max(-1.0, min(1.0, parent.food_weight + rng.uniform(-0.2, 0.2))),
                    hazard_weight=max(-1.0, min(1.0, parent.hazard_weight + rng.uniform(-0.2, 0.2))),
                )
            )
    best = max(population, key=_score)
    return EvolutionResult(initial_best_score=initial, best_score=_score(best), best_policy=best)
