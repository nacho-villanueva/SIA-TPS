import sys

import arcade

from TP1.Algorithms.AStar import AStar
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from TP1.heuristics import heuristic_1, heuristic_2, heuristic_non_admisible
from TP1.heuristics2 import get_heuristic1


def main(file):
    state = GameState.from_filepath(file)
    sokoban = Sokoban(state)
    algorithm = AStar(sokoban, heuristic_1, test_deadlocks=True)
    solution = algorithm.run()

    print(f"Solution found = {len(solution) > 0}")
    print(algorithm.statistics)
    state = GameState.from_filepath(file)
    shower_app = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.01, move_automatically=False)
    arcade.run()


if __name__ == "__main__":
    config_file = "../TestCodes/testGame1.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)
