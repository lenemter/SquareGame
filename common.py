import pygame
from time import time_ns

# Window
window_size_x, window_size_y = (1280, 720)
window_size_x_2, window_size_y_2 = (window_size_x // 2, window_size_y // 2)
WINDOW_NAME = "SquareGame"

# Game
BLOCK_SIZE_X, BLOCK_SIZE_Y = (72, 72)
FPS = 120

# Player
SPEED = 0.005
BULLET_SPEED = 0.007
HEALTH_LIMIT = 3
FLY_LIMIT = 30

# Colors
WHITE = pygame.color.Color("#fAf8FF")
PLAYER_COLOR = pygame.color.Color("#3745F5")
BACKGROUND_COLOR = pygame.color.Color("#1E2331")

BUTTON_COLOR = pygame.color.Color("#33505D")
BUTTON_HOVER_COLOR = pygame.color.Color("#51827B")
BUTTON_SIZE_X, BUTTON_SIZE_Y = 400, 60

STATS_COLOR = pygame.color.Color("#DDDDDD")

def get_time_ms():
    return time_ns() // 1_000_000
