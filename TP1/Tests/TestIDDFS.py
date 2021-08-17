import sys

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file):
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    iddfs = IDDFS(game, 500, 5, 5)
    solution = iddfs.run()

    if solution:
        print(iddfs.statistics)
        state = GameState.from_filepath(file)
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=True)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    config_file = "../TestCodes/testGame1.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (../config.txt)")
    main(config_file)