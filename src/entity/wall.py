from typing import override

import pymunk
from src.entity.entity import Entity
from src.game.display import Display


class Wall(Entity):
    def __init__(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        thickness: int = 10,
        color: tuple[int, int, int] = (50, 50, 50)
    ) -> None:
        self.start = start
        self.end = end
        self.thickness = thickness
        self.color = color

    @override
    def add_to_space(self, space: pymunk.Space) -> None:
        shape = pymunk.Segment(space.static_body, self.start, self.end, self.thickness / 2)
        shape.elasticity = 1.0
        shape.friction = 0.0
        space.add(shape)

    @override
    def update(self, dt: float) -> None:
        pass  # Static wall, nothing to update

    @override
    def draw(self, display: Display) -> None:
        display.draw_line(self.start, self.end, self.color, self.thickness)
