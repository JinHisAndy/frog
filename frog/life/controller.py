from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .world import Action, CellKind, Observation


class Policy(Protocol):
    sensor_radius: int

    def act(self, observation: Observation) -> Action: ...


@dataclass(frozen=True)
class LinearPolicy:
    food_weight: float
    hazard_weight: float
    sensor_radius: int = 3

    @classmethod
    def move_right(cls) -> "LinearPolicy":
        return cls(food_weight=1.0, hazard_weight=0.0)

    def act(self, observation: Observation) -> Action:
        score = 0.0
        for (dx, _), kind in observation.visible_cells.items():
            if dx == 0:
                continue
            direction = 1.0 if dx > 0 else -1.0
            if kind is CellKind.FOOD:
                score += direction * self.food_weight
            elif kind is CellKind.HAZARD:
                score -= direction * self.hazard_weight
        return Action(dx=1 if score > 0 else -1 if score < 0 else 0)
