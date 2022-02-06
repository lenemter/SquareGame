import pygame

from utils import *


class Button:
    def __init__(self, text, pos):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Impact", 20)
        self.set_text(text)

    def set_text(self, text):
        self.text = self.font.render(text, True, WHITE)
        self.size = self.text.get_size()
        self.surface = pygame.Surface((self.size[0] + 50, self.size[1] + 10))
        self.surface.fill(BACKGROUND_COLOR)
        self.surface.blit(self.text, (25, 5))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        screen.blit(button.surface, (self.x, self.y))

    def click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pass


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    button = Button("Sus", (200, 200))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        button.show()
        clock.tick(100)
        pygame.display.flip()
