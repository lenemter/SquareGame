import pygame


# Sprite groups
all_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
hearts_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
# enemy_group = pygame.sprite.Group()
# enemy_bullet_group = pygame.sprite.Group()

# "Random" sprites placement on start
entropy = 0
entropy_step = 1000
