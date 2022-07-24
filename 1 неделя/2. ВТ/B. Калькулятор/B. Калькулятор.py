from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QButtonGroup, QLabel
from sys import argv, exit

label_template = '<html><head/><body><p align="right"><span style=" font-size:36pt;">{}</span></p></body></html>'
error_template = '<html><head/><body><p align="right"><span style=" font-size:20pt;">{}</span></p></body></html>'
class Stack(list):
    def __init__(self, x=None):
        super(Stack, self).__init__()
        if not x is None:
            self.append(x)
    def push(self, condition):
        self.append(int(condition))
    def top(self):
        return self[-1]

class Calculator(QMainWindow):
    request_dict = {
        '0': 0,
        '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1,
        ',': 2,
        '*': 3, '/': 3, '^': 3,
        '+': 4, '-': 4,
        '(': 5,
        ')': 6,
        '<': 7,
        'C': 8,
        '=': 9
    }
    def __init__(self):
        super(Calculator, self).__init__()
        uic.loadUi("C:/Users/1/PycharmProjects/летняя практика/1 неделя/2. ВТ/B. Калькулятор/calculator.ui", self)
        self.buttons = QButtonGroup()
        self.buttons.buttonClicked.connect(self.request)
        for i in range(22):
            exec( f'self.buttons.addButton(self.pushButton_{i})')
        self.conditions_stack = Stack(self.request_dict['0'])
        self.parenthesis_count = 0
        self.expression = '0'
        self.label.setText(label_template.format(self.expression))

    def request(self, button):
        sender: str = button.text()
        if '!' in self.label.text():
            if sender == 'C':
                self.request_processing('C')
            elif sender != '<--':
                pass
            else:
                self.request_processing('<')
                self.label.setText(label_template.format(self.expression))
            return

        if sender == 'x^y':
            sender = '^'
        elif sender == '<--':
            sender = '<'

        if sender == 'COPY':
            import clipboard
            clipboard.copy(self.label.text())
        else:
            self.request_processing(sender)

    def calculate(self, expression: str):
        expression = expression.replace(',', '.').replace('^', '**') + (self.parenthesis_count * ')')
        try:
            result = eval(expression)
        except ZeroDivisionError:
            self.request_processing('+')
            self.label.setText(error_template.format('Деление на ноль! Нажмите "&lt;--", чтобы вернуться.'))
        except OverflowError:
            self.request_processing('+')
            self.label.setText(error_template.format('Недопустимые вычисления! Нажмите "&lt;--", чтобы вернуться.'))
        else:
            result = str(eval(expression)).replace('.', ',')
            self.request_processing('C')
            for sym in result:
                self.request_processing(sym)

    def request_processing(self, sender: str):
        def check() -> bool:
            if self.parenthesis_count == 0:
                return True
            return False
        def do(request, actions: str):
            for action in actions.split(', '):
                if action == '_':
                    return
                elif action[:2] == '->':
                    for sender in action[4:-1]:
                        self.request_processing(sender)
                elif action == '++':
                    self.parenthesis_count += 1
                elif action == '--':
                    if check():
                        return
                    self.parenthesis_count -= 1
                elif action.isdigit() or action[0] == '*':
                    if action[0] == '*':
                        do(request, '<')
                    self.expression += request
                    self.conditions_stack.push(action[-1])
                elif action == '<':
                    self.expression = self.expression[:-1]
                    self.conditions_stack.pop()
                elif action == 'C':
                    self.expression = '0'
                    self.conditions_stack.clear()
                    self.conditions_stack.push('0')
                    self.parenthesis_count = 0
                    self.label.setText(label_template.format(self.expression))
                elif action == '=':
                    self.calculate(self.expression)

        conditions_table: list = [
            # 0          1-9                  ,            *,/,^               +,-                 (               )          <--       C     =
            ['_',        '*2',                '4',         '6',                '*1',	           '++, *7',       '_',       '_',      '_',  '='      ],  # 0 - "0"
            ['3',        '2',                 '_',         '_',	               '*1',               '++, 7',        '_',       '<',      'C',  '-> "<="'],  # 1 - sign_
            ['2',        '2',                 '4',         '6',                '6',                '-> "*(", ++',  '--, 8',   '<',      'C',  '='      ],  # 2 - digit_
            ['_',        '_',                 '4',         '6',                '6',                '-> "*(", ++',  '--, *8',  '<',      'C',  '='      ],  # 3 - 0_
            ['5',        '5',                 '_',         f'-> "0{sender}"',  f'-> "0{sender}"',  '-> "*(", ++',  '--, 8',   '<',      'C',  '-> "<=' ],  # 4 - ,_
            ['5',        '5',                 '_',         '6',                '6',                '-> "*(", ++',  '--, 8',   '<',      'C',  '='      ],  # 5 - ,digit_
            ['3',        '2',                 '-> "0,"',   '*6',               '*6',               '++, 7',        '_',       '<',      'C',  '-> "<="'],  # 6 - op_
            ['3',        '2',                 '-> "0,"',   '_',                '1',                '++, 7',        '_',       '--, <',  'C',  '-> "<="'],  # 7 - (_
            ['-> "*0"',  f'-> "*{sender}"',   '-> "*0,"',  '6',                '6',                '-> "*(", ++',  '--, 8',   '++, <',  'C',  '='      ]   # 8 - )_
        ]
        condition = self.conditions_stack.top()
        request = self.request_dict[sender]
        do(sender, conditions_table[condition][request])


        if self.expression == '':
            self.conditions_stack = Stack(self.request_dict['0'])
            self.expression = '0'
        if '!' not in self.label.text():
            self.label.setText(label_template.format(self.expression))


if __name__ == '__main__':
    app = QApplication(argv)
    win = Calculator()
    win.show()
    exit(app.exec())