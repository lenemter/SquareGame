import pygame
from dataclasses import dataclass

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y
from images import PISTOL, AK_47, BLASTER
from globals import game_group_1, weapon_group, entropy_step
import globals


@dataclass
class WeaponInfo:
    name: str
    damage: int
    delay: int
    w: float
    l: float
    color: pygame.color.Color
    image: pygame.Surface


weapons = (
    WeaponInfo(
        "Пистолет",
        3,
        250,
        0.25,
        0.25,
        pygame.color.Color("#FFC82C"),
        PISTOL,
    ),
    WeaponInfo(
        "Автомат",
        1,
        160,
        0.2,
        0.2,
        pygame.color.Color("#FFC82C"),
        AK_47,
    ),
    WeaponInfo(
        "Бластер",
        3,
        180,
        0.2,
        0.2,
        pygame.color.Color("#FFC82C"),
        BLASTER,
    ),
)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_info):
        super().__init__(game_group_1, weapon_group)

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.weapon_info = weapon_info

        self.image = pygame.transform.scale(
            self.weapon_info.image, (self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y)
        )
        self.rect = self.image.get_rect()
        self.rect.x = 100000
        self.rect.y = 100000
        globals.entropy += entropy_step

    def draw(self, surface, dx, dy):
        x = self.x * BLOCK_SIZE_X + dx
        y = self.y * BLOCK_SIZE_Y + dy

        surface.blit(self.image, (x, y))
        self.rect.x = x
        self.rect.y = y
