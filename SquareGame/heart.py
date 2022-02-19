import pygame

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y
from images import HEART_IMAGE
from globals import game_group_1, hearts_group, entropy_step
import globals


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(game_group_1, hearts_group)
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.heal_amount = 1

        self.image = pygame.transform.scale(
            HEART_IMAGE,
            (self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y),
        )
        self.rect = self.image.get_rect()
        self.rect.x = globals.entropy
        self.rect.y = globals.entropy
        globals.entropy += entropy_step

    def draw(self, surface, dx, dy):
        x = self.x * BLOCK_SIZE_X + dx
        y = self.y * BLOCK_SIZE_Y + dy

        surface.blit(self.image, (x, y))
        self.rect.x = x
        self.rect.y = y