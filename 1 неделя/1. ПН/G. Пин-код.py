def check_pin(pinCode: str) -> str:
    from math import sqrt, floor, log2

    def is_prime(num: int) -> bool:
        for d in range(2, floor(sqrt(num) + 1)):
            if num % 2 == 0:
                return False
        return True

    pinCode = pinCode.split('-')
    if all((
            is_prime(int(pinCode[0])),
            pinCode[1] == pinCode[1][::-1],
            log2(int(pinCode[2])) == int(log2(int(pinCode[2])))
    )):
        return 'Корректен'
    return 'Некорректен'

if __name__ == '__main__':
    print(check_pin('7-101-4'))