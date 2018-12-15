from aoc2018 import readlines
from collections import defaultdict


WALL = '#'
ELF = 'E'
GOBLIN = 'G'


def cords_key(cords):
    return cords[1], cords[0]
    

class Unit:
    def __init__(self, x, y, power=3):
        self.x = x
        self.y = y
        self.hp = 200
        self.power = power

    def move(self, cords):
        self.x, self.y = cords
        if isinstance(self.x, tuple) or isinstance(self.y, tuple):
            raise 'xx'

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def is_dead(self):
        return not self.is_alive

    @property
    def cords(self):
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.cords == other.cords
        return False

    def __lt__(self, other):
        return cords_key(self.cords) < cords_key(other.cords)

    def __repr__(self):
        return '%s(%d, %d, %d)' % (self.__class__.__name__, self.x, self.y, self.hp)

    @property
    def is_goblin(self):
        return False

    @property
    def is_elf(self):
        return False

    def attack(self, enemy):
        enemy.hp -= self.power


class Elf(Unit):
    @property
    def is_elf(self):
        return True

    def __str__(self):
        if self.is_alive:
            return ELF
        return 'e'


class Goblin(Unit):
    @property
    def is_goblin(self):
        return True

    def __str__(self):
        if self.is_alive:
            return GOBLIN
        return 'g'


class Maze:
    def __init__(self, maze, units):
        self.maze = maze
        self.units = units
        self.max_x = max([c[0] for c in maze.keys()])
        self.max_y = max([c[1] for c in maze.keys()])

    def tick(self):
        self.units = sorted([u for u in self.units if u.is_alive])
        for unit in self.units:
            if unit.is_dead:
                continue

            attacked = self.attempt_attack(unit)
            if attacked:
                continue

            enemies = self.enemies(unit)
            attack_positions = self.attack_positions(enemies)
            next_cords = self.find_move(unit.cords, attack_positions)
            if next_cords is None:
                continue

            del self.maze[unit.cords]

            unit.move(next_cords)
            self.maze[next_cords] = unit

            self.attempt_attack(unit)

    def attempt_attack(self, unit):
        enemy = self.pick_adjacent_target(unit)
        if enemy:
            unit.attack(enemy)
            if enemy.is_dead:
                del self.maze[enemy.cords]
            return True

    def pick_adjacent_target(self, unit):
        x, y = unit.cords
        targets = []
        for n_cords in self.adjacent_cords(unit.cords):
            if n_cords in self.maze and WALL != self.maze[n_cords]:
                other_unit = self.maze[n_cords]
                if other_unit.is_elf == unit.is_elf:
                    continue
                targets.append(other_unit)

        targets = sorted(targets, key=lambda u: (u.hp, u))
        if targets:
            return targets[0]

    @staticmethod
    def adjacent_cords(cords):
        x, y = cords
        for mx, my in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            yield (x + mx, y + my)

    def enemies(self, unit):
        return [u for u in self.units if u.is_alive and u.is_elf != unit.is_elf]

    def attack_positions(self, enemies):
        positions = set()
        for e in enemies:
            positions.update(self.possible_moves(e.cords))
        return positions

    def possible_moves(self, cords):
        return [c for c in self.adjacent_cords(cords) if not self.is_occupied(c)]

    def find_move(self, start, ends):
        paths = []
        seen = {}

        im_close = []

        for m in self.possible_moves(start):
            if m in ends:
                im_close.append(m)
            paths.append((m, m))
            seen[(m, start)] = 0

        if im_close:
            im_close = sorted(im_close, key=cords_key)
            return im_close[0]

        next_moves = []

        while not next_moves and paths:
            new_paths = []
            for starting_point, last_point in paths:
                for next_step in self.possible_moves(last_point):
                    possible_path = (starting_point, next_step)
                    if possible_path in seen:
                        continue

                    seen[possible_path] = True

                    if next_step in ends:
                        next_moves.append(starting_point)

                    new_paths.append(possible_path)
            paths = new_paths

        sorted_next_moves = sorted(next_moves, key=cords_key)
        if sorted_next_moves:
            return sorted_next_moves[0]

    def is_occupied(self, cords):
        if cords in self.maze:
            if self.maze[cords] == WALL:
                return True
            return self.maze[cords].is_alive
        return False

    @property
    def has_elves(self):
        return any([u.is_elf for u in self.units if u.is_alive])

    @property
    def has_enemies(self):
        elves = 0
        goblins = 0
        for u in self.units:
            if u.is_dead:
                continue
            if u.is_goblin:
                goblins += 1
            else:
                elves += 1
        return not (elves == 0 or goblins == 0)

    def __str__(self):
        rows = []
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                rows.append(str(self.maze.get((x, y), '.')))
            rows.append('\n')
        return ''.join(rows)


def parse(lines):
    maze = {}
    units = []
    for y, row in enumerate(lines):
        for x, element in enumerate(row):
            if element == WALL:
                maze[(x, y)] = WALL
            elif element == ELF:
                e = Elf(x, y)
                maze[(x, y)] = e
                units.append(e)
            elif element == GOBLIN:
                g = Goblin(x, y)
                maze[(x, y)] = g
                units.append(g)
    return Maze(maze, units)


lines0 = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".split('\n')


lines1 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""".split('\n')


def simulate(maze):
    rounds = 0
    while True:
        maze.tick()
        if not maze.has_enemies:
            break
        rounds +=1 

    return sum([u.hp for u in maze.units if u.is_alive]) * rounds


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    m = parse(readlines())
    print(simulate(m))
