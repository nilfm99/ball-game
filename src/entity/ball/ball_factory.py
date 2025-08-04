import math
import random

import pygame
import pymunk

from src.configuration.configuration import Configuration
from src.entity.ball.ball import Ball
from src.entity.ball.face_configuration import FaceConfiguration


class BallFactory:
    def __init__(
        self,
        configuration: Configuration,
        ball_specs: list[tuple[str, pygame.Color, FaceConfiguration | None]],
    ):
        self.configuration = configuration
        self.ball_specs = ball_specs

    def random_position(self) -> pymunk.Vec2d:
        x = random.uniform(
            self.configuration.ball_radius,
            self.configuration.sim_width - self.configuration.ball_radius,
        )
        y = random.uniform(
            self.configuration.ball_radius,
            self.configuration.sim_height - self.configuration.ball_radius,
        )
        return pymunk.Vec2d(x, y)

    def random_velocity(self) -> pymunk.Vec2d:
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(self.configuration.min_initial_speed, self.configuration.max_initial_speed)
        return pymunk.Vec2d(speed, 0).rotated(angle)

    def is_overlapping(self, pos: pymunk.Vec2d, other_positions: list[pymunk.Vec2d]) -> bool:
        for other in other_positions:
            if (pos - other).length < 2 * self.configuration.ball_radius:  # type: ignore
                return True
        return False

    def make_balls(self) -> list[Ball]:
        positions = []
        balls = []
        max_tries = 1000
        for i, (name, color, faces) in enumerate(self.ball_specs):
            for _ in range(max_tries):
                pos = self.random_position()
                if not self.is_overlapping(pos, positions):
                    positions.append(pos)
                    break
            else:
                raise RuntimeError(f"Couldn't find non-overlapping position for ball {name}!")
            vel = self.random_velocity()
            ang_vel = random.uniform(0.5, 2)
            balls.append(
                Ball(
                    name,
                    position=pos,
                    velocity=vel,
                    angular_velocity=ang_vel,
                    radius=self.configuration.ball_radius,
                    color=color,
                    faces=faces,
                )
            )
        return balls