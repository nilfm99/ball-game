from typing import override

import pygame

from src.display.display import Display
from src.visuals.visual_effect import VisualEffect


class FaceImplosionEffect(VisualEffect):
    def __init__(
            self,
            pos: tuple[float, float],
            initial_radius: float,
            angle_deg: float,
            face_surface: pygame.Surface,
            duration: float = 1
    ):
        super().__init__(duration)
        self.pos = pos
        self.initial_radius = initial_radius
        self.angle_deg = angle_deg
        self.face_surface = face_surface
        self.initial_duration = duration

    @override
    def draw(self, display: Display) -> None:
        progress = 1.0 - (self.timer_seconds / self.initial_duration)
        scale = max(0.01, 1.0 - progress)  # Avoid scale=0 for blit
        alpha = int(255 * (1 - progress))

        # Rotate the face image
        rotated_face = pygame.transform.rotate(self.face_surface, self.angle_deg)

        # Scale the face image down
        orig_size = rotated_face.get_size()
        new_size = (max(1, int(orig_size[0] * scale)), max(1, int(orig_size[1] * scale)))
        scaled_face = pygame.transform.smoothscale(rotated_face, new_size).convert_alpha()
        scaled_face.set_alpha(alpha)

        # Center the scaled image at the position
        x, y = self.pos
        rect = scaled_face.get_rect(center=(x, y))
        display.sim_surface.blit(scaled_face, rect)
