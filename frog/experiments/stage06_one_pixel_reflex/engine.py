from __future__ import annotations

from .model import OnePixelReflex


def train_one_pixel_reflex(*, training: list[tuple[bool, bool]]) -> OnePixelReflex:
    """Train from (pixel, sweet_feedback) pairs; act() later receives only the pixel."""
    positive = sum(1 for pixel, sweet in training if pixel and sweet)
    negative = sum(1 for pixel, sweet in training if pixel and not sweet)
    return OnePixelReflex(positive_count=positive, negative_count=negative)
