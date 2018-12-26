from collections import namedtuple, Counter, defaultdict
import re
from aoc2018 import readlines
from aoc2018.day23e1 import LINE_REGEX, Cords as C, Nanobot as N


class Cords(C):
    def add(self, other):
        return Cords(self.x + other.x, self.y + other.y, self.z + other.z)


def dummy(cords):
    return Nanobot(cords, 0)


class Nanobot(N):
    def intersects(self, other):
        """
        >>> Nanobot(Cords(0, 0, 0), 3).intersects(Nanobot(Cords(4, 0, 0), 1))
        True
        >>> Nanobot(Cords(0, 0, 0), 3).intersects(Nanobot(Cords(0, 4, 0), 1))
        True
        >>> Nanobot(Cords(0, 0, 0), 3).intersects(Nanobot(Cords(0, 0, 4), 1))
        True
        >>> Nanobot(Cords(0, 0, 0), 1).intersects(Nanobot(Cords(3, 0, 0), 1))
        False
        >>> Nanobot(Cords(0, 0, 0), 1).intersects(Nanobot(Cords(1, 0, 0), 0))
        True
        """
        distance = self.cords.distance(other.cords)
        return self.radius + other.radius >= distance

    @property
    def corners(self):
        """
        >>> Nanobot(Cords(0, 0, 0), 3).corners
        ((Cords(x=-3, y=0, z=0), Cords(x=3, y=0, z=0)), (Cords(x=0, y=-3, z=0), Cords(x=0, y=3, z=0)), (Cords(x=0, y=0, z=-3), Cords(x=0, y=0, z=3)))
        """
        return (
            (
                self.cords.add(Cords(-self.radius, 0, 0)),
                self.cords.add(Cords(self.radius, 0, 0))
            ),
            (
                self.cords.add(Cords(0, -self.radius, 0)),
                self.cords.add(Cords(0, self.radius, 0))
            ),
            (
                self.cords.add(Cords(0, 0, -self.radius)),
                self.cords.add(Cords(0, 0, self.radius))
            )
        )


class Cuboid:
    def __init__(self, nanobots):
        self.nanobots = nanobots
        self._find_corners()

    def _build_shrinking_points(self, axis_index):
        shrinking_points = {}

        zero = Cords(0, 0, 0)

        for n in self.nanobots:
            axes = n.corners
            start, end = axes[axis_index]

            for c in [n.cords, start, end]:
                axis_value = c[axis_index]
                if axis_value not in shrinking_points:
                    shrinking_points[axis_value] = c
                elif zero.distance(c) < zero.distance(shrinking_points[axis_value]):
                    shrinking_points[axis_value] = c

        return sorted(shrinking_points.values(), key=lambda c: c[axis_index], reverse=True), sorted(shrinking_points.values(), key=lambda c: c[axis_index])

    def _find_corners(self):
        self._shrinking_points = tuple([self._build_shrinking_points(i) for i in range(3)])
        self._axes_ranges = {
            i: (self._shrinking_points[i][0].pop(), self._shrinking_points[i][1].pop()) for i in range(3)
        }

    def _how_many(self, axis_range, which_cord):
        left, right = axis_range
        in_range = 0
        for b in self.nanobots:
            bleft = which_cord(b) - b.radius
            bright = which_cord(b) + b.radius
            bot_range = (bleft, bright)
            r1, r2 = sorted([axis_range, bot_range])
            if r1[1] >= r2[0]:
                in_range += 1
        return in_range

    def shrink(self, axis_index):
        zero = Cords(0, 0, 0)

        meta = {0: 'x', 1: 'y', 2: 'z'}

        print(meta[axis_index])
        print([c[axis_index] for c in self._shrinking_points[axis_index][0]])
        print([c[axis_index] for c in self._shrinking_points[axis_index][1]])

        while self._shrinking_points[axis_index][0] and self._shrinking_points[axis_index][1]:
            current_min, current_max = self._axes_ranges[axis_index]

            print()
            print(current_min, current_max)
            how_many = self._how_many((current_min[axis_index], current_max[axis_index]), lambda b: b.cords[axis_index])
            print('>> %s in range <%d, %d>: %d' % (meta[axis_index], current_min[axis_index], current_max[axis_index], how_many))

            wannabe_left = self._shrinking_points[axis_index][0][-1]
            wannabe_right = self._shrinking_points[axis_index][1][-1]

            x = self._how_many((wannabe_left[axis_index], current_max[axis_index]), lambda b: b.cords[axis_index])
            y = self._how_many((current_min[axis_index], wannabe_right[axis_index]), lambda b: b.cords[axis_index])
            print('left after changing %d to %d: %d' % (current_min[axis_index], wannabe_left[axis_index], x))
            print('right after changing %d to %d: %d' % (current_max[axis_index], wannabe_right[axis_index], y))

            if x == y:
                d1 = wannabe_left.distance(zero)
                d2 = wannabe_right.distance(zero)
                if d1 == d2:
                    if wannabe_left == wannabe_right:
                        current_min = self._shrinking_points[axis_index][0].pop()
                    else:
                        raise Exception('!')
                if d1 < d2:
                    current_min = self._shrinking_points[axis_index][0].pop()
                else:
                    current_max = self._shrinking_points[axis_index][1].pop()
            if x > y:
                current_min = self._shrinking_points[axis_index][0].pop()
            else:
                current_max = self._shrinking_points[axis_index][1].pop()
            self._axes_ranges[axis_index] = (current_min, current_max)


        how_many = self._how_many((self._axes_ranges[axis_index][0][axis_index], self._axes_ranges[axis_index][1][axis_index]), lambda b: b.cords[axis_index])
        print('%s in range <%d, %d>: %d' % (meta[axis_index], self._axes_ranges[axis_index][0][axis_index], self._axes_ranges[axis_index][1][axis_index], how_many))


