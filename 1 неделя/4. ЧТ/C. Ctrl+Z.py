import pygame
from base import Game, colors
from random import randint

def random_RGB() -> tuple:
    R = randint(0, 255)
    G = randint(0, 255)
    B = randint(0, 255)
    if R+G+B < 100:
        R += randint(0, randint(30, 50))
        G += randint(0, randint(30, 50))
        B += randint(0, randint(30, 50))
    return R, G, B

class Stack(list):
    def __init__(self):
        super(Stack, self).__init__()
    def push(self, condition: pygame.Rect) -> None:
        self.append(condition)
    def size(self) -> int:
        return len(self)

class Rectangles(Game):
    def __init__(self, WIDTH: int, HEIGHT: int, COLOR=None, BACKGROUND=colors.BLACK, BORDER=4) -> None:
        super(Rectangles, self).__init__(WIDTH, HEIGHT, BACKGROUND=BACKGROUND)
        pygame.display.set_caption("Прямоугольники")
        self.rects_color = COLOR
        self.border = BORDER
        self.__stack__ = Stack()
        self.__drawing__ = False
        self.__current_rect__ = pygame.Rect(0, 0, 0, 0)

    def __execute_events__(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__close__()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__drawing__ = True
                self.__current_rect__.update(event.pos, (0, 0))
            if event.type == pygame.MOUSEMOTION:
                self.__current_rect__.size = (event.pos[0] - self.__current_rect__.left,
                                              event.pos[1] - self.__current_rect__.top)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.__drawing__ = False
                rect = self.__current_rect__.copy()
                rect.normalize()
                self.__stack__.push(rect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:
                    if self.__stack__.size() > 0:
                        self.__stack__.pop()

    def __render__(self) -> None:
        for rect in self.__stack__:
            if self.rects_color is None:
                color = random_RGB()
            else:
                color = self.rects_color
            pygame.draw.rect(self.screen, color, rect, self.border)
        if self.__drawing__:
            rect = self.__current_rect__.copy()
            rect.normalize()
            if self.rects_color is None:
                color = random_RGB()
            else:
                color = self.rects_color
            pygame.draw.rect(self.screen, color, rect, self.border)

if __name__ == '__main__':
    game = Rectangles(900, 700, BORDER=10)
    game.run(FPS=60)