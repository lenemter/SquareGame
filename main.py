from ctypes.wintypes import SIZE
import pygame

from utils import *

# Globals
all_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, player_group)
        self.rect = pygame.Rect(
            x * BLOCK_SIZE[0], y * BLOCK_SIZE[1], BLOCK_SIZE[0], BLOCK_SIZE[1]
        )
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames   

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, 0)

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.rect.x -= 5
                print('left')
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.rect.x += 5
                print('right')
            if event.key in (pygame.K_UP, pygame.K_w):
                self.rect.y -= 5
                print('up')
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.rect.y += 5
                print('bottom')

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                print('left stop')
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                print('right stop')
            if event.key in (pygame.K_UP, pygame.K_w):
                print('up stop')
            if event.key in (pygame.K_DOWN, pygame.K_s):
                print('bottom stop')


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_group, walls_group)
        self.x = x
        self.y = y
        self.size = BLOCK_SIZE
        self.rect = pygame.Rect(
            x * BLOCK_SIZE[0], y * BLOCK_SIZE[1], BLOCK_SIZE[0], BLOCK_SIZE[1]
        )

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 1)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for obj in all_group:
            # obj.rect.x -= self.x
            # obj.rect.y -= self.y
            obj.draw()

    def update(self, target):
        self.x = -(target.rect.x + target.rect.w // 2 - WINDOW_SIZE[0] // 2)
        self.y = -(target.rect.y + target.rect.h // 2 - WINDOW_SIZE[1] // 2)


class Menu:
    def __init__(self):
        self.player = None
        self.level = []
        self.camera = Camera()
        self.load_map()

    def load_map(self):
        with open("levels/menu.txt", mode="r", encoding="UTF-8") as file:
            level = file.readlines()
        x, y = None, None
        for y in range(len(level)):
            self.level.append([])
            for x in range(len(level[y])):
                if level[y][x] == " ":
                    pass
                elif level[y][x] == "#":
                    wall = Wall(x, y)
                    self.level[-1].append(wall)
                    wall.draw()
                elif level[y][x] == "@":
                    self.player = Player(x, y)
                    self.player.draw()

    def event_handler(self, event):
        self.camera.update(self.player)
        self.camera.draw()

        self.player.event_handler(event)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("<Название>")
    screen.fill(BACKGROUND_COLOR)
    menu = Menu()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            menu.event_handler(event)

        pygame.display.flip()

    pygame.quit()
