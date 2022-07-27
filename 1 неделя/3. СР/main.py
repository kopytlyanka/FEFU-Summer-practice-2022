from window import Window
from PyQt5.QtWidgets import QApplication
from sys import argv, exit


if __name__ == '__main__':
    app = QApplication(argv)
    window = Window()
    window.show()
    exit(app.exec())