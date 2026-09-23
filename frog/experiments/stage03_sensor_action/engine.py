from __future__ import annotations

from .model import LocalObservation, SensorAction


class LocalSensorEnvironment:
    def __init__(self, *, width: int, food: tuple[int, int], sensor_radius: int) -> None:
        if width <= 0 or sensor_radius < 0 or not 0 <= food[0] < width:
            raise ValueError("invalid world or food position")
        self.width = width
        self.food = food
        self.sensor_radius = sensor_radius

    def observe(self, *, position: tuple[int, int]) -> LocalObservation:
        offset = self.food[0] - position[0]
        return LocalObservation(food_offset=offset if abs(offset) <= self.sensor_radius else None)

    @staticmethod
    def greedy_visible_policy(observation: LocalObservation) -> SensorAction:
        if observation.food_offset is None or observation.food_offset == 0:
            return SensorAction.IDLE
        return SensorAction.RIGHT if observation.food_offset > 0 else SensorAction.LEFT
