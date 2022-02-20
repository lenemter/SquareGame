import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import logging
import pygame


def load_image(name):
    if not os.path.isfile(name):
        logging.error(f"File not found: '{name}'")
    image = pygame.image.load(name).convert_alpha()
    return image


HEART_HUD_IMAGE = load_image("images/heart_hud.png")
HEART_IMAGES = load_image("images/heart.png")
BAD_HEART_HUD_IMAGE = load_image("images/bad_heart_hud.png")
PISTOL_IMAGE = load_image("images/Pistol.png")
AK_47_IMAGE = load_image("images/AK-47.png")
BLASTER_IMAGE = load_image("images/Blaster.png")
PORTAL_IMAGE = load_image("images/BluePortal.png")
