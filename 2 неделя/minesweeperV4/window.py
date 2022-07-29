import pygame
from PyQt6.QtWidgets import (
    QWidget, QMainWindow,
    QGridLayout, QVBoxLayout, QFormLayout,
    QLabel, QLCDNumber, QDialog,
    QPushButton, QSpinBox, QRadioButton, QCheckBox,
    QSpacerItem, QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMouseEvent, QCloseEvent, QAction, QActionGroup, QIcon
from tools import Difficulty
import configparser
import sys
# Константы ------------------------------------------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini')

cell_size = int(config['DEFAULT']['cell_size'])
paddings = int(cell_size / 3)
panel_size = int(cell_size * 1.5)
LCD_width = int(cell_size * 2.5)
B_size = int(cell_size * 1.3)
w_max = int(config['DEFAULT']['w_max'])
h_max = int(config['DEFAULT']['h_max'])

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
# Диалог для ввода пользовательских настроек ---------------------------------------------------------------------------
class InputDifficulty(QDialog):
    def __init__(self, win, cur_diff: Difficulty):
        super(InputDifficulty, self).__init__()
        self.win = win

        self.setWindowTitle('Set Custom Difficulty')
        self.setModal(True)
        self.setFixedSize(300, 400)

        self.Layout = QVBoxLayout()
        for name in ['Easy start', 'Open accord', 'Set accord', 'Inform flag', 'NF mode']:
            check = QCheckBox()
            check.setText(name)
            if config['SETTINGS'][name.lower().replace(' ', '_')] == 'True': check.setCheckState(Qt.CheckState.Checked)
            self.Layout.addWidget(check)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.Layout.addWidget(separator)

        for name in ['Easy', 'Normal', 'Hard', 'Custom']:
            option = QRadioButton()
            option.setText(name)
            self.Layout.addWidget(option)
            if name == 'Easy':
                option.setChecked(True)
            if name == 'Custom':
                self.form = QFormLayout()
                self.form.setSpacing(10)
                option.toggled.connect(self.switch_difficulty)
                for field in ['Height', 'Width', 'Mines']:
                    spin = QSpinBox()
                    spin.setEnabled(False)
                    if field == 'Mines': spin.setMinimum(2)
                    else: spin.setMinimum(8)
                    spin.setMaximum(1000)
                    spin.setPrefix(field + ':   ')
                    spin.valueChanged.connect(self.check_value)
                    self.form.addWidget(spin)
                self.Layout.addLayout(self.form)
        self.setLayout(self.Layout)

        confirm_btn = QPushButton("Confirm")
        confirm_btn.clicked.connect(self.confirm)
        self.Layout.addWidget(confirm_btn)

    def switch_difficulty(self):
        name = self.sender().text()
        for i in range(self.form.count()):
            self.form.itemAt(i).widget().setEnabled(False)
            if name == 'Custom':
                self.form.itemAt(i).widget().setEnabled(True)

    def check_value(self):
        name = self.sender().prefix()[:-4]
        value = self.sender().value()
        if name == 'Height' and value > h_max: value = h_max
        if name == 'Width'  and value > w_max: value = w_max
        if name == 'Mines':
            w = self.sender().parent().form.itemAt(0).widget().value()
            h = self.sender().parent().form.itemAt(1).widget().value()
            if value > w * h - 9: value = w * h - 9
        self.sender().setValue(value)

    def confirm(self):
        difficulty = None
        for i in range(6, 10):
            if self.Layout.itemAt(i).widget().isChecked():
                name = self.Layout.itemAt(i).widget().text()
                if name != 'Custom':
                    difficulty = name.lower()
                else:
                    difficulty = []
                    for j in range(self.form.count()):
                        difficulty.append(str(self.form.itemAt(j).widget().value()))
                    difficulty = ', '.join(difficulty)

        config.set('SETTINGS', 'difficulty', difficulty)
        for i in range(5):
            name = self.Layout.itemAt(i).widget().text().replace(' ', '_')
            if self.Layout.itemAt(i).widget().isChecked():
                config.set('SETTINGS', name, 'True')
            else:
                config.set('SETTINGS', name, 'False')

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.win.__difficulty__ = Difficulty(config['SETTINGS']['difficulty'])
        self.close()
# ----------------------------------------------------------------------------------------------------------------------
# Кнопка рестарта ------------------------------------------------------------------------------------------------------
class RestartButton(QPushButton):
    def __init__(self):
        super(RestartButton, self).__init__()
        self.setFixedSize(B_size, B_size)
        self.setCheckable(True)
# ----------------------------------------------------------------------------------------------------------------------
# Сапер ----------------------------------------------------------------------------------------------------------------
class MSWindow(QMainWindow):
    def __init__(self):
        self.__mouse_event__ = None
        self.__need_to_restart__ = False
        self.__game_state__ = -1
        self.__difficulty_input__ = InputDifficulty(self, Difficulty(config['SETTINGS']['difficulty']))
        self.__difficulty__ = Difficulty(config['SETTINGS']['difficulty'])
        self.parameters = {
            'paddings': 0,
            'MSCounter_width': 0,
            'MSCounter_height': 0,
            'MSRestart_Button_size': 0,
            'offset': 0
        }
        self.__surface_width__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.columns
        self.__surface_height__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.rows
        super(MSWindow, self).__init__()
        self.setWindowIcon(QIcon('icons/icon.png'))

        self.menubar = self.menuBar()
        gameMenu = self.menubar.addMenu('Game')
        gameMenuActions = QActionGroup(self)
        for panel in ['Settings']:
            action = QAction('Settings', self)
            gameMenuActions.addAction(action)
            gameMenu.addAction(action)
        gameMenu.triggered.connect(lambda: self.__difficulty_input__.show())

        self.setFixedSize(self.__surface_width__ + paddings * 2,
                          self.__surface_height__ + panel_size + paddings * 2 + self.menubar.height())
        windowWidget = QWidget()
        windowLayout = QVBoxLayout()
        windowLayout.setContentsMargins(paddings, paddings, paddings, paddings)
        windowLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        windowWidget.setLayout(windowLayout)
        self.setCentralWidget(windowWidget)

        panelLayout = QGridLayout()
        panelLayout.setContentsMargins(1, 0, 1, 0)
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

    def convert_coordinates(self, x, y) -> tuple:
        offset = int(int(config['DEFAULT']['cell_size'])/5)
        y_offset = panel_size + paddings * 3 + offset
        if (paddings < x < self.width() - paddings) and \
                (y_offset < y < self.height() - paddings - 1):
            x -= paddings
            y -= y_offset
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
            self.__mouse_event__ = (x, y, '?')

    def restart(self):
        self.__need_to_restart__ = True
        self.timerWidget.clear()
        self.__surface_width__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.columns
        self.__surface_height__ = int(config['DEFAULT']['cell_size']) * self.__difficulty__.rows
        self.setFixedSize(self.__surface_width__ + paddings * 2,
                          self.__surface_height__ + panel_size + paddings * 2.8 + self.menubar.height())

    def closeEvent(self, close: QCloseEvent) -> None:
        sys.exit()
# ----------------------------------------------------------------------------------------------------------------------