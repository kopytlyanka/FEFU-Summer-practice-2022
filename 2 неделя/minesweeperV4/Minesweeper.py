from PyQt6.QtWidgets import QApplication
from window import MSWindow
from logic import MSLogic
import sys

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MSWindow()
    while True:
        content = MSLogic(win)