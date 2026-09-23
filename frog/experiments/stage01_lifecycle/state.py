from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class LifeAction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"


@dataclass(frozen=True)
class LifeState:
    x: int
    y: int
    energy: int
    tick: int
    alive: bool
    foods: frozenset[tuple[int, int]] = frozenset()
