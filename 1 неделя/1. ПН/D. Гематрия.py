def read_to(self: list) -> None:
    while True:
        try:
            word = input()
            if word == '':
                raise EOFError
            self.append(word)
        except EOFError:
            break

def gematria(word: str) -> int:
    return sum(map(lambda x: ord(x)-ord('A')+1, word.upper()))

if __name__ == '__main__':
    dictionary = list()
    read_to(dictionary)
    dictionary.sort(key=gematria)
    print(dictionary)