def clusters(bots, which_cord):
    """
    >>> clusters([Nanobot(Cords(-7, 0, 0), 3), Nanobot(Cords(-6, 0, 0), 5), Nanobot(Cords(-13, 0, 0), 1), Nanobot(Cords(0, 0, 0), 7), Nanobot(Cords(8, 0, 0), 1), Nanobot(Cords(13, 0, 0), 3)], lambda b: b.cords.x)
    {(-11, 9): [Nanobot(cords=Cords(x=-6, y=0, z=0), radius=5), Nanobot(cords=Cords(x=-7, y=0, z=0), radius=3), Nanobot(cords=Cords(x=0, y=0, z=0), radius=7), Nanobot(cords=Cords(x=8, y=0, z=0), radius=1)], (-14, -12): [Nanobot(cords=Cords(x=-13, y=0, z=0), radius=1)], (10, 16): [Nanobot(cords=Cords(x=13, y=0, z=0), radius=3)]}
    >>> clusters([Nanobot(Cords(0, 0, 0), 3), Nanobot(Cords(5, 0, 0), 1)], lambda b: b.cords.x)
    {(4, 6): [Nanobot(cords=Cords(x=5, y=0, z=0), radius=1)], (-3, 3): [Nanobot(cords=Cords(x=0, y=0, z=0), radius=3)]}
    """
    bots = sorted(bots, key=lambda b: which_cord(b) - b.radius, reverse=True)
    cluster_bots = []
    data = {}
    cluster_start = cluster_end = None

    while bots:
        bot = bots.pop()
        if cluster_start is None:
            cluster_start = which_cord(bot) - bot.radius
            cluster_end = which_cord(bot) + bot.radius
            cluster_bots.append(bot)
        elif cluster_end >= which_cord(bot) - bot.radius:
            cluster_end = which_cord(bot) + bot.radius
            cluster_bots.append(bot)
        else:
            data[(cluster_start, cluster_end)] = cluster_bots

            cluster_start = which_cord(bot) - bot.radius
            cluster_end = which_cord(bot) + bot.radius
            cluster_bots = [bot]

    data[(cluster_start, cluster_end)] = cluster_bots

    return data


def solve(lines):
    nanobots = parse(lines)
    cuboid = Cuboid(nanobots)
    cuboid.shrink(2)


def parse(lines):
    nanobots = []
    for l in lines:
        g = LINE_REGEX.match(l).groups()
        nanobots.append(Nanobot(Cords(*map(int, g[:3])), int(g[3])))
    return nanobots


lines = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    #print(solve(readlines()))
    print(solve(lines))
