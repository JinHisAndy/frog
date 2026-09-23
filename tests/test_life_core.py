from frog.life.controller import LinearPolicy
from frog.life.organism import Organism
from frog.life.world import CellKind, GridWorld, Position


def test_organism_loses_energy_then_gains_energy_only_after_eating_food():
    world = GridWorld.from_cells(width=3, height=1, cells={Position(1, 0): CellKind.FOOD})
    organism = Organism.at(Position(0, 0), energy=3)

    state = world.step(organism, LinearPolicy.move_right())

    assert state.organism.energy == 7
    assert state.organism.alive
    assert state.world.cell_at(Position(1, 0)) is CellKind.EMPTY


def test_observation_is_local_and_cannot_reveal_a_distant_hazard():
    world = GridWorld.from_cells(width=6, height=1, cells={Position(5, 0): CellKind.HAZARD})
    organism = Organism.at(Position(0, 0), energy=5)

    observation = world.observe(organism, radius=1)

    assert observation.visible_cells == {(0, 0): CellKind.EMPTY, (1, 0): CellKind.EMPTY}
    assert observation.energy == 5


def test_policy_uses_observation_to_choose_foodward_action_not_world_truth():
    world = GridWorld.from_cells(width=3, height=1, cells={Position(2, 0): CellKind.FOOD})
    organism = Organism.at(Position(0, 0), energy=5)
    policy = LinearPolicy(food_weight=2.0, hazard_weight=0.0)

    action = policy.act(world.observe(organism, radius=3))

    assert action.dx == 1
