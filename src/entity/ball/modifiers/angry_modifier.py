from src.entity.ball.modifiers.ball_modifier import BallModifier


class AngryModifier(BallModifier):
    SECONDS_PER_DAMAGE = 0.1

    def __init__(self, damage: int) -> None:
        super().__init__(damage * self.SECONDS_PER_DAMAGE)
