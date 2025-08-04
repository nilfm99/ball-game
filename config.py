SIM_SIZE = (1280, 720)
HUD_SIDE_PADDING = 10
TOP_HUD_HEIGHT = 40
BOTTOM_HUD_HEIGHT = 80
FPS = 60


def get_sim_area():
    sim_left = HUD_SIDE_PADDING
    sim_top = TOP_HUD_HEIGHT
    sim_width, sim_height = SIM_SIZE
    return sim_left, sim_top, sim_width, sim_height
