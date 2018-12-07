from aoc2018 import readlines
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])


def parse(lines):
    points = []

    max_x = 0
    max_y = 0

    for line in lines:
        [x, y] = map(int, line.split(', '))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        points.append(Point(x, y))

    return points, max_x, max_y


def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def check(starting_point, all_points):
    points_to_check = set((starting_point, ))
    checked = set((starting_point, ))
    size = 0

    while points_to_check:
        point = points_to_check.pop()
        checked.add(point)

        distances = set()
        for other_point in all_points:
            if other_point == starting_point:
                continue
            distances.add(distance(point, other_point))

        d = distance(point, starting_point)
        if d >= min(distances):
            continue

        if point.x == 0 or point.y == 0 or point.x == max_x or point.y == max_y:
            return -1

        size += 1

        p = Point(point.x - 1, point.y)
        if p not in checked:
            points_to_check.add(p)

        p = Point(point.x, point.y + 1)
        if p not in checked:
            points_to_check.add(p)

        p = Point(point.x + 1, point.y)
        if p not in checked:
            points_to_check.add(p)

        p = Point(point.x, point.y - 1)
        if p not in checked:
            points_to_check.add(p)

    return size

if __name__ == '__main__':
    lines = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split('\n')
    points, max_x, max_y = parse(readlines())
    result = []
    for p in points:
        result.append((check(p, points), p))

    print("\n".join(map(str, reversed(sorted(result)))))

