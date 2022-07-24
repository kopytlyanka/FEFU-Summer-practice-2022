if __name__ == '__main__':
    method_name = {
        'read': 'R',
        'write': 'W',
        'execute': 'X'
    }
    database = dict()
    answer = list()
    for _ in range(int(input())):
        file = input().split()
        database[file[0]] = tuple(file[i] for i in range(1, len(file)))
    for _ in range(int(input())):
        request, file = tuple(input().split())
        if method_name[request] in database[file]:
            answer.append('OK')
        else:
            answer.append('Access denied')
    print(*answer, sep='\n', end='')