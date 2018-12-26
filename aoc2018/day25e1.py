from collections import namedtuple
from aoc2018 import readlines


class Cords(namedtuple('metacords', ['x', 'y', 'z', 't'])):
    def distance(self, other):
        return (
            abs(self.x - other.x) +
            abs(self.y - other.y) +
            abs(self.z - other.z) +
            abs(self.t - other.t)
        )


def parse(lines):
    cords = []
    for l in lines:
        cords.append(Cords(*[int(e) for e in l.split(',')]))
    return cords


def solve(lines):
    """
    >>> solve([])
    1
    """
    cords = parse(lines)

    current_cid = 0

    constellations = {}
    for c in cords:
        valid_constellations = []
        for cid, constellation in constellations.items():
            for constellation_point in constellation:
                if c.distance(constellation_point) <= 3:
                    valid_constellations.append(cid)
                    break
        if len(valid_constellations) > 1:
            cid = valid_constellations[0]
            constellations[cid].append(c)
            for cid_to_merge in valid_constellations[1:]:
                constellations[cid].extend(constellations[cid_to_merge])
                del constellations[cid_to_merge]
        elif len(valid_constellations) == 1:
            [cid] = valid_constellations
            constellations[cid].append(c)
        else:
            constellations[current_cid] = [c]
            current_cid += 1

    return len(constellations)


# 4
lines1 = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""".split('\n')


# 3
lines2 = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""".split('\n')


# 8
lines3 = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
    # print(solve(lines3))
