import re
from collections import defaultdict


class Claim:

    REX = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.overlaps = False

    def __repr__(self):
        return "Claim(%d, %d, %d, %d, %d)" % (self.id, self.x, self.y, self.width, self.height)

    @classmethod
    def parse(cls, line):
        return cls(*map(int, cls.REX.match(line).groups()))

    @property
    def maxx(self):
        return self.x + self.width - 1

    @property
    def maxy(self):
        return self.y + self.height - 1

    def mark(self, fabric):
        for i in range(self.x, self.maxx + 1):
            for j in range(self.y, self.maxy + 1):
                fabric[i][j].append(self)
                if len(fabric[i][j]) >= 2:
                    for c in fabric[i][j]:
                        c.overlaps = True


fabric = defaultdict(lambda: defaultdict(list))
claims = []


for line in input.split("\n"):
    claim = Claim.parse(line)
    claim.mark(fabric)
    claims.append(claim)

duplicated = 0

for lines in fabric.values():
    for cell in lines.values():
        if len(cell) > 1:
            duplicated += 1

for c in claims:
    if not c.overlaps:
        print(c)

print(duplicated)
