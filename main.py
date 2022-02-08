# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import logging

from utils import (
    TEST_LEVEL,
    WINDOW_SIZE_X,
    WINDOW_SIZE_Y,
    WINDOW_SIZE_X_2,
    WINDOW_SIZE_Y_2,
    WINDOW_NAME,
    FPS,
)

logging.basicConfig(level=logging.DEBUG)
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE)
pygame.display.set_caption(WINDOW_NAME)

from images import *
from globals import *

from camera import Camera
from player import Player
from wall import Wall
from heart import Heart


class TestLevel:
    def __init__(self):
        self.player = None
        self.camera = Camera()
        self.load_map()

    def load_map(self):
        with open(TEST_LEVEL, mode="r", encoding="UTF-8") as file:
            level = file.readlines()

        for y, row in enumerate(level):
            for x, cell in enumerate(row):
                if cell == "#":
                    Wall(x, y)
                elif cell == "@":
                    self.player = Player(x, y)
                elif cell == "H":
                    Heart(x, y)

    def event_handler(self, events, events_types, time):
        for bullet in player_bullet_group:
            bullet.event_handler(time)
        self.player.event_handler(events, events_types, time)

    def draw(self, surface):
        self.camera.update(self.player)
        self.camera.draw(surface)


def main():
    level = TestLevel()
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        events_types = {event.type for event in events}

        if pygame.QUIT in events_types:
            running = False
            break

        for event in events:
            if event.type == pygame.VIDEORESIZE:
                WINDOW_SIZE_X = event.w
                WINDOW_SIZE_X_2 = WINDOW_SIZE_X // 2
                WINDOW_SIZE_Y = event.h
                WINDOW_SIZE_Y_2 = WINDOW_SIZE_Y // 2

        level.event_handler(events, events_types, clock.tick(FPS))

        level.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
