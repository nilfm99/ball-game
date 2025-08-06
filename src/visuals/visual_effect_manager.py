from src.game.display import Display
from src.visuals.visual_effect import VisualEffect


class VisualEffectManager:
    def __init__(self):
        self.effects: list[VisualEffect] = []

    def add(self, effect: VisualEffect):
        self.effects.append(effect)

    def update(self, dt: float):
        for effect in self.effects:
            effect.update(dt)
        self.effects = [e for e in self.effects if e.is_alive()]

    def draw(self, display: Display):
        for effect in self.effects:
            effect.draw(display)
