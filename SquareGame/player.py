import pygame
import math

from common import (
    BLOCK_SIZE_X,
    BLOCK_SIZE_Y,
    BASE_SPEED,
    BULLET_SPEED,
    PLAYER_COLOR,
    BASE_HEALTH_LIMIT,
    TO_DEG,
    get_time_ms,
)
from globals import (
    game_group_3,
    hearts_group,
    player_bullet_group,
    walls_group,
    weapon_group,
    entropy_step,
    portal_group,
    enemy_bullet_group,
)
import globals

from bullet import Bullet
from weapon import weapons
from hud import HUD1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(game_group_3)

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
        self.health_limit = BASE_HEALTH_LIMIT
        self.health = BASE_HEALTH_LIMIT

        # Weapon
        self.weapon = weapons[0]
        self.last_shooting_time = get_time_ms()

        self.last_hit_time = 0

        # Rooms
        self.last_room = None

        HUD1()

    def draw(self, surface, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, 0)

        self.draw_weapon(surface, dx, dy)

    def draw_weapon(self, surface, dx, dy):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        player_center_x = self.x + self.w / 2
        player_center_y = self.y + self.h / 2

        distance_x = (mouse_x - dx) / BLOCK_SIZE_X - player_center_x
        distance_y = (mouse_y - dy) / BLOCK_SIZE_Y - player_center_y
        angle = math.atan2(distance_y, distance_x)  # in radians
        angle = angle * TO_DEG  # to degrees
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

    def event_handler(self, time):
        # Movement
        self.handle_movement(time)
        # Hearts
        heart_hits = pygame.sprite.spritecollide(self, hearts_group, False)
        for heart in heart_hits:
            self.pickup_heart(heart)
        # Shooting
        self.handle_shooting()
        # Weapon pickup
        self.handle_weapon()
        # Portal
        self.handle_portals()
        # Hit by enemy
        enemy_hits = pygame.sprite.spritecollide(self, enemy_bullet_group, False)
        for hit in enemy_hits:
            if self.last_hit_time + 1000 <= get_time_ms():
                self.last_hit_time = get_time_ms()
                self.health -= hit.damage
            hit.kill()
        # Death
        if self.health <= 0:
            globals.game.show_death_screen()

    def handle_movement(self, time):
        keys = pygame.key.get_pressed()
        dx = (
            (
                max(keys[pygame.K_RIGHT], keys[pygame.K_d])
                - max(keys[pygame.K_LEFT], keys[pygame.K_a])
            )
            * BASE_SPEED
            * time
        )
        dy = (
            (
                max(keys[pygame.K_DOWN], keys[pygame.K_s])
                - max(keys[pygame.K_UP], keys[pygame.K_w])
            )
            * BASE_SPEED
            * time
        )

        # Fix player's speed when moving diagonally
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

    def pickup_heart(self, heart):
        if self.health >= BASE_HEALTH_LIMIT:
            return None
        else:
            self.health += heart.heal_amount
            heart.kill()
            globals.game.hearts += 1

    def handle_shooting(self):
        if (
            pygame.mouse.get_pressed()[0]
            and get_time_ms() >= self.last_shooting_time + self.weapon.delay
        ):
            self.last_shooting_time = get_time_ms()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            player_center_x = self.x + (self.w - self.weapon.w) / 2
            player_center_y = self.y + (self.h - self.weapon.l) / 2

            distance_x = (
                (mouse_x - self.last_camera_dx) / BLOCK_SIZE_X
                - player_center_x
                - self.weapon.w / 2
            )
            distance_y = (
                (mouse_y - self.last_camera_dy) / BLOCK_SIZE_Y
                - player_center_y
                - self.weapon.l / 2
            )
            angle = math.atan2(distance_y, distance_x)

            speed_x = math.cos(angle) * BULLET_SPEED
            speed_y = math.sin(angle) * BULLET_SPEED

            Bullet(
                player_bullet_group,
                player_center_x,
                player_center_y,
                speed_x,
                speed_y,
                self.weapon.w,
                self.weapon.l,
                self.weapon.damage,
                self.weapon.color,
            )

    def handle_weapon(self):
        weapon_hits = pygame.sprite.spritecollide(self, weapon_group, False)
        for weapon in weapon_hits:
            if weapon.weapon_info != self.weapon:
                self.weapon = weapon.weapon_info
                weapon.kill()
                globals.game.weapons += 1

    def handle_portals(self):
        if (
            pygame.sprite.spritecollideany(self, portal_group)
            and pygame.mouse.get_pressed()[0]
        ):
            globals.game.levels += 1
            globals.game.level.remove_all_objects()
            globals.game.launch_level()
