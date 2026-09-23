from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Move(StrEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"


@dataclass(frozen=True)
class GridState:
    x: int
    y: int
    tick: int

    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "tick": self.tick}


@dataclass(frozen=True)
class Trajectory:
    seed: int
    width: int
    height: int
    states: tuple[GridState, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "width": self.width,
            "height": self.height,
            "states": [state.to_dict() for state in self.states],
        }
