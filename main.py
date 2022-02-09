# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import logging

import common
from common import (
    WINDOW_NAME,
    FPS,
    BACKGROUND_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
)

pygame.init()
screen = pygame.display.set_mode((common.window_size_x, common.window_size_y), pygame.RESIZABLE)

from test_level import launch_level
from button import Button


def main():
    logging.basicConfig(level=logging.DEBUG)

    pygame.display.set_caption(WINDOW_NAME)

    x_pos = (common.window_size_x - BUTTON_SIZE_X) // 2
    buttons_group = pygame.sprite.Group()
    play_button = Button(
        group=buttons_group,
        x=x_pos,
        y=100,
        w=BUTTON_SIZE_X,
        h=BUTTON_SIZE_Y,
        text="Играть",
        callback=launch_level,
        args=(screen,),
    )

    collections_button = Button(
        group=buttons_group,
        x=x_pos,
        y=175,
        w=BUTTON_SIZE_X,
        h=BUTTON_SIZE_Y,
        text="Коллекции",
    )

    stats_button = Button(
        group=buttons_group,
        x=x_pos,
        y=250,
        w=BUTTON_SIZE_X,
        h=BUTTON_SIZE_Y,
        text="Статистика",
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)
        play_button.draw(screen)
        collections_button.draw(screen)
        stats_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        events = pygame.event.get()
        events_types = {event.type for event in events}

        if pygame.QUIT in events_types:
            running = False

        for event in events:
            if event.type == pygame.VIDEORESIZE:
                common.window_size_x = event.w
                common.window_size_x_2 = event.w // 2
                common.window_size_y = event.h
                common.window_size_y_2 = event.h // 2
                x_pos = (event.w - BUTTON_SIZE_X) // 2

        for button in buttons_group:
            result = button.event_handler(events, events_types)
            if result:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
