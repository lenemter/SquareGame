import random
import pygame

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, BACKGROUND_COLOR
from globals import game_group_2, walls_group, entropy_step
import globals


class Wall(pygame.sprite.Sprite):
    color = pygame.color.Color("#FFFFFF")

    def __init__(self, x, y):
        if (x, y) in globals.created_walls_cords:
            del self
            return None
        else:
            globals.created_walls_cords.add((x, y))

        super().__init__(game_group_2, walls_group)

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.rect = pygame.Rect(
            globals.entropy,
            globals.entropy,
            BLOCK_SIZE_X,
            BLOCK_SIZE_Y,
        )
        globals.entropy += entropy_step

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy

        pygame.draw.rect(surface, BACKGROUND_COLOR, self.rect, 0)
        pygame.draw.rect(surface, self.color, self.rect, 4)
