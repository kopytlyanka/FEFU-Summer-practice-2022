import sqlite3


DB_NAME = 'films.db'


class DBConn:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.genres = dict(self.conn.execute('select title, id from genres').fetchall())
        self.genre_lookup = [k for k, _ in self.genres.items()]


    def filter_films(self, name: str=None, genre: str=None) -> list:
        query, has_where = 'select * from Films', False
        if genre and genre.lower() != 'все':
            query = f'{query} where genre={self.genres[genre]}'
            has_where = True

        if name:
            op = 'where'
            if has_where:
                op = 'and'
            has_where = True
            query = f"{query} {op} LOWER(title) like '%{name}%'"

        query += ' order by LOWER(title) asc'

        return self.conn.execute(query).fetchall()


    def add_film(self, film):
        self.conn.execute('insert into Films(title, year, genre, duration) values(?, ?, ?, ?)', film)
        self.conn.commit()