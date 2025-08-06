from abc import ABC, abstractmethod

from src.display.display import Display


class VisualEffect(ABC):
    def __init__(self, timer_seconds: float) -> None:
        self.timer_seconds = timer_seconds

    @abstractmethod
    def draw(self, display: Display) -> None:
        pass

    def update(self, dt: float) -> None:
        self.timer_seconds = max(0.0, self.timer_seconds - dt)

    def is_alive(self) -> bool:
        return self.timer_seconds > 0
