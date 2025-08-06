from abc import ABC, abstractmethod

from src.game.display import Display


class Entity(ABC):
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the entity's state. dt is the time step in seconds."""
        pass

    @abstractmethod
    def draw(self, display: Display) -> None:
        """Draw the entity on the given Pygame surface."""
        pass
