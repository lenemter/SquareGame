import pygame
from dataclasses import dataclass

from common import BLOCK_SIZE_X, BLOCK_SIZE_Y
from images import PISTOL, AK_47, BLASTER


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
        pygame.transform.scale(
            PISTOL,
            (0.5 * BLOCK_SIZE_X, 0.5 * BLOCK_SIZE_Y),
        ),
    ),
    WeaponInfo(
        "Автомат",
        1,
        160,
        0.2,
        0.2,
        pygame.color.Color("#FFC82C"),
        pygame.transform.scale(
            AK_47,
            (0.5 * BLOCK_SIZE_X, 0.5 * BLOCK_SIZE_Y),
        ),
    ),
    WeaponInfo(
        "Бластер",
        3,
        180,
        0.2,
        0.2,
        pygame.color.Color("#FFC82C"),
        pygame.transform.scale(
            BLASTER,
            (0.5 * BLOCK_SIZE_X, 0.5 * BLOCK_SIZE_Y),
        ),
    ),
)
