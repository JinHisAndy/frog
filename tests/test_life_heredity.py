from frog.life.development import BranchGene, develop_line
from frog.life.evolution import evolve_policies


def test_development_program_compresses_a_branching_layout_deterministically():
    gene = BranchGene(split=True, left=BranchGene(), right=BranchGene(split=True, left=BranchGene(), right=BranchGene()))

    assert develop_line(gene, depth_limit=3) == ((0.0, 0.5), (0.5, 0.75), (0.75, 1.0))


def test_evolution_preserves_or_improves_best_policy_for_foodward_world():
    result = evolve_policies(seed=9, generations=6, population_size=10)

    assert result.best_score >= result.initial_best_score
    assert result.best_policy.food_weight >= -1.0
