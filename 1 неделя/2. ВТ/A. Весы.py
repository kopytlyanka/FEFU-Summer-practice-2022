class Balance:
    def __init__(self, l=0, r=0):
        self.left_scale = l
        self.right_scale = r
    def add_left(self, cargo):
        self.left_scale += cargo
    def add_right(self, cargo):
        self.right_scale += cargo
    def result(self) -> str:
        if self.left_scale > self.right_scale:
            return 'L'
        elif self.right_scale > self.left_scale:
            return 'R'
        return '='

if __name__ == '__main__':
    balance = Balance()