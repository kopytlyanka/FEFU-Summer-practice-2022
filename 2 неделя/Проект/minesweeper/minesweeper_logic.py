from pygame import display, event, QUIT, MOUSEBUTTONDOWN, HIDDEN, transform

from PyQt6.QtGui import QPixmap, QImage

from base import GameBase
from difficulty import Difficulty
from field import Field
from _image_list import image
from minesweeper_window import MinesweeperWindow

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Игровое окно ---------------------------------------------------------------------------------------------------------
class MinesweeperLogic(GameBase):
    ########################################
    # Инициализация
    def __init__(self, difficulty=Difficulty(config['SETTINGS']['difficulty'])) -> None:
        self.__difficulty__ = difficulty
        self.cell_size = int(config['DEFAULT']['cell_size'])
        self.rows = difficulty.rows
        self.columns = difficulty.columns
        self.mines = difficulty.mines
        super(MinesweeperLogic, self).__init__(self.cell_size * self.columns, self.cell_size * self.rows)
        self.screen = self.__display__.set_mode((self.width, self.height), HIDDEN)
        self.field = Field(difficulty)
        display.set_icon(image.icon)
        display.set_caption('Сапер')

    ########################################
    # Переопределение унаследованных методов
    def __execute_events__(self, win=None) -> None:
        for _event in event.get():
            if _event.type == QUIT:
                self.__close__()
            if _event.type == MOUSEBUTTONDOWN and _event.button in (1, 3):
                w = _event.pos[0] // self.cell_size
                h = _event.pos[1] // self.cell_size
                if h < 0:
                    return
                if _event.button == 1:
                    self.open_cell(w, h, win)
                elif _event.button == 3:
                    self.set_flag(w, h, win)

    def __render__(self) -> None:
        value = None
        for w in range(self.columns):
            for h in range(self.rows):
                if self.field.existence:
                    value = self.field.display[h][w]
                if value is None:
                    picture = image.closed
                elif value > 8:
                    picture = image.bomb
                elif value == -1:
                    picture = image.flag
                elif value == -2:
                    picture = image.inform
                elif value == -3:
                    picture = image.no_bomb
                elif value == -4:
                    picture = image.bombed
                else:
                    picture = image.num[self.field.display[h][w]]
                picture = transform.scale(picture, (self.cell_size, self.cell_size))
                self.screen.blit(picture, (w * self.cell_size, h * self.cell_size))

    ########################################
    # Открытие клетки
    def open_cell(self, w, h, win=None) -> None:
        import sys
        sys.setrecursionlimit(0x7fffffff)

        if win is None:
            if self.field.display is None:
                self.field.create_from((w, h))
        else:
            if win.__game_state__ == -1:
                self.field.create_from((w, h))
                win.__game_state__ = 1

        if win is None:
            if self.field.__num__of_open__ == self.field.__num__of_clean__:
                return
        else:
            if win.__game_state__ in (0, 2):
                return

        if self.field.display[h][w] is None:
            self.field.display[h][w] = self.field.data[h][w]
            if self.field.data[h][w] > 8:
                if not (win is None):
                    win.__game_state__ = 0
                self.field.display[h][w] = -4
                self.open_all()
                return
            if self.field.data[h][w] in range(9):
                self.field.__num__of_open__ += 1
            if self.field.data[h][w] == 0:
                for i in (h-1, h, h+1):
                    for j in (w-1, w, w+1):
                        if all((i >= 0, i < self.rows, j >= 0, j < self.columns)):
                            self.open_cell(j, i, win)

        if self.field.__num__of_open__ == self.field.__num__of_clean__:
            for mine in self.field.__mines_list__:
                self.field.display[mine[1]][mine[0]] = -1
            if not(win is None):
                win.__game_state__ = 2

        sys.setrecursionlimit(1000)

    def open_all(self):
        right_mines = 0
        for h in range(self.rows):
            for w in range(self.columns):

                if self.field.display[h][w] is None:
                    if 0 <= self.field.data[h][w] <= 8:
                        self.field.__num__of_open__ += 1
                    self.field.display[h][w] = self.field.data[h][w]

                if self.field.display[h][w] < 0:
                    if self.field.display[h][w] == -1 and self.field.data[h][w] > 8:
                            right_mines += 1
                    elif self.field.display[h][w] != -4:
                        self.field.display[h][w] = self.field.data[h][w]
                        self.field.__num__of_open__ += 1
        self.mines = self.__difficulty__.mines - right_mines

    ########################################
    # Установка флагов
    def set_flag(self, w, h, win=None, inform=None) -> None:
        if win is None:
            if self.field.__num__of_open__ == self.field.__num__of_clean__:
                return
        else:
            if win.__game_state__ != 1:
                return
            if not(inform is None):
                if not(self.field.display[h][w] in range(9)) and self.field.display[h][w] != -2:
                    if self.field.display[h][w] == -1:
                        self.mines += 1
                        self.field.display[h][w] = -2
                    elif self.field.display[h][w] != -2:
                        self.field.display[h][w] = None
                return

        if self.field.display is None:
            return
        if self.field.display[h][w] is None:
            if self.mines > 0:
                self.field.display[h][w] = -1
                self.mines -= 1
        elif self.field.display[h][w] < 0:
            if self.field.display[h][w] == -1:
                self.mines += 1
            self.field.display[h][w] = None

    ########################################
    # Метод запуска в окне pyQT
    def run_in_PyQT(self, win: MinesweeperWindow, FPS=60) -> None:
        import time
        self.__existence__ = True
        w = self.cell_size * self.columns
        h = self.cell_size * self.rows
        while self.__existence__:
            self.__clock__.tick(FPS)
            start = time.time()
            self.__execute_events__(win)
            end = time.time()
            self.__render__()

            if win.__game_state__ == 1:
                if win.timerWidget == 0:
                    win.timerWidget.set(0)
                win.timerWidget.set(win.timerWidget + 1 / FPS + (end-start))
            ########################################
            # Взаимодействия с pyQT
            if type(win.__mouse_event__) is tuple:
                _w = win.__mouse_event__[0] // self.cell_size
                _h = win.__mouse_event__[1] // self.cell_size
                if win.__mouse_event__[2] == 'l':
                    self.open_cell(_w, _h, win)
                elif win.__mouse_event__[2] == 'r':
                    self.set_flag(_w, _h, win)
                else:
                    self.set_flag(_w, _h, win, '?')
                win.__mouse_event__ = None

            if win.__need_to_restart__:
                self.field = Field(self.__difficulty__)
                self.mines = self.__difficulty__.mines
                win.__need_to_restart__ = False
                win.__game_state__ = -1

            win.minesWidget.set(self.mines)

            ########################################
            ## Отрисовка поля

            surface = display.get_surface()
            img = QImage(surface.get_buffer().raw, w, h, QImage.Format.Format_RGB32)
            pix = QPixmap()
            pix.convertFromImage(img)

            win.fieldWidget.setPixmap(pix)
            win.fieldWidget.setFixedSize(w, h)
            win.show()
            win.fieldWidget.deleteLater()

            ########################################
        ########################################

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    game = MinesweeperLogic(Difficulty('easy'))
    game.run()