import json

from frog.experiments.stage00_kernel.engine import GridEnvironment
from frog.experiments.stage00_kernel.state import GridState, Move


def test_step_clamps_agent_at_grid_boundary_and_advances_one_tick():
    environment = GridEnvironment(width=5, height=5)
    initial = GridState(x=0, y=0, tick=0)

    next_state = environment.step(initial, Move.LEFT)

    assert next_state == GridState(x=0, y=0, tick=1)


def test_same_seed_and_actions_produce_byte_identical_trajectory_json():
    environment = GridEnvironment(width=5, height=5)

    first = environment.run(seed=17, steps=12)
    second = environment.run(seed=17, steps=12)

    assert json.dumps(first.to_dict(), sort_keys=True) == json.dumps(second.to_dict(), sort_keys=True)
