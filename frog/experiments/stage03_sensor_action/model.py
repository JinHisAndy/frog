from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SensorAction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"


@dataclass(frozen=True)
class LocalObservation:
    food_offset: int | None
