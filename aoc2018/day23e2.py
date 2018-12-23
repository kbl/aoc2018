from collections import namedtuple, Counter, defaultdict
import re
from aoc2018 import readlines
from aoc2018.day23e1 import LINE_REGEX, Cords, Nanobot as N


def parse(lines):
    nanobots = []
    for l in lines:
        g = LINE_REGEX.match(l).groups()
        nanobots.append(Nanobot(Cords(*map(int, g[:3])), int(g[3])))
    return nanobots



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
        """
        distance = self.cords.distance(other.cords)
        return self.radius + other.radius >= distance


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
    (minx, maxx), (miny, maxy), (minz, maxz) = _findminmax(nanobots)

    print(minx, maxx)
    for c, b in clusters(nanobots, lambda b: b.cords.z).items():
        print(c, len(b))
    for c, b in clusters(nanobots, lambda b: b.cords.y).items():
        print(c, len(b))
    for c, b in clusters(nanobots, lambda b: b.cords.x).items():
        print(c, len(b))

    bots = set(nanobots)
    to_check = list(nanobots)

    intersections = defaultdict(list)

    while to_check:
        being_checked = to_check.pop()
        how_many = len([b for b in bots if b != being_checked and being_checked.intersects(b)])
        intersections[how_many].append(being_checked)

    the_most_intersections = max(intersections.keys())
    print(the_most_intersections)
    print(intersections[the_most_intersections])

    return 0


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
    #print(solve(lines))
