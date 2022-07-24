if __name__ == '__main__':
    height, weight, count = map(int, input().split())
    field = [
        [0 for _ in range(weight)]
        for _ in range(height)
    ]
    for _ in range(count):
        h, w = map(lambda x: int(x) - 1, input().split())
        field[h][w] = '*'
        for i in range(h - 1, h + 2):
            for j in range(w - 1, w + 2):
                if all((
                        i >= 0, i < height,
                        j >= 0, j < weight,
                )) and type(field[i][j]) is int:
                    field[i][j] += 1
    print(*map(
            lambda row: ' '.join(map(str, row)),
            field
        ), sep='\n', end=''
    )