from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QLCDNumber,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QInputDialog,
    QLineEdit,
    QDialog,
    QHBoxLayout,
    QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QCloseEvent, QAction, QActionGroup
from difficulty import Difficulty
import configparser
import sys
config = configparser.ConfigParser()
config.read('config.ini')

# Константы ------------------------------------------------------------------------------------------------------------
paddings = int(int(config['DEFAULT']['cell_size']) / 3)
panel_size = int(int(config['DEFAULT']['cell_size']) * 1.5)
LCD_width = int(int(config['DEFAULT']['cell_size']) * 2.5)
B_size = int(int(config['DEFAULT']['cell_size']) * 1.3)

# LCDCounter -----------------------------------------------------------------------------------------------------------
class LCDCounter(QLCDNumber):
    def __init__(self, count=0) -> None:
        super(LCDCounter, self).__init__()
        self.setMinimumSize(LCD_width, panel_size)
        self.setMaximumWidth(LCD_width)
        self.setDigitCount(3)
        self.__value__ = count
        self.displayLCD()
    def __add__(self, n: (int, float)) -> float:
        return self.__value__ + n
    def __sub__(self, n: (int, float)) -> float:
        return self.__value__ - n
    def __eq__(self, n: (int, float)) -> bool:
        return self.__value__ == n
    def __ne__(self, n: (int, float)) -> bool:
        return self.__value__ != n
    def __lt__(self, n: (int, float)):
        return self.__value__ < n
    def __gt__(self, n: (int, float)) -> bool:
        return self.__value__ > n
    def __le__(self, n: (int, float)) -> bool:
        return self.__value__ <= n
    def __ge__(self, n: (int, float)) -> bool:
        return self.__value__ >= n
    def __int__(self) -> int:
        return int(self.__value__)

    def clear(self) -> None:
        self.__value__ = 0
        self.displayLCD()
    def set(self, n: int) -> None:
        self.__value__ = n
        self.displayLCD()
    def displayLCD(self) -> None:
        if self.__value__ < 0:
            raise ValueError
        elif self.__value__ > 1000:
            self.display('999')
        else:
            self.display(str(int(self.__value__)).zfill(3))
# ----------------------------------------------------------------------------------------------------------------------
# Диалог для ввода пользоватеьской сложности----------------------------------------------------------------------------
class InputDifficulty(QDialog):
    def __init__(self):
        super(InputDifficulty, self).__init__()
        self.setWindowTitle('Host Parameters')
        self.setModal(True)
        self.line_host = QLineEdit()
        self.line_user = QLineEdit()
        self.line_pass = QLineEdit()
        self.connect = QPushButton("connect")
        self.hbox = QHBoxLayout()

        self.form = QFormLayout()
        self.form.setSpacing(20)

        self.form.addRow("&Host:", self.line_host)
        self.form.addRow("&User:", self.line_user)
        self.form.addRow("&Password:", self.line_pass)
        self.form.addRow("Session:", self.hbox)

        self.setLayout(self.form)
# ----------------------------------------------------------------------------------------------------------------------
# Кнопка рестарта ------------------------------------------------------------------------------------------------------
class RestartButton(QPushButton):
    def __init__(self):
        super(RestartButton, self).__init__()
        self.setFixedSize(B_size, B_size)
        self.setCheckable(True)
# ----------------------------------------------------------------------------------------------------------------------
# Сапер ----------------------------------------------------------------------------------------------------------------
class MinesweeperWindow(QMainWindow):
    def __init__(self):
        self.__mouse_event__ = None
        self.__need_to_restart__ = False
        self.__game_state__ = -1
        self.__difficulty_input__ = InputDifficulty()
        self.__difficulty__ = Difficulty(config['SETTINGS']['difficulty'])
        self.__surface_width__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.columns
        self.__surface_height__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.rows
        super(MinesweeperWindow, self).__init__()

        self.menubar = self.menuBar()
        difficultyMenu = self.menubar.addMenu('Difficulty')
        difficultyMenuActions = QActionGroup(self)

        for difficulty in ['Easy', 'Normal', 'Hard', 'Custom']:
            action = QAction(difficulty, self)
            difficultyMenuActions.addAction(action)
            if difficulty == 'Custom':
                difficultyMenu.addSeparator()
            difficultyMenu.addAction(action)
        difficultyMenuActions.triggered.connect(self.change_difficulty)

        self.setFixedSize(self.__surface_width__ + paddings * 2,
                          self.__surface_height__ + panel_size + paddings * 2 + self.menubar.height())
        windowWidget = QWidget()
        windowLayout = QVBoxLayout()
        windowLayout.setContentsMargins(paddings, paddings, paddings, paddings)
        windowLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        windowWidget.setLayout(windowLayout)
        self.setCentralWidget(windowWidget)

        panelLayout = QGridLayout()
        self.fieldWidget = QLabel()
        self.fieldWidget.setScaledContents(True)
        self.fieldWidget.setMinimumSize(self.__surface_width__, self.__surface_height__)

        self.minesWidget = LCDCounter()
        self.restartWidget = RestartButton()
        self.restartWidget.clicked.connect(self.restart)
        self.timerWidget = LCDCounter()

        spliter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        panelLayout.addWidget(self.minesWidget, 0, 0)
        panelLayout.addItem(spliter, 0, 1)
        panelLayout.addWidget(self.restartWidget, 0, 3)
        panelLayout.addItem(spliter, 0, 4)
        panelLayout.addWidget(self.timerWidget, 0, 5)

        windowLayout.addLayout(panelLayout)
        windowLayout.addWidget(self.fieldWidget)

    def change_difficulty(self, action: QAction):
        config.set('SETTINGS', 'difficulty', action.text().lower())
        if action.text() == 'Custom':
            self.__difficulty_input__.open()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def convert_coordinates(self, x, y) -> tuple:
        offset = int(int(config['DEFAULT']['cell_size'])/5)
        if (paddings < x < self.__surface_width__ + paddings) and \
                (paddings * 2 + panel_size + self.menubar.height() - offset < y <
                 self.__surface_height__ + paddings * 2 + panel_size + self.menubar.height() - offset):
            x -= (paddings + 1)
            y -= (paddings * 2 + panel_size + 1 + self.menubar.height() - offset)
            return x, y
        return None, None

    def mousePressEvent(self, click: QMouseEvent) -> None:
        if click.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            x, y = self.convert_coordinates(click.pos().x(), click.pos().y())
            if x is None or y is None:
                return
            if click.button() is Qt.MouseButton.LeftButton:
                self.__mouse_event__ = (x, y, 'l')
            else:
                self.__mouse_event__ = (x, y, 'r')

    def mouseDoubleClickEvent(self, click: QMouseEvent) -> None:
        if click.button() is Qt.MouseButton.RightButton:
            x, y = self.convert_coordinates(click.pos().x(), click.pos().y())
            if x is None or y is None:
                return
            if eval(config['SETTINGS']['inform']):
                self.__mouse_event__ = (x, y, '?')

    def restart(self):
        self.__need_to_restart__ = True
        self.timerWidget.clear()

    def closeEvent(self, close: QCloseEvent) -> None:
        sys.exit()
# ----------------------------------------------------------------------------------------------------------------------