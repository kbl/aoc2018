import re
from aoc2018 import readlines
from datetime import datetime
from collections import defaultdict, Counter


class Guard:
    def __init__(self):
        self.stats = Counter()
        self.how_many = 0

    def update(self, minutes):
        self.how_many += len(minutes)
        self.stats.update(minutes)

    def __str__(self):
        return str(self.how_many)

    def __repr__(self):
        return str(self.how_many)


guards = defaultdict(lambda: Guard())


def exercise(lines):
    regex = re.compile(r'\[(.+)\] (.+)')
    data = []
    for line in lines:
        when, what = regex.match(line).groups()
        when = datetime.strptime(when, '%Y-%m-%d %H:%M')
        data.append((when, what))
    data.sort()
    guard = None
    falls_asleep = None
    for when, what in data:
        if 'Guard' in what:
            guard = int(what.split('#')[1].split(' ')[0])
            continue

        if 'falls asleep' == what:
            falls_asleep = when.minute
            continue
        
        if falls_asleep is None:
            raise Exception("xxx", guard)

        guards[guard].update(range(falls_asleep, when.minute))
        falls_asleep = None

    id, _ = sorted(guards.items(), key=lambda kv: kv[1].how_many, reverse=True)[0]
    minute, _ = sorted(guards[id].stats.items(), key=lambda kv: kv[1], reverse=True)[0]
    print(id, minute, id * minute)

    most_frequent_minute_for_guard = list(
        map(
            lambda kv: (
                kv[0],
                sorted(
                    kv[1].stats.items(),
                    key=lambda m: m[1],
                    reverse=True
                )[0]
            )
            ,guards.items()
        )
    )

    id, (minute, _) = sorted(most_frequent_minute_for_guard, key=lambda g: g[1][1], reverse=True)[0]
    print(id, minute, id * minute)


if __name__ == '__main__':
    exercise(readlines())
