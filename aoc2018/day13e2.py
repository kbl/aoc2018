from enum import Enum
from aoc2018 import readlines
from aoc2018.day13e1 import CollisionException, Paths as P


class Paths(P):
    def tick(self):
        carts = {}
        for i, c in enumerate(sorted(self.carts.values())):
            if c.cords in carts:
                del carts[c.cords]
                continue

            new_cart = c.tick(self.options(c.cords))
            if new_cart.cords in carts:
                del carts[new_cart.cords]
                continue

            carts[new_cart.cords] = new_cart

        if len(carts) == 1:
            raise CollisionException(list(carts.values())[0].cords)
        self.carts = carts


if __name__ == '__main__':
    p = P.parse(readlines(strip=False))
    p = Paths(p.maze, p.carts, p.max_x, p.max_y)
    while True:
        p.tick()

