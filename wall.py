import pygame

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, WHITE
from globals import game_group_1, walls_group, entropy_step
import globals


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(game_group_1, walls_group)

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.rect = pygame.Rect(
            globals.entropy, globals.entropy, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y
        )
        globals.entropy += entropy_step

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, WHITE, self.rect, 1)
