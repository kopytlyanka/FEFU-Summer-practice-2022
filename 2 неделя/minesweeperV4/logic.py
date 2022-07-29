import array

import pygame

from PyQt6.QtGui import QPixmap, QImage

from tools import *
from window import MSWindow
import configparser
import time

config = configparser.ConfigParser()


# Игровое окно ---------------------------------------------------------------------------------------------------------
class MSLogic:
    ########################################
    # Инициализация
    def __init__(self, win: MSWindow) -> None:
        config.read('config.ini')
        difficulty = Difficulty(config['SETTINGS']['difficulty'])
        self.__easy_start__ = True if config['SETTINGS']['easy_start'] == 'True' else False
        self.__nf_mode__ = True if config['SETTINGS']['nf_mode'] == 'True' else False
        self.__open_accord__ = True if config['SETTINGS']['open_accord'] == 'True' and \
                                        self.__nf_mode__ == False else False
        self.__set_accord__ = True if config['SETTINGS']['set_accord'] == 'True' and \
                                      self.__nf_mode__ == False else False
        self.__inform__ = True if config['SETTINGS']['inform_flag'] == 'True' else False
        self.difficulty = Difficulty(config['SETTINGS']['difficulty'])
        self.rows = difficulty.rows
        self.columns = difficulty.columns
        self.mines = difficulty.mines
        self.cell_size = int(config['DEFAULT']['cell_size'])
        self.field = Field(difficulty, easy_start=self.__easy_start__)
        FPS = int(config['DEFAULT']['fps'])
        self.screen = pygame.display.set_mode((self.cell_size * self.columns, self.cell_size * self.rows),
                                              pygame.HIDDEN)
        self.__existence__ = True
        w = self.cell_size * self.columns
        h = self.cell_size * self.rows
        while True:
            pygame.time.Clock().tick(FPS)
            start = time.time()
            pygame.event.get()
            end = time.time()
            self.__render__()

            if win.__game_state__ == 1:
                if win.timerWidget == 0:
                    win.timerWidget.set(0)
                win.timerWidget.set(win.timerWidget + 1 / FPS + (end - start))
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
                pygame.display.quit()
                self.field = Field(self.difficulty)
                self.mines = self.difficulty.mines
                win.__need_to_restart__ = False
                win.__game_state__ = -1

            win.minesWidget.set(self.mines)

            ########################################
            # Отрисовка поля

            surface = pygame.display.get_surface()
            if surface is None: return
            img = QImage(surface.get_buffer().raw, w, h, QImage.Format.Format_RGB32)
            pix = QPixmap()
            pix.convertFromImage(img)

            win.fieldWidget.setPixmap(pix)
            win.fieldWidget.setFixedSize(w, h)
            win.show()
            win.fieldWidget.deleteLater()

    ########################################

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
                picture = pygame.transform.scale(picture, (self.cell_size, self.cell_size))
                self.screen.blit(picture, (w * self.cell_size, h * self.cell_size))

    ########################################
    # Открытие клетки
    def open_cell(self, w, h, win: MSWindow, open_accord=None, set_accord=None) -> None:
        import sys
        sys.setrecursionlimit(0x7fffffff)
        if open_accord is None: open_accord = self.__open_accord__
        if set_accord is None: set_accord = self.__set_accord__
        if win.__game_state__ == -1:
            self.field.create_from((w, h))
            win.__game_state__ = 1

        if win.__game_state__ in (0, 2):
            return

        if self.field.display[h][w] in range(9) or self.field.display[h][w] is None:
            if self.field.data[h][w] > 8:
                win.__game_state__ = 0
                self.field.display[h][w] = -4
                self.open_all()
                return
            if self.field.data[h][w] in range(9):
                if self.field.display[h][w] is None:
                    self.field.__num_of_open__ += 1
                self.field.display[h][w] = self.field.data[h][w]

                need_to_open = []
                need_to_check = []
                for i in (h - 1, h, h + 1):
                    for j in (w - 1, w, w + 1):
                        if all((i >= 0, i < self.rows, j >= 0, j < self.columns)):
                            if open_accord:
                                if self.field.display[i][j] is None:
                                    need_to_open.append([i, j])
                                elif self.field.display[i][j] == -1:
                                    need_to_check.append([i, j])
                            elif self.field.data[h][w] == 0 and self.field.display[i][j] is None:
                                self.field.display[h][w] = 0
                                self.open_cell(j, i, win)

                if open_accord:
                    if len(need_to_check) == self.field.data[h][w]:
                        if len(need_to_open) > 0:
                            for cell in need_to_check:
                                self.field.display[cell[0]][cell[1]] = None
                            for cell in need_to_open:
                                self.open_cell(cell[1], cell[0], win, set_accord=False)
                            for cell in need_to_check:
                                self.field.display[cell[0]][cell[1]] = -1

                if set_accord:
                    if len(need_to_open) + len(need_to_check) == self.field.data[h][w]:
                        for cell in need_to_open:
                            self.field.display[cell[0]][cell[1]] = -1

        if self.field.__num_of_open__ == self.field.__num_of_clean__:
            for mine in self.field.__mines_list__:
                self.field.display[mine[1]][mine[0]] = -1
            win.__game_state__ = 2

    def open_all(self):
        right_mines = 0
        for h in range(self.rows):
            for w in range(self.columns):

                if self.field.display[h][w] is None:
                    if 0 <= self.field.data[h][w] <= 8:
                        self.field.__num_of_open__ += 1
                    self.field.display[h][w] = self.field.data[h][w]

                if self.field.display[h][w] < 0:
                    if self.field.display[h][w] == -1:
                        if self.field.data[h][w] > 8:
                            right_mines += 1
                        else:
                            self.field.display[h][w] = -3
                    elif self.field.display[h][w] != -4:
                        self.field.display[h][w] = self.field.data[h][w]
                        self.field.__num_of_open__ += 1
        self.mines = self.difficulty.mines - right_mines

    ########################################
    # Установка флагов
    def set_flag(self, w, h, win: MSWindow, inform=None) -> None:
        if self.__nf_mode__: return
        if not(inform is None) and not self.__inform__: return

        if win.__game_state__ != 1:
            return
        if not (inform is None):
            if not (self.field.display[h][w] in range(9)) and self.field.display[h][w] != -2:
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

# ----------------------------------------------------------------------------------------------------------------------
