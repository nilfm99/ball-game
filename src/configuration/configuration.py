from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    fps: int = 60
    sim_size: tuple[int, int] = (1280, 720)
    hud_side_padding: int = 10
    top_hud_height: int = 40
    bottom_hud_height: int = 80
    hud_color: tuple[int, int, int] = (245, 235, 220)
    ball_radius: int = 60
    title: str = "Boink"

    @property
    def min_initial_speed(self) -> float:
        return 5.0 * self.fps

    @property
    def max_initial_speed(self) -> float:
        return 10.0 * self.fps

    @property
    def sim_left(self) -> int:
        return self.hud_side_padding

    @property
    def sim_top(self) -> int:
        return self.top_hud_height

    @property
    def sim_width(self) -> int:
        return self.sim_size[0]

    @property
    def sim_height(self) -> int:
        return self.sim_size[1]

    @property
    def window_width(self) -> int:
        return self.sim_width + 2 * self.hud_side_padding

    @property
    def window_height(self) -> int:
        return self.sim_height + self.top_hud_height + self.bottom_hud_height