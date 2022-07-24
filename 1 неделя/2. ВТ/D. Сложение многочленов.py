class Polynomial:
    def __init__(self, coefficients=None):
        if coefficients is None:
            coefficients = list()
        self.coefficients = coefficients.copy()
    def __add__(self, other):
        from itertools import zip_longest
        return Polynomial([
            x + y for x, y in zip_longest(
                self.coefficients, other.coefficients, fillvalue=0
            )
        ])
    def __call__(self, x: (int, float)):
        return sum(map(lambda a, i: a * x ** i,
                       self.coefficients, range(len(self.coefficients))))


if __name__ == '__main__':
    poly1 = Polynomial()
    poly2 = Polynomial()