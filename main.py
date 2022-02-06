from asyncio import events
import pygame
import logging

from utils import *

# Globals
all_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, player_group)

        # Basic stuff
        self.x = x
        self.y = y
        self.w = 0.5
        self.h = 0.5
        self.rect = pygame.Rect(0, 0, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y)
        
        # Camera
        self.last_camera_dx = 0
        self.last_camera_dy = 0

    def draw(self, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, 0)

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


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, walls_group)
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.rect = pygame.Rect(0, 0, self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y)

    def draw(self, dx, dy):
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_X + dy
        pygame.draw.rect(screen, WHITE, self.rect, 1)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        # logging.debug(f"CAM: {self.x=} {self.y=}")
        for obj in all_group:
            obj.draw(self.x, self.y)

    def update(self, target):
        print(self.x, self.y)
        self.x = target.rect.w // 2 - target.x * BLOCK_SIZE_X + WINDOW_SIZE_X_2
        self.y = target.rect.h // 2 - target.y * BLOCK_SIZE_Y + WINDOW_SIZE_Y_2


class TestLevel:
    def __init__(self):
        self.player = None
        self.level = []
        self.camera = Camera()
        self.load_map()

    def load_map(self):
        with open("levels/1.txt", mode="r", encoding="UTF-8") as file:
            level = file.readlines()
        for y in range(len(level)):
            self.level.append([])
            for x in range(len(level[y])):
                if level[y][x] == " ":
                    pass
                elif level[y][x] == "#":
                    wall = Wall(x, y)
                    self.level[-1].append(wall)
                elif level[y][x] == "@":
                    self.player = Player(x, y)

    def event_handler(self, event, time):
        self.player.event_handler(event, time)
        self.camera.update(self.player)
        self.camera.draw()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE)
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(WINDOW_NAME)

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
