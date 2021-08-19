import sys
import argparse
from distutils.util import strtobool
from os.path import isfile

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.DFS import DFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file, test_deadlocks):
    if not isfile(file):
        print(f"File not found: {file}")
        exit(1)
    state = GameState.from_filepath(file)
    sokoban = Sokoban(state)
    algorithm = DFS(sokoban, test_deadlocks=test_deadlocks)
    solution = algorithm.run()

    print(f"Solution found = {len(solution) > 0}")
    print(algorithm.statistics)
    state = GameState.from_filepath(file)
    shower_app = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.01)
    arcade.run()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("DFS espera 2 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        main(tablero_argv, bool(strtobool(test_deadlocks_argv)))
