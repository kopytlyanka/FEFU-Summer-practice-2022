from PyQt6.QtWidgets import QApplication
from pygame import display
from minesweeper_window import MinesweeperWindow
from minesweeper_logic import MinesweeperLogic
import sys

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    content = MinesweeperLogic()
    surface = display.get_surface()
    win = MinesweeperWindow()
    content.run_in_PyQT(win, FPS=20)
    sys.exit(app.exec())