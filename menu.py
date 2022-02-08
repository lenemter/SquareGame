import pygame

from utils import *


class Button:
    def __init__(self, color, coordinates, dimensions, text=''):
        self.color = color
        self.x, self.y = coordinates[0], coordinates[1]
        self.width, self.height = dimensions[0], dimensions[1]
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont("Impact", 32)
            text = font.render(self.text, True, WHITE)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def hover(self, mouse_position):
        if self.x < mouse_position[0] < self.x + self.width:
            if self.y < mouse_position[1] < self.y + self.height:
                return True
        return False


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((500, 400))
    screen.fill(BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    play_button = Button(BUTTON_COLOR, (50, 100), (400, 50), "Играть")
    collections_button = Button(BUTTON_COLOR, (50, 175), (400, 50), "Коллекции")
    stats_button = Button(BUTTON_COLOR, (50, 250), (400, 50), "Статистика")
    settings_button = Button(BUTTON_COLOR, (50, 325), (400, 50), "Настройки")

    while True:
        play_button.draw(screen)
        collections_button.draw(screen)
        stats_button.draw(screen)
        settings_button.draw(screen)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.hover(mouse_position):
                    print("Кнопка Играть нажата")
                if collections_button.hover(mouse_position):
                    print("Кнопка Коллекции нажата")
                if stats_button.hover(mouse_position):
                    print("Кнопка Статистика нажата")
                if settings_button.hover(mouse_position):
                    print("Кнопка Настройки нажата")

            if event.type == pygame.MOUSEMOTION:
                if play_button.hover(mouse_position):
                    play_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    play_button.color = BUTTON_COLOR

                if collections_button.hover(mouse_position):
                    collections_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    collections_button.color = BUTTON_COLOR

                if stats_button.hover(mouse_position):
                    stats_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    stats_button.color = BUTTON_COLOR

                if settings_button.hover(mouse_position):
                    settings_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    settings_button.color = BUTTON_COLOR

        pygame.display.flip()
