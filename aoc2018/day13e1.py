from enum import Enum
from aoc2018 import readlines


class CollisionException(BaseException):
    pass


class Turn(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

    def next(self):
        return Turn((self.value + 1) % 3)


class Roads(Enum):
    HORIZONTAL = 0  # -
    VERTICAL = 1  # |
    TURN_UP = 2  # /
    TURN_DOWN = 3  # \
    INTERSECTION = 4  # +

    def __str__(self):
        if self == self.HORIZONTAL:
            return '-'
        if self == self.VERTICAL:
            return '|'
        if self == self.TURN_UP:
            return '/'
        if self == self.TURN_DOWN:
            return '\\'
        return '+'


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn(self, turn):
        """
        >>> Direction.RIGHT.turn(Roads.TURN_UP)
        <Direction.UP: 3>
        >>> Direction.RIGHT.turn(Roads.TURN_DOWN)
        <Direction.DOWN: 1>

        >>> Direction.LEFT.turn(Roads.TURN_UP)
        <Direction.DOWN: 1>
        >>> Direction.LEFT.turn(Roads.TURN_DOWN)
        <Direction.UP: 3>

        >>> Direction.UP.turn(Roads.TURN_UP)
        <Direction.RIGHT: 0>
        >>> Direction.UP.turn(Roads.TURN_DOWN)
        <Direction.LEFT: 2>

        >>> Direction.DOWN.turn(Roads.TURN_UP)
        <Direction.LEFT: 2>
        >>> Direction.DOWN.turn(Roads.TURN_DOWN)
        <Direction.RIGHT: 0>
        """
        turns = {
            Direction.RIGHT: {
                Roads.TURN_UP: Direction.UP,
                Roads.TURN_DOWN: Direction.DOWN,
            },
            Direction.LEFT: {
                Roads.TURN_UP: Direction.DOWN,
                Roads.TURN_DOWN: Direction.UP,
            },
            Direction.UP: {
                Roads.TURN_UP: Direction.RIGHT,
                Roads.TURN_DOWN: Direction.LEFT,
            },
            Direction.DOWN: {
                Roads.TURN_UP: Direction.LEFT,
                Roads.TURN_DOWN: Direction.RIGHT,
            },
        }
        return turns[self][turn]

    def turn_on_intersection(self, turn):
        """
        >>> Direction.RIGHT.turn_on_intersection(Turn.LEFT)
        <Direction.UP: 3>
        >>> Direction.RIGHT.turn_on_intersection(Turn.STRAIGHT)
        <Direction.RIGHT: 0>
        >>> Direction.RIGHT.turn_on_intersection(Turn.RIGHT)
        <Direction.DOWN: 1>

        >>> Direction.LEFT.turn_on_intersection(Turn.LEFT)
        <Direction.DOWN: 1>
        >>> Direction.LEFT.turn_on_intersection(Turn.STRAIGHT)
        <Direction.LEFT: 2>
        >>> Direction.LEFT.turn_on_intersection(Turn.RIGHT)
        <Direction.UP: 3>

        >>> Direction.UP.turn_on_intersection(Turn.LEFT)
        <Direction.LEFT: 2>
        >>> Direction.UP.turn_on_intersection(Turn.STRAIGHT)
        <Direction.UP: 3>
        >>> Direction.UP.turn_on_intersection(Turn.RIGHT)
        <Direction.RIGHT: 0>

        >>> Direction.DOWN.turn_on_intersection(Turn.LEFT)
        <Direction.RIGHT: 0>
        >>> Direction.DOWN.turn_on_intersection(Turn.STRAIGHT)
        <Direction.DOWN: 1>
        >>> Direction.DOWN.turn_on_intersection(Turn.RIGHT)
        <Direction.LEFT: 2>
        """

        turns = {
            Direction.RIGHT: {
                Turn.LEFT: Direction.UP,
                Turn.STRAIGHT: Direction.RIGHT,
                Turn.RIGHT: Direction.DOWN,
            },
            Direction.LEFT: {
                Turn.LEFT: Direction.DOWN,
                Turn.STRAIGHT: Direction.LEFT,
                Turn.RIGHT: Direction.UP,
            },
            Direction.UP: {
                Turn.LEFT: Direction.LEFT,
                Turn.STRAIGHT: Direction.UP,
                Turn.RIGHT: Direction.RIGHT,
            },
            Direction.DOWN: {
                Turn.LEFT: Direction.RIGHT,
                Turn.STRAIGHT: Direction.DOWN,
                Turn.RIGHT: Direction.LEFT,
            }
        }

        return turns[self][turn]


    def move(self, cords):
        """
        >>> Direction.UP.move((1, 1))
        (1, 0)
        >>> Direction.DOWN.move((1, 1))
        (1, 2)
        >>> Direction.LEFT.move((1, 1))
        (0, 1)
        >>> Direction.RIGHT.move((1, 1))
        (2, 1)
        """
        x, y = cords
        if self == Direction.UP:
            return (x, y - 1)
        if self == Direction.DOWN:
            return (x, y + 1)
        if self == Direction.LEFT:
            return (x - 1, y)
        return (x + 1, y)


class Cart:
    def __init__(self, cords, direction, next_turn=Turn.LEFT, initial_cords=None):
        self.initial_cords = initial_cords or cords
        self.cords = cords
        self.direction = direction
        self.next_turn = next_turn
        self.crashed = False

    def tick(self, moves):
        """
        >>> Cart((1, 1), Direction.LEFT).tick({Direction.LEFT: Roads.HORIZONTAL, Direction.RIGHT: Roads.HORIZONTAL})
        Cart((0, 1), Direction.LEFT)
        >>> Cart((1, 1), Direction.UP).tick({Direction.UP: Roads.VERTICAL, Direction.DOWN: Roads.VERTICAL})
        Cart((1, 0), Direction.UP)

        >>> Cart((1, 1), Direction.RIGHT, Turn.LEFT).tick({Direction.RIGHT: Roads.INTERSECTION, Direction.LEFT: Roads.HORIZONTAL})
        Cart((2, 1), Direction.UP, Turn.STRAIGHT)
        >>> Cart((1, 1), Direction.RIGHT, Turn.STRAIGHT).tick({Direction.RIGHT: Roads.INTERSECTION, Direction.LEFT: Roads.HORIZONTAL})
        Cart((2, 1), Direction.RIGHT, Turn.RIGHT)
        >>> Cart((1, 1), Direction.RIGHT, Turn.RIGHT).tick({Direction.RIGHT: Roads.INTERSECTION, Direction.LEFT: Roads.HORIZONTAL})
        Cart((2, 1), Direction.DOWN)

        >>> Cart((1, 1), Direction.RIGHT).tick({Direction.RIGHT: Roads.TURN_UP, Direction.LEFT: Roads.HORIZONTAL})
        Cart((2, 1), Direction.UP)
        >>> Cart((1, 1), Direction.RIGHT).tick({Direction.RIGHT: Roads.TURN_DOWN, Direction.LEFT: Roads.HORIZONTAL})
        Cart((2, 1), Direction.DOWN)
        
        >>> Cart((1, 1), Direction.LEFT).tick({Direction.LEFT: Roads.TURN_UP, Direction.RIGHT: Roads.HORIZONTAL})
        Cart((0, 1), Direction.DOWN)
        >>> Cart((1, 1), Direction.LEFT).tick({Direction.LEFT: Roads.TURN_DOWN, Direction.RIGHT: Roads.HORIZONTAL})
        Cart((0, 1), Direction.UP)
        """
        if moves[self.direction] == Roads.INTERSECTION:
            new_direction = self.direction.turn_on_intersection(self.next_turn)
            new_next_turn = self.next_turn.next()
        elif moves[self.direction] in [Roads.TURN_UP, Roads.TURN_DOWN]:

            new_direction = self.direction.turn(moves[self.direction])
            new_next_turn = self.next_turn
        else:
            moves[self.direction]  # sanity_check
            new_direction = self.direction
            new_next_turn = self.next_turn

        return Cart(self.direction.move(self.cords), new_direction, new_next_turn, self.initial_cords)

    def __str__(self):
        return {
            Direction.UP: '^',
            Direction.DOWN: 'v',
            Direction.LEFT: '<',
            Direction.RIGHT: '>',
        }[self.direction]

    def __repr__(self):
        if self.next_turn == Turn.LEFT:
            return 'Cart(%s, %s)' % (self.cords, self.direction)
        return 'Cart(%s, %s, %s)' % (self.cords, self.direction, self.next_turn)

    def __eq__(self, other):
        return self.cords == other.cords and self.direction == other.direction

    def __lt__(self, other):
        """
        >>> sorted([Cart((1, 1), Direction.LEFT), Cart((1, 0), Direction.LEFT), Cart((0, 1), Direction.LEFT)])
        [Cart((1, 0), Direction.LEFT), Cart((0, 1), Direction.LEFT), Cart((1, 1), Direction.LEFT)]
        """
        x, y = self.cords
        ox, oy = other.cords
        return (y, x, self.direction) < (oy, ox, other.direction)


class Paths:
    ROADS = set(['/', '|', '\\', '-', '+'])
    CARTS = set(['>', '^', '<', 'v'])
    DIRECTIONS = {
        '>': Direction.RIGHT,
        'v': Direction.DOWN,
        '<': Direction.LEFT,
        '^': Direction.UP
    }

    def __init__(self, maze, carts, max_x, max_y):
        self.maze = maze
        self.carts = carts
        self.max_x = max_x
        self.max_y = max_y

    def __str__(self):
        rows = []
        for y in range(self.max_y):
            row = []
            for x in range(self.max_x):
                is_cart = False
                cords = (x, y)
                if cords in self.carts:
                    row.append(str(self.carts[cords]))
                elif cords in self.maze:
                    row.append(str(self.maze[cords]))
                else:
                    row.append(' ')
            rows.append(''.join(row))
        return '\n'.join(rows)

    def tick(self):
        carts = {}
        for i, c in enumerate(sorted(self.carts.values())):
            if c.cords in carts:
                raise CollisionException(c.cords)
            new_cart = c.tick(self.options(c.cords))
            if new_cart.cords in carts:
                raise CollisionException(new_cart.cords)
            carts[new_cart.cords] = new_cart
        self.carts = carts

    def options(self, cords):
        return {d: self.maze.get(d.move(cords)) for d in Direction}

        x, y = cords
        options = {
            Roads.HORIZONTAL: {
                Direction.RIGHT: (x + 1, y),
                Direction.LEFT: (x - 1, y),
            },
            Roads.VERTICAL: {
                Direction.DOWN: (x, y + 1),
                Direction.UP: (x, y - 1),
            },
            Roads.INTERSECTION: {
                Direction.DOWN: (x, y + 1),
                Direction.UP: (x, y - 1),
                Direction.RIGHT: (x + 1, y),
                Direction.LEFT: (x - 1, y),
            }
        }
        if self.maze[cords] in options:
            return options[self.maze[cords]]

        if self.maze[cords] == Roads.TURN_UP: # /
            if self.maze.get((x - 1, y)) in [Roads.HORIZONTAL, Roads.INTERSECTION]: #-/
                return {
                    Direction.LEFT: (x - 1, y),
                    Direction.UP: (x, y - 1),
                }
            # /-
            return {
                Direction.RIGHT: (x + 1, y),
                Direction.DOWN: (x, y + 1),
            }

        if self.maze.get((x - 1, y)) in [Roads.HORIZONTAL, Roads.INTERSECTION]: #-\
            return {
                Direction.LEFT: (x - 1, y),
                Direction.DOWN: (x, y + 1),
            }
        # \-
        return {
            Direction.RIGHT: (x + 1, y),
            Direction.UP: (x, y - 1),
        }

    @staticmethod
    def parse(lines):
        maze = {}
        carts = {}
        max_x = 0
        max_y = 0
        for y, line in enumerate(lines):
            row = []
            max_y = max(max_y, y)
            for x, char in enumerate(line):
                max_x = max(max_x, x)
                cords = (x, y)
                if char in Paths.ROADS:
                    if char == '-':
                        maze[cords] = Roads.HORIZONTAL
                    elif char == '|':
                        maze[cords] = Roads.VERTICAL
                    elif char == '+':
                        maze[cords] = Roads.INTERSECTION
                    elif char == '/':
                        maze[cords] = Roads.TURN_UP
                    else:
                        maze[cords] = Roads.TURN_DOWN
                elif char in Paths.CARTS:
                    if char in ['<', '>']:
                        maze[cords] = Roads.HORIZONTAL
                    else:
                        maze[cords] = Roads.VERTICAL
                    direction = Paths.DIRECTIONS[char]
                    carts[cords] = Cart(cords, direction)
        return Paths(maze, carts, max_x + 1, max_y + 1)


lines = """/->-\ 
|   |  /----\ 
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    p = Paths.parse(readlines(strip=False))
    while True:
        p.tick()

