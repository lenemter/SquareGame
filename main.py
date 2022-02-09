import pygame
import logging

from common import (
    window_size_x_2,
    window_size_y_2,
    WINDOW_NAME,
    FPS,
    BACKGROUND_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
)

from test_level import launch_level
from button import Button

# Removes "Hello from the pygame community. https://www.pygame.org/contribute.html"
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

logging.basicConfig(level=logging.DEBUG)
pygame.init()
screen = pygame.display.set_mode((window_size_x_2, window_size_y_2), pygame.RESIZABLE)
pygame.display.set_caption(WINDOW_NAME)


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((window_size_x_2, window_size_y_2))
    screen.fill(BACKGROUND_COLOR)

    x_pos = (screen.get_width() - BUTTON_SIZE_X) // 2

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

    running = True

    while running:
        play_button.draw(screen)
        collections_button.draw(screen)
        stats_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        events = pygame.event.get()
        events_types = {event.type for event in events}

        if pygame.QUIT in events_types:
            running = False

        for button in buttons_group:
            result = button.event_handler(events, events_types)
            if result:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
