import os.path
import logging
import pygame


def load_image(name):
    if not os.path.isfile(name):
        logging.error(f"File not found: '{name}'")
    image = pygame.image.load(name).convert_alpha()
    return image


HEART_IMAGE = load_image("images/heart.png")
BAD_HEART_IMAGE = load_image("images/bad_heart.png")
