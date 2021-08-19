import sys
from distutils.util import strtobool
from os.path import isfile

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file, test_deadlocks):
    if not isfile(file):
        print(f"File not found: {file}")
        exit(1)
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    iddfs = IDDFS(game, 500, 5, 5, test_deadlocks=test_deadlocks)
    solution = iddfs.run()

    if solution:
        print(iddfs.statistics)
        state = GameState.from_filepath(file)
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("IDDFS espera 2 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        main(tablero_argv, bool(strtobool(test_deadlocks_argv)))