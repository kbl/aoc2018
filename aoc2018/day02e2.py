from collections import Counter
from aoc2018 import readlines


def _generate_all_but_one_letter(word):
    for i in range(len(word)):
      yield (i, word[:i] + word[i + 1:])


def exercise(lines):
    seen = Counter()

    for line in lines:
        seen.update(_generate_all_but_one_letter(line))

    for (_, x), count in seen.items():
        if count == 2:
            return x


if __name__ == '__main__':
    print(exercise(readlines()))
