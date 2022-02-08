import pygame

from utils import BLOCK_SIZE_X,  BLOCK_SIZE_Y
from images import HEART_IMAGE
from globals import all_group, hearts_group

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, hearts_group)
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

    def draw(self, surface, dx, dy):
        surface.blit(
            self.image, (self.x * BLOCK_SIZE_X + dx, self.y * BLOCK_SIZE_Y + dy)
        )
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy