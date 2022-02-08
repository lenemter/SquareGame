import pygame

import common
from common import TEST_LEVEL, FPS
from globals import player_bullet_group

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


def launch_level(surface):
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
                common.window_size_x_2 = event.w // 2
                common.window_size_y_2 = event.h // 2

        level.event_handler(events, events_types, clock.tick(FPS))

        level.draw(surface)
        pygame.display.flip()

    pygame.quit()