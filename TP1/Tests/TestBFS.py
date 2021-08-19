from distutils.util import strtobool
from os.path import isfile

import arcade
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
import sys
from TP1.Algorithms.BFS import BFS


def main(file, test_deadlocks):
    if not isfile(file):
        print(f"File not found: {file}")
        exit(1)
    state = GameState.from_filepath(file)
    sokoban = Sokoban(state)
    algorithm = BFS(sokoban, check_deadlock=test_deadlocks)
    algorithm.run()
    print(algorithm.statistics)
    shower_app = AlgorithmShowerApplication(sokoban, algorithm.run(), update_rate=1 / 4)
    arcade.run()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("BFS espera 2 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        main(tablero_argv, bool(strtobool(test_deadlocks_argv)))
