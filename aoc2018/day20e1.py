from collections import namedtuple
from aoc2018 import readlines


directions = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}


Room = namedtuple('Room', ['x', 'y'])


class Maze:
    def __init__(self, rooms=None, doors=None):
        self.rooms = rooms or set()
        self.doors = doors or set()

    @staticmethod
    def parse(lines):
        [line] = lines
        instructions = line[1:-1]

        start = Room(0, 0)
        rooms = set([start])
        maze = Maze(rooms)
        maze._trace(start, list(instructions))
        return maze

    def _trace(self, starting_position, instructions):
        """
        >>> Maze()._trace(Room(0, 0), list('NE'))
        [Room(x=1, y=1)]
        >>> Maze()._trace(Room(0, 0), list('NE(N|S|)'))
        [Room(x=1, y=1)]
        >>> Maze()._trace(Room(0, 0), list('N|S'))
        [Room(x=0, y=1), Room(x=0, y=-1)]
        >>> Maze()._trace(Room(0, 0), list('NE(N|S)'))
        [Room(x=1, y=2), Room(x=1, y=0)]
        >>> Maze()._trace(Room(0, 0), list('NE(N|S)'))
        [Room(x=1, y=2), Room(x=1, y=0)]
        >>> Maze()._trace(Room(0, 0), list('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN'))
        [Room(x=2, y=2)]
        """
        positions = [starting_position]

        end_positions = []

        while instructions:
            c = instructions[0]
            instructions = instructions[1:]

            if c == '(':
                last_index, should_branch = self._closing_bracket(instructions)
                if should_branch:
                    new_positions = []
                    for current in positions:
                        new_positions.extend(self._trace(current, instructions[:last_index]))
                    positions = new_positions
                    instructions = instructions[last_index + 1:]
                else:
                    for current in positions:
                        self._trace(current, instructions[:last_index])
                    instructions = instructions[last_index + 2:]
            elif c == '|':
                end_positions.extend(positions)
                positions = [starting_position]
            elif c == ')':
                continue
            else:
                mx, my = directions[c]
                new_positions = []
                for current in positions:
                    new_room = Room(current.x + mx, current.y + my)
                    self.rooms.add(new_room)
                    self.doors.add(self._door(current, new_room))
                    new_positions.append(new_room)
                positions = new_positions

        end_positions.extend(positions)
        return end_positions

    def shortest_paths(self, start):
        paths = {start: 0}
        positions = [start]

        while positions:
            new_positions = []
            for current in positions:
                for mx, my in directions.values():
                    adjacent = Room(current.x + mx, current.y + my)
                    if adjacent in paths:
                        continue
                    if adjacent not in self.rooms:
                        continue
                    if self._door(current, adjacent) not in self.doors:
                        continue
                    paths[adjacent] = paths[current] + 1
                    new_positions.append(adjacent)
            positions = new_positions

        return paths

    @staticmethod
    def _door(a, b):
        return tuple(sorted([a, b]))

    @staticmethod
    def _closing_bracket(instructions):
        """
        >>> Maze._closing_bracket(list('E)N)'))
        (1, True)
        >>> Maze._closing_bracket(list('E|)N)'))
        (1, False)
        >>> Maze._closing_bracket(list('NEEE|)NEE)'))
        (4, False)
        >>> Maze._closing_bracket(list('NEEE)NEE)'))
        (4, True)
        >>> Maze._closing_bracket(list('NE|SE(EE|(E|N|)))EEE|)'))
        (16, True)
        >>> Maze._closing_bracket(list('NE|SE(EE|(E|N|)))'))
        (16, True)
        >>> Maze._closing_bracket(list('NE|SE(EE|(E|N|))|)EEE|)'))
        (16, False)
        >>> Maze._closing_bracket(list('NE|SE(EE|(E|N|))|)'))
        (16, False)
        """
        brackets_count = 1
        for i, c in enumerate(instructions):
            if c == '(':
                brackets_count += 1
            elif c == ')':
                brackets_count -= 1

            if brackets_count == 0:
                break
        if instructions[i - 1] == '|':
            return i - 1, False
        return i, True


def solve(lines):
    """
    >>> solve(['^WNE$'])
    3
    >>> solve(['^ENWWW(NEEE|SSE(EE|N))$'])
    10
    >>> solve(['^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'])
    18
    """
    start = Room(0, 0)
    path_lengths = Maze.parse(lines).shortest_paths(start).values()
    return max(path_lengths)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
