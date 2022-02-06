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

        self.last_camera_dx = 0
        self.last_camera_dy = 0

    def draw(self, dx, dy):
        self.last_camera_dx = dx
        self.last_camera_dy = dy
        self.rect.x = self.x * BLOCK_SIZE_X + dx
        self.rect.y = self.y * BLOCK_SIZE_Y + dy
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, 0)

    def event_handler(self, event):
        keys = pygame.key.get_pressed()
        dx = (
            max(keys[pygame.K_RIGHT], keys[pygame.K_d])
            - max(keys[pygame.K_LEFT], keys[pygame.K_a])
        ) * SPEED
        dy = (
            max(keys[pygame.K_DOWN], keys[pygame.K_s])
            - max(keys[pygame.K_UP], keys[pygame.K_w])
        ) * SPEED

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.x += dx
        self.rect.x += dx * BLOCK_SIZE_X
        self.y += dy
        self.rect.y += dy * BLOCK_SIZE_Y

        for wall in walls_group:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.x = wall.x - self.w
                    self.rect.x = self.x * BLOCK_SIZE_X + self.last_camera_dx
                    break
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.x = wall.x + wall.w
                    self.rect.x = self.x * BLOCK_SIZE_X + self.last_camera_dx
                    break
                if dy > 0:  # Moving down; Hit the top side of the wall
                    # print("COLIDE")
                    self.y = wall.y - self.h
                    self.rect.y = self.y * BLOCK_SIZE_Y + self.last_camera_dy
                    break
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.y = wall.y + wall.h
                    self.rect.y = self.y * BLOCK_SIZE_Y + self.last_camera_dy
                    break
        self.rect.x = self.x * BLOCK_SIZE_X + self.last_camera_dx
        self.rect.y = self.y * BLOCK_SIZE_Y + self.last_camera_dy


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
            # logging.debug(f"OBJ: {obj.x=} {obj.y=}")
            obj.draw(self.x, self.y)

    def update(self, target):
        self.x = target.x + self.x + target.w // 2 - WINDOW_SIZE[0] // 2
        self.y = target.y + self.y + target.h // 2 - WINDOW_SIZE[1] // 2


class Menu:
    def __init__(self):
        self.player = None
        self.level = []
        self.camera = Camera()
        self.load_map()

    def load_map(self):
        with open("levels/menu.txt", mode="r", encoding="UTF-8") as file:
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

    def event_handler(self, event):
        # self.camera.update(self.player)  # PROBLEM HERE
        self.player.event_handler(event)
        self.camera.draw()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption("<Название>")

    menu = Menu()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        menu.event_handler(event)
        pygame.display.flip()

    pygame.quit()
