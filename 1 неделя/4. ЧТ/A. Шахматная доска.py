import pygame
from base import Game, colors

class Chess(Game):
    def __init__(self, SIZE: int, COUNT: int) -> None:
        self.size = SIZE - SIZE % COUNT
        self.count = COUNT
        self.cell_size = SIZE//COUNT
        super(Chess, self).__init__(self.size, self.size, BACKGROUND=colors.WHITE)
        pygame.display.set_caption("Шахматы")

    def __render__(self) -> None:
        for x in range(self.count):
            for y in range(self.count):
                if (x+y) % 2 == 0:
                    pygame.draw.rect(self.screen, colors.BLACK,
                                     (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))


if __name__ == '__main__':
    game = Chess(400, 10)
    game.run(FPS=60)