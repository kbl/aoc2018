from collections import Counter
from aoc2018 import readlines


def exercise(lines):
    twos = 0
    threes = 0

    for line in lines:
        has_two = False;
        has_three = False;

        for _, count in Counter(line).items():
            if count == 2:
                has_two = True
            if count == 3:
                has_three = True

        if has_two:
            twos += 1 
        if has_three:
            threes += 1 

    return twos * threes


if __name__ == '__main__':
    print(exercise(readlines()))
