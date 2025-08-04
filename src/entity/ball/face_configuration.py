from pathlib import Path

import pygame


class FaceConfiguration:
    def __init__(
        self,
        happy_path: Path,
        sad_path: Path,
        diameter: int,
    ):
        self.happy_path = happy_path
        self.sad_path = sad_path
        self.diameter = diameter
        self.happy_surface = None
        self.sad_surface = None

    def load_images(self):
        self.happy_surface = self.load_circular_image(self.happy_path, self.diameter)
        self.sad_surface = self.load_circular_image(self.sad_path, self.diameter)

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