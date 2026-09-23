from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReflexAction:
    bite: bool


@dataclass(frozen=True)
class OnePixelReflex:
    positive_count: int
    negative_count: int

    def act(self, pixel: bool) -> ReflexAction:
        learned_positive = self.positive_count > self.negative_count and self.positive_count > 0
        return ReflexAction(bite=pixel and learned_positive)
