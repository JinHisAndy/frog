from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TwoPixelAction:
    bite: bool


@dataclass(frozen=True)
class TwoPixelReflex:
    table: dict[tuple[bool, bool], bool]

    def act(self, pixels: tuple[bool, bool]) -> TwoPixelAction:
        return TwoPixelAction(bite=self.table.get(pixels, False))


@dataclass(frozen=True)
class EvaluationReport:
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int

    @property
    def total(self) -> int:
        return self.true_positive + self.true_negative + self.false_positive + self.false_negative

    @property
    def accuracy(self) -> float:
        return (self.true_positive + self.true_negative) / self.total if self.total else 0.0
