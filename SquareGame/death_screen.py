import pygame
import common
from common import (
    FONT_ANTIALIAS,
    STATS_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
)
import globals
from button import Button

title_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20)
stats_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16)


class DeathScreen:
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game

        globals.running = False

        self.render_game_stats()

    def render_game_stats(self):
        x_pos = (common.window_size_x - BUTTON_SIZE_X) // 2
        buttons_group = pygame.sprite.Group()
        button = Button(
            group=buttons_group,
            x=x_pos,
            y=250,
            w=BUTTON_SIZE_X,
            h=BUTTON_SIZE_Y,
            text="Играть",
            # callback=start,
            # args=(screen,),
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

        stats = [str(self.game.games), str(self.game.deaths), str(self.game.kills),
                 str(self.game.upgrades), str(self.game.weapons),
                 str(self.game.hearts), str(self.game.rooms), str(self.game.levels)]

        height = 400

        text = title_font.render("Статистика", FONT_ANTIALIAS, STATS_COLOR)
        self.surface.blit(text, ((common.window_size_x - text.get_width()) // 2, 360))

        for i in range(len(stats_keys)):
            stat = stats_font.render(stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR)
            self.surface.blit(stat, ((self.surface.get_width() - stat.get_width()) // 2, height))
            height += 30

        running = True

        while running:
            button.draw(self.surface)

            events = pygame.event.get()
            events_types = {event.type for event in events}

            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    common.window_size_x = event.w
                    common.window_size_x_2 = event.w // 2
                    common.window_size_y = event.h
                    common.window_size_y_2 = event.h // 2
                    x_pos = (event.w - BUTTON_SIZE_X) // 2
                    button.x = x_pos

            for button in buttons_group:
                result = button.event_handler(events, events_types)
                if result:
                    running = False
                    globals.game.stop()  # Stopping here because game can be None
                    break
