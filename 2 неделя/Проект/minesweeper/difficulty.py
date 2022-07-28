# Класс сложности ------------------------------------------------------------------------------------------------------
class Difficulty:
    ########################################
    # Инициализация
    def __init__(self, *args):
        difficulties = {
            'easy': {'rows': 8, 'columns': 8, 'mines': 10},
            'normal': {'rows': 16, 'columns': 16, 'mines': 40},
            'hard': {'rows': 16, 'columns': 30, 'mines': 99}
        }
        self.rows = None
        self.columns = None
        self.mines = None

        self.diff = None

        ########################################
        ## Если передана строка
        if all(map(lambda arg: type(arg) is str, args)):
            if len(args) > 1:
                raise Exception(f'there should be exactly 1 name, got {len(args)} instead')
            if args[0] in difficulties.keys():
                arg = args[0]
                self.diff = arg
                self.rows = difficulties[arg]['rows']
                self.columns = difficulties[arg]['columns']
                self.mines = difficulties[arg]['mines']
            else:
                arg = 'custom'
                args = args[0].replace('(', '').replace(')', '').split(', ')
                self.rows, self.columns, self.mines = tuple(map(int, args))
        ########################################
        ## Если переданы числа
        elif all(map(lambda arg: type(arg) is int, args)):
            if len(args) != 3:
                raise Exception(f'there should be exactly 3 values: rows: int, columns: int and mines: int, got {len(args)} instead')
            self.rows = args[0]
            self.columns = args[1]
            self.mines = args[2]

        ########################################
        ## В случае некорректного ввода
        else:
            raise SyntaxError

        ########################################
    ########################################
    def __repr__(self):
        return f'{self.rows}, {self.columns}, {self.mines}'
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass