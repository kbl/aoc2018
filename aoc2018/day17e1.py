from collections import namedtuple
from aoc2018 import readlines


def parse(lines):
    min_y = 100000000
    max_y = -10000000
    clay = set()
    for line in lines:
        x, y = sorted(line.split(', '))
        parsed_x = list(map(int, x[2:].split('..')))
        parsed_y = list(map(int, y[2:].split('..')))

        if len(parsed_x) > 1:
            xmin, xmax = parsed_x
            [y] = parsed_y

            min_y = min(min_y, y)
            max_y = max(max_y, y)

            for x in range(xmin, xmax + 1):
                clay.add((x, y))

        if len(parsed_y) > 1:
            [x] = parsed_x
            ymin, ymax = parsed_y

            min_y = min(min_y, ymin)
            max_y = max(max_y, ymax)

            for y in range(ymin, ymax + 1):
                clay.add((x, y))
    return clay, min_y, max_y


class Cords(namedtuple('metacords', ['x', 'y'])):
    def below(self):
        return self.__class__(self.x, self.y + 1)

    def above(self):
        return self.__class__(self.x, self.y - 1)

    def left(self):
        return self.__class__(self.x - 1, self.y)

    def right(self):
        return self.__class__(self.x + 1, self.y)


class Drop(Cords):
    def drip(self, clay, water):
        b = self.below()
        if b in water:
            existing_surface = water[b]
            existing_surface.input_streams.append(b)
            return None, existing_surface
        if b in clay:
            c = Cords(*self)
            s = Surface(c, c, self)
            water[c] = s
            return None, s
        return b, None


class Surface:
    def __init__(self, left, right, drop):
        self.left = left
        self.right = right
        if isinstance(drop, Drop):
            self.input_streams = [drop]
        elif drop is None:
            self.input_streams = []
        else:
            self.input_streams = drop

    def __str__(self):
        return 'Surface(%s, %s, %s)' % (self.left, self.right, self.input_streams)

    __repr__ = __str__

    def __iter__(self):
        y = self.left.y
        return iter([Cords(x, y) for x in range(self.left.x, self.right.x + 1)])

    def __eq__(self, other):
        return list(self) == list(other)

    def blocked(self, clay):
        return self.left.left() in clay and self.right.right() in clay

    def flow(self, clay, water):
        while True:
            ll = self.left.left()
            if ll in clay:
                break
            if ll in water:
                other_surface = water[ll]
                self.left = other_surface.left
                self.input_streams.extend(other_surface.input_streams)
                continue

            bll = ll.below()
            if bll in clay or bll in water:
                self.left = ll
            else:
                break

        while True:
            rr = self.right.right()
            if rr in clay:
                break
            if rr in water:
                other_surface = water[rr]
                self.right = other_surface.right
                self.input_streams.extend(other_surface.input_streams)
                continue

            brr = rr.below()
            if brr in clay or brr in water:
                self.right = rr
            else:
                break

        for c in self:
            water[c] = self

        drops = []
        ll = Drop(*self.left.left())
        if ll not in clay:
            drops.append(ll)

        rr = Drop(*self.right.right())
        if rr not in clay:
            drops.append(rr)

        return drops

    def raise_level(self, water):
        surfaces = []
        for s in self.input_streams:
            above = s.above()
            if above in water:
                continue
            point = Cords(*above)
            s = Surface(point, point, above)
            water[point] = s
            surfaces.append(s)
        return surfaces


class Clay:
    def __init__(self, clay, miny, maxy):
        self.clay = clay
        self.miny = miny
        self.maxy = maxy
        self.water = {}
        self.water_streams = set()

    def solve(self):
        drops = [Drop(500, 0)]

        while drops:
            drop = drops.pop()
            if drop in self.water_streams or drop.y > self.maxy:
                continue

            self.water_streams.add(drop)
            new_drop, surface = drop.drip(self.clay, self.water)
            if new_drop:
                drops.append(new_drop)
                continue

            new_drops = surface.flow(self.clay, self.water)
            if not new_drops:
                new_drops = []
                surfaces = [surface]
                while surfaces:
                    s = surfaces.pop()
                    for raised_surface in s.raise_level(self.water):
                        new_surface_drops = raised_surface.flow(self.clay, self.water)
                        if new_surface_drops:
                            new_drops.extend(new_surface_drops)
                        else:
                            surfaces.append(raised_surface)

            drops.extend(new_drops)

        return self.stats()

    def stats(self):
        water_in_containers = set()
        for surface in list(self.water.values()):
            if surface.blocked(self.clay):
                water_in_containers.update(surface)
        water_in_containers = len(water_in_containers)

        all_water = sum([1 for (x, y) in set(self.water).union(self.water_streams) if y >= self.miny and y <= self.maxy])

        return all_water, water_in_containers

    def __str__(self):
        minx = maxx = None
        water = set(self.water).union(self.water_streams)
        for x, y in self.clay.union(water):
            if minx is None:
                minx = x
                maxx = x
                continue
            minx = min(minx, x)
            maxx = max(maxx, x)

        rows = [
            '     ' + ''.join([str(x // 100) for x in range(minx, maxx + 1)]),
            '     ' + ''.join([str((x % 100) // 10) for x in range(minx, maxx + 1)]),
            '     ' + ''.join([str(x % 10) for x in range(minx, maxx + 1)]),
        ]
        for y in range(0, self.maxy + 1):
            row = ['%4d ' % y]
            for x in range(minx, maxx + 1):
                cords = (x, y)
                if cords == (500, 0):
                    row.append('+')
                elif cords in self.clay:
                    row.append('#')
                elif cords in self.water:
                    row.append('~')
                elif cords in self.water_streams:
                    row.append('|')
                else:
                    row.append(' ')
            rows.append(''.join(row))
        return '\n'.join(rows)


lines = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    clay = Clay(*parse(readlines()))
    print(clay.solve())
