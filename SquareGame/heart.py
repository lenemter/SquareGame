import pygame

import globals
from common import BLOCK_SIZE_X, BLOCK_SIZE_Y, get_time_ms
from images import HEART_IMAGES
from globals import game_group_2, hearts_group


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(game_group_2, hearts_group)

        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.heal_amount = 1

        self.frames = []
        self.cut_sheet(HEART_IMAGES, 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(
            globals.entropy,
            globals.entropy,
            self.w * BLOCK_SIZE_X,
            self.h * BLOCK_SIZE_Y,
        )
        globals.entropy += globals.entropy_step
        self.last_updated = get_time_ms()

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(
                    pygame.transform.scale(
                        sheet.subsurface(pygame.Rect(frame_location, rect.size)),
                        (self.w * BLOCK_SIZE_X, self.h * BLOCK_SIZE_Y),
                    )
                )

    def update_image(self):
        if self.last_updated + 400 <= get_time_ms():
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

            self.last_updated = get_time_ms()

    def draw(self, surface, dx, dy):
        self.update_image()

        x = self.x * BLOCK_SIZE_X + dx
        y = self.y * BLOCK_SIZE_Y + dy

        surface.blit(self.image, (x, y))
        self.rect.x = x
        self.rect.y = y
