from __future__ import annotations

from .state import LifeAction, LifeState


class FoodEnvironment:
    def __init__(
        self,
        *,
        width: int,
        height: int,
        foods: set[tuple[int, int]],
        initial_energy: int,
        food_energy: int,
    ) -> None:
        if width <= 0 or height <= 0 or initial_energy <= 0 or food_energy <= 0:
            raise ValueError("dimensions and energy values must be positive")
        self.width = width
        self.height = height
        self.foods = frozenset(foods)
        self.initial_energy = initial_energy
        self.food_energy = food_energy

    def initial_state(self, *, x: int = 0, y: int = 0) -> LifeState:
        return LifeState(x=x, y=y, energy=self.initial_energy, tick=0, alive=True, foods=self.foods)

    def step(self, state: LifeState, action: LifeAction) -> LifeState:
        if not state.alive:
            return state
        dx = {LifeAction.LEFT: -1, LifeAction.RIGHT: 1, LifeAction.IDLE: 0}[action]
        x = max(0, min(self.width - 1, state.x + dx))
        position = (x, state.y)
        foods = state.foods
        energy = state.energy - 1
        if position in foods:
            foods = foods - {position}
            energy += self.food_energy
        return LifeState(
            x=x,
            y=state.y,
            energy=max(0, energy),
            tick=state.tick + 1,
            alive=energy > 0,
            foods=foods,
        )
