import math
import random
from typing import override

import pygame
import pymunk

from src.entity.ball.ball_spawn_config import BallSpawnConfig
from src.entity.ball.modifiers.angry_modifier import AngryModifier
from src.entity.ball.modifiers.ball_modifiers import BallModifiers
from src.entity.ball.modifiers.pulse_modifier import PulseModifier
from src.entity.entity import Entity
from src.faces.loaded_face_configuration import LoadedFaceConfiguration
from src.display.display import Display
from src.visuals.damage_number_effect import DamageNumberEffect
from src.visuals.face_implosion_effect import FaceImplosionEffect
from src.visuals.halo_effect import HaloEffect
from src.visuals.implosion_effect import ImplosionEffect
from src.visuals.visual_effect_manager import VisualEffectManager


class Ball(Entity):
    COLLISION_TYPE = 1
    SPEEDUP_RATE = 0.005
    SPEEDUP_CHANCE = 0.1
    VELOCITY_CAP = 2000

    CRIT_SECONDS = 1

    def __init__(
        self,
        spawn_config: BallSpawnConfig,
        space: pymunk.Space,
        visual_effect_manager: VisualEffectManager,
    ) -> None:
        self.prototype = spawn_config.prototype
        self.radius = spawn_config.radius
        self.mass = spawn_config.mass
        self.health = spawn_config.initial_health

        self.hit_timer_seconds = 0.0

        self.body: pymunk.Body = pymunk.Body(
            self.mass,
            pymunk.moment_for_circle(self.mass, 0, self.radius),
        )
        self.body.position = spawn_config.position
        self.body.velocity = spawn_config.velocity
        self.body.angular_velocity = spawn_config.angular_velocity
        self.body.user_data = self

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 1.0
        self.shape.friction = 0.1

        self.shape.collision_type = self.COLLISION_TYPE
        self.space = space
        self.space.add(self.body, self.shape)

        self.faces = LoadedFaceConfiguration(self.prototype.faces) if self.prototype.faces else None

        self.visual_effect_manager = visual_effect_manager
        self.modifiers = BallModifiers()

    @override
    def update(self, dt: float) -> None:
        if self.health <= 0:
            return

        self.modifiers.update(dt)

        if random.random() < self.SPEEDUP_CHANCE and self.body.velocity.length < self.VELOCITY_CAP:
            self.body.velocity *= 1 + self.SPEEDUP_RATE

    @override
    def draw(self, display: Display) -> None:
        if self.health <= 0:
            return

        pos = (self.body.position.x, self.body.position.y)

        alpha = self.modifiers.get_pulse_alpha()
        if self.prototype.faces is not None:
            angle_deg = -self.body.angle * 180 / math.pi
            display.draw_image(self.get_current_face(), pos, angle_deg, alpha)
        else:
            display.draw_circle(pos, self.radius, self.prototype.color, alpha)

        # Health text below the ball
        health_text = f"{int(self.health)}"
        health_font = pygame.font.SysFont('Arial', 20, bold=True)
        text_center = (pos[0], pos[1] + self.radius + 12)
        display.draw_text(health_text, text_center, health_font, (80, 80, 80))

    def deal_damage(self, damage: int, is_crit: bool) -> None:
        pass

    def receive_damage(self, damage: int, is_crit: bool) -> None:
        if damage > 0:
            self.health = max(0, self.health - damage)

            self.modifiers.add(AngryModifier(damage))
            self.modifiers.add(PulseModifier())

            self.visual_effect_manager.add(
                DamageNumberEffect(
                    self,
                    damage,
                    is_crit,
                )
            )

            if is_crit:
                self.visual_effect_manager.add(
                    HaloEffect(
                        self,
                        duration=self.CRIT_SECONDS,
                    )
                )

            if self.health == 0:
                self.space.remove(self.body, self.shape)
                if self.faces:
                    self.visual_effect_manager.add(
                        FaceImplosionEffect(
                            pos=(self.body.position.x, self.body.position.y),
                            angle_deg=-self.body.angle * 180 / math.pi,
                            face_surface=self.faces.angry_surface,
                            initial_radius=self.radius + 10,
                            duration=0.5
                        )
                    )
                else:
                    self.visual_effect_manager.add(
                        ImplosionEffect(
                            pos=(self.body.position.x, self.body.position.y),
                            color=self.prototype.color,
                            initial_radius=self.radius + 10,
                            duration=0.5
                        )
                    )


    def get_current_face(self) -> pygame.Surface:
        assert self.faces is not None
        return self.faces.angry_surface if self.modifiers.is_angry() else self.faces.happy_surface

    @property
    def name(self) -> str:
        return self.prototype.name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}) at ({self.body.position.x}, {self.body.position.y})"

    def __repr__(self) -> str:
        return self.__str__()