from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BranchGene:
    split: bool = False
    left: "BranchGene | None" = None
    right: "BranchGene | None" = None

    def __post_init__(self) -> None:
        if self.split and (self.left is None or self.right is None):
            raise ValueError("split gene requires both child genes")
        if not self.split and (self.left is not None or self.right is not None):
            raise ValueError("leaf gene cannot have child genes")


def develop_line(gene: BranchGene, *, depth_limit: int) -> tuple[tuple[float, float], ...]:
    if depth_limit < 0:
        raise ValueError("depth_limit must be non-negative")
    leaves: list[tuple[float, float]] = []

    def visit(current: BranchGene, start: float, end: float, depth: int) -> None:
        if not current.split or depth >= depth_limit:
            leaves.append((start, end))
            return
        midpoint = (start + end) / 2
        assert current.left is not None and current.right is not None
        visit(current.left, start, midpoint, depth + 1)
        visit(current.right, midpoint, end, depth + 1)

    visit(gene, 0.0, 1.0, 0)
    return tuple(leaves)
