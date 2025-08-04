from pathlib import Path

import pygame

from src.configuration.configuration import Configuration
from src.entity.ball.ball_factory import BallFactory
from src.entity.ball.face_configuration import FaceConfiguration
from src.game.game import Game


def main():
    configuration = Configuration()

    nil_faces = FaceConfiguration(
        Path("resources/nil_happy.png"),
        Path("resources/nil_angry.png"),
        2 * configuration.ball_radius,
    )
    jin_faces = FaceConfiguration(
        Path("resources/jin_happy.png"),
        Path("resources/jin_angry.png"),
        2 * configuration.ball_radius,
    )

    ball_specs = [
        ("nil", pygame.Color("lightblue"), nil_faces),
        ("jin", pygame.Color("lightgreen"), jin_faces),
        ("bubu", pygame.Color("lightcoral"), None),
        ("kachupuchu", pygame.Color("lightpink"), None),
    ]

    factory = BallFactory(
        configuration,
        ball_specs=ball_specs,
    )

    game = Game(configuration, factory.make_balls)
    game.run()


if __name__ == "__main__":
    main()