from pathlib import Path

from src.configuration.configuration import Configuration
from src.entity.ball.ball_spawn_config_factory import BallSpawnConfigFactory
from src.entity.ball.ball_prototype import BallPrototype
from src.faces.face_configuration import FaceConfiguration
from src.game.game import Game


def _get_faces(name: str, configuration: Configuration) -> FaceConfiguration:
    return FaceConfiguration(
        Path(f"resources/{name}_happy.png"),
        Path(f"resources/{name}_angry.png"),
        2 * configuration.ball_radius,
    )


def main():
    configuration = Configuration()

    factory = BallSpawnConfigFactory(
        configuration,
        ball_prototypes=[
            BallPrototype(name=name, faces=_get_faces(name, configuration))
            for name in ["nil", "jin", "papa", "mama", "martina"]
        ],
    )

    game = Game(configuration, factory.make_balls)
    game.run()


if __name__ == "__main__":
    main()