import pygame

from utils import *


class Button:
    def __init__(self, screen, coordinates, dimensions, text=''):
        self.screen = screen
        self.color = BUTTON_COLOR
        self.x, self.y = coordinates[0], coordinates[1]
        self.width, self.height = dimensions[0], dimensions[1]
        self.text = text

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont("ComicSans", 32)
            text = font.render(self.text, True, WHITE)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def hover(self):
        mouse_position = pygame.mouse.get_pos()
        if self.x < mouse_position[0] < self.x + self.width:
            if self.y < mouse_position[1] < self.y + self.height:
                return True
        return False


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)

    screen = pygame.display.set_mode((WINDOW_SIZE_X_2, WINDOW_SIZE_Y_2))
    screen.fill(BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    x_pos = (screen.get_width() - BUTTON_SIZE_X) / 2

    play_button = Button(screen, (x_pos, 100), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Играть")
    collections_button = Button(screen, (x_pos, 175), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Коллекции")
    stats_button = Button(screen, (x_pos, 250), (BUTTON_SIZE_X, BUTTON_SIZE_Y), "Статистика")

    running = True

    while running:
        play_button.draw()
        collections_button.draw()
        stats_button.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.hover():
                    print("Кнопка Играть нажата")
                if collections_button.hover():
                    print("Кнопка Коллекции нажата")
                if stats_button.hover():
                    print("Кнопка Статистика нажата")

            if event.type == pygame.MOUSEMOTION:
                if play_button.hover():
                    play_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    play_button.color = BUTTON_COLOR

                if collections_button.hover():
                    collections_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    collections_button.color = BUTTON_COLOR

                if stats_button.hover():
                    stats_button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    stats_button.color = BUTTON_COLOR

        pygame.display.flip()
