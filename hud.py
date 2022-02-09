import pygame

from common import HEALTH_LIMIT, BLOCK_SIZE_X, BLOCK_SIZE_Y
from globals import gui_group_1
from images import HEART_IMAGE, BAD_HEART_IMAGE


class HUD1(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(gui_group_1)
        
        self.player = player

    def draw(self, surface):
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        player_health = self.player.health
        for i in range(1, HEALTH_LIMIT + 1):
            sprite = pygame.sprite.Sprite()
            sprite.image = self.image = pygame.transform.scale(
                HEART_IMAGE if i <= player_health else BAD_HEART_IMAGE,
                (1.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y),
            )
            surface.blit(self.image, ((i * 1.2 - 1) * BLOCK_SIZE_X, 0.2 * BLOCK_SIZE_Y))
