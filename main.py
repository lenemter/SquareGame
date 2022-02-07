# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import logging

from utils import *

logging.basicConfig(level=logging.DEBUG)
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE)
pygame.display.set_caption(WINDOW_NAME)

from images import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group)
        global entropy

        # Basic stuff
        self.x = x
        self.y = y
        self.w = 0.5
        self.h = 0.5
        self.rect = pygame.Rect(
            entropy, entropy, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y
        )
        entropy += entropy_step

        # Camera
        self.last_camera_dx = 0
        self.last_camera_dy = 0

        self.health = 0

    def draw(self, surface, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, 0)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        for i in range(1, HEALTH_LIMIT + 1):
            sprite = pygame.sprite.Sprite()
            sprite.image = self.image = pygame.transform.scale(
                HEART_IMAGE if i <= self.health else BAD_HEART_IMAGE,
                (1.2 * BLOCK_SIZE_X, 1.2 * BLOCK_SIZE_Y),
            )
            surface.blit(self.image, ((i * 1.2 - 1) * BLOCK_SIZE_X, 0.2 * BLOCK_SIZE_Y))

    def event_handler(self, event, time):
        keys = pygame.key.get_pressed()
        dx = (
            (
                max(keys[pygame.K_RIGHT], keys[pygame.K_d])
                - max(keys[pygame.K_LEFT], keys[pygame.K_a])
            )
            * SPEED
            * time
        )
        dy = (
            (
                max(keys[pygame.K_DOWN], keys[pygame.K_s])
                - max(keys[pygame.K_UP], keys[pygame.K_w])
            )
            * SPEED
            * time
        )

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

        # Hearts
        heart_hits = pygame.sprite.spritecollide(self, hearts_group, False)
        for heart in heart_hits:
            self.pickup_heart(heart)

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

        # logging.debug(self.x, self.y)

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
        if self.health >= HEALTH_LIMIT:
            return None
        else:
            self.health += heart.heal_amount
            heart.kill()
            logging.debug(self.health)


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, hearts_group)
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.heal_amount = 1

        self.image = pygame.transform.scale(
            HEART_IMAGE,
            (self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y),
        )
        self.rect = self.image.get_rect()

    def draw(self, surface, dx, dy):
        surface.blit(
            self.image, (self.x * BLOCK_SIZE_X + dx, self.y * BLOCK_SIZE_Y + dy)
        )
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, walls_group)
        global entropy

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.rect = pygame.Rect(
            entropy, entropy, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y
        )
        entropy += entropy_step

    def draw(self, surface, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_X + dy
        pygame.draw.rect(surface, WHITE, self.rect, 1)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, surface):
        screen.fill(BACKGROUND_COLOR)
        # logging.debug(f"CAM: {self.x=} {self.y=}")
        for obj in all_group:
            obj.draw(surface, self.x, self.y)

    def update(self, target):
        self.x = target.rect.w // 2 - target.x * BLOCK_SIZE_X + WINDOW_SIZE_X_2
        self.y = target.rect.h // 2 - target.y * BLOCK_SIZE_Y + WINDOW_SIZE_Y_2


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

    def event_handler(self, event, time):
        self.player.event_handler(event, time)
        self.camera.update(self.player)
        self.camera.draw(screen)


if __name__ == "__main__":

    # Sprite groups
    all_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    weapon_group = pygame.sprite.Group()
    hearts_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    player_bullet_group = pygame.sprite.Group()

    # "Random" sprites placement on start
    entropy = 0
    entropy_step = 1000

    level = TestLevel()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_SIZE_X = event.w
                WINDOW_SIZE_X_2 = WINDOW_SIZE_X // 2
                WINDOW_SIZE_Y = event.h
                WINDOW_SIZE_Y_2 = WINDOW_SIZE_Y // 2

        level.event_handler(event, clock.tick(FPS))
        pygame.display.flip()

    pygame.quit()
