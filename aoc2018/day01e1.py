from aoc2018 import readlines


def exercise(lines):
    return sum(map(int, lines))


if __name__ == '__main__':
    print(exercise(readlines()))
