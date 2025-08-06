from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entity.ball.ball import Ball


class BallModifier:
    def __init__(self, duration: float) -> None:
        self.duration = duration

    def update(self, dt: float) -> None:
        self.duration = max(0.0, self.duration - dt)

    def is_active(self) -> bool:
        return self.duration > 0

    def apply(self, ball: Ball) -> None:
        """Override in subclasses to modify drawing or behavior."""
        pass
