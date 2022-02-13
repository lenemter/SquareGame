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

        self.color_interval = 10
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
            font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 24)
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
            if (
                self.color != BUTTON_HOVER_COLOR
                and get_time_ms() > self.last_color_change + self.color_interval
            ):
                self.last_color_change = get_time_ms()
                self.color += self.color_change_speed
        else:
            if (
                self.color != BUTTON_COLOR
                and get_time_ms() > self.last_color_change + self.color_interval
            ):
                self.last_color_change = get_time_ms()
                self.color -= self.color_change_speed
            return None

        if pygame.MOUSEBUTTONUP in events_types:
            if self.callback is None:
                print(f'Кнопка "{self.text}" нажата')
            else:
                self.callback(*self.args, **self.kwargs)
                return True
