from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReflexMemory:
    evidence: dict[tuple[bool, ...], int] = field(default_factory=dict)

    def observe(self, *, pattern: tuple[bool, ...], action: str, outcome: int) -> None:
        if action != "bite":
            return
        self.evidence[pattern] = self.evidence.get(pattern, 0) + outcome

    def predict(self, pattern: tuple[bool, ...]) -> str:
        value = self.evidence.get(pattern, 0)
        if value > 0:
            return "bite"
        if value < 0:
            return "avoid"
        return "explore"
