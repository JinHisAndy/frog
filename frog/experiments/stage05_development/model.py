from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SplitGene:
    split: bool = False
    children: tuple["SplitGene", "SplitGene"] | tuple[()] = ()

    def __post_init__(self) -> None:
        if self.split and len(self.children) != 2:
            raise ValueError("a split gene must have exactly two children")
        if not self.split and self.children:
            raise ValueError("a leaf gene must not have children")


@dataclass(frozen=True)
class Leaf:
    start: float
    end: float
    depth: int


@dataclass(frozen=True)
class Layout:
    leaves: tuple[Leaf, ...]
