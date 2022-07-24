if __name__ == '__main__':
    nums = [n for n in range(10, 100)]
    print(sum(map(
                lambda n: (n ** 2),
                filter(
                    lambda n: (n % 9 != 0),
                    nums
                )
            )))