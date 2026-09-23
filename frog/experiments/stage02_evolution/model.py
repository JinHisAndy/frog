from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Genome:
    weights: tuple[float, ...]

    def fitness(self) -> float:
        """A transparent toy objective: positive motion points toward one fixed food source."""
        return self.weights[0]
