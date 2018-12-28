from collections import namedtuple, Counter, defaultdict
import re
from aoc2018 import readlines
from aoc2018.day23e1 import LINE_REGEX, Cords as C, Nanobot as N


class Cords(C):
    def add(self, other):
        return Cords(self.x + other.x, self.y + other.y, self.z + other.z)


class Range(namedtuple('metaange', ['min', 'max'])):
    def intersects(self, other):
        """
        >>> Range(0, 3).intersects(Range(1, 2))
        True
        >>> Range(0, 3).intersects(Range(1, 4))
        True
        >>> Range(0, 3).intersects(Range(-1, 2))
        True
        >>> Range(0, 3).intersects(Range(-1, 4))
        True
        >>> Range(0, 3).intersects(Range(3, 4))
        True
        >>> Range(0, 3).intersects(Range(-3, 0))
        True
        >>> Range(0, 3).intersects(Range(-3, -1))
        False
        >>> Range(0, 3).intersects(Range(4, 5))
        False
        """
        a, b = sorted([self, other])
        return a.max >= b.min

    def partition(self):
        """
        >>> Range(0, 10).partition()
        (Range(min=0, max=5), Range(min=6, max=10))
        >>> Range(0, 9).partition()
        (Range(min=0, max=4), Range(min=5, max=9))
        >>> Range(-10, 10).partition()
        (Range(min=-10, max=0), Range(min=1, max=10))
        >>> Range(-10, -4).partition()
        (Range(min=-10, max=-7), Range(min=-6, max=-4))
        >>> Range(0, 2).partition()
        (Range(min=0, max=1), Range(min=2, max=2))
        >>> Range(0, 1).partition()
        (Range(min=0, max=0), Range(min=1, max=1))
        >>> Range(0, 0).partition()
        (Range(min=0, max=0),)
        """
        if self.size == 1:
            return (self, )

        half = abs(self.max - self.min) // 2
        return Range(self.min, self.min + half), Range(self.min + half + 1, self.max)

    def merge(self, other):
        """
        >>> Range(0, 5).merge(Range(7, 15))
        Range(min=0, max=15)
        """
        return Range(min(self.min, other.min), max(self.max, other.max))

    def contains(self, value):
        return self.min <= value and self.max >= value

    @property
    def size(self):
        """
        >>> Range(-10, 10).size
        21
        """
        return abs(self.max - self.min) + 1


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
    def ranges(self):
        """
        >>> Nanobot(Cords(0, 1, 2), 3).ranges
        (Range(min=-3, max=3), Range(min=-2, max=4), Range(min=-1, max=5))
        """
        return (
            Range(self.cords.x - self.radius, self.cords.x + self.radius),
            Range(self.cords.y - self.radius, self.cords.y + self.radius),
            Range(self.cords.z - self.radius, self.cords.z + self.radius),
        )
        
    @property
    def corners(self):
        """
        >>> Nanobot(Cords(0, 0, 0), 3).corners
        [Cords(x=-3, y=0, z=0), Cords(x=3, y=0, z=0), Cords(x=0, y=-3, z=0), Cords(x=0, y=3, z=0), Cords(x=0, y=0, z=-3), Cords(x=0, y=0, z=3)]
        """
        return [
            self.cords.add(Cords(-self.radius, 0, 0)),
            self.cords.add(Cords(self.radius, 0, 0)),
            self.cords.add(Cords(0, -self.radius, 0)),
            self.cords.add(Cords(0, self.radius, 0)),
            self.cords.add(Cords(0, 0, -self.radius)),
            self.cords.add(Cords(0, 0, self.radius))
        ]


class Cuboid:
    def __init__(self, range_x, range_y, range_z):
        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z

    @property
    def size(self):
        return self.range_x.size * self.range_y.size * self.range_z.size

    @property
    def ranges(self):
        return (self.range_x, self.range_y, self.range_z)

    @property
    def corners(self):
        corners = []
        for x in self.range_x:
            for y in self.range_y:
                for z in self.range_z:
                    corners.append(Cords(x, y, z))
        return corners
                    
    @property
    def distance(self):
        zero = Cords(0, 0, 0)
        return min([zero.distance(c) for c in self.corners])

    def __repr__(self):
        return "Cuboid(%r, %r, %r)" % (self.range_x, self.range_y, self.range_z)

    def has_in_range(self, nanobot):
        """
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(0, 0, 0), 3))
        True
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(0, 0, 0), 13))
        True
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(0, 0, 0), 1))
        True
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(7, 0, 0), 7))
        True
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(7, 0, 0), 7))
        True
        >>> Cuboid(Range(-4, 4), Range(-4, 4), Range(-4, 4)).has_in_range(Nanobot(Cords(12, 12, 12), 7))
        False
        """
        for c in self.corners:
            if nanobot.has_in_range(c):
                return True

        for c in nanobot.corners:
            if self.range_x.contains(c.x) and self.range_y.contains(c.y) and self.range_z.contains(c.z):
                return True

        return False

    def how_many_in_range(self, nanobots):
        """
        # >>> Cuboid(Range(49401928, 49401928), Range(12058903, 12058903), Range(41374452, 41374452)).how_many_in_range([Nanobot(Cords(65950023, 59587453, 53524633), 62514381), Nanobot(Cords(94076556, 13944972, 66655558), 65325923)])
        # 0
        """
        return sum([1 for n in nanobots if self.has_in_range(n)])

    def partition(self):
        """
        >>> list(Cuboid(Range(0, 4), Range(2, 6), Range(4, 8)).partition())
        [Cuboid(Range(min=0, max=2), Range(min=2, max=4), Range(min=4, max=6)), Cuboid(Range(min=0, max=2), Range(min=2, max=4), Range(min=7, max=8)), Cuboid(Range(min=0, max=2), Range(min=5, max=6), Range(min=4, max=6)), Cuboid(Range(min=0, max=2), Range(min=5, max=6), Range(min=7, max=8)), Cuboid(Range(min=3, max=4), Range(min=2, max=4), Range(min=4, max=6)), Cuboid(Range(min=3, max=4), Range(min=2, max=4), Range(min=7, max=8)), Cuboid(Range(min=3, max=4), Range(min=5, max=6), Range(min=4, max=6)), Cuboid(Range(min=3, max=4), Range(min=5, max=6), Range(min=7, max=8))]
        """
        for x in self.range_x.partition():
            for y in self.range_y.partition():
                for z in self.range_z.partition():
                    yield Cuboid(x, y, z)


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

    range_x = range_y = range_z = Range(0, 0)

    for n in nanobots:
        rx, ry, rz = n.ranges
        range_x = rx.merge(range_x)
        range_y = ry.merge(range_y)
        range_z = ry.merge(range_z)


    c = Cuboid(range_x, range_y, range_z)
    queue = [(1000, c.size, c.distance, c)]

    while queue:
        how_many, size, distance, c = queue.pop()
        if size == 1:
            return distance
        
        for new_c in c.partition():
            how_many = new_c.how_many_in_range(nanobots)
            queue.append((how_many, new_c.size, new_c.distance, new_c))

        queue = sorted(queue, key=lambda x: (x[0], -x[1], -x[2]))


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
    print(solve(readlines()))
