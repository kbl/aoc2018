import re          
from aoc2018 import readlines
from aoc2018.day10e1 import Sky, Star


if __name__ == '__main__':
    stars = [Star.parse(line) for line in lines.split('\n')]
    stars = [Star.parse(line) for line in readlines()]
    sky = Sky(stars)

    previous_diff_x = sky.max_x - sky.min_x

    while True:
        diff_x = sky.max_x - sky.min_x
        if diff_x > previous_diff_x:
            print(i - 1)
            break
        previous_diff_x = diff_x
        sky = sky.tick()
        if i % 1000 == 0:
            print(diff_x)
