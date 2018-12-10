from aoc2018 import readlines
from aoc2018.day09e1 import Game


if __name__ == '__main__':
    tokens = list(readlines())[0].split()
    players = int(tokens[0])
    max_marble = int(tokens[6]) * 100
    game = Game(players, max_marble)
    while not game.is_finished():
        game.turn()

    print(game.highest_score())
