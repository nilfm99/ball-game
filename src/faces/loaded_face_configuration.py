from pathlib import Path

import pygame

from src.faces.face_configuration import FaceConfiguration


class LoadedFaceConfiguration:
    def __init__(
        self,
        face_configuration: FaceConfiguration,
    ):
        self.happy_surface = self.load_circular_image(face_configuration.happy_path, face_configuration.diameter)
        self.sad_surface = self.load_circular_image(face_configuration.sad_path, face_configuration.diameter)

    @staticmethod
    def load_circular_image(path: Path, diameter: int) -> pygame.Surface:
        # Load and scale the image
        img = pygame.image.load(str(path)).convert_alpha()
        img = pygame.transform.smoothscale(img, (diameter, diameter))

        # Create a circular mask
        mask = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (diameter // 2, diameter // 2), diameter // 2)

        # Apply mask to image
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return img