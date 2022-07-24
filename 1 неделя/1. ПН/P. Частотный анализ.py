if __name__ == '__main__':
    from sys import stdin
    text = dict()
    while True:
        line = stdin.readline().replace('\n', '')
        if line == '':
            break
        for word in line.split():
            if word not in text.keys():
                text[word] = 1
            text[word] += 1
    answer = sorted(
            text.items(),
            key=lambda item: (-item[1], item[0])
    )
    print(*map(lambda x: x[0], answer), sep='\n', end='')