from aoc2018.day17e1 import Clay, Surface, Drop
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
                symbols.add((x, y))

    return symbols


def test_expand():
    representation = """
    ...v...
    ..###.."""
    clay = parse_symbol(representation, '#')
    water = parse_symbol(representation, '~')
    [drop] = list(parse_symbol(representation, 'v'))
    drop = Drop(drop)
    new_drop, s = drop.drip(clay, water)
    assert new_drop is None
    assert s.left == (1, 0)
    assert s.right == (5, 0)
    assert s.water == set([(x, 0) for x in range(1, 6)])
 
 
def test_expand_clay_on_right():
    representation = """
    ...v.#.
    ..####."""
    clay = parse_symbol(representation, '#')
    water = parse_symbol(representation, '~')
    [drop] = list(parse_symbol(representation, 'v'))
    drop = Drop(drop)
    _, s = drop.drip(clay, water)

    assert s.left == (1, 0)
    assert s.right == (4, 0)


def test_expand_clay_on_left():
    representation = """
    .#.v..
    .####."""
    clay = parse_symbol(representation, '#')
    water = parse_symbol(representation, '~')
    [drop] = list(parse_symbol(representation, 'v'))
    drop = Drop(drop)
    _, s = drop.drip(clay, water)

    assert s.left == (2, 0)
    assert s.right == (5, 0)


def test_expand_on_water():
    representation = """
    ...v....
    .~##~~#."""
    clay = parse_symbol(representation, '#')
    water = parse_symbol(representation, '~')
    [drop] = list(parse_symbol(representation, 'v'))
    drop = Drop(drop)
    _, s = drop.drip(clay, water)
    assert s.left == (1, 0)
    assert s.right == (7, 0)


