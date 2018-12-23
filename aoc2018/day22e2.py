from collections import namedtuple
from aoc2018 import readlines
from aoc2018.day22e1 import Maze as M


ROCKY = 0
WET = 1
NARROW = 2


Region = namedtuple('Region', ['gi', 'erosion', 'type'])


MAGIC = 20183
TYPE = 3

CLIMBING_GEAR = 0
TORCH = 1
NEITHER = 2

MOVE_TIME = 1
SWITCH_TIME = 7

ALLOWED_EQUIPMENT = {
    ROCKY: [CLIMBING_GEAR, TORCH],
    WET: [CLIMBING_GEAR, NEITHER],
    NARROW: [TORCH, NEITHER],
}


def move_time(times_from, allowed_to, switch_to):
    """
    >>> move_time([0, 1, None], [TORCH, NEITHER], TORCH)
    2
    >>> move_time([0, 1, None], [TORCH, NEITHER], NEITHER)
    9
    """
    if times_from[switch_to] is not None:
        return times_from[switch_to] + MOVE_TIME
    [allowed] = [e for e in allowed_to if times_from[e] is not None]
    return times_from[allowed] + MOVE_TIME + SWITCH_TIME


class Maze(M):
    def __init__(self, depth, target):
        super(Maze, self).__init__(depth, target)
        x, y = target
        # instaead of precomputing stuff I could have implemented 
        # logic that checks if it's worth going further outside of map boundaries
        # 
        # It's worth exploring if path to target without any gear switching
        # is shorther than current one.
        self._precompute((x * 4, y + 100))

    def shortest_path(self, target):
        required_time = {
            (0, 0): [SWITCH_TIME, 0, None]
        }

        positions = set([(0, 0)])

        while positions:
            new_positions = set()

            for cords in positions:
                x, y = cords
                current_time = required_time[cords]

                for mx, my in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx = x + mx
                    ny = y + my
                    new_cords = (nx, ny)
                    if nx < 0 or ny < 0 or new_cords not in self.maze:
                        continue

                    new_cords_equipment = ALLOWED_EQUIPMENT[self.maze[new_cords].type]
                    if new_cords not in required_time:
                        new_time = [None, None, None]
                        for e in new_cords_equipment:
                            new_time[e] = move_time(current_time, new_cords_equipment, e)
                        required_time[new_cords] = new_time
                        new_positions.add(new_cords)
                    else:
                        changed = False
                        old_time = required_time[new_cords]

                        for e in new_cords_equipment:
                            min_time = move_time(current_time, new_cords_equipment, e)

                            if old_time[e] > min_time:
                                old_time[e] = min_time
                                changed = True
                        if changed:
                            new_positions.add(new_cords)
            positions = new_positions

        return required_time[target][TORCH]


def solve(m):
    return m.shortest_path(m.target)


def parse(lines):
    depth = int(lines[0].split(' ')[1])
    target = tuple(map(int, lines[1].split(' ')[1].split(',')))
    return Maze(depth, target)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(parse(readlines())))

