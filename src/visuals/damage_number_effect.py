from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

if TYPE_CHECKING:
    from src.entity.ball.ball import Ball
from src.visuals.visual_effect import VisualEffect


class DamageNumberEffect(VisualEffect):
    def __init__(self, ball: Ball, amount: int, is_crit: bool):
        super().__init__(2 if is_crit else 1)
        self.ball = ball
        self.amount = amount
        self.is_crit = is_crit

    @override
    def draw(self, display):
        color = (255, 0, 0) if not self.is_crit else (255, 180, 0)
        font = pygame.font.SysFont('Arial', 25, bold=True)
        alpha = int(255 * (self.timer_seconds / 1.0))
        text = f"-{self.amount}"
        pos_x = self.ball.body.position.x
        pos_y = self.ball.body.position.y - self.ball.radius - 18
        display.draw_text(text, (pos_x, pos_y), font, color, alpha=alpha)
