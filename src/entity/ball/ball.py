import math
import random
from typing import override

import pygame
import pymunk

from src.entity.ball.face_configuration import FaceConfiguration
from src.entity.entity import Entity
from src.game.display import Display


class Ball(Entity):
    COLLISION_TYPE = 1
    MAX_CRIT_TIMER = 60
    ANGRY_FACE_PER_DAMAGE = 5
    SPEEDUP_RATE = 0.001
    SPEEDUP_CHANCE = 0.1
    VELOCITY_CAP = 2000

    def __init__(
        self,
        name: str,
        position: pymunk.Vec2d,
        velocity: pymunk.Vec2d,
        angular_velocity: float,
        color: pygame.Color,
        radius: float = 40,
        mass: float = 1,
        initial_health: int = 100,
        faces: FaceConfiguration | None = None,
    ) -> None:
        self.health = initial_health
        self.crit_timer = 0
        self.hit_timer = 0
        self.faces = faces

        self.name = name
        self.radius = radius
        self.color = color

        moment: float = pymunk.moment_for_circle(mass, 0, radius)
        self.body: pymunk.Body = pymunk.Body(mass, moment)
        self.body.position = position
        self.body.velocity = velocity
        self.body.angular_velocity = angular_velocity
        self.body.user_data = self

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1.0
        self.shape.friction = 0.1

        self.shape.collision_type = self.COLLISION_TYPE

    def load_faces(self) -> None:
        if self.faces is not None:
            self.faces.load_images()

    @override
    def add_to_space(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)

    @override
    def update(self, dt: float) -> None:
        self.crit_timer = max(0, self.crit_timer - 1)
        self.hit_timer = max(0, self.hit_timer - 1)
        if random.random() < self.SPEEDUP_CHANCE and self.body.velocity.length < self.VELOCITY_CAP:
            self.body.velocity *= 1 + self.SPEEDUP_RATE

    @override
    def draw(self, display: Display) -> None:
        if self.health <= 0:
            return

        pos = (self.body.position.x, self.body.position.y)

        # Ball base
        display.draw_circle(pos, self.radius, self.color)

        # Face image (rotated)
        if self.faces is not None:
            angle_deg = -self.body.angle * 180 / math.pi
            display.draw_image(self.get_current_face(), pos, angle_deg)

        # Crit halo
        if self.crit_timer > 0:
            max_halo_radius = self.radius + 20
            min_halo_radius = self.radius + 8
            halo_radius = int(
                min_halo_radius + (max_halo_radius - min_halo_radius) * (self.crit_timer / self.MAX_CRIT_TIMER)
            )
            alpha = int(180 * (self.crit_timer / self.MAX_CRIT_TIMER))
            display.draw_halo(pos, halo_radius, alpha)

        # Health text below the ball
        health_text = f"{int(self.health)}"
        health_font = pygame.font.SysFont('Arial', 18, bold=True)
        text_center = (pos[0], pos[1] + self.radius + 12)
        display.draw_text(health_text, text_center, health_font, (80, 80, 80))

    def set_crit(self) -> None:
        self.crit_timer = self.MAX_CRIT_TIMER

    def set_hit(self, damage: int) -> None:
        self.hit_timer = damage * self.ANGRY_FACE_PER_DAMAGE

    def get_current_face(self) -> pygame.Surface:
        assert self.faces is not None
        return self.faces.happy_surface if self.hit_timer == 0 else self.faces.sad_surface

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}) at ({self.body.position.x}, {self.body.position.y})"

    def __repr__(self) -> str:
        return self.__str__()