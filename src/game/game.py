from collections.abc import Callable

import pygame
import pymunk

from src.collisions.collision_handler import CollisionHandler
from src.configuration.configuration import Configuration
from src.entity.ball.ball import Ball
from src.entity.wall import Wall
from src.game.display import Display


class Game:
    @staticmethod
    def _create_walls(
            resolution: tuple[int, int],
            thickness: int = 10,
    ) -> list[Wall]:
        width, height = resolution
        return [
            Wall((0, 0), (width, 0), thickness),  # Bottom
            Wall((0, height), (width, height), thickness),  # Top
            Wall((0, 0), (0, height), thickness),  # Left
            Wall((width, 0), (width, height), thickness)  # Right
        ]

    @staticmethod
    def _create_space() -> pymunk.Space:
        space = pymunk.Space()
        space.damping = 1.0
        space.on_collision(
            Ball.COLLISION_TYPE,
            Ball.COLLISION_TYPE,
            pre_solve=CollisionHandler.handle_ball_collision,
        )
        return space

    def __init__(
            self,
            configuration: Configuration,
            balls_factory: Callable[[], list[Ball]],
    ):
        self.configuration = configuration
        self.space = self._create_space()
        self.walls = self._create_walls(self.configuration.sim_size)
        self.balls_factory = balls_factory
        
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

    def main_loop(
            self,
            balls: list[Ball],
    ) -> Ball | None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise InterruptedError()

            dt = min(
                self.clock.tick(self.configuration.fps) / 1000.0,
                1 / self.configuration.fps
            )
            self.display.clear()

            self.space.step(dt)

            alive_balls = [ball for ball in balls if ball.health > 0]
            entities = self.walls + balls
            if len(alive_balls) == 0:
                return None
            elif len(alive_balls) == 1:
                return alive_balls[0]

            for entity in entities:
                entity.update(dt)
                entity.draw(self.display)

            self.display.draw_hud(self._get_ball_info(balls))
            self.display.blit_simulation()
            self.display.flip()

    def pause_until_fight_again(
            self,
            balls: list[Ball],
            winner_name: str
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

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        paused = False

            self.display.clear()
            self.display.blit_simulation()
            self.display.draw_hud(self._get_ball_info(balls))
            winner_text = f"{winner_name} won!!"
            font = pygame.font.SysFont('Arial', 48, bold=True)
            text_surf = font.render(winner_text, True, (255, 215, 0))
            text_rect = text_surf.get_rect(center=(self.configuration.window_width // 2, self.configuration.window_height // 2))
            self.display.screen.blit(text_surf, text_rect)
            button_font = pygame.font.SysFont('Arial', 36, bold=True)
            self.display.draw_fight_again_button(button_rect, button_font)
            self.display.flip()

    def run(self) -> None:
        while True:
            self.space = self._create_space()
            balls = self.balls_factory()
            for ball in balls:
                ball.load_faces()

            self.walls = self._create_walls(self.configuration.sim_size)
            for wall in self.walls:
                wall.add_to_space(self.space)

            for ball in balls:
                ball.add_to_space(self.space)

            winner = self.main_loop(balls)
            winner_name = winner.name if winner is not None else "No one"
            self.pause_until_fight_again(balls, winner_name)
