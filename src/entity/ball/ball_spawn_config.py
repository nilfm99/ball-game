from dataclasses import dataclass

import pymunk

from src.entity.ball.ball_prototype import BallPrototype


@dataclass(frozen=True)
class BallSpawnConfig:
    prototype: BallPrototype
    position: pymunk.Vec2d
    velocity: pymunk.Vec2d
    angular_velocity: float
    radius: float = 40
    mass: float = 1
    initial_health: int = 100