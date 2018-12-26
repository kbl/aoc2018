from collections import namedtuple
import re
from aoc2018 import readlines


LINE_REGEX = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')


class Nanobot(namedtuple('metaanobot', ['cords', 'radius'])):
    def hasinrange(self, other):
        return self.cords.distance(other.cords) <= self.radius


class Cords(namedtuple('metacords', ['x', 'y', 'z'])):
    def distance(self, other):
        """
        >>> Cords(0, 0, 0).distance(Cords(1, 2, 3))
        6
        >>> Cords(0, 0, 1).distance(Cords(0, 0, -1))
        2
        >>> Cords(0, 0, -1).distance(Cords(0, 0, 1))
        2
        """
        d = 0
        for c1, c2 in zip(self, other):
            d += abs(c1 - c2)
        return d


def parse(lines):
    nanobots = []
    for l in lines:
        g = LINE_REGEX.match(l).groups()
        nanobots.append(Nanobot(Cords(*map(int, g[:3])), int(g[3])))
    return nanobots


def solve(lines):
    nanobots = parse(lines)
    biggest = sorted(nanobots, key=lambda n: n.radius)[-1]
    in_range = 0

    return len([n for n in nanobots if biggest.hasinrange(n)])


lines = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
