from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from src.display.display import Display

if TYPE_CHECKING:
    from src.entity.ball.ball import Ball
from src.visuals.visual_effect import VisualEffect


class DamageNumberEffect(VisualEffect):
    def __init__(
            self,
            ball: Ball,
            amount: int,
            is_crit: bool,
            min_size: int = 20,
            max_size: int = 80,
    ) -> None:
        super().__init__(self._get_duration(is_crit))
        self.ball = ball
        self.amount = amount
        self.is_crit = is_crit
        self.min_size = min_size
        self.max_size = max_size

    @staticmethod
    def _get_duration(is_crit: bool) -> int:
        return 2 if is_crit else 1

    def _get_font_size(self, damage: int) -> int:
        return self.min_size + (self.max_size - self.min_size) * damage // 100

    def _get_y_drift(self) -> int:
        max_drift = 100
        duration = self._get_duration(self.is_crit)
        return duration * int(max_drift * (1 - self.timer_seconds / duration))

    @override
    def draw(self, display: Display) -> None:
        color = (255, 0, 0) if not self.is_crit else (255, 180, 0)
        font = pygame.font.SysFont('Arial', self._get_font_size(damage=self.amount), bold=True)
        alpha = int(255 * self.timer_seconds / self._get_duration(self.is_crit))
        text = f"-{self.amount}"
        pos_x = self.ball.body.position.x
        pos_y = self.ball.body.position.y - self.ball.radius - 18 - self._get_y_drift()
        display.draw_text(text, (pos_x, pos_y), font, color, alpha=alpha)