# def test_drop_on_water():
#     representation = """
#     ..v..
#     .~~~."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     new_drop, new_surface = drop.drip(clay, water)
#     assert new_drop is None
#     assert new_surface is None
# 
# 
# def test_drop_on_air():
#     representation = """
#     ..v..
#     .#.#."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     new_drop, new_surface = drop.drip(clay, water)
#     assert new_drop == (2, 1)
#     assert new_surface is None
# 
# 
# def test_produces_clay_on_left():
#     representation = """
#     .#.v..
#     .####."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     _, s = drop.drip(clay, water)
#     [new_drop] = s.drops
# 
#     assert new_drop == (5, 1)
# 
# 
# def test_produces_clay_on_right():
#     representation = """
#     ..v.#.
#     .####."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     _, s = drop.drip(clay, water)
#     [new_drop] = s.drops
# 
#     assert new_drop == (0, 1)
# 
# 
# def test_produces_clay_below():
#     representation = """
#     ..v..
#     .###."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     _, s = drop.drip(clay, water)
#     [new_d1, new_d2] = s.drops
# 
#     assert new_d1 == (0, 1)
#     assert new_d2 == (4, 1)
# 
# 
# def test_produces_water_below():
#     representation = """
#     ..v..
#     .###~"""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     _, s = drop.drip(clay, water)
#     [new_drop] = s.drops
# 
#     assert new_drop == (0, 1)
# 
# 
# def test_produces_clay_only_on_side():
#     representation = """
#     .#v..
#     ....."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     new_drop, s = drop.drip(clay, water)
# 
#     assert s is None
#     assert new_drop == (2, 1)
# 
# 
# def test_produces_container_with_hole():
#     representation = """
#     .#.v#.
#     .#.##."""
#     clay = parse_symbol(representation, '#')
#     water = parse_symbol(representation, '~')
#     [drop] = list(parse_symbol(representation, 'v'))
#     drop = Drop(drop)
#     new_drop, s = drop.drip(clay, water)
#     [newer_drop] = s.drops
# 
#     assert new_drop is None
#     assert s.left == (2, 0)
#     assert s.right == (3, 0)
#     assert newer_drop == (2, 1)
# 
# 
# def test_parsing():
#     clay, water = parse("""
#     ...+...
#     ..~~~..
#     ..*#*..
#     ..*#*..""")
#     assert len(clay.clay) == 2
#     assert (500, 2) in clay.clay
#     assert (500, 3) in clay.clay
#     assert clay.miny == 2
#     assert clay.maxy == 3
#     assert water == 4
# 
# 
# def test_str():
#     clay, _ = parse("""
#     ...+...
#     .......
#     .......
#     ...#...""")
#     clay.solve()
#     print(clay)
#     assert str(clay) == """.+.
# .~.
# ~~~
# ~#~"""
# 
# 
# def test_basic_solve():
#     clay, water = parse("""
#     ...+...
#     ...~...
#     ..~~~..
#     ..*#*...""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_basic_container():
#     clay, water = parse("""
#     ...+...
#     .~~~~~.
#     .*#*#*.
#     .*###*..""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_overflow_right():
#      clay, water = parse("""
#      ...+...
#      ...~...
#      ..#***.
#      ..#*#*.
#      ..###*..""")
#      solution = clay.solve()
#      print(clay)
#      assert solution == water
# 
# 
# def test_overflow_left():
#     clay, water = parse("""
#     ...+...
#     ...~...
#     .***#..
#     .*#*#..
#     .*###..""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_container_with_hole():
#     clay, water = parse("""
#     ...+...
#     ...~...
#     .#.*#..
#     .#**#..
#     .#*##..""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_containers_below():
#     clay, water = parse("""
#     ...+....
#     ...~....
#     .#****..
#     .#**#*..
#     .#**#*..
#     .####*..
#     .....*..
#     ..*****#
#     ..*#***#
#     ..*#####""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_containers_below():
#     clay, water = parse("""
#     ...+....
#     ...~....
#     #.#*....
#     #.#****.
#     #.#**#*
#     #.#**#*.
#     #****#*.
#     ######*.
#     .******#
#     .*######""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_weird_container():
#     clay, water = parse("""
#     ..+......
#     ..~......
#     .#*******
#     .#*#***#*
#     .#*#*#*#*
#     .#*###*#*
#     .#*****#*
#     .#######*""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_weird_container2():
#     clay, water = parse("""
#     ..+......
#     ***#.#...
#     *#*#.#.#.
#     *#*###.#.
#     *#*****#.
#     *#######.""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_several_sources():
#     clay, water = parse("""
#     ....+.....
#     ...~~~....
#     ...*#*...
#     ...*.*...
#     .********.
#     .*#****#*.
#     .*######*.""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_several_sources2():
#     clay, water = parse("""
#     ...+.....
#     ..~~~~...
#     ..*##*...
#     .#*****..
#     .##**#*..
#     ...****#.
#     ...***##.
#     ...***...
#     .*******.
#     .*#***#*.
#     .*#####*.""")
# 
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_container_with_empty_box():
#     clay, water = parse("""
#     ......+...
#     ......~...
#     ....****#.
#     .****#**#.
#     .*#**#**#.
#     .*#*****#.
#     .*#######.""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# 
# def test_container_with_box2():
#     clay, water = parse("""
#     ....+........
#     ...~~~.......
#     ...*#*.......
#     ...*.*.......
#     .************
#     .*#********#*
#     .*#********#*
#     .*#****###*#*
#     .*#****#.#*#*
#     .*#****###*#*
#     .*#********#*
#     .*##########*.""")
#     solution = clay.solve()
#     print(clay)
#     assert solution == water
# 
# # ...+...
# # ...v...
# # .~~~~~#
# # #~#~#~#
# # #~###~#
# # #~~~~~#
# # #######
# 
# 
# # def test_container_with_box3():
# #     clay, water = parse("""
# #     .....+....
# #     ..........
# #     .*******#.
# #     .*#*#*#*#.
# #     .*#*###*#.
# #     .*#*****#.
# #     .*#######.""")
# #     solution = clay.solve()
# #     print(clay)
# #     assert solution == water
