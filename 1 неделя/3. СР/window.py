import datetime
from PyQt5.QtWidgets import QMainWindow, QWidget
from add_widget_ui import Ui_Form
from window_ui import Ui_MainWindow
from db_manager import DBConn


class AddPrompt(QWidget, Ui_Form):
    def __init__(self, db_conn):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.submit)

        self.genres_combo.addItems(db_conn.genre_lookup)
        self.genres_combo.setCurrentText(db_conn.genre_lookup[0])

        self.db = db_conn

        self.year_spin.setMaximum(datetime.datetime.now().year)
        self.year_spin.setMinimum(1895)

        self.duration_spin.setMaximum(9999)
        self.duration_spin.setMinimum(1)

    def submit(self):
        if not self.validate(self.title_input.text()): return

        self.db.add_film((self.title_input.text(), self.year_spin.value(),
                          self.db.genres[self.genres_combo.currentText()], self.duration_spin.value()))
        self.close()

    def validate(self, title: str) -> bool:
        if title.strip() == '':
            self.errors.setText('Название вашего фильма не должно быть пустым!')
            return False

        return True


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db = DBConn()
        self.prompt = AddPrompt(self.db)
        self.setupUi(self)
        self.combo_genres.addItem('Все')
        self.combo_genres.addItems(self.db.genres.keys())
        self.combo_genres.setCurrentText('Все')

        self.btn_search.clicked.connect(self.display_films)
        self.btn_add.clicked.connect(self.show_form)
        self.display_films()

    def display_films(self):
        name = self.name_search.text()
        genre = self.combo_genres.currentText()
        films = self.db.filter_films(name, genre)

        self.name_search.clear()
        self.films_list.clear()
        self.films_list.scrollToTop()
        for f in films:
            genre = f[3] - 1
            if 11 < f[3] < 15:
                genre -= 1
            elif f[3] >= 15:
                genre -= 2
            item = f"'{f[1]}'\nГод: {f[2]}\nЖанр: {self.db.genre_lookup[genre]}\nВремя просмотра: {f[4]}м"
            self.films_list.addItem(item)

    def show_form(self):
        self.prompt.show()