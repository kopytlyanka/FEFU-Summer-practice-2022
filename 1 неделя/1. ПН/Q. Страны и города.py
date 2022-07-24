if __name__ == '__main__':
    database = dict()
    answer = list()
    for _ in range(int(input())):
        country = input().split()
        for i in range(1, len(country)):
            database[country[i]] = country[0]
    for _ in range(int(input())):
        answer.append(database[input()])
    print(*answer, sep='\n', end='')