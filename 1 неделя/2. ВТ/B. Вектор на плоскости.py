class MyVector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __add__(self, other):
        return MyVector(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __sub__(self, other):
        return MyVector(self.x - other.x, self.y - other.y)
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    def __mul__(self, n: (int, float)):
        return MyVector(self.x * n, self.y * n)
    def __rmul__(self, n: (int, float)):
        return MyVector(self.x * n, self.y * n)
    def __imul__(self, n: (int, float)):
        self.x *= n
        self.y *= n
        return self
    def __repr__(self):
        return f'MyVector({self.x}, {self.y})'
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    def __abs__(self):
        from math import sqrt
        return sqrt(self.x**2 + self.y**2)


if __name__ == '__main__':
    v1 = MyVector()
    v2 = MyVector()