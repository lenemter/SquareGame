import pygame
import math

from globals import *
from utils import *
from images import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y, speed_x, speed_y, w=0.2, h=0.2, fly_limit=30):
        super().__init__(all_group, group)

        self.x = x
        self.start_x = x
        self.y = y
        self.start_y = y
        self.w = w
        self.h = h
        self.fly_limit = fly_limit
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE_X,
            self.y * BLOCK_SIZE_Y,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_X + dy
        pygame.draw.rect(surface, PLAYER_BULLET_COLOR, self.rect, 0, 16)

    def event_handler(self, time):
        fly_distance = math.sqrt(
            abs(self.start_x * self.start_x - self.x * self.x)
            + abs(self.start_y * self.start_y - self.y * self.y)
        )  # Distance between start and end
        in_wall = pygame.sprite.spritecollideany(self, walls_group)
        if fly_distance > self.fly_limit or in_wall:
            self.kill()
        else:
            self.x += self.speed_x * time
            self.y += self.speed_y * time
