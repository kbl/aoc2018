from collections import deque
from aoc2018 import readlines


def solve(searched_sequence):
    """
    >>> solve("01245")
    5
    >>> solve("51589")
    9
    >>> solve("59414")
    2018
    >>> solve("92510")
    18
    """
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    searched_sequence = deque([int(c) for c in searched_sequence])
    last_recipes = deque(maxlen=len(searched_sequence))

    while True:
        s = recipes[elf1] + recipes[elf2]
        for c in str(s):
            recipes.append(int(c))
            last_recipes.append(int(c))
            if searched_sequence == last_recipes:
                return len(recipes) - len(last_recipes)

        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


if __name__ == '__main__':
    # import doctest
    # print(doctest.testmod())

    print(solve(list(readlines())[0]))
