import sys
from os.path import isfile

import arcade

from TP1.Algorithms.AStar import AStar
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from TP1.heuristics import heuristic_1, heuristic_2


def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)
    algorithm = AStar(sokoban, heuristic_2, test_deadlocks=True)
    movements = algorithm.run()
    shower_app = AlgorithmShowerApplication(sokoban, movements, update_rate=0.01, move_automatically=False)
    print(algorithm.statistics)
    arcade.run()


if __name__ == "__main__":
    config_file = "../TestCodes/testGame10.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)