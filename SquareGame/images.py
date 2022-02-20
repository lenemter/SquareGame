import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import logging
import pygame


def load_image(name):
    if not os.path.isfile(name):
        logging.error(f"File not found: '{name}'")
    image = pygame.image.load(name).convert_alpha()
    return image


HEART_IMAGE = load_image("images/heart.png")
BAD_HEART_IMAGE = load_image("images/bad_heart.png")
PISTOL = load_image("images/Pistol.png")
AK_47 = load_image("images/AK-47.png")
BLASTER = load_image("images/Blaster.png")
PORTAL = load_image("images/BluePortal.png")
