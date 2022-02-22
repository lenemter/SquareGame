import pygame
import math
import random

from common import (
    BLOCK_SIZE_X,
    BLOCK_SIZE_Y,
    BASE_SPEED,
    BULLET_SPEED,
    TO_DEG,
    get_time_ms,
)
from globals import (
    game_group_4,
    enemy_group,
    enemy_bullet_group,
    walls_group,
    player_bullet_group,
    entropy_step,
)
import globals

from bullet import Bullet
from weapon import weapons


class Enemy(pygame.sprite.Sprite):
    color = pygame.color.Color("#FF0000")

    def __init__(self, x, y):
        super().__init__(game_group_4, enemy_group)

        # Basic stuff
        self.x = x
        self.y = y
        self.w = 0.6
        self.h = 0.6
        self.rect = pygame.Rect(
            globals.entropy,
            globals.entropy,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )
        globals.entropy += entropy_step

        # Camera
        self.last_camera_dx = 0
        self.last_camera_dy = 0

        # Health
        self.health = random.randint(2, 4)

        self.weapon = random.choice(weapons)
        self.last_shooting_time = get_time_ms()

        # Random stats
        self.shooting_delay = random.randint(300, 1100)
        self.speed = BASE_SPEED * random.uniform(0.9, 1.1) * 0.5
        self.bullet_speed = BULLET_SPEED * random.uniform(0.6, 1.4)

        self.angle = random.uniform(-180, 180)

        # Room activity
        self.is_active = False

    def activate(self):
        self.is_active = True
        self.last_shooting_time = get_time_ms()

    def draw(self, surface, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, self.color, self.rect, 0)

        self.draw_weapon(surface)

    def draw_weapon(self, surface):
        image = pygame.transform.rotate(
            pygame.transform.scale(
                self.weapon.image
                if abs(self.angle) < 90
                else pygame.transform.flip(self.weapon.image, False, True),
                (self.w * 1.5 * BLOCK_SIZE_X, self.h * 1.5 * BLOCK_SIZE_Y),
            ),
            -self.angle,
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

    def event_handler(self, time):
        if self.is_active:
            # Shooting
            self.handle_shooting()
            # Movement
            self.handle_movement(time)
            # Weapon
            self.handle_weapon_rotation()

            bullet_hits = pygame.sprite.spritecollide(self, player_bullet_group, False)
            for bullet in bullet_hits:
                self.health -= bullet.damage
                if self.health <= 0:
                    globals.game.kills += 1
                    self.kill()
                bullet.kill()
        else:
            bullet_hits = pygame.sprite.spritecollide(self, player_bullet_group, True)

    def handle_movement(self, time):
        dx = (1 if globals.game.player.x > self.x else -1) * self.speed * time
        dy = (1 if globals.game.player.y > self.y else -1) * self.speed * time

        if dx != 0 and dy != 0:
            dx /= 1.1
            dy /= 1.1

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
        if (
            get_time_ms()
            >= self.last_shooting_time + self.weapon.delay * 2 + self.shooting_delay
        ):
            self.last_shooting_time = get_time_ms()

            enemy_center_x = self.x + (self.w - self.weapon.w) / 2
            enemy_center_y = self.y + (self.h - self.weapon.l) / 2

            distance_x = globals.game.player.x - enemy_center_x - self.weapon.w / 2
            distance_y = globals.game.player.y - enemy_center_y - self.weapon.l / 2
            angle = math.atan2(distance_y, distance_x)

            speed_x = math.cos(angle) * self.bullet_speed
            speed_y = math.sin(angle) * self.bullet_speed

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

    def handle_weapon_rotation(self):
        enemy_center_x = self.x + self.w / 2
        enemy_center_y = self.y + self.h / 2

        distance_x = globals.game.player.x - enemy_center_x
        distance_y = globals.game.player.y - enemy_center_y
        angle = math.atan2(distance_y, distance_x)  # in radians
        self.angle = angle * TO_DEG  # to degrees
