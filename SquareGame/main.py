# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import logging

from common import (
    BASE_WINDOW_SIZE,
    FPS,
    FONT_ANTIALIAS,
    BACKGROUND_COLOR,
    STATS_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
)

pygame.init()
screen = pygame.display.set_mode(BASE_WINDOW_SIZE, pygame.RESIZABLE)

from images import ICON, ICON32
import globals
from button import Button
from stats import render_stats, update_stats
from level_generator import generate_level
from death_screen import DeathScreen


class Game:
    def __init__(self, surface):
        self.current_level = 0
        self.surface = surface
        self.is_running = False
        self.closed_death_screen = False
        self.player = None
        self.level = None

        # Stats
        self.games = 1
        self.kills = 0
        self.rooms = 0
        self.levels = 0
        self.max_level = 0
        self.weapons = 0
        self.hearts = 0

    def end(self):
        update_stats(
            {
                "games": self.games,
                "kills": self.kills,
                "rooms": self.rooms,
                "levels": self.levels,
                "max_level": self.max_level,
                "weapons": self.weapons,
                "hearts": self.hearts,
            }
        )

    def launch_level(self):
        self.current_level += 1
        if self.current_level > self.max_level:
            self.max_level = self.current_level

        self.level = generate_level()
        clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running and globals.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    globals.is_running = False
                    break

            self.level.event_handler(clock.tick(FPS))

            self.level.draw(self.surface)
            pygame.display.flip()

    def show_death_screen(self):
        globals.created_walls_cords.clear()

        for obj in globals.game_group_1:
            obj.kill()

        for obj in globals.game_group_2:
            obj.kill()

        for obj in globals.game_group_3:
            obj.kill()

        for obj in globals.game_group_4:
            obj.kill()

        for obj in globals.gui_group_1:
            obj.kill()

        self.player.kill()

        self.is_running = False
        if not self.closed_death_screen:
            DeathScreen(self.surface)


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.is_running = False

        self.title_font = pygame.font.Font(
            "fonts/Press_Start_2P/PressStart2P-Regular.ttf", 44
        )

        self.run()

    def stop(self):
        self.is_running = False
        globals.is_running = False

    def run(self):
        buttons_group = pygame.sprite.Group()
        Button(
            group=buttons_group,
            x=(self.surface.get_width() - BUTTON_SIZE_X) // 2,
            y=200,
            w=BUTTON_SIZE_X,
            h=BUTTON_SIZE_Y,
            text="Играть",
            callback=self.start_game,
        )
        Button(
            group=buttons_group,
            x=(self.surface.get_width() - BUTTON_SIZE_X) // 2,
            y=300,
            w=BUTTON_SIZE_X,
            h=BUTTON_SIZE_Y,
            text="Выйти",
            callback=self.stop,
        )

        clock = pygame.time.Clock()
        self.is_running = True

        self.surface.fill(BACKGROUND_COLOR)
        text = self.title_font.render("SquareGame", FONT_ANTIALIAS, STATS_COLOR)
        self.surface.blit(
            text, ((self.surface.get_width() - text.get_width()) // 2, 80)
        )

        render_stats(self.surface)

        while self.is_running and globals.is_running:
            for button in buttons_group:
                button.x = (self.surface.get_width() - button.w) // 2
                button.draw(self.surface)

            events = pygame.event.get()
            events_types = {event.type for event in events}

            if pygame.QUIT in events_types:
                self.is_running = False
                globals.is_running = False
                break

            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    self.surface.fill(BACKGROUND_COLOR)

                    for button in buttons_group:
                        button.x = (self.surface.get_width() - button.w) // 2
                        button.draw(self.surface)

                    self.surface.blit(
                        text, ((self.surface.get_width() - text.get_width()) // 2, 80)
                    )
                    render_stats(self.surface)

            for button in buttons_group:
                button.event_handler(events, events_types)

            pygame.display.flip()
            clock.tick(FPS)

    def start_game(self):
        globals.game = Game(self.surface)
        globals.game.launch_level()
        self.end_game()

    def end_game(self):
        globals.game.end()
        globals.game = None

        # Redraw text
        self.surface.fill(BACKGROUND_COLOR)
        text = self.title_font.render("SquareGame", FONT_ANTIALIAS, STATS_COLOR)
        self.surface.blit(
            text, ((self.surface.get_width() - text.get_width()) // 2, 120)
        )

        render_stats(self.surface)


def main():
    logging.basicConfig(level=logging.DEBUG)
    pygame.display.set_caption("SquareGame")

    # Checking the OS because Windows only allows 32x32 icons
    if os.name == "nt":
        pygame.display.set_icon(ICON32)
    else:
        pygame.display.set_icon(ICON)

    Menu(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
