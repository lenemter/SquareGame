import pygame

from common import (
    WINDOW_SIZE_X,
    WINDOW_SIZE_Y,
    WINDOW_NAME,
    BUTTON_COLOR,
    BUTTON_HIGHLIGHT_COLOR,
    WHITE,
    BACKGROUND_COLOR,
    BUTTON_SIZE_X,
    BUTTON_SIZE_Y,
)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, coordinates, dimensions, text=""):
        super().__init__(group)
        self.color = BUTTON_COLOR
        self.x, self.y = coordinates[0], coordinates[1]
        self.width, self.height = dimensions[0], dimensions[1]
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, self.width, self.height), 0
        )

        if self.text != "":
            font = pygame.font.SysFont("ComicSans", 32)
            text = font.render(self.text, True, WHITE)
            surface.blit(
                text,
                (
                    self.x + (self.width - text.get_width()) // 2,
                    self.y + (self.height - text.get_height()) // 2,
                ),
            )

    def is_hovered(self):
        mouse_position = pygame.mouse.get_pos()
        return (
            self.x < mouse_position[0] < self.x + self.width
            and self.y < mouse_position[1] < self.y + self.height
        )

    def event_handler(self, events, events_types):
        if self.is_hovered():
            self.color = BUTTON_HIGHLIGHT_COLOR
        else:
            self.color = BUTTON_COLOR
            return None

        if pygame.MOUSEBUTTONDOWN in events_types:
            print(f'Кнопка "{self.text}" нажата')


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)

    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    screen.fill(BACKGROUND_COLOR)

    x_pos = (screen.get_width() - BUTTON_SIZE_X) / 2

    buttons_group = pygame.sprite.Group()

    play_button = Button(
        buttons_group, (x_pos, 100), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Играть"
    )
    collections_button = Button(
        buttons_group, (x_pos, 175), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Коллекции"
    )
    stats_button = Button(
        buttons_group, (x_pos, 250), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Статистика"
    )

    running = True

    while running:
        play_button.draw(screen)
        collections_button.draw(screen)
        stats_button.draw(screen)

        events = pygame.event.get()
        events_types = {event.type for event in events}

        if pygame.QUIT in events_types:
            running = False

        for button in buttons_group:
            button.event_handler(events, events_types)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
