from frog.experiments.stage03_sensor_action.engine import LocalSensorEnvironment
from frog.experiments.stage03_sensor_action.model import SensorAction


def test_observation_hides_food_outside_local_radius():
    environment = LocalSensorEnvironment(width=5, food=(4, 0), sensor_radius=1)

    observation = environment.observe(position=(0, 0))

    assert observation.food_offset is None


def test_greedy_policy_moves_toward_visible_food_without_world_access():
    environment = LocalSensorEnvironment(width=5, food=(2, 0), sensor_radius=3)

    action = environment.greedy_visible_policy(environment.observe(position=(0, 0)))

    assert action is SensorAction.RIGHT
