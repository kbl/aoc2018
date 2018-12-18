from aoc2018 import readlines
from aoc2018.day18e1 import evolve, parse, TREE, LUMBERYARD, count


def solve(lines):
    data = parse(lines)

    cycle_start = None
    desired_minute = 1000000000

    key = lambda d: tuple(sorted(d.items()))
    stat = lambda d: count(d, TREE) * count(d, LUMBERYARD)

    seen = {key(data): 0}
    after_minute = {0: stat(data)}

    for current_minute in range(1, desired_minute + 1):
        data = {cords: evolve(data, cords, item) for cords, item in data.items()}
        k = key(data)
        if k in seen:
            cycle_start = seen[k]
            break
        seen[k] = current_minute
        after_minute[current_minute] = stat(data)

    cycle_duration = current_minute - cycle_start
    minutes_after_cycle_start = (desired_minute - cycle_start) % cycle_duration
    forseen_future = cycle_start + minutes_after_cycle_start

    return after_minute[forseen_future]


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
