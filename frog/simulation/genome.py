from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Genome:
    """Heritable behavioral parameters; the founder knows no semantic category."""

    food_attraction: float
    hazard_avoidance: float
    horizontal_bias: float
    vertical_bias: float
    exploration: float
    reproduction_threshold_delta: float = 0.0
    basal_cost_delta: float = 0.0

    @classmethod
    def founder(cls) -> "Genome":
        return cls(
            food_attraction=0.0,
            hazard_avoidance=0.0,
            horizontal_bias=0.0,
            vertical_bias=0.0,
            exploration=1.0,
        )
