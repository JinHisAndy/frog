from frog.experiments.stage02_evolution.engine import evolve_population
from frog.experiments.stage02_evolution.model import Genome


def test_mutation_stays_inside_gene_bounds_and_is_seeded():
    result = evolve_population(seed=7, generations=8, population_size=12)

    assert result.best_fitness >= result.initial_best_fitness
    assert all(-1.0 <= gene <= 1.0 for genome in result.final_population for gene in genome.weights)
    assert result == evolve_population(seed=7, generations=8, population_size=12)


def test_genome_scores_foodward_action_higher_than_opposite_action():
    assert Genome((1.0,)).fitness() > Genome((-1.0,)).fitness()
