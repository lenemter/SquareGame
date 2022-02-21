import pygame

import common
import globals
from common import (
    FONT_ANTIALIAS,
    STATS_COLOR,
    BUTTON_SIZE_Y,
    FPS,
    BACKGROUND_COLOR,
)
from button import Button

title_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20)
stats_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16)


class DeathScreen:
    def __init__(self, surface):
        self.surface = surface
        self.is_running = False
        self.run()

    def run(self):
        self.surface.fill(BACKGROUND_COLOR)
        x_pos = (self.surface.get_width() - 600) // 2
        buttons_group = pygame.sprite.Group()
        button = Button(
            group=buttons_group,
            x=x_pos,
            y=250,
            w=600,
            h=BUTTON_SIZE_Y,
            text="Выйти в главное меню",
            callback=self.close,
        )

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

        stats = [
            str(globals.game.games),
            str(globals.game.deaths),
            str(globals.game.kills),
            str(globals.game.upgrades),
            str(globals.game.weapons),
            str(globals.game.hearts),
            str(globals.game.rooms),
            str(globals.game.levels),
        ]

        self.is_running = True
        clock = pygame.time.Clock()

        while self.is_running and globals.is_running:
            self.surface.fill(BACKGROUND_COLOR)
            button.draw(self.surface)

            height = 400

            text = title_font.render("Статистика игры", FONT_ANTIALIAS, STATS_COLOR)
            self.surface.blit(
                text, ((self.surface.get_width() - text.get_width()) // 2, 360)
            )

            for i in range(len(stats_keys)):
                stat = stats_font.render(
                    stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR
                )
                self.surface.blit(
                    stat, ((self.surface.get_width() - stat.get_width()) // 2, height)
                )
                height += 30

            pygame.display.flip()
            clock.tick(FPS)

            events = pygame.event.get()
            events_types = {event.type for event in events}

            if pygame.QUIT in events_types:
                self.is_running = False
                globals.is_running = False

            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    common.window_size_x = event.w
                    common.window_size_x_2 = event.w // 2
                    common.window_size_y = event.h
                    common.window_size_y_2 = event.h // 2
                    x_pos = (self.surface.get_width() - 600) // 2
                    button.x = x_pos

            for button in buttons_group:
                button.event_handler(events, events_types)

    def close(self):
        self.is_running = False
