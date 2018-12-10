import re          
from aoc2018 import readlines


class Sky:
    def __init__(self, stars):
        self.stars = stars
        self.coordinates = {s.coordinates for s in stars}

    @property
    def max_x(self):
        return max([s.x for s in self.stars])

    @property
    def min_x(self):
        return min([s.x for s in self.stars])

    @property
    def max_y(self):
        return max([s.y for s in self.stars])

    @property
    def min_y(self):
        return min([s.y for s in self.stars])

    def tick(self):
        stars = [s.tick() for s in self.stars]
        sky = Sky(stars)
        return sky

    def __str__(self):
        minx = self.min_x
        miny = self.min_y
        maxx = self.max_x
        maxy = self.max_y
        lines = []
        for y in range(miny, maxy + 1):
            line = []
            for x in range(minx, maxx + 1):
                if (x, y) in self.coordinates:
                    line.append('#')
                else:
                    line.append('.')
            lines.append(''.join(line))
        return '\n'.join(lines)


class Star:
    DATA_REGEXP = re.compile("< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>")

    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.coordinates = (x, y)

    def tick(self):
        return Star(self.x + self.velocity_x,
                    self.y + self.velocity_y,
                    self.velocity_x,
                    self.velocity_y)

    @staticmethod
    def parse(line):
        x, y, vel_x, vel_y = map(int, Star.DATA_REGEXP.search(line).groups())
        return Star(x, y, vel_x, vel_y)

lines = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""



if __name__ == '__main__':
    stars = [Star.parse(line) for line in readlines()]
    sky = Sky(stars)

    previous_diff_x = sky.max_x - sky.min_x

    i = 0
    while True:
        diff_x = sky.max_x - sky.min_x
        if diff_x > previous_diff_x:
            print(previous_sky)
            break
        previous_diff_x = diff_x
        previous_sky = sky
        sky = sky.tick()
        i += 1
        if i % 1000 == 0:
            print(diff_x)
