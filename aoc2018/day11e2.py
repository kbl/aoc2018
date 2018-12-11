from aoc2018 import readlines
from aoc2018.day11e1 import Grid


if __name__ == '__main__':
    serial = int(list(readlines())[0])
    g = Grid(serial)
    sums = []
    for i in range(1, 301):
        sums.append((g.max_power_sum(i), i))

    sums = sorted(sums, reverse=True)
    ((_, (x, y)), i) = sums[0]
    print('%d,%d,%d' % (x, y, i))
