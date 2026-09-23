from __future__ import annotations

from dataclasses import dataclass

from .world import Position


@dataclass(frozen=True)
class Organism:
    position: Position
    energy: int

    @classmethod
    def at(cls, position: Position, *, energy: int) -> "Organism":
        return cls(position=position, energy=energy)

    @property
    def alive(self) -> bool:
        return self.energy > 0

    def with_state(self, *, position: Position, energy: int) -> "Organism":
        return Organism(position=position, energy=energy)
