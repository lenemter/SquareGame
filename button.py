import pygame

from common import (
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    WHITE,
    get_time_ms,
)
from globals import gui_group_custom


class Button(pygame.sprite.Sprite):
    def __init__(
        self, group, x, y, w, h, text="", callback=None, args=tuple(), kwargs=dict()
    ):
        super().__init__(gui_group_custom, group)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text = text
        self.color = BUTTON_COLOR
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        self.color_interval = 30
        self.last_color_change = 0
        self.color_change_speed = pygame.color.Color(
            abs(self.color.r - BUTTON_HOVER_COLOR.r) // 10,
            abs(self.color.g - BUTTON_HOVER_COLOR.g) // 10,
            abs(self.color.b - BUTTON_HOVER_COLOR.b) // 10,
            0,
        )

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
            if self.color != BUTTON_HOVER_COLOR:
                self.color += self.color_change_speed
        else:
            if self.color != BUTTON_COLOR:
                self.color -= self.color_change_speed
            return None

        if pygame.MOUSEBUTTONDOWN in events_types:
            if self.callback is None:
                print(f'Кнопка "{self.text}" нажата')
            else:
                self.callback(*self.args, **self.kwargs)
                return True
