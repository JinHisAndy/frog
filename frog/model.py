from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Chemical(StrEnum):
    DOPAMINE = "dopamine"
    NOREPINEPHRINE = "norepinephrine"
    GLUTAMATE = "glutamate"
    GABA = "gaba"
    NONE = "none"


@dataclass
class Node:
    identifier: str
    threshold: float
    chemical: Chemical = Chemical.NONE
    layer: int = 0
    current_input: float = 0.0
    activated: bool = False

    def reset(self) -> None:
        self.current_input = 0.0
        self.activated = False

    def evaluate(self) -> bool:
        self.activated = self.current_input >= self.threshold
        return self.activated

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.identifier,
            "threshold": self.threshold,
            "chemical": self.chemical.value,
            "layer": self.layer,
            "current_input": self.current_input,
            "activated": self.activated,
        }


@dataclass
class Link:
    source: str
    target: str
    weight: float
    modulated_by: Chemical = Chemical.NONE
    plasticity_delta: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "modulated_by": self.modulated_by.value,
            "plasticity_delta": self.plasticity_delta,
        }


@dataclass(frozen=True)
class Observation:
    pixels: tuple[bool, bool, bool, bool]
    pain: bool = False
    sweet: bool = False

    def to_dict(self) -> dict[str, object]:
        return {"pixels": list(self.pixels), "pain": self.pain, "sweet": self.sweet}


@dataclass(frozen=True)
class Action:
    flee: bool
    bite: bool

    def to_dict(self) -> dict[str, bool]:
        return {"flee": self.flee, "bite": self.bite}


@dataclass
class Frame:
    index: int
    phase: str
    message: str
    observation: Observation
    active_chemicals: list[Chemical] = field(default_factory=list)
    action: Action | None = None
    network: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "index": self.index,
            "phase": self.phase,
            "message": self.message,
            "observation": self.observation.to_dict(),
            "active_chemicals": [chemical.value for chemical in self.active_chemicals],
            "action": self.action.to_dict() if self.action else None,
            "network": self.network,
        }
