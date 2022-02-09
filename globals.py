import pygame


# Sprite groups
game_group_1 = pygame.sprite.Group()  # Lowest
game_group_2 = pygame.sprite.Group()
game_group_3 = pygame.sprite.Group()  # Highest

gui_group_1 = pygame.sprite.Group()  # Lowest
gui_group_2 = pygame.sprite.Group()
gui_group_3 = pygame.sprite.Group()  # Highest

gui_group_custom = pygame.sprite.Group()

walls_group = pygame.sprite.Group()
hearts_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
# enemy_group = pygame.sprite.Group()
# enemy_bullet_group = pygame.sprite.Group()

# "Random" sprites placement on start
entropy = 0
entropy_step = 1000
