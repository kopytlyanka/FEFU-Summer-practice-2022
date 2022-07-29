from random import sample
import re
from pygame.image import load
from PyQt6.QtGui import QImage, QPixmap
# ----------------------------------------------------------------------------------------------------------------------
# Картинки -------------------------------------------------------------------------------------------------------------
class image:
    bomb = load('src/bomb.png')
    bombed = load('src/bombed.png')
    closed = load('src/closed.png')
    flag = load('src/flag.png')
    icon = load('icons/icon.png')
    inform = load('src/inform.png')
    no_bomb = load('src/no_bomb.png')
    num = [
        load('src/num0.png'),
        load('src/num1.png'),
        load('src/num2.png'),
        load('src/num3.png'),
        load('src/num4.png'),
        load('src/num5.png'),
        load('src/num6.png'),
        load('src/num7.png'),
        load('src/num8.png')
    ]
def image_load(n):
    if n is None:
        return image.closed
    elif n == -4:
        return image.bombed
    elif n == -3:
        return image.no_bomb
    elif n == -2:
        return image.inform
    elif n == -1:
        return image.flag
    elif n in range(9):
        return image.num[n]
    elif n > 8:
        return image.bomb
# ----------------------------------------------------------------------------------------------------------------------
# Класс сложности ------------------------------------------------------------------------------------------------------
class Difficulty:
    def __init__(self, mode: str):
        difficulties = {
            'easy': {'rows': 8, 'columns': 8, 'mines': 10},
            'normal': {'rows': 16, 'columns': 16, 'mines': 40},
            'hard': {'rows': 16, 'columns': 30, 'mines': 99}
        }
        self.rows = None
        self.columns = None
        self.mines = None
        self.name = None
        if mode in difficulties.keys():
            self.rows = difficulties[mode]['rows']
            self.columns = difficulties[mode]['columns']
            self.mines = difficulties[mode]['mines']
            self.name = mode
        else:
            mode = re.findall('\d+', mode)
            if len(mode) == 3:
                self.rows = int(mode[0])
                self.columns = int(mode[1])
                self.mines = int(mode[2])
                self.name = 'custom'
            else:
                raise SyntaxError

    def __repr__(self):
        return f'{self.rows}, {self.columns}, {self.mines}'
# ----------------------------------------------------------------------------------------------------------------------
# Класс поля -----------------------------------------------------------------------------------------------------------
class Field:
    def __init__(self, difficulty: Difficulty, easy_start=None) -> None:
        self.columns = difficulty.columns
        self.rows = difficulty.rows
        self.mines = difficulty.mines
        self.data = None
        self.display = None
        self.__mines_list__ = None
        self.existence = False
        self.__need_to_open_list__ = None
        self.__num_of_open__ = None
        self.__num_of_clean__ = None
        self.__easy_start__ = easy_start

    def create_from(self, start_cell: tuple):
        self.__num_of_open__ = 0
        self.__num_of_clean__ = self.columns * self.rows - self.mines
        self.data = self.__create_field__(0, start_cell=start_cell)
        self.display = self.__create_field__(None)
        self.existence = True

    def __create_field__(self, value, start_cell=None) -> list:
        width = self.columns
        height = self.rows
        field = [
            [value for _ in range(width)]
            for _ in range(height)
        ]
        if value is None:
            return field
        ######################################################
        # Генерация списка мин
        self.__mines_list__ = []
        for i in range(width):
            for j in range(height):
                if not self.__easy_start__:
                    if (i, j) == start_cell:
                        continue
                elif all((
                        start_cell[0]-1 <= i, i <= start_cell[0]+1,
                        start_cell[1]-1 <= j, j <= start_cell[1]+1
                )):
                    continue
                self.__mines_list__.append((i, j))
        self.__mines_list__ = sample(self.__mines_list__, self.mines)
        ######################################################
        # Расстановка мин
        for mine in self.__mines_list__:
            w, h = mine
            field[h][w] = 10
            for i in (h-1, h, h+1):
                for j in (w-1, w, w+1):
                    if all((i >= 0, i < height, j >= 0, j < width)):
                            field[i][j] += 1

        return field
        ######################################################
# ----------------------------------------------------------------------------------------------------------------------