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


# class Cuboid(namedtuple('metacuboid', ['left', 'right'])):
#     def intersects(self, nanobot):
#         """
#         >>> Cuboid(Cords(-3, -3, -3), Cords(3, 3, 3)).intersects(Nanobot(Cords(0, 0, 0), 2))
#         True
#         >>> Cuboid(Cords(-3, -3, -3), Cords(3, 3, 3)).intersects(Nanobot(Cords(-4, -4, -4), 20))
#         True
# 
#         """
#         nx, ny, nz = nanobot.cords
#         nr = nanobot.radius
#         # center inside
#         if (nx >= self.left.x and nx <= self.right.x and
#             ny >= self.left.y and ny <= self.right.y and
#             nz >= self.left.z and nz <= self.right.z):
#             return True
# 
#         nz + nr
# 
#         return False


def how_many(bots, axis_range, which_cord):
    left, right = axis_range
    in_range = 0
    for b in bots:
        bleft = which_cord(b) - b.radius
        bright = which_cord(b) + b.radius
        bot_range = (bleft, bright)
        r1, r2 = sorted([axis_range, bot_range])
        if r1[1] >= r2[0]:
            in_range += 1
    return in_range


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


def _findminmax(nanobots):
    minx = maxx = None
    miny = maxy = None
    minz = maxz = None
    for n in nanobots:
        if minx is None or minx > n.cords.x - n.radius:
            minx = n.cords.x - n.radius
        if miny is None or miny > n.cords.y - n.radius:
            miny = n.cords.y - n.radius
        if minz is None or minz > n.cords.z - n.radius:
            minz = n.cords.z - n.radius

        if maxx is None or maxx < n.cords.x + n.radius:
            maxx = n.cords.x + n.radius
        if maxy is None or maxy < n.cords.y + n.radius:
            maxy = n.cords.y + n.radius
        if maxz is None or maxz < n.cords.z + n.radius:
            maxz = n.cords.z + n.radius

    return (minx, maxx), (miny, maxy), (minz, maxz)


def solve(lines):
    nanobots = parse(lines)

    xminus = []
    xplus = []

    yminus = []
    yplus = []

    zminus = []
    zplus = []

    for n in nanobots:
        xaxis, yaxis, zaxis = n.corners
        xminus.append(xaxis[1])
        xplus.append(xaxis[0])

        yminus.append(yaxis[1])
        yplus.append(yaxis[0])

        zminus.append(zaxis[1])
        zplus.append(zaxis[0])

    xminus = sorted(xminus, reverse=True)
    xmplus = sorted(xplus)

    yminus = sorted(yminus, reverse=True)
    ymplus = sorted(yplus)

    zminus = sorted(zminus, reverse=True)
    zmplus = sorted(zplus)

    zero = Cords(0, 0, 0)

    leftovers = set(nanobots)

    minx = xminus.pop()
    maxx = xplus.pop()

    miny = yminus.pop()
    maxy = yplus.pop()

    minz = zminus.pop()
    maxz = zplus.pop()

    print(how_many(nanobots, (minx.x, maxx.x), lambda b: b.cords.x))

    while xminus and xplus:
        x = how_many(nanobots, (xminus[-1].x, maxx.x), lambda b: b.cords.x)
        y = how_many(nanobots, (minx.x, xplus[-1].x), lambda b: b.cords.x)

        if x == y:
            d1 = xminus[-1].distance(zero)
            d2 = xplus[-1].distance(zero)
            if d1 == d2:
                raise Exception('!')
            if d1 < d2:
                minx = xminus.pop()
            else:
                maxx = xplus.pop()
        if x > y:
            minx = xminus.pop()
        else:
            maxx = xplus.pop()

    while yminus and yplus:
        x = how_many(nanobots, (yminus[-1].y, maxy.y), lambda b: b.cords.y)
        y = how_many(nanobots, (miny.y, yplus[-1].y), lambda b: b.cords.y)

        if x == y:
            d1 = yminus[-1].distance(zero)
            d2 = yplus[-1].distance(zero)
            if d1 == d2:
                raise Exception('!')
            if d1 < d2:
                miny = yminus.pop()
            else:
                maxy = yplus.pop()
        if x > y:
            miny = yminus.pop()
        else:
            maxy = yplus.pop()

    print(1)

    while zminus and zplus:
        print(2)
        x = how_many(nanobots, (zminus[-1].z, maxz.z), lambda b: b.cords.z)
        y = how_many(nanobots, (minz.z, zplus[-1].z), lambda b: b.cords.z)

        if x == y:
            d1 = zminus[-1].distance(zero)
            d2 = zplus[-1].distance(zero)
            if d1 == d2:
                raise Exception('!')
            if d1 < d2:
                minz = zminus.pop()
            else:
                maxz = zplus.pop()
        if x > y:
            minz = zminus.pop()
        else:
            maxz = zplus.pop()

    print(minx, maxx)
    print(miny, maxy)
    print(minz, maxz)


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
