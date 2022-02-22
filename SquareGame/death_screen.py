import pygame

import globals
from common import (
    FPS,
    BACKGROUND_COLOR,
    BUTTON_SIZE_Y,
    FONT_ANTIALIAS,
    STATS_COLOR,
)
from button import Button

MENU_BUTTON_WIDTH = 600


class DeathScreen:
    def __init__(self, surface):
        self.surface = surface
        self.is_running = False
        self.run()

    def run(self):
        stats_keys = [
            "Количество сыгранных игр: ",
            "Количество убитых врагов: ",
            "Количество пройденных комнат: ",
            "Количество пройденных уровней: ",
            "Максимальный уровень: ",
            "Количество взятого оружия: ",
            "Количество взятых сердечек: ",
        ]

        stats = [
            str(globals.game.games),
            str(globals.game.kills),
            str(globals.game.rooms),
            str(globals.game.levels),
            str(globals.game.max_level),
            str(globals.game.weapons),
            str(globals.game.hearts),
        ]

        # Fonts
        death_font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 44
        )
        title_font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20
        )
        stats_font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16
        )

        self.is_running = True
        clock = pygame.time.Clock()

        buttons_group = pygame.sprite.Group()
        Button(
            group=buttons_group,
            x=(self.surface.get_width() - MENU_BUTTON_WIDTH) // 2,
            y=250,
            w=600,
            h=BUTTON_SIZE_Y,
            text="Выйти в главное меню",
            callback=self.close,
        )

        self.surface.fill(BACKGROUND_COLOR)

        you_died_text = death_font.render("Вы умерли!", FONT_ANTIALIAS, STATS_COLOR)
        self.surface.blit(
            you_died_text,
            ((self.surface.get_width() - you_died_text.get_width()) // 2, 80),
        )

        stats_title_text = title_font.render(
            "Статистика игры:", FONT_ANTIALIAS, STATS_COLOR
        )
        self.surface.blit(
            stats_title_text,
            ((self.surface.get_width() - stats_title_text.get_width()) // 2, 340),
        )

        height = 380
        for i in range(len(stats_keys)):
            stat = stats_font.render(
                stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR
            )
            self.surface.blit(
                stat, ((self.surface.get_width() - stat.get_width()) // 2, height)
            )
            height += 30

        while self.is_running and globals.is_running:
            for button in buttons_group:
                button.draw(self.surface)

            events = pygame.event.get()
            events_types = {event.type for event in events}

            if pygame.QUIT in events_types:
                self.is_running = False
                globals.is_running = False

            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    self.surface.fill(BACKGROUND_COLOR)

                    for button in buttons_group:
                        button.x = (self.surface.get_width() - button.w) // 2
                        button.draw(self.surface)

                    self.surface.blit(
                        you_died_text,
                        (
                            (self.surface.get_width() - you_died_text.get_width()) // 2,
                            120,
                        ),
                    )

                    self.surface.blit(
                        stats_title_text,
                        (
                            (self.surface.get_width() - stats_title_text.get_width())
                            // 2,
                            360,
                        ),
                    )

                    height = 400
                    for i in range(len(stats_keys)):
                        stat = stats_font.render(
                            stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR
                        )
                        self.surface.blit(
                            stat,
                            (
                                (self.surface.get_width() - stat.get_width()) // 2,
                                height,
                            ),
                        )
                        height += 30

            for button in buttons_group:
                button.event_handler(events, events_types)

            pygame.display.flip()
            clock.tick(FPS)

    def close(self):
        self.is_running = False
        globals.game.closed_death_screen = True
