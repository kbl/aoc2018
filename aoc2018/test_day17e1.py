from aoc2018.day17e1 import Clay, Surface, Drop, Cords
import pytest

def parse(representation):
    clay = set()
    miny = 10
    maxy = 0
    lines = [l.strip() for l in representation.split('\n') if len(l.strip())]
    x500 = lines[0].index('+')
    water = 0
    for y, row in enumerate(lines[1:], 1):
        for x, e in enumerate(row, 500 - x500):
            if e == '#':
                clay.add((x, y))
                miny = min(y, miny)
                maxy = max(y, maxy)
            if e == '*':
                water += 1

    return Clay(clay, miny, maxy), water


def parse_symbol(representation, symbol):
    symbols = set()
    lines = [l.strip() for l in representation.split('\n') if len(l.strip())]
    for y, row in enumerate(lines):
        for x, e in enumerate(row):
            if e == symbol:
                if symbol == 'v':
                    symbols.add(Drop(x, y))
                else:
                    symbols.add(Drop(x, y))

    return symbols


def parse_water(representation, symbol='~'):
    water = {}
    lines = [l.strip() for l in representation.split('\n') if len(l.strip())]
    for y, row in enumerate(lines):
        previous_was_water = False
        surface_left = None
        for x, e in enumerate(row):
            if e == symbol:
                if previous_was_water:
                    continue
                else:
                    surface_left = x
                    print('x', x)
                    previous_was_water = True
                    continue
            if previous_was_water:
                previous_was_water = False
                s = Surface(Cords(surface_left, y), Cords(x - 1, y), None)
                for w in s:
                    water[w] = s

    if previous_was_water:
        s = Surface(Cords(surface_left, y), Cords(x, y), None)
        for w in s:
            water[w] = s

    return water


def test_parse_water():
    representation = """
    .~~~.
    ~.~.~"""
    water = parse_water(representation)
    for x, y in sorted(water.items(), key=lambda z: (z[0][1], z[0][0])):
        print(x, y)
    assert len(water) == 6
    assert list(water[(1, 0)]) == list(water[(3, 0)])
    assert list(water[(1, 0)]) == [(1, 0), (2, 0), (3, 0)]
    assert water[(1, 0)] != water[(0, 1)]
    assert water[(0, 1)] != water[(2, 1)]


def test_drip():
    representation = """
    ..v..
    ....."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    new_drop, surface = drop.drip(clay, water)
    assert new_drop == (2, 1)
    assert surface is None


def test_multiple_drips():
    representation = """
    .v..v
    ~~~~~"""
    clay = set()
    water = parse_water(representation)
    surface = water[(0, 1)]
    drop1 = Drop(1, 0)
    drop2 = Drop(4, 0)

    assert surface.input_streams == []

    _, new_surface = drop1.drip(clay, water)
    assert surface == new_surface
    assert surface.input_streams == [drop1.below()]

    _, new_surface = drop2.drip(clay, water)
    assert surface == new_surface
    assert surface.input_streams == [drop1.below(), drop2.below()]


def test_drip_on_clay():
    representation = """
    ...v...
    ..###.."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    new_drop, surface = drop.drip(clay, water)
    assert new_drop is None
    assert water[drop] == surface
    assert surface.left == drop
    assert surface.right == drop
    assert surface.input_streams == [drop]


def test_surface_iterable():
    assert list(Surface(Cords(1, 0), Cords(3, 0), None)) == [(1, 0), (2, 0), (3, 0)]


def test_flow():
    representation = """
    ...v...
    ..###.."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    _, surface = drop.drip(clay, water)

    [drop1, drop2] = surface.flow(clay, water)

    assert drop1 == (1, 0)
    assert drop2 == (5, 0)
    assert list(surface) == [(2, 0), (3, 0), (4, 0)]
    assert len(water) == 3
    assert water[(2, 0)] == surface
    assert water[(3, 0)] == surface
    assert water[(4, 0)] == surface


def test_flow_clay_on_right():
    representation = """
    ...v.#.
    ..####."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    _, surface = drop.drip(clay, water)

    [drop1] = surface.flow(clay, water)

    assert drop1 == (1, 0)
    assert list(surface) == [(2, 0), (3, 0), (4, 0)]


def test_flow_clay_on_left():
    representation = """
    .#.v..
    .####."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    _, surface = drop.drip(clay, water)

    [drop1] = surface.flow(clay, water)

    assert drop1 == (5, 0)
    assert list(surface) == [(2, 0), (3, 0), (4, 0)]


def test_flow_on_water():
    representation = """
    ...v....
    ..##~~#."""
    clay = parse_symbol(representation, '#')
    water = parse_water(representation)
    [drop] = list(parse_symbol(representation, 'v'))
    _, surface = drop.drip(clay, water)

    [drop1, drop2] = surface.flow(clay, water)

    assert drop1 == (1, 0)
    assert drop2 == (7, 0)
    assert list(surface) == [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]


