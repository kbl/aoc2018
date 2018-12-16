from aoc2018 import readlines
from aoc2018.day16e1 import operations, BEFORE_RE, AFTER_RE, parse
from collections import defaultdict, deque


def solve(tripples, program):
    mapping = find_instructions(tripples)
    untangle_mapping(mapping)
    registers = [0, 0, 0, 0]
    for operation, a, b, c in program:
        mapping[operation](registers, a, b, c)

    return registers[0]


def find_instructions(triples):
    operation_mapping = defaultdict(set)

    how_many = 0
    for before, instruction, after in triples:
        works = 0
        for o in operations:
            if after == o(list(before), *instruction[1:]):
                operation_mapping[instruction[0]].add(o)

    return operation_mapping


def untangle_mapping(mapping):
    already_matched = set()
    keys_to_check = deque(mapping.keys())
    while keys_to_check:
        key = keys_to_check.pop()
        mapping[key] -= already_matched
        if len(mapping[key]) == 1:
            already_matched |= mapping[key]
        else:
            keys_to_check.appendleft(key)

    for key, operations in mapping.items():
        mapping[key] = operations.pop()


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    tripples, program = parse(readlines())
    print(solve(tripples, program))
