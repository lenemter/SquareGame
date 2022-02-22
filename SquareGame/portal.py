import pygame

import globals
from globals import game_group_2, portal_group, entropy_step
from images import PORTAL_IMAGE
from common import BLOCK_SIZE_X, BLOCK_SIZE_Y


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(game_group_2, portal_group)
        global entropy_step

        self.x = x
        self.y = y
        self.w = 2
        self.h = 4

        self.image = pygame.transform.scale(
            PORTAL_IMAGE, (self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y)
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
