from frog.experiments.stage01_lifecycle.engine import FoodEnvironment
from frog.experiments.stage01_lifecycle.state import LifeAction, LifeState


def test_food_increases_energy_once_and_is_removed():
    environment = FoodEnvironment(width=3, height=1, foods={(1, 0)}, initial_energy=3, food_energy=5)

    state = environment.step(environment.initial_state(), LifeAction.RIGHT)

    assert state.energy == 7
    assert state.alive is True
    assert state.foods == frozenset()


def test_energy_depletion_ends_lifecycle():
    environment = FoodEnvironment(width=1, height=1, foods=set(), initial_energy=1, food_energy=5)

    state = environment.step(LifeState(x=0, y=0, energy=1, tick=0, alive=True), LifeAction.IDLE)

    assert state.energy == 0
    assert state.alive is False
