import pygame
import math
import random

from common import (
    BLOCK_SIZE_X,
    BLOCK_SIZE_Y,
    BASE_SPEED,
    BULLET_SPEED,
    ENEMY_COLOR,
    BASE_HEALTH_LIMIT,
    get_time_ms,
    ENEMY_SPEED,
)
from globals import (
    game_group_3,
    enemy_group,
    enemy_bullet_group,
    walls_group,
    weapon_group,
    player_bullet_group,
    entropy_step,
)
import globals

from bullet import Bullet
from weapon import weapons
from player import Player
from stats import update_stats


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__(game_group_3, enemy_group)

        # Basic stuff
        self.x = x
        self.y = y
        self.player = player
        self.w = 0.6
        self.h = 0.6
        self.rect = pygame.Rect(
            globals.entropy,
            globals.entropy,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )
        self.health = 2
        globals.entropy += entropy_step

        # Camera
        self.last_camera_dx = 0
        self.last_camera_dy = 0

        # Health
        self.health_limit = BASE_HEALTH_LIMIT
        self.health = BASE_HEALTH_LIMIT

        self.weapon = random.choice(weapons)
        self.last_shooting_time = get_time_ms()

        self.delay = random.randint(0, 1000)

    def draw(self, surface, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect, 0)

        self.draw_weapon(surface)

    def draw_weapon(self, surface):
        enemy_center_x = self.x + self.w / 2
        enemy_center_y = self.y + self.h / 2

        distance_x = self.player.x - enemy_center_x
        distance_y = self.player.y - enemy_center_y
        angle = math.atan2(distance_y, distance_x)  # in radians
        angle = angle * (180 / math.pi)  # to degrees
        image = pygame.transform.rotate(
            pygame.transform.scale(
                self.weapon.image
                if abs(angle) < 90
                else pygame.transform.flip(self.weapon.image, False, True),
                (self.w * 1.5 * BLOCK_SIZE_X, self.h * 1.5 * BLOCK_SIZE_Y),
            ),
            -angle,
        )
        surface.blit(
            image,
            image.get_rect(
                center=(
                    self.rect.x + self.w / 2 * BLOCK_SIZE_X,
                    self.rect.y + self.h / 2 * BLOCK_SIZE_Y,
                )
            ),
        )

    def event_handler(self, events, events_types, time):
        # Shooting
        self.handle_shooting()
        # Movement
        self.handle_movement(time)

        bullet_hits = pygame.sprite.spritecollide(self, player_bullet_group, False)

        for bullet in bullet_hits:
            self.health -= bullet.damage
            if self.health <= 0:
                self.kill()
            bullet.kill()

    def handle_movement(self, time):
        dx = (ENEMY_SPEED if self.player.x > self.x else -ENEMY_SPEED) * BASE_SPEED * time
        dy = (ENEMY_SPEED if self.player.y > self.y else -ENEMY_SPEED) * BASE_SPEED * time

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        last_rect_x = self.rect.x
        last_rect_y = self.rect.y

        self.x += dx
        self.rect.x = int(self.x * BLOCK_SIZE_X + self.last_camera_dx)
        if self.rect.x == last_rect_x and dx != 0:
            self.x -= dx
            self.rect.x = last_rect_x
            return None

        self.y += dy
        self.rect.y = int(self.y * BLOCK_SIZE_Y + self.last_camera_dy)
        if self.rect.y == last_rect_y and dy != 0:
            self.y -= dy
            self.rect.y = last_rect_y
            return None

        walls_hits = pygame.sprite.spritecollide(self, walls_group, False)
        for wall in walls_hits:
            if dx > 0:  # Moving right; Hit the left side of the wall
                self.x = wall.x - self.w
                self.rect.x = last_rect_x
                break
            elif dx < 0:  # Moving left; Hit the right side of the wall
                self.x = wall.x + wall.w
                self.rect.x = last_rect_x
                break
            elif dy > 0:  # Moving down; Hit the top side of the wall
                self.y = wall.y - self.h
                self.rect.y = last_rect_y
                break
            elif dy < 0:  # Moving up; Hit the bottom side of the wall
                self.y = wall.y + wall.h
                self.rect.y = last_rect_y
                break

    def handle_shooting(self):
        if get_time_ms() >= self.last_shooting_time + self.weapon.delay * 3 + self.delay:
            self.last_shooting_time = get_time_ms()

            enemy_center_x = self.x + (self.w - self.weapon.w) / 2
            enemy_center_y = self.y + (self.h - self.weapon.l) / 2

            distance_x = self.player.x - enemy_center_x - self.weapon.w / 2
            distance_y = self.player.y - enemy_center_y - self.weapon.l / 2
            angle = math.atan2(distance_y, distance_x)

            speed_x = (math.cos(angle) * BULLET_SPEED) * 0.6
            speed_y = (math.sin(angle) * BULLET_SPEED) * 0.6

            Bullet(
                enemy_bullet_group,
                enemy_center_x,
                enemy_center_y,
                speed_x,
                speed_y,
                self.weapon.w,
                self.weapon.l,
                self.weapon.damage,
                self.weapon.color,
            )
