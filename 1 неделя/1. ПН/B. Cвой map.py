def python_map(function, *collections):
    answer = []
    collection = list(eval(f'zip{collections}'))
    for element in collection:
        answer.append(eval(f'function{element}'))
    return answer

if __name__ == '__main__':
    print(python_map(lambda x, y: bin(x+y), [0, 5], [1, 1]))