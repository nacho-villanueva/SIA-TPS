import sys

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file, max_depth=100, min_depth=1):
    state = GameState.from_filepath("../config.txt")
    game = Sokoban(state)
    iddfs = IDDFS(game, max_depth)
    solution = iddfs.run(minimum_depth=min_depth)

    if solution:
        state = GameState.from_filepath("../config.txt")
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=False)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    config_file = "./config.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (../config.txt)")
    main(config_file)
