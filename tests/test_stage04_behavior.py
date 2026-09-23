from frog.experiments.stage04_behavior.engine import AvoidHazardEnvironment
from frog.experiments.stage04_behavior.model import AvoidAction


def test_avoid_policy_moves_away_from_visible_hazard():
    environment = AvoidHazardEnvironment(width=5, hazard=2, sensor_radius=3)

    action = environment.avoid_policy(environment.observe(position=1))

    assert action is AvoidAction.LEFT


def test_hidden_hazard_does_not_leak_through_observation():
    environment = AvoidHazardEnvironment(width=8, hazard=7, sensor_radius=1)

    assert environment.observe(position=0).hazard_offset is None
