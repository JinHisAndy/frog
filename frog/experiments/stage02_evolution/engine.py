from __future__ import annotations

import random
from dataclasses import dataclass

from .model import Genome


@dataclass(frozen=True)
class EvolutionResult:
    initial_best_fitness: float
    best_fitness: float
    final_population: tuple[Genome, ...]


def _mutate(parent: Genome, random_source: random.Random) -> Genome:
    value = parent.weights[0] + random_source.uniform(-0.25, 0.25)
    return Genome((max(-1.0, min(1.0, value)),))


def evolve_population(*, seed: int, generations: int, population_size: int) -> EvolutionResult:
    if generations < 0 or population_size < 2:
        raise ValueError("generations must be non-negative and population_size must be at least two")
    random_source = random.Random(seed)
    population = [Genome((random_source.uniform(-1.0, 1.0),)) for _ in range(population_size)]
    initial_best = max(genome.fitness() for genome in population)
    for _ in range(generations):
        parent = max(population, key=Genome.fitness)
        population = [parent, *[_mutate(parent, random_source) for _ in range(population_size - 1)]]
    return EvolutionResult(
        initial_best_fitness=initial_best,
        best_fitness=max(genome.fitness() for genome in population),
        final_population=tuple(population),
    )
