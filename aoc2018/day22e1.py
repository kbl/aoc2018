from collections import namedtuple
from aoc2018 import readlines


ROCKY = 0
WET = 1
NARROW = 2


Region = namedtuple('Region', ['gi', 'erosion', 'type'])


MAGIC = 20183
TYPE = 3

class Maze:
    def __init__(self, depth, target):
        self.maze = {
            (0, 0): Region(0, depth % MAGIC, depth % TYPE),
            target: Region(0, depth % MAGIC, depth % TYPE),
        }
        self.depth = depth
        self.target = target
        self._precompute(self.target)

    def _precompute(self, target):
        tx, ty = target
        for y in range(ty + 1):
            for x in range(tx + 1):
                if (x, y) not in self.maze:
                    self.maze[(x, y)] = self._compute(x, y)

    def _compute(self, x, y):
        if x == 0:
            gi = y * 48271
            erosion = (gi + self.depth) % MAGIC
            return Region(gi, erosion, erosion % TYPE)
        if y == 0:
            gi = x * 16807
            erosion = (gi + self.depth) % MAGIC
            return Region(gi, erosion, erosion % TYPE)

        gi = self.maze[(x - 1, y)].erosion * self.maze[(x, y - 1)].erosion
        erosion = (gi + self.depth) % MAGIC
        return Region(gi, erosion, erosion % TYPE)

    def __str__(self):
        rep = ['.', '=', '|']

        rows = []
        for y in range(11):
            row = []
            for x in range(11):
                row.append(rep[self.maze[(x, y)].type])
            rows.append(''.join(row))
        return '\n'.join(rows)


def solve(m):
    return sum([r.type for r in m.maze.values()])
        

def parse(lines):
    depth = int(lines[0].split(' ')[1])
    target = tuple(map(int, lines[1].split(' ')[1].split(',')))
    return Maze(depth, target)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(parse(readlines())))

