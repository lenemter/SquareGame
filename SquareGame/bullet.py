import pygame
import math

from globals import game_group_2, walls_group
from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, BULLET_FLY_LIMIT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y, speed_x, speed_y, w, h, damage, color):
        super().__init__(game_group_2, group)

        self.x = x
        self.start_x = x
        self.y = y
        self.start_y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE_X,
            self.y * BLOCK_SIZE_Y,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )

        self.damage = damage
        self.color = color

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, self.color, self.rect, 0, 16)

    def event_handler(self, time):
        fly_distance = math.sqrt(
            abs(self.start_x * self.start_x - self.x * self.x)
            + abs(self.start_y * self.start_y - self.y * self.y)
        )  # Distance between start and end
        if fly_distance > BULLET_FLY_LIMIT or pygame.sprite.spritecollideany(
            self, walls_group
        ):
            self.kill()
        else:
            self.x += self.speed_x * time
            self.y += self.speed_y * time
