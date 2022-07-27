from difficulty import Difficulty
from random import sample
# Класс поля -----------------------------------------------------------------------------------------------------------
class Field:
    ########################################
    # Инициализация
    def __init__(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.data = None
        self.display = None
        self.__mines_list__ = None
        self.existence = False
        self.__num__of_open__ = None
        self.__num_of_clean__ = None

    ########################################
    # Установка полей
    def create_from(self, start_cell: tuple):
        self.data = self.__create_field__(0, start_cell=start_cell)
        self.display = self.__create_field__(None)
        self.existence = True

    ########################################
    # Создание атрибутов
    def __create_field__(self, value, start_cell=None) -> list:
        width = self.difficulty.columns
        height = self.difficulty.rows
        self.__num__of_open__ = 0
        self.__num__of_clean__ = width * height - self.difficulty.mines
        field = [
            [value for _ in range(width)]
            for _ in range(height)
        ]
        if value is None:
            return field
        ## Генерация списка мин -------------------
        self.__mines_list__ = []
        for i in range(width):
            for j in range(height):
                if (i, j) != start_cell:
                    self.__mines_list__.append((i, j))
        self.__mines_list__ = sample(self.__mines_list__, self.difficulty.mines)
        ##-----------------------------------------
        ## Расстановка мин ------------------------
        for mine in self.__mines_list__:
            w, h = mine
            field[h][w] = 10
            for i in (h-1, h, h+1):
                for j in (w-1, w, w+1):
                    if all((i >= 0, i < height, j >= 0, j < width)):
                        field[i][j] += 1
        return field
        ##-----------------------------------------
    ########################################
# ----------------------------------------------------------------------------------------------------------------------