def test_drop_on_water():
    representation = """
    ..v..
    .~~~."""
    clay = parse_symbol(representation, '#')
    water = parse_water(representation)
    [drop] = list(parse_symbol(representation, 'v'))
    existing_surface = water[(2, 1)]

    _, new_surface = drop.drip(clay, water)

    assert new_surface == existing_surface


def test_flow_merge_surfaces():
    representation = """
    ........
    #.v..v.#
    ########"""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop1, drop2] = list(parse_symbol(representation, 'v'))
    
    drop1.drip(clay, water)
    drop2.drip(clay, water)

    assert len(water) == 2
    assert id(water[drop1]) != id(water[drop2])

    water[drop1].flow(clay, water)

    for x, y in water.items():
        print(x, id(y))

    assert id(water[drop1]) == id(water[drop2])
    assert water[drop1].input_streams == [drop1, drop2]


def test_flow_container_with_hole():
    representation = """
    .#.v#.
    .#.##."""
    clay = parse_symbol(representation, '#')
    water = {}
    [drop] = list(parse_symbol(representation, 'v'))
    _, surface = drop.drip(clay, water)

    [new_drop] = surface.flow(clay, water)

    assert len(water) == 1
    assert list(surface) == [(3, 0)]
    assert new_drop == (2, 0)


def test_parsing():
    clay, water = parse("""
    ...+...
    ..~~~..
    ..*#*..
    ..*#*..""")
    assert len(clay.clay) == 2
    assert (500, 2) in clay.clay
    assert (500, 3) in clay.clay
    assert clay.miny == 2
    assert clay.maxy == 3
    assert water == 4


def test_str():
    clay, _ = parse("""
    ...+...
    .......
    .......
    ...#...""")
    clay.solve()
    print(clay)
    assert str(clay) == """   455
   900
   901
 0 .+.
 1 .|.
 2 |~|
 3 |#|"""


def test_basic_solve():
    clay, water = parse("""
    ...+...
    ...~...
    ..~~~..
    ..*#*...""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_basic_container():
    clay, water = parse("""
    ...+...
    .~~~~~.
    .*#*#*.
    .*###*..""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_overflow_right():
     clay, water = parse("""
     ...+...
     ...~...
     ..#***.
     ..#*#*.
     ..###*..""")
     solution = clay.solve()
     print(clay)
     assert solution == water


def test_overflow_left():
    clay, water = parse("""
    ...+...
    ...~...
    .***#..
    .*#*#..
    .*###..""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_container_with_hole():
    clay, water = parse("""
    ...+...
    ...~...
    .#.*#..
    .#**#..
    .#*##..""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_containers_below():
    clay, water = parse("""
    ...+....
    ...~....
    .#****..
    .#**#*..
    .#**#*..
    .####*..
    .....*..
    ..*****#
    ..*#***#
    ..*#####""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_containers_below2():
    clay, water = parse("""
    ...+....
    ...~....
    #.#*....
    #.#****.
    #.#**#*
    #.#**#*.
    #****#*.
    ######*.
    .******#
    .*######""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_weird_container():
    clay, water = parse("""
    ..+......
    ..~......
    .#*******
    .#*#***#*
    .#*#*#*#*
    .#*###*#*
    .#*****#*
    .#######*""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_weird_container2():
    clay, water = parse("""
    ..+......
    ***#.#...
    *#*#.#.#.
    *#*###.#.
    *#*****#.
    *#######.""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_several_sources():
    clay, water = parse("""
    ....+.....
    ...~~~....
    ...*#*...
    ...*.*...
    .********.
    .*#****#*.
    .*######*.""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_several_sources2():
    clay, water = parse("""
    ...+.....
    ..~~~~...
    ..*##*...
    .#*****..
    .##**#*..
    ...****#.
    ...***##.
    ...***...
    .*******.
    .*#***#*.
    .*#####*.""")

    solution = clay.solve()
    print(clay)
    assert solution == water


def test_container_with_empty_box():
    clay, water = parse("""
    ......+...
    ......~...
    ....****#.
    .****#**#.
    .*#**#**#.
    .*#*****#.
    .*#######.""")
    solution = clay.solve()
    print(clay)
    assert solution == water


def test_container_with_box2():
    clay, water = parse("""
    ....+........
    ...~~~.......
    ...*#*.......
    ...*.*.......
    .************
    .*#********#*
    .*#********#*
    .*#****###*#*
    .*#****#.#*#*
    .*#****###*#*
    .*#********#*
    .*##########*.""")
    solution = clay.solve()
    print(clay)
    assert solution == water

def test_container_with_box3():
    clay, water = parse("""
    .....+....
    ..........
    .*******#.
    .*#*#*#*#.
    .*#*###*#.
    .*#*****#.
    .*#######.""")
    solution = clay.solve()
    print(clay)
    assert solution == water
