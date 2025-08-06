from src.entity.ball.modifiers.angry_modifier import AngryModifier
from src.entity.ball.modifiers.ball_modifier import BallModifier
from src.entity.ball.modifiers.pulse_modifier import PulseModifier


class BallModifiers:
    def __init__(self) -> None:
        self.modifiers: list[BallModifier] = []

    def update(self, dt: float) -> None:
        for modifier in self.modifiers:
            modifier.update(dt)
        self.modifiers = [modifier for modifier in self.modifiers if modifier.is_active()]

    def add(self, modifier: BallModifier) -> None:
        self.modifiers.append(modifier)

    def is_angry(self) -> bool:
        return any(isinstance(modifier, AngryModifier) for modifier in self.modifiers)

    def get_pulse_alpha(self) -> int:
        for modifier in self.modifiers:
            if isinstance(modifier, PulseModifier):
                return modifier.get_alpha()
        return 255  # Default alpha (fully opaque)