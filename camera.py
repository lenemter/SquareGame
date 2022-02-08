from utils import (
    BLOCK_SIZE_X,
    BLOCK_SIZE_Y,
    WINDOW_SIZE_X_2,
    WINDOW_SIZE_Y_2,
    BACKGROUND_COLOR,
)
from globals import all_group


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        # logging.debug(f"CAM: {self.x=} {self.y=}")
        for obj in all_group:
            obj.draw(surface, self.x, self.y)

    def update(self, target):
        self.x = target.rect.w // 2 - target.x * BLOCK_SIZE_X + WINDOW_SIZE_X_2
        self.y = target.rect.h // 2 - target.y * BLOCK_SIZE_Y + WINDOW_SIZE_Y_2
