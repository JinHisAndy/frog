from __future__ import annotations

import random

from .state import GridState, Move, Trajectory


class GridEnvironment:
    def __init__(self, *, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("grid dimensions must be positive")
        self.width = width
        self.height = height

    def step(self, state: GridState, move: Move) -> GridState:
        dx, dy = {
            Move.UP: (0, -1),
            Move.DOWN: (0, 1),
            Move.LEFT: (-1, 0),
            Move.RIGHT: (1, 0),
            Move.IDLE: (0, 0),
        }[move]
        return GridState(
            x=max(0, min(self.width - 1, state.x + dx)),
            y=max(0, min(self.height - 1, state.y + dy)),
            tick=state.tick + 1,
        )

    def run(self, *, seed: int, steps: int) -> Trajectory:
        if steps < 0:
            raise ValueError("steps must not be negative")
        random_source = random.Random(seed)
        state = GridState(x=self.width // 2, y=self.height // 2, tick=0)
        states = [state]
        for _ in range(steps):
            state = self.step(state, random_source.choice(list(Move)))
            states.append(state)
        return Trajectory(seed=seed, width=self.width, height=self.height, states=tuple(states))
