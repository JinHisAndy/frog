from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimpleWorldConfig:
    """External controls for the first finite-world experiment."""

    width: int = 128
    height: int = 128
    initial_resource_density: float = 0.02
    resource_regeneration_rate: float = 0.0001
    initial_organisms: int = 1
    max_ticks: int = 10_000
    seed: int = 1


@dataclass(frozen=True)
class CellDefaults:
    """Founder phenotype. Evolution changes the genome, not these world axioms."""

    initial_energy: int = 20
    reproduction_threshold: int = 30
    reproduction_energy: int = 15
    food_energy: int = 12
    basal_cost: int = 1
    move_cost: int = 1
    hazard_damage: int = 10
    sensor_radius: int = 1
    max_age: int = 500


@dataclass(frozen=True)
class EvolutionConfig:
    mutation_probability: float = 0.10
    mutation_sigma: float = 0.15
    population_limit: int = 10_000
    objective: str = "viable_descendants"
