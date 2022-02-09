import pygame
from time import time_ns


# Window
window_size_x, window_size_y = (1280, 720)
window_size_x_2, window_size_y_2 = (window_size_x // 2, window_size_y // 2)
WINDOW_NAME = "<Название>"

# Game
TEST_LEVEL = "levels/test_level.txt"
BLOCK_SIZE_X, BLOCK_SIZE_Y = (72, 72)
FPS = 120

# Player
SPEED = 0.005
BULLET_SPEED = 0.008
HEALTH_LIMIT = 3
FLY_LIMIT = 30

# Colors
WHITE = pygame.color.Color("white")
PLAYER_COLOR = pygame.color.Color("blue")
PLAYER_BULLET_COLOR = pygame.color.Color("cadetblue4")
BACKGROUND_COLOR = pygame.color.Color("#333333")

BUTTON_COLOR = pygame.color.Color("#555555")
BUTTON_HOVER_COLOR = pygame.color.Color("#777777")
BUTTON_SIZE_X, BUTTON_SIZE_Y = 400, 50


def get_time_ms():
    return time_ns() // 1_000_000
