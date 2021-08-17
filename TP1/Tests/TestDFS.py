import sys

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.DFS import DFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file):
    state = GameState.from_filepath(file)
    sokoban = Sokoban(state)
    algorithm = DFS(sokoban, test_deadlocks=True, random_choose=False)
    solution = algorithm.run()

    if solution:
        print("Solution found!")
        print(algorithm.statistics)
        state = GameState.from_filepath(file)
        shower_app = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.01)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    config_file = "../TestCodes/testGame1.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)
