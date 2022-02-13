import common
from common import (
    BLOCK_SIZE_X,
    BLOCK_SIZE_Y,
    BACKGROUND_COLOR,
)
from globals import (
    game_group_1,
    game_group_2,
    game_group_3,
    gui_group_1,
    gui_group_2,
    gui_group_3,
)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)

        for obj in game_group_1:
            obj.draw(surface, self.x, self.y)
        for obj in game_group_2:
            obj.draw(surface, self.x, self.y)
        for obj in game_group_3:
            obj.draw(surface, self.x, self.y)

        for obj in gui_group_1:
            obj.draw(surface)
        for obj in gui_group_2:
            obj.draw(surface)
        for obj in gui_group_3:
            obj.draw(surface)

    def update(self, target):
        self.x = target.rect.w // 2 - target.x * BLOCK_SIZE_X + common.window_size_x_2
        self.y = target.rect.h // 2 - target.y * BLOCK_SIZE_Y + common.window_size_y_2
