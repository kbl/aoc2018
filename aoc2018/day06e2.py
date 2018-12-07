from aoc2018 import readlines
from collections import namedtuple
from aoc2018.day06e1 import parse, Point, distance


def check(starting_point, all_points, allowed_distance):
    points_to_check = set((starting_point, ))
    checked = set((starting_point, ))
    size = 0

    while points_to_check:
        point = points_to_check.pop()
        checked.add(point)

        sum_distance = sum([distance(point, p) for p in all_points])
        if sum_distance >= allowed_distance:
            continue

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
    print(check(Point(int(max_x / 2), int(max_y / 2)), points, 10000))

