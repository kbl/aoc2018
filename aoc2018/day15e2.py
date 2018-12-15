from aoc2018 import readlines
from aoc2018.day15e1 import Elf, Goblin, Maze, WALL, ELF, GOBLIN, simulate
from collections import defaultdict


def parse(lines, elf_power):
    maze = {}
    units = []
    for y, row in enumerate(lines):
        for x, element in enumerate(row):
            if element == WALL:
                maze[(x, y)] = WALL
            elif element == ELF:
                e = Elf(x, y, elf_power)
                maze[(x, y)] = e
                units.append(e)
            elif element == GOBLIN:
                g = Goblin(x, y)
                maze[(x, y)] = g
                units.append(g)
    return Maze(maze, units)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    loosing_power = 3
    winning_power = 200
    outcomes = {}

    while loosing_power + 1 != winning_power:
        difference = winning_power - loosing_power
        elves_power = loosing_power + difference // 2

        print('Attempting fight with elves power %d.' % elves_power)
        m = parse(readlines(), elves_power)
        elves_before = len([u for u in m.units if u.is_elf and u.is_alive])
        outcome = simulate(m)
        outcomes[elves_power] = outcome
        elves_after = len([u for u in m.units if u.is_elf and u.is_alive])
        all_elves_survived =  elves_before == elves_after

        if all_elves_survived:
            print('All elves survived when their power was %d.' % elves_power)
            winning_power = elves_power
        else:
            print('%d elves died when their power was %d.' % (elves_before - elves_after, elves_power))
            loosing_power = elves_power

    print(outcomes[winning_power])
