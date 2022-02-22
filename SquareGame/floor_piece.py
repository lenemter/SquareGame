import pygame

import globals
from common import BLOCK_SIZE_X, BLOCK_SIZE_Y
from globals import game_group_1, entropy_step


class FloorPiece(pygame.sprite.Sprite):
    color = pygame.color.Color("#253841")

    def __init__(self, x, y, w=1, h=1):
        super().__init__(game_group_1)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(
            globals.entropy,
            globals.entropy,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )
        globals.entropy += entropy_step

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy

        pygame.draw.rect(surface, self.color, self.rect, 0)
