import pygame


# Window
WINDOW_SIZE_X, WINDOW_SIZE_Y = (1280, 720)
WINDOW_SIZE_X_2, WINDOW_SIZE_Y_2 = (WINDOW_SIZE_X // 2, WINDOW_SIZE_Y // 2)
WINDOW_NAME = "<Название>"

# Game
TEST_LEVEL = "levels/test_level.txt"
BLOCK_SIZE_X, BLOCK_SIZE_Y = (50, 50)
FPS = 120

# Player
SPEED = 0.005
BULLET_SPEED = 0.005
HEALTH_LIMIT = 3

# Colors
WHITE = pygame.color.Color("white")
PLAYER_COLOR = pygame.color.Color("blue")
BACKGROUND_COLOR = pygame.color.Color("#333333")
