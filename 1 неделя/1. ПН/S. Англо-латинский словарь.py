if __name__ == '__main__':
    from collections import defaultdict
    dictionary = defaultdict(list)
    for _ in range(int(input())):
        translation = input().replace(' - ', ' ').replace(', ', ' ').split()
        for i in range(1, len(translation)):
            dictionary[translation[i]].append(translation[0])
    print(len(dictionary.keys()))
    answer = sorted(dictionary.keys())
    for word in answer:
        print(word, '-', end=' ')
        print(*sorted(dictionary[word]), sep=', ')