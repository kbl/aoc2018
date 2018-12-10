from aoc2018 import readlines

from collections import deque


class Circle:
    def __init__(self):
        self.marbles = deque([0])

    def turn(self, marble):
        if marble % 23 == 0:
            self.marbles.rotate(7)
            other_marble = self.marbles.pop()
            self.marbles.rotate(-1)
            return marble + other_marble

        self.marbles.rotate(-1)
        self.marbles.append(marble)
        return 0

    def __str__(self):
        line = []
        for i, m in enumerate(self.marbles):
            line.append(" %2d " % m)
        return "".join(line)


class Game:
    def __init__(self, players, max_marble):
        self.players = [0] * players
        self.max_marble = max_marble

        self._current_player = 0
        self._current_marble = 1

        self.circle = Circle()

    def highest_score(self):
        return max(self.players)

    def turn(self):
        points = self.circle.turn(self._current_marble)
        if points:
            self.players[self._current_player] += points
        self._current_player = (self._current_player + 1) % len(self.players)
        self._current_marble += 1

    def is_finished(self):
        return self.max_marble + 2 == self._current_marble

    def __str__(self):
        return "[%2d] %s" % (self._current_player, self.circle)


if __name__ == '__main__':
    tokens = list(readlines())[0].split()
    players = int(tokens[0])
    max_marble = int(tokens[6])
    game = Game(players, max_marble)
    while not game.is_finished():
        game.turn()

    print(game.highest_score())
