import pygame
import common
from common import (
    WINDOW_NAME,
    FPS,
    FONT_ANTIALIAS,
    BACKGROUND_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
    STATS_COLOR,
)

title_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20)
stats_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16)


class DeathScreen:
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game

        self.render_game_stats()

    def render_game_stats(self):
        text = title_font.render("Статистика", FONT_ANTIALIAS, STATS_COLOR)
        self.surface.blit(text, ((common.window_size_x - text.get_width()) // 2, 360))

        stats_keys = [
            "Количество сыгранных игр: ",
            "Количество смертей: ",
            "Количество убитых врагов: ",
            "Количество взятых прокачек: ",
            "Количество взятого оружия: ",
            "Количество взятых сердечек: ",
            "Количество пройденных комнат: ",
            "Количество пройденных уровней: ",
        ]

        stats = [str(self.game.games), str(self.game.deaths), str(self.game.kills),
                 str(self.game.upgrades), str(self.game.weapons),
                 str(self.game.hearts), str(self.game.rooms), str(self.game.levels)]

        height = 400

        for i in range(len(stats_keys)):
            stat = stats_font.render(stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR)
            self.surface.blit(stat, ((self.surface.get_width() - stat.get_width()) // 2, height))
            height += 30
