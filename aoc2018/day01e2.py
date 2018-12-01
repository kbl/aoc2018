from aoc2018 import readlines


def exercise(lines):
    elements = list(map(int, lines))
    index = 0
    value = 0
    seen = set()

    while True:
        value += elements[index]
        if value in seen:
            return value
        seen.add(value)
        index = (index + 1) % len(elements)


if __name__ == '__main__':
    print(exercise(readlines()))
