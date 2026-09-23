from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AvoidAction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"


@dataclass(frozen=True)
class HazardObservation:
    hazard_offset: int | None
