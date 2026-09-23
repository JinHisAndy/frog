from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING


class CellKind(StrEnum):
    EMPTY = "empty"
    FOOD = "food"
    HAZARD = "hazard"


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Action:
    dx: int
    dy: int = 0


@dataclass(frozen=True)
class Observation:
    visible_cells: dict[tuple[int, int], CellKind]
    energy: int


@dataclass(frozen=True)
class WorldStep:
    world: "GridWorld"
    organism: "Organism"


class GridWorld:
    def __init__(self, *, width: int, height: int, cells: dict[Position, CellKind]) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("world dimensions must be positive")
        self.width = width
        self.height = height
        self._cells = dict(cells)

    @classmethod
    def from_cells(cls, *, width: int, height: int, cells: dict[Position, CellKind]) -> "GridWorld":
        return cls(width=width, height=height, cells=cells)

    def cell_at(self, position: Position) -> CellKind:
        return self._cells.get(position, CellKind.EMPTY)

    def observe(self, organism: "Organism", *, radius: int) -> Observation:
        visible: dict[tuple[int, int], CellKind] = {}
        for x in range(max(0, organism.position.x - radius), min(self.width, organism.position.x + radius + 1)):
            for y in range(max(0, organism.position.y - radius), min(self.height, organism.position.y + radius + 1)):
                visible[(x - organism.position.x, y - organism.position.y)] = self.cell_at(Position(x, y))
        return Observation(visible_cells=visible, energy=organism.energy)

    def step(self, organism: "Organism", policy: "Policy") -> WorldStep:
        if not organism.alive:
            return WorldStep(world=self, organism=organism)
        action = policy.act(self.observe(organism, radius=policy.sensor_radius))
        next_position = Position(
            max(0, min(self.width - 1, organism.position.x + action.dx)),
            max(0, min(self.height - 1, organism.position.y + action.dy)),
        )
        energy = organism.energy - 1
        cells = dict(self._cells)
        if cells.get(next_position) is CellKind.FOOD:
            energy += 5
            del cells[next_position]
        if cells.get(next_position) is CellKind.HAZARD:
            energy -= 5
        next_organism = organism.with_state(position=next_position, energy=max(0, energy))
        return WorldStep(world=GridWorld(width=self.width, height=self.height, cells=cells), organism=next_organism)


if TYPE_CHECKING:
    from .controller import Policy
    from .organism import Organism
