import pygame

import globals
import common
from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, WHITE, FONT_ANTIALIAS
from globals import gui_group_1
from images import HEART_IMAGE, BAD_HEART_IMAGE


class HUD1(pygame.sprite.Sprite):
    # can be optimized
    def __init__(self):
        super().__init__(gui_group_1)

        self.font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20
        )

    def draw(self, surface):
        self.draw_health_bar(surface)
        self.draw_weapon_bar(surface)
        self.draw_level_info(surface)

    def draw_health_bar(self, surface):
        player_health_limit = globals.game.player.health_limit
        player_health = globals.game.player.health

        for i in range(1, player_health_limit + 1):
            image = pygame.transform.scale(
                HEART_IMAGE if i <= player_health else BAD_HEART_IMAGE,
                (1.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y),
            )
            surface.blit(image, ((i * 1.2 - 1) * BLOCK_SIZE_X, 0.2 * BLOCK_SIZE_Y))

    def draw_weapon_bar(self, surface):
        weapon = globals.game.player.weapon
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

    def draw_level_info(self, surface):
        current_level = globals.game.current_level
        text = self.font.render(f"Уровень {current_level}", FONT_ANTIALIAS, WHITE)
        surface.blit(
            text,
            (
                common.window_size_x_2 - text.get_width() // 2,
                0.2 * BLOCK_SIZE_Y + text.get_height() // 2,
            ),
        )
