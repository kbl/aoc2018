from aoc2018 import readlines
from aoc2018.day12e1 import Pots


if __name__ == '__main__':
    lines = list(readlines())
    pots = Pots.parse(lines)

    previous_pots = None
    already_seen_pots = set()
    already_seen_pots.add(str(pots))
    generation = 0

    while True:
        generation += 1
        previous_pots = pots
        pots = pots.next_generation()
        str_pots = str(pots)
        if str_pots in already_seen_pots:
            break
        already_seen_pots.add(str_pots)

    desired_generation = 50000000000
    previous_value = previous_pots.value()
    value_difference = pots.value() - previous_value
    missing_generations = desired_generation - generation

    print(missing_generations * value_difference + pots.value())
