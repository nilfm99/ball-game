from dataclasses import dataclass

import pygame

from src.faces.face_configuration import FaceConfiguration


@dataclass(frozen=True)
class BallPrototype:
    name: str
    color: pygame.Color | None = None
    faces: FaceConfiguration | None = None

    def __post_init__(self) -> None:
        if (self.color is None and self.faces is None) or (self.color is not None and self.faces is not None):
            raise ValueError("Exactly one of 'color' or 'faces' must be provided.")
