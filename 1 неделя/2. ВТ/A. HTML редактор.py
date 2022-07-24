from sys import argv, exit
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QTextBrowser,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

class HTML_editor(QWidget):
    def __init__(self):
        super(HTML_editor, self).__init__()
        self.setWindowTitle('HTML editor')
        self.content = QHBoxLayout(self)

        self.edit_input = QTextEdit()
        for action in ('clear', 'copy', 'paste'):
            exec(f'self.b_edit_{action} = QPushButton("{action.capitalize()}")')
        self.browser_output = QTextBrowser()

        self.layout_init()
        self.monitor_input()

    def layout_init(self):
        edit_tool_box = QHBoxLayout()
        for action in ('clear', 'copy', 'paste'):
            exec(
                f'edit_tool_box.addWidget(self.b_edit_{action})\n'
                f'self.b_edit_{action}.clicked.connect(self.edit_{action})'
            )

        for name in ('edit', 'browser'):
            exec(
                f'self.{name}_{"in" if name == "edit" else "out"}put.setMinimumSize(300, 240)\n'
                f'{name}_box = QVBoxLayout()\n'
                f'{name}_box.addWidget(QLabel({chr(39)+"input your HTML here"+chr(39) if name == "edit" else chr(34)+"here"+chr(39)+"s how it will look like on your website"+chr(34)}))\n'
                f'{name}_box.addWidget(self.{name}_{"in" if name == "edit" else "out"}put)\n'
                f'{"edit_box.addLayout(edit_tool_box)" if name == "edit" else ""}\n'
                f'self.content.addLayout({name}_box)\n'
            )


    def monitor_input(self):
        self.edit_input.textChanged.connect(self.change_output)
    def change_output(self):
        self.browser_output.setText(self.edit_input.toPlainText())

    def edit_clear(self):
        self.edit_input.setText('')
    def edit_copy(self):
        import clipboard
        clipboard.copy(self.edit_input.toPlainText())
    def edit_paste(self):
        import clipboard
        self.edit_input.setText(clipboard.paste())


if __name__ == '__main__':
    app = QApplication(argv)
    win = HTML_editor()
    win.show()
    exit(app.exec())