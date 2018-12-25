from aoc2018.day24e1 import Group as G, IMMUNE_SYSTEM, INFECTION, simulate
from aoc2018 import readlines


BOOST = 0


class Group(G):
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if self.group_type == IMMUNE_SYSTEM:
            self.unit_power += BOOST


def parse(lines):
    immune_system = []
    infection = []
    group_type = IMMUNE_SYSTEM
    group_number = 1
    for line in lines[1:]:
        if not line:
            continue
        if line.startswith('Infection'):
            group_type = INFECTION
            group_number = 1
            now_infections = True
            continue

        g = Group.parse(group_number, group_type, line)
        group_number += 1
        if group_type == INFECTION:
            infection.append(g)
        else:
            immune_system.append(g)
    return immune_system, infection


def solve(lines):
    global BOOST

    immune_system, infection = parse(lines)
    immune_system, infection = simulate(immune_system, infection)

    while infection:
        BOOST += 1
        immune_system, infection = parse(lines)
        immune_system, infection = simulate(immune_system, infection)
    
    return sum([g.unit_count for g in immune_system])


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
