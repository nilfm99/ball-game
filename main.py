from pathlib import Path

import pygame

from src.configuration.configuration import Configuration
from src.entity.ball.ball_spawn_config_factory import BallSpawnConfigFactory
from src.entity.ball.ball_prototype import BallPrototype
from src.faces.face_configuration import FaceConfiguration
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

    ball_prototypes = [
        BallPrototype(name="nil", color=pygame.Color("lightblue"), faces=nil_faces),
        BallPrototype(name="jin", color=pygame.Color("lightgreen"), faces=jin_faces),
        BallPrototype(name="hehehe", color=pygame.Color("lightcoral")),
        BallPrototype(name="anununu", color=pygame.Color("lightpink")),
    ]

    factory = BallSpawnConfigFactory(
        configuration,
        ball_prototypes=ball_prototypes,
    )

    game = Game(configuration, factory.make_balls)
    game.run()


if __name__ == "__main__":
    main()