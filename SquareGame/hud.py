import pygame

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, WHITE, FONT_ANTIALIAS, HUD_COLOR
from globals import gui_group_1
from images import HEART_IMAGE, BAD_HEART_IMAGE


class HUD1(pygame.sprite.Sprite):
    # can be optimized
    def __init__(self, player):
        super().__init__(gui_group_1)

        self.player = player

        self.font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20
        )

    def draw(self, surface):
        self.draw_health_bar(surface)
        self.draw_weapon_bar(surface)

    def draw_health_bar(self, surface):
        player_health_limit = self.player.health_limit
        player_health = self.player.health

        # pygame.draw.rect(
        #     surface,
        #     HUD_COLOR,
        #     (0, 0, ((player_health + 1) * 1.2 - 0.8) * BLOCK_SIZE_X, 2.6 * BLOCK_SIZE_Y),
        #     0,
        # )
        
        for i in range(1, player_health_limit + 1):
            image = pygame.transform.scale(
                HEART_IMAGE if i <= player_health else BAD_HEART_IMAGE,
                (1.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y),
            )
            surface.blit(image, ((i * 1.2 - 1) * BLOCK_SIZE_X, 0.2 * BLOCK_SIZE_Y))

    def draw_weapon_bar(self, surface):
        weapon = self.player.weapon
        image = pygame.transform.scale(
            weapon.image, (1.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y)
        )
        surface.blit(image, (0.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y))

        text = self.font.render(weapon.name, FONT_ANTIALIAS, WHITE)
        surface.blit(
            text,
            (
                1.6 * BLOCK_SIZE_X,
                1.7 * BLOCK_SIZE_Y,
            ),
        )
