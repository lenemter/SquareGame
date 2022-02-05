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

        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE_X, BLOCK_SIZE_Y)

    def draw(self, delta_x, delta_y):
        self.rect.x = self.x * BLOCK_SIZE_X + delta_x
        self.rect.y = self.y * BLOCK_SIZE_Y + delta_y
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, 0)

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.x -= 5
                print("left")
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.x += 5
                print("right")
            if event.key in (pygame.K_UP, pygame.K_w):
                self.y -= 5
                print("up")
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.y += 5
                print("bottom")

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                print("left stop")
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                print("right stop")
            if event.key in (pygame.K_UP, pygame.K_w):
                print("up stop")
            if event.key in (pygame.K_DOWN, pygame.K_s):
                print("bottom stop")


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, walls_group)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE_X, BLOCK_SIZE_Y)

    def draw(self, delta_x, delta_y):
        self.rect.x = self.x * BLOCK_SIZE_X + delta_x
        self.rect.y = self.y * BLOCK_SIZE_X + delta_y
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
            obj.draw(obj.x - self.x, obj.y - self.y)

    def update(self, target):
        self.x = (target.x + self.x + target.w // 2 - WINDOW_SIZE[0] // 2)
        self.y = (target.y + self.y + target.h // 2 - WINDOW_SIZE[1] // 2)


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
        self.player.event_handler(event)
        # self.camera.update(self.player)  # PROBLEM HERE
        self.camera.draw()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption("<Название>")

    menu = Menu()
    # clock = pygame.time.Clock()
    running = True
    # pygame.key.set_repeat()
    # x_pos = 0
    # v = 20
    # fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # clock.tick(fps)
        menu.event_handler(event)
        pygame.display.flip()

    pygame.quit()
