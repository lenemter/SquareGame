import pygame

from common import (
    BUTTON_COLOR,
    BUTTON_HIGHLIGHT_COLOR,
    WHITE,
)


class Button(pygame.sprite.Sprite):
    def __init__(
        self, group, x, y, w, h, text="", callback=None, args=tuple(), kwargs=dict()
    ):
        super().__init__(group)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text = text
        self.color = BUTTON_COLOR
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text != "":
            font = pygame.font.SysFont("ComicSans", 32)
            text = font.render(self.text, True, WHITE)
            surface.blit(
                text,
                (
                    self.x + (self.w - text.get_width()) // 2,
                    self.y + (self.h - text.get_height()) // 2,
                ),
            )

    def is_hovered(self):
        mouse_position = pygame.mouse.get_pos()
        return (
            self.x < mouse_position[0] < self.x + self.w
            and self.y < mouse_position[1] < self.y + self.h
        )

    def event_handler(self, events, events_types):
        if self.is_hovered():
            self.color = BUTTON_HIGHLIGHT_COLOR
        else:
            self.color = BUTTON_COLOR
            return None

        if pygame.MOUSEBUTTONDOWN in events_types:
            if self.callback is None:
                print(f'Кнопка "{self.text}" нажата')
            else:
                self.callback(*self.args, **self.kwargs)
                return True
