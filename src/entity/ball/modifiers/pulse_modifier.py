import math
from src.entity.ball.modifiers.ball_modifier import BallModifier

class PulseModifier(BallModifier):
    DURATION = 0.7
    NUM_PULSES = 3

    def __init__(
            self,
            duration: float = DURATION,
            min_alpha: int = 120,
            max_alpha: int = 255,
            min_scale: float = 0.92,
            max_scale: float = 1.08,
    ):
        super().__init__(duration)
        self.initial_duration = duration
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.min_scale = min_scale
        self.max_scale = max_scale

    def get_progress(self) -> float:
        return 1.0 - (self.duration / self.initial_duration)

    def get_alpha(self) -> int:
        # Ease in-out: alpha dips in the middle, returns to max at the end
        progress = self.get_progress()
        # Use a bell-curve shape: dips at the middle, max at start/end
        # alpha = min + (max - min) * |cos(pi * progress)|
        pulse = abs(math.cos(math.pi * progress * self.NUM_PULSES))
        return int(self.min_alpha + (self.max_alpha - self.min_alpha) * pulse)

    def get_scale(self) -> float:
        # Pop scale: starts big, shrinks, then returns to normal
        progress = self.get_progress()
        # Use a similar bell-curve shape, but inverted for scale
        # scale = min_scale + (max_scale - min_scale) * sin(pi * progress)
        pulse = math.sin(math.pi * progress)
        return self.min_scale + (self.max_scale - self.min_scale) * pulse