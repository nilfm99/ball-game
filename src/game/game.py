from collections.abc import Callable

import pygame
import pymunk

from src.collisions.collision_handler import CollisionHandler
from src.configuration.configuration import Configuration
from src.entity.ball.ball import Ball
from src.entity.ball.ball_spawn_config import BallSpawnConfig
from src.entity.wall import Wall
from src.game.display import Display
from src.visuals.visual_effect_manager import VisualEffectManager


class Game:
    @staticmethod
    def _create_walls(
            space: pymunk.Space,
            resolution: tuple[int, int],
            thickness: int = 10,
    ) -> list[Wall]:
        width, height = resolution
        return [
            Wall(space, (0, 0), (width, 0), thickness),  # Bottom
            Wall(space, (0, height), (width, height), thickness),  # Top
            Wall(space, (0, 0), (0, height), thickness),  # Left
            Wall(space, (width, 0), (width, height), thickness)  # Right
        ]

    @staticmethod
    def _create_space() -> pymunk.Space:
        space = pymunk.Space()
        space.damping = 1.0
        space.on_collision(
            Ball.COLLISION_TYPE,
            Ball.COLLISION_TYPE,
            begin=CollisionHandler.handle_ball_collision,
        )
        return space

    def __init__(
            self,
            configuration: Configuration,
            balls_factory: Callable[[], list[BallSpawnConfig]],
    ):
        self.configuration = configuration
        self.space = self._create_space()
        self.balls_factory = balls_factory
        self.visual_effect_manager = VisualEffectManager()
        
        pygame.init()
        pygame.font.init()

        self.display = Display(self.configuration)
        self.clock = pygame.time.Clock()

    @staticmethod
    def _get_ball_info(balls: list[Ball]) -> list[dict[str, str | int]]:
        return [
            {
                "name": ball.name,
                "health": ball.health,
            }
            for ball in balls
        ]

    def step_simulation(self, walls: list[Wall], balls: list[Ball], dt: float) -> None:
        self.space.step(dt)
        entities = walls + balls
        for entity in entities:
            entity.update(dt)
            entity.draw(self.display)
        self.visual_effect_manager.update(dt)
        self.visual_effect_manager.draw(self.display)
        self.display.draw_hud(self._get_ball_info(balls))
        self.display.blit_simulation()

    def run_main_loop(
            self,
            walls: list[Wall],
            balls: list[Ball],
    ) -> None:
        button_width, button_height = 220, 60
        button_rect = pygame.Rect(
            (
                self.configuration.window_width // 2 - button_width // 2,
                self.configuration.window_height // 2 + 60,
                button_width,
                button_height,
            )
        )

        while True:
            alive_balls = [ball for ball in balls if ball.health > 0]
            finished = len(alive_balls) < 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise InterruptedError()
                if finished:
                    if (
                            (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos)) or
                            (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE))
                    ):
                        return

            dt = min(
                self.clock.tick(self.configuration.fps) / 1000.0,
                1 / self.configuration.fps
            )
            self.display.clear()

            self.step_simulation(walls, balls, dt)

            if finished:
                overlay = pygame.Surface(
                    (self.configuration.window_width, self.configuration.window_height),
                    pygame.SRCALPHA,
                )
                overlay.fill((0, 0, 0, 96))  # 96/255 alpha for subtle dimming
                self.display.screen.blit(overlay, (0, 0))

                winner_name = alive_balls[0].name if len(alive_balls) == 1 else "No one"
                winner_text = f"{winner_name} won!!"
                font = pygame.font.SysFont('Arial', 48, bold=True)
                text_surf = font.render(winner_text, True, (255, 215, 0))
                text_rect = text_surf.get_rect(
                    center=(self.configuration.window_width // 2, self.configuration.window_height // 2)
                )
                self.display.screen.blit(text_surf, text_rect)

                button_font = pygame.font.SysFont('Arial', 36, bold=True)
                self.display.draw_fight_again_button(button_rect, button_font)

            self.display.flip()

    def run(self) -> None:
        try:
            while True:
                self.space = self._create_space()

                walls = self._create_walls(self.space, self.configuration.sim_size)

                ball_spawn_configs = self.balls_factory()
                balls = [
                    Ball(
                        spawn_config,
                        self.space,
                        self.visual_effect_manager,
                    )
                    for spawn_config in ball_spawn_configs
                ]

                self.run_main_loop(walls, balls)
        except InterruptedError:
            print("Exiting...")
