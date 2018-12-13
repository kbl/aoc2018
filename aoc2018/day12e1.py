from aoc2018 import readlines
from collections import deque, defaultdict, namedtuple


producing_plant_combinations = []


class potdict(defaultdict):
    def __missing__(self, key):
        new = self[key] = self.default_factory(key)
        return new


class Pot:
    def __init__(self, index, has_plant):
        self.index = index
        self.has_plant = has_plant

    def __bool__(self):
        return self.has_plant

    def __str__(self):
        if self.has_plant:
            return '#'
        return '.'

    __repr__ = __str__


class Pots:
    def __init__(self, pots, producing_combinations):
        self.pots = potdict(lambda i: Pot(i, False))
        self.producing_combinations = producing_combinations
        self.min_index = None
        self.max_index = None
        if pots:
            for pot in pots:
                if not pot.has_plant:
                    continue
                if self.min_index is None or pot.index < self.min_index:
                    self.min_index = pot.index
                if self.max_index is None or pot.index > self.max_index:
                    self.max_index = pot.index
                self.pots[pot.index] = pot

    @staticmethod
    def parse(lines):
        pots = Pots._parse_initial_state(lines[0].split("initial state: ")[1])
        producing_plant_combinations = Pots._parse_combinations(lines[2:])
        return Pots(pots, producing_plant_combinations)

    @staticmethod
    def _parse_initial_state(line):
        return [Pot(i, True) for (i, l) in enumerate(line) if l == '#']

    @staticmethod
    def _parse_combinations(lines):
        combinations = set()
        for line in lines:
            if line.endswith('#'):
                combination = line.split(' ')[0]
                combinations.add(tuple(map(lambda l: l == '#', combination)))

        return combinations

    def next_generation(self):
        pots = deque(maxlen=5)
        pots.append(self.pots[self.min_index - 4])
        pots.append(self.pots[self.min_index - 3])
        pots.append(self.pots[self.min_index - 2])
        pots.append(self.pots[self.min_index - 1])

        next_generation = []

        for i in range(self.min_index, self.max_index + 4):
            pots.append(self.pots[i])
            next_generation.append(self._next_generation_pot(pots))

        return Pots(next_generation, self.producing_combinations)

    def _next_generation_pot(self, pots):
        current_plants = tuple(map(bool, pots))
        has_plant_in_next_generation = current_plants in self.producing_combinations
        middle_pot = pots[2]
        return Pot(middle_pot.index, has_plant_in_next_generation)

    def value(self):
        return sum([p.index for p in self.pots.values() if p.has_plant])

    def __str__(self):
        str_pots = []
        for i in range(self.min_index, self.max_index + 1):
            str_pots.append(self.pots[i])
        return ''.join(map(str, str_pots))


lines = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".split('\n')

if __name__ == '__main__':
    lines = list(readlines())
    pots = Pots.parse(lines)

    for i in range(20):
        pots = pots.next_generation()

    print(pots.value())

