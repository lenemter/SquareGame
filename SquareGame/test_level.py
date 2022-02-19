import pygame
import random

import common
from common import FPS
from globals import player_bullet_group

from camera import Camera
from player import Player
from enemy import Enemy
from wall import Wall
from heart import Heart
from hud import HUD1
from weapon import Weapon, weapons
from stats import update_stats


class TestLevel:
    def __init__(self):
        self.player = None
        self.hud_1 = None
        self.enemy = None
        self.camera = Camera()
        self.player_x, self.player_y = 0, 0
        self.load_map()
        update_stats({"games": 1, "rooms": 1, "levels": 1})

    def load_map(self):
        test_level = f"levels/{random.randint(1, 3)}.txt"
        with open(test_level, mode="r", encoding="UTF-8") as file:
            level = file.readlines()

        for y, row in enumerate(level):
            for x, cell in enumerate(row):
                if cell == "#":
                    Wall(x, y)
                elif cell == "@":
                    self.player = Player(x, y)
                    self.hud_1 = HUD1(self.player)
                elif cell == "H":
                    Heart(x, y)
                elif cell == "P":
                    Weapon(x, y, weapons[0])
                elif cell == "A":
                    Weapon(x, y, weapons[1])
                elif cell == "B":
                    Weapon(x, y, weapons[2])
                elif cell == "E":
                    self.enemy = Enemy(x, y, self.player)

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
