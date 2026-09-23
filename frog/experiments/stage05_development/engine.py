from __future__ import annotations

from .model import Layout, Leaf, SplitGene


def develop(gene: SplitGene, *, max_depth: int) -> Layout:
    if max_depth < 0:
        raise ValueError("max_depth must not be negative")
    leaves: list[Leaf] = []

    def visit(current: SplitGene, start: float, end: float, depth: int) -> None:
        if not current.split or depth >= max_depth:
            leaves.append(Leaf(start=start, end=end, depth=depth))
            return
        midpoint = (start + end) / 2
        visit(current.children[0], start, midpoint, depth + 1)
        visit(current.children[1], midpoint, end, depth + 1)

    visit(gene, 0.0, 1.0, 0)
    return Layout(leaves=tuple(leaves))
