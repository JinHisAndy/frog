from __future__ import annotations

from .model import AvoidAction, HazardObservation


class AvoidHazardEnvironment:
    def __init__(self, *, width: int, hazard: int, sensor_radius: int) -> None:
        if width <= 0 or not 0 <= hazard < width or sensor_radius < 0:
            raise ValueError("invalid hazard environment")
        self.width = width
        self.hazard = hazard
        self.sensor_radius = sensor_radius

    def observe(self, *, position: int) -> HazardObservation:
        offset = self.hazard - position
        return HazardObservation(offset if abs(offset) <= self.sensor_radius else None)

    @staticmethod
    def avoid_policy(observation: HazardObservation) -> AvoidAction:
        if observation.hazard_offset is None or observation.hazard_offset == 0:
            return AvoidAction.IDLE
        return AvoidAction.LEFT if observation.hazard_offset > 0 else AvoidAction.RIGHT
