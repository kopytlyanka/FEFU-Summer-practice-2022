from sys import argv, exit
import json
import datetime
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QSpinBox,
    QFrame,
    QScrollArea,
    QPushButton
)

class Item(QWidget):
    def __init__(self, image, name, cost):
        super(Item, self).__init__()
        self.setFixedWidth(580)
        self.item = QHBoxLayout(self)
        self.item.setSpacing(0)
        ###########################
        # Info
        name_font = QFont('Bahnschrift SemiLight SemiConde', 20)
        cost_font = QFont('Bahnschrift SemiLight SemiConde', 15)

        self.name = QLabel(name)
        self.name.setFont(QFont(name_font))
        self.name.setContentsMargins(10, 0, 0, 0)

        self.cost = QLabel(cost)
        self.cost.setFont(cost_font)
        self.cost.setContentsMargins(280, 0, 0, 0)
        r = QLabel('₽')
        r.setFont(QFont(cost_font))
        self.count = QSpinBox()
        self.count.setMaximumWidth(60)

        info = QVBoxLayout()
        info.addWidget(self.name)

        cost_layout = QHBoxLayout()
        cost_layout.addWidget(self.count)
        cost_layout.addWidget(r)
        cost_layout.addWidget(self.cost)
        info.addLayout(cost_layout)
        self.item.addLayout(info)
        ###########################
        # Image
        self.image = QLabel()
        self.image.setScaledContents(True)
        self.image.setPixmap(QPixmap(image))
        self.image.setMaximumSize(140, 100)
        self.item.addWidget(self.image)

class KFC(QWidget):
    def __init__(self):
        super(KFC, self).__init__()
        self.setWindowTitle('KFC')
        self.setFixedSize(620, 400)
        self.main = QVBoxLayout(self)
        self.main.setSpacing(0)
        self.main.setContentsMargins(1, 10, 1, 0)

        def AddLineTo_(place, weight=0, lp=0, tp=0, rp=0, bp=0):
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setLineWidth(weight)
            line.setContentsMargins(lp, tp, rp, bp)
            place.addWidget(line)
        ###########################
        # HEADER
        self.header = QLabel('Добро пожаловать в KFC!')
        font = QFont("Bahnschrift Condensed", 25)
        font.setBold(True)
        font.setItalic(True)
        self.header.setFont(font)
        self.header.setContentsMargins(20, 0, 0, 0)
        self.main.addWidget(self.header)
        AddLineTo_(self.main, weight=3, rp=50, lp=3)
        ###########################
        # CONTENT
        self.menu = QScrollArea()
        self.content = QVBoxLayout()
        self.content.setSpacing(0)
        with open('products.json', encoding='utf-8') as file:
            products = json.load(file)
        for product in products:
            exec(
                f'self.item{product["id"]} = Item(product["src"], product["name"], product["cost"])\n'
                f'self.content.addWidget(self.item{product["id"]})'
            )
            AddLineTo_(self.content, 0)
        menu_content = QWidget()
        menu_content.setLayout(self.content)
        self.menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.menu.setWidget(menu_content)
        self.main.addWidget(self.menu)
        ###########################
        # Bottom
        AddLineTo_(self.main, weight=3, lp=50, rp=3)
        self.buy = QPushButton('КУПИТЬ')
        self.buy.setFont(QFont('Arial', 12))
        self.buy.setMaximumWidth(300)
        self.buy.clicked.connect(printReceipt)
        self.main.addWidget(self.buy, alignment=Qt.AlignmentFlag.AlignRight)
        ###########################

class Receipt(QScrollArea):
    def __init__(self, products: list):
        super(Receipt, self).__init__()
        self.setWindowTitle('RECEIPT')
        self.setFixedWidth(400)
        self.horizontalScrollBar().setEnabled(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        receipt = QWidget()
        receipt.setMaximumWidth(self.width())
        content = QVBoxLayout()
        content.setAlignment(Qt.AlignmentFlag.AlignTop)

        def addLabelTo_(place, text, font, aligment=Qt.AlignmentFlag.AlignCenter):
            label = QLabel(text)
            label.setFont(font)
            label.setAlignment(aligment)
            place.addWidget(label)
        ###########################
        # Fonts
        label_font = QFont('Bahnschrift Light', 12)
        big_font = QFont('Bahnschrift Light', 17)
        big_font.setBold(True)
        result_font = QFont('Lucida Console', 25)
        result_font.setBold(True)
        result_font.setUnderline(True)
        item_font = QFont('Consolas', 10)
        item_font.setUnderline(True)
        ###########################
        # Text
        addLabelTo_(content, 'ООО "KFC"', label_font)
        addLabelTo_(content, 'г.Владивосток, п. Аякс 3', label_font)
        addLabelTo_(content, '='*100, label_font)
        addLabelTo_(content, '*КАССОВЫЙ ЧЕК*', big_font)
        count = 0
        result = float(0)
        for item in products:
            count += item.count.value()
            result += item.count.value()*int(item.cost.text())
            cost = f'{item.count.value()} × {float(item.cost.text())}'
            name = item.name.text()
            addLabelTo_(content, name+' '*(53-len(name+cost))+cost, item_font, aligment=Qt.AlignmentFlag.AlignLeft)
            addLabelTo_(content, str(eval(cost.replace('×', '*'))), label_font, aligment=Qt.AlignmentFlag.AlignRight)
        addLabelTo_(content, 'Колличество товарных позиций'+' '*(25-len(str(count)))+str(count),
                    item_font, aligment=Qt.AlignmentFlag.AlignLeft)
        addLabelTo_(content, '=' * 100, label_font)
        addLabelTo_(content, 'ИТОГ' + ' '*(10-len(str(count))) + str(result),
                    result_font, aligment=Qt.AlignmentFlag.AlignRight)
        addLabelTo_(content, '=' * 100, label_font)
        addLabelTo_(content, 'КАССИР  Беспалько Максим', label_font, aligment=Qt.AlignmentFlag.AlignLeft)
        addLabelTo_(content, f'ДАТА  {datetime.date.today()}      ВРЕМЯ  {str(datetime.datetime.now().time())[:8]}',
                    label_font, aligment=Qt.AlignmentFlag.AlignLeft)
        addLabelTo_(content, 'МЕСТО РАССЧЕТОВ:  АЯКС', label_font, aligment=Qt.AlignmentFlag.AlignLeft)
        addLabelTo_(content, '_' * 100, label_font)
        ###########################
        # End
        self.buy = QPushButton('<---')
        self.buy.setMaximumWidth(200)
        self.buy.clicked.connect(returnMenu)
        content.addWidget(self.buy, alignment=Qt.AlignmentFlag.AlignRight)

        receipt.setLayout(content)
        self.setWidget(receipt)
        self.setFixedHeight(min(content.sizeHint().height(), 600))

def printReceipt():
    global win
    with open('products.json', encoding='utf-8') as file:
        menu = json.load(file)
    products = []
    for i in range(1, len(menu)+1):
        exec(
            f'if win.item{i}.count.value() > 0:\n'
            f'\tproducts.append(win.item{i})'
        )
    if len(products) != 0:
        receipt = Receipt(products)
        win = receipt
        win.show()

def returnMenu():
    global win
    menu = KFC()
    win = menu
    win.show()


if __name__ == '__main__':
    app = QApplication(argv)
    win = KFC()
    win.show()
    exit(app.exec())