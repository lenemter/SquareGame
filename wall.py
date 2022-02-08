import pygame

from utils import BLOCK_SIZE_X, BLOCK_SIZE_Y, WHITE
from globals import all_group, walls_group, entropy, entropy_step


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, walls_group)
        global entropy

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.rect = pygame.Rect(
            entropy, entropy, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y
        )
        entropy += entropy_step

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_X + dy
        pygame.draw.rect(surface, WHITE, self.rect, 1)
