from frog.experiments.stage05_development.engine import develop
from frog.experiments.stage05_development.model import SplitGene


def test_same_tree_gene_develops_same_layout_with_node_budget():
    gene = SplitGene(split=True, children=(SplitGene(), SplitGene(split=True, children=(SplitGene(), SplitGene()))))

    first = develop(gene, max_depth=3)
    second = develop(gene, max_depth=3)

    assert first == second
    assert len(first.leaves) == 3
    assert all(0 <= leaf.start < leaf.end <= 1 for leaf in first.leaves)


def test_depth_limit_turns_deeper_splits_into_leaves():
    gene = SplitGene(split=True, children=(SplitGene(split=True, children=(SplitGene(), SplitGene())), SplitGene()))

    layout = develop(gene, max_depth=1)

    assert len(layout.leaves) == 2
