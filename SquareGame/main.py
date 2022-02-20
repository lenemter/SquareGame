# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import logging

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

pygame.init()
screen = pygame.display.set_mode(
    (common.window_size_x, common.window_size_y), pygame.RESIZABLE
)

import globals
from button import Button
from stats import render_stats, update_stats
from level_generator import generate_level


class Game:
    def __init__(self):
        self.current_level = 0
        self.surface = None
        self.player = None
        self.level = None

        # Stats
        self.deaths = 0
        self.games = 1
        self.kills = 0
        self.upgrades = 0
        self.weapons = 0
        self.hearts = 0
        self.rooms = 0
        self.levels = 0

    def stop(self):
        update_stats(
            {
                "games": self.games,
                "deaths": self.deaths,
                "kills": self.kills,
                "upgrades": self.upgrades,
                "weapons": self.weapons,
                "hearts": self.hearts,
                "rooms": self.rooms,
                "levels": self.levels,
            }
        )

    def launch_level(self, surface=None):
        self.current_level += 1
        if surface is None:
            surface = self.surface
        self.surface = surface

        self.level = generate_level()
        clock = pygame.time.Clock()
        globals.running = True

        while globals.running:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    common.window_size_x_2 = event.w // 2
                    common.window_size_y_2 = event.h // 2
                elif event.type == pygame.QUIT:
                    globals.running = False
                    break

            self.level.event_handler(clock.tick(FPS))

            self.level.draw(surface)
            pygame.display.flip()


def start(surface):
    globals.game = Game()
    globals.game.launch_level(surface)
    pygame.quit()


def main():
    logging.basicConfig(level=logging.DEBUG)

    pygame.display.set_caption(WINDOW_NAME)

    x_pos = (common.window_size_x - BUTTON_SIZE_X) // 2
    buttons_group = pygame.sprite.Group()
    play_button = Button(
        group=buttons_group,
        x=x_pos,
        y=250,
        w=BUTTON_SIZE_X,
        h=BUTTON_SIZE_Y,
        text="Играть",
        callback=start,
        args=(screen,),
    )

    title_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 44)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        text = title_font.render(WINDOW_NAME, FONT_ANTIALIAS, STATS_COLOR)
        screen.blit(text, ((common.window_size_x - text.get_width()) // 2, 120))

        play_button.draw(screen)
        render_stats(screen)
        pygame.display.flip()
        clock.tick(FPS)

        events = pygame.event.get()
        events_types = {event.type for event in events}

        if pygame.QUIT in events_types:
            running = False

        for event in events:
            if event.type == pygame.VIDEORESIZE:
                common.window_size_x = event.w
                common.window_size_x_2 = event.w // 2
                common.window_size_y = event.h
                common.window_size_y_2 = event.h // 2
                x_pos = (event.w - BUTTON_SIZE_X) // 2
                play_button.x = x_pos

        for button in buttons_group:
            result = button.event_handler(events, events_types)
            if result:
                running = False
                globals.game.stop()  # Stopping here because game can be None
                break

    pygame.quit()


if __name__ == "__main__":
    main()
