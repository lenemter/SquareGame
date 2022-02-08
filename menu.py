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
            font = pygame.font.SysFont('comicsans', 32)
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

    screen = pygame.display.set_mode((500, 500))
    screen.fill(BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    button = Button(BUTTON_COLOR, (50, 150), (400, 50), "New game")
    test_button = Button(BUTTON_COLOR, (50, 250), (400, 50), "Tset")

    while True:
        button.draw(screen)
        test_button.draw(screen)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.hover(mouse_position):
                    print('ABOBA')
                if test_button.hover(mouse_position):
                    print('TETS')

            if event.type == pygame.MOUSEMOTION:
                if button.hover(mouse_position):
                    button.color = BUTTON_HIGHLIGHT_COLOR
                else:
                    button.color = BUTTON_COLOR

                if test_button.hover(mouse_position):
                    test_button.color = BACKGROUND_COLOR
                else:
                    test_button.color = BUTTON_HIGHLIGHT_COLOR

        pygame.display.flip()
