import sys
from aoc2018 import readlines
from collections import deque


class Grid:
    GRID_SIZE = 300

    def __init__(self, serial):
        self.serial = serial
        self._init_grid()

    def _init_grid(self):
        self.grid = []
        for y in range(self.GRID_SIZE):
            line = [self._power(x + 1, y + 1) for x in range(self.GRID_SIZE)]
            self.grid.append(line)

    def _power(self, x, y):
        rack_id = (x + 10)
        power_level = rack_id * (rack_id * y + self.serial)
        power_level = (power_level % 1000) // 100 - 5
        return power_level

    def max_power_sum(self, square_size=3):
        partial_sums = []

        for y in range(self.GRID_SIZE):
            power_sum = deque(maxlen=square_size)
            line = []
            for x in range(self.GRID_SIZE):
                power_sum.append(self.grid[y][x])
                if len(power_sum) == square_size:
                    line.append(sum(power_sum))
            partial_sums.append(line)

        sums = [[] for _ in range(self.GRID_SIZE - square_size + 1)]
        for x in range(self.GRID_SIZE - square_size + 1):
            power_sum = deque(maxlen=square_size)
            for y in range(self.GRID_SIZE):
                power_sum.append(partial_sums[y][x])
                if len(power_sum) == square_size:
                    sums[y - square_size + 1].append(sum(power_sum))

        max_sum = -(2**32 - 1)
        max_x = 0
        max_y = 0
        for y, line in enumerate(sums):
            for x, value in enumerate(line):
                if value > max_sum:
                    max_sum = value
                    max_x = x + 1
                    max_y = y + 1

        return (max_sum, (max_x, max_y))

    def __str__(self):
        return Grid.str_matrix(self.grid)

    @staticmethod
    def str_matrix(matrix):
        matrix_str = []
        for line in matrix:
            line_str = []
            for element in line:
                line_str.append('%2d' % element)
            matrix_str.append(' '.join(line_str))

        return '\n'.join(matrix_str)


if __name__ == '__main__':
    serial = int(list(readlines())[0])
    g = Grid(serial)
    (_, (x, y)) = g.max_power_sum()
    print('%d,%d' % (x, y))
