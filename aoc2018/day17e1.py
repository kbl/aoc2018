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



def below(cords):
    x, y = cords
    return (x, y + 1)

def above(cords):
    x, y = cords
    return (x, y - 1)

def left(cords):
    x, y = cords
    return (x - 1, y)

def right(cords):
    x, y = cords
    return (x + 1, y)


class Drop(tuple):
    def drip(self, clay, water):
        b = below(self)
        if b in water:
            return None, None

        if b in clay:
            return None, Surface(self, clay, water)

        return Drop(b), None


class Surface:

    def __init__(self, drop, clay, water):
        self.produced_by = drop
        self.left = drop
        self.right = drop

        self._expand(clay, water)
        self.drops = self._produce_streams(clay, water)
    
    @property
    def level(self):
        return self.left[1]

    def _produce_streams(self, clay, water):
        blocking = clay.union(water)
        produces = []
        lb = below(self.left)

        if self.left == self.right and lb not in blocking:
            return [Drop(lb)]

        if lb not in blocking:
            produces.append(Drop(lb))

        rb = below(self.right)
        if rb not in blocking:
            produces.append(Drop(rb))
        return produces

    @property
    def water(self):
        return set([(x, self.level) for x in range(self.left[0], self.right[0] + 1)])

    def _expand(self, clay, water):
        blocking = clay.union(water)
        while True:
            ll = left(self.left)
            lb = below(self.left)
            if ll in blocking or lb not in blocking:
                break
            if lb in water and below(ll) not in blocking:
                break
            self.left = ll

        while True:
            rr = right(self.right)
            rb = below(self.right)
            if rr in blocking or rb not in blocking:
                break
            if rb in water and below(rr) not in blocking:
                break
            self.right = rr

        return self

    def __str__(self):
        pb = None
        if self.produced_by:
            pb = self.produced_by
        return 'Surface(%s, %s, %s)' % (self.left, self.right, pb)


class Clay:
    def __init__(self, clay, miny, maxy):
        self.clay = clay
        self.miny = miny
        self.maxy = maxy
        self.water = set()
        self.water_streams = set()

    def has_border(self, drop):
        l = left(drop)
        blocking = self.clay.union(self.water)
        s = Surface(drop, self.clay, self.water)
        return left(s.left) in blocking or right(s.right) in blocking

    def solve(self):
        drops = [Drop((500, 0))]
        self.water_streams.update(drops)
        surfaces = {}

        j = 0
        while drops:
            j += 1
            if j > 100:
                pass
                #break
            drop = drops.pop()
            if drop[1] > self.maxy:
                continue
            print()
            print('handling drop', drop)
            print(self)

            new_drop, new_surface = drop.drip(self.clay, self.water)
            if new_drop:
                self.water_streams.add(new_drop)
                drops.append(new_drop)
                print('adding new drop', new_drop, drops)
                continue

            if not new_surface:
                print('attempt to create surface from drop', drop)
                if not self.has_border(drop):
                    print('surface does not have border')
                    continue
                new_surface = Surface(drop, self.clay, self.water)

            for w in new_surface.water:
                surfaces[w] = new_surface

            # if not new_surface:
            #     new_surface = Surface(drop, self.clay, self.water)

            print('handling new surface', new_surface)

            i = 0
            while True:
                i += 1
                if i > 15:
                    pass
                    #break
                new_drops = new_surface.drops
                if new_drops and self.water_streams.issuperset(new_drops):
                    print('drops were already handled, skipping', new_drops, drops)
                    break
                self.water.update(new_surface.water)
                if new_drops:
                    self.water_streams.update(new_drops)
                    drops.extend(new_drops)
                    print('adding new dropsss', new_drops, drops)
                    break
                            
                if above(new_surface.produced_by) in surfaces:
                    new_surface = surfaces[above(new_surface.produced_by)]
                    print('water level raises reusing 1', new_surface)
                    new_surface._expand(self.clay, self.water)
                    print('water level raises reusing 2', new_surface)
                    print()
                else:
                    new_surface = Surface(above(new_surface.produced_by), self.clay, self.water)
                    for w in new_surface.water:
                        surfaces[w] = new_surface
                    print('water level raises producing', new_surface)
                    print(self)

        print()

        return sum([1 for (x, y) in self.water.union(self.water_streams) if y >= self.miny and y <= self.maxy])

    def __str__(self):
        minx = miny = None
        water = self.water.union(self.water_streams)
        for x, _ in self.clay.union(water):
            if minx is None:
                minx = x
                maxx = x
                continue
            minx = min(minx, x)
            maxx = max(maxx, x)

        rows = []
        for y in range(0, self.maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                cords = (x, y)
                if cords == (500, 0):
                    row.append('+')
                elif cords in self.clay:
                    row.append('#')
                elif cords in self.water:
                    row.append('~')
                elif cords in self.water_streams:
                    row.append('v')
                else:
                    row.append('.')
            rows.append(''.join(row))
        return '\n'.join(rows)


    def fill_container(self, stream, water_in_container=None):
        print('filling', stream, len(self.water))
        if stream.y > self.maxy:
            return []

        if water_in_container is None:
            water_in_container = {stream}

        streams = []

        bound_l = stream
        something_below = water_in_container.union(self.clay).union(self.water)
        something_on_sides = self.clay.union(self.water)

        while _left(bound_l) not in something_on_sides:
            if _below(bound_l) not in something_below:
                break
            bound_l = _left(bound_l)

        bound_r = stream
        while _right(bound_r) not in something_on_sides:
            if _below(bound_r) not in something_below:
                break
            bound_r = _right(bound_r)

        blocked = self.clay.union(water_in_container)
        if _below(bound_l) not in blocked:
            print('not in blocked', _left(bound_l), 'adding source', bound_l)
            streams.append(bound_l)

        if _below(bound_r) not in blocked:
            print('not in blocked', _right(bound_r), 'adding source', bound_r)
            streams.append(bound_r)

        before = len(water_in_container)
        for x in range(bound_l.x, bound_r.x + 1):
            w = (x, bound_l.y)
            if w not in self.clay:
                print('WATER 2', w)
                water_in_container.add(w)
        print('--- filled', len(water_in_container) - before)

        if not streams:
            water_in_container, streams = self.fill_container(_above(stream), water_in_container)
        return water_in_container, streams


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

    # 1230 too low
    # 2003 too low
    # 4000 too low
    # 38456
    clay, miny, maxy = parse(readlines())
    clay = Clay(clay, miny, maxy)
    solution = clay.solve()

    print('DUPA')

    minx = 10000
    maxx = 0
    c = clay.clay
    for (x, y) in c:
        minx = min(minx, x)
        maxx = max(maxx, x)

    print(clay)
    print(solution)
