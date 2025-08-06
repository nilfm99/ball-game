from typing import override

import pygame

from src.display.display import Display
from src.visuals.visual_effect import VisualEffect


class ImplosionEffect(VisualEffect):
    def __init__(
            self,
            pos: tuple[float, float],
            initial_radius: float,
            color: pygame.Color = pygame.Color(100, 200, 255),
            duration: float = 1,
    ):
        super().__init__(duration)
        self.pos = pos
        self.initial_radius = initial_radius
        self.color = color
        self.duration = duration

    @override
    def draw(self, display: Display) -> None:
        progress = 1.0 - (self.timer_seconds / self.duration)
        radius = int(self.initial_radius * (1 - progress))
        if radius <= 0:
            return
        alpha = int(255 * (1 - progress))
        # Draw a shrinking, fading circle
        display.draw_circle(self.pos, radius, self.color, alpha=alpha)
