from frog.simulation.config import CellDefaults, EvolutionConfig, SimpleWorldConfig
from frog.simulation.genome import Genome


def test_simple_world_defaults_are_small_finite_and_externally_tunable():
    config = SimpleWorldConfig()

    assert (config.width, config.height) == (128, 128)
    assert config.initial_resource_density == 0.02
    assert config.resource_regeneration_rate == 0.0001
    assert config.initial_organisms == 1
    assert config.max_ticks == 10_000


def test_founder_cell_starts_neutral_without_food_or_hazard_knowledge():
    genome = Genome.founder()

    assert genome.food_attraction == 0.0
    assert genome.hazard_avoidance == 0.0
    assert genome.horizontal_bias == 0.0
    assert genome.vertical_bias == 0.0
    assert genome.exploration == 1.0


def test_initial_cell_attributes_make_survival_and_reproduction_possible_but_not_free():
    defaults = CellDefaults()

    assert defaults.initial_energy == 20
    assert defaults.reproduction_threshold == 30
    assert defaults.reproduction_energy == 15
    assert defaults.food_energy == 12
    assert defaults.basal_cost == 1
    assert defaults.max_age == 500


def test_evolution_defaults_mutate_some_offspring_but_not_every_property_every_time():
    config = EvolutionConfig()

    assert 0 < config.mutation_probability < 1
    assert 0 < config.mutation_sigma < 1
    assert config.objective == "viable_descendants"
