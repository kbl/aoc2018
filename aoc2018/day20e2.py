from aoc2018 import readlines
from aoc2018.day20e1 import Maze, Room


def solve(lines):
    start = Room(0, 0)
    path_lengths = Maze.parse(lines).shortest_paths(start).values()
    return len([p for p in path_lengths if p >= 1000])


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
