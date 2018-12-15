from aoc2018 import readlines


def solve(recipes_no):
    """
    >>> solve(9)
    '5158916779'
    >>> solve(5)
    '0124515891'
    >>> solve(18)
    '9251071085'
    >>> solve(2018)
    '5941429882'
    """
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    next_recipes = 10

    while len(recipes) < recipes_no + next_recipes:
        s = recipes[elf1] + recipes[elf2]
        for c in str(s):
            recipes.append(int(c))

        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

    return ''.join(map(str, recipes[recipes_no:recipes_no + next_recipes]))


if __name__ == '__main__':
    # import doctest
    # print(doctest.testmod())

    print(solve(int(list(readlines())[0])))
