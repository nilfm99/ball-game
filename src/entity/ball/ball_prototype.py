from dataclasses import dataclass

import pygame

from src.faces.face_configuration import FaceConfiguration


@dataclass(frozen=True)
class BallPrototype:
    name: str
    color: pygame.Color
    faces: FaceConfiguration | None = None
