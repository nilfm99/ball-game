import pygame

from src.configuration.configuration import Configuration


class Display:
    def __init__(
        self,
        configuration: Configuration,
    ):
        self.configuration = configuration

        self.screen = pygame.display.set_mode(
            (self.configuration.window_width, self.configuration.window_height),
            pygame.DOUBLEBUF,
            vsync=1,
        )
        self.sim_surface = pygame.Surface((self.configuration.sim_width, self.configuration.sim_height))
        self.font = pygame.font.SysFont('Arial', 20)

    def draw_circle(
            self,
            center: tuple[float, float],
            radius: float,
            color: pygame.Color,
            alpha: int = 255,
            width: int = 0,
    ) -> None:
        """Draw a circle with optional alpha transparency."""
        diameter = int(radius * 2)
        temp_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        # Draw the circle at the center of the temporary surface
        circle_color = (*color[:3], alpha)
        pygame.draw.circle(temp_surface, circle_color, (radius, radius), int(radius), width)

        # Calculate the top-left position to blit the temp surface
        blit_pos = (center[0] - radius, center[1] - radius)
        self.sim_surface.blit(temp_surface, blit_pos)

    def draw_line(
            self,
            start: tuple[float, float],
            end: tuple[float, float],
            color: tuple[int, int, int],
            width: int = 1,
    ) -> None:
        pygame.draw.line(self.sim_surface, color, start, end, width)

    def draw_image(
            self,
            image: pygame.Surface,
            center: tuple[float, float],
            angle_deg: float = 0
    ) -> None:
        if angle_deg != 0:
            image = pygame.transform.rotate(image, angle_deg)
        rect = image.get_rect(center=center)
        self.sim_surface.blit(image, rect.topleft)

    def draw_halo(
            self,
            center: tuple[float, float],
            halo_radius: int,
            color: pygame.Color,
    ) -> None:
        halo_surf = pygame.Surface((halo_radius * 2, halo_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            halo_surf,
            color,
            (halo_radius, halo_radius),
            halo_radius
        )
        self.sim_surface.blit(halo_surf, (center[0] - halo_radius, center[1] - halo_radius))

    def draw_text(
            self,
            text: str,
            center: tuple[float, float],
            font: pygame.font.Font,
            color: tuple[int, int, int],
            alpha: int = 255,
    ) -> None:
        text_surf = font.render(text, True, color).convert_alpha()
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=center)
        self.sim_surface.blit(text_surf, text_rect)

    def clear(self) -> None:
        self.screen.fill(self.configuration.hud_color)
        # Top HUD
        pygame.draw.rect(
            self.screen,
            self.configuration.hud_color,
            (
                    0,
                    0,
                    self.configuration.window_width,
                    self.configuration.top_hud_height,
            ),
        )
        # Bottom HUD
        pygame.draw.rect(
            self.screen,
            self.configuration.hud_color,
            (
                0,
                self.configuration.sim_height + self.configuration.top_hud_height,
                self.configuration.window_width,
                self.configuration.bottom_hud_height,
            )
        )
        # Simulation area
        self.sim_surface.fill("white")

    def blit_simulation(self) -> None:
        self.screen.blit(self.sim_surface, (self.configuration.hud_side_padding, self.configuration.top_hud_height))

    def draw_top_hud(self) -> None:
        text_surface = self.font.render(self.configuration.title, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.configuration.window_width // 2, self.configuration.top_hud_height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_bottom_hud(self, ball_info: list[dict[str, str | int]]) -> None:
        """
        Draws a HUD at the bottom with name and health for each item.

        Each item should be a dict with the following keys: name and health
        """
        font = self.font
        line_spacing = font.get_height() + 5
        lines_per_column = max(1, self.configuration.bottom_hud_height // line_spacing)
        num_items = len(ball_info)
        num_columns = (num_items + lines_per_column - 1) // lines_per_column
        col_width = self.configuration.window_width // num_columns

        for idx, item in enumerate(ball_info):
            col = idx // lines_per_column
            row = idx % lines_per_column
            y = self.configuration.top_hud_height + self.configuration.sim_height + 10 + row * line_spacing
            x = 10 + col * col_width

            name = str(item["name"])
            health = int(item["health"])

            text = f"{name}: {health:.0f}"
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (x, y))

    def draw_hud(self, ball_info: list[dict[str, str | int]]) -> None:
        self.draw_top_hud()
        self.draw_bottom_hud(ball_info)

    def draw_fight_again_button(
            self,
            button_rect: pygame.Rect,
            font: pygame.Font
    ) -> None:
        pygame.draw.rect(self.screen, (220, 180, 60), button_rect, border_radius=12)
        pygame.draw.rect(self.screen, (120, 80, 0), button_rect, width=3, border_radius=12)
        text_surf = font.render("Fight Again", True, (50, 30, 0))
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)

    @staticmethod
    def flip() -> None:
        pygame.display.flip()