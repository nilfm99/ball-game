from __future__ import annotations

from typing import TYPE_CHECKING

from src.game.display import Display

if TYPE_CHECKING:
    from src.entity.ball.ball import Ball
from src.visuals.visual_effect import VisualEffect


class HaloEffect(VisualEffect):
    def __init__(self, ball: Ball, duration: float = 1.0):
        super().__init__(duration)
        self.ball = ball
        self.radius = ball.radius
        self.duration = duration

    def draw(self, display: Display) -> None:
        if self.ball.health <= 0:
            return
        pos = (self.ball.body.position.x, self.ball.body.position.y)
        progress = self.timer_seconds / self.duration
        max_halo_radius = self.radius + 20
        min_halo_radius = self.radius + 8
        halo_radius = int(min_halo_radius + (max_halo_radius - min_halo_radius) * progress)
        alpha = int(180 * progress)
        display.draw_halo(pos, halo_radius, alpha)
