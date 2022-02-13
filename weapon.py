import pygame
from dataclasses import dataclass

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
