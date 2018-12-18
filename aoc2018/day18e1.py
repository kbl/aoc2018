from collections import defaultdict
from aoc2018 import readlines


lines = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".split('\n')


EMPTY = '.'
TREE = '|'
LUMBERYARD = '#'


def _adjacent(x, y):
    return [(x - 1, y),
            (x - 1, y - 1),
            (x    , y - 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x    , y + 1),
            (x - 1, y + 1)]


def _adjacent_types(data, cords, serched_type):
    return len([1 for a in _adjacent(*cords) if data.get(a) == serched_type])


def parse(lines):
    representation = {}
    for y, row in enumerate(lines):
        if row.strip():
            for x, element in enumerate(row.strip()):
                representation[(x, y)] = element
    return representation


def evolve(data, cords, item):
    tree_count = _adjacent_types(data, cords, TREE)
    lumber_count = _adjacent_types(data, cords, LUMBERYARD)

    if item == EMPTY:
        if tree_count >= 3:
            return TREE
        return EMPTY

    if item == TREE:
        if lumber_count >= 3:
            return LUMBERYARD
        return TREE

    if lumber_count > 0 and tree_count > 0:
        return LUMBERYARD

    return EMPTY


def count(data, item):
    return len([1 for v in data.values() if v == item])


def solve(lines):
    data = parse(lines)

    for i in range(10):
        data = {cords: evolve(data, cords, item) for cords, item in data.items()}

    return count(data, TREE) * count(data, LUMBERYARD)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
