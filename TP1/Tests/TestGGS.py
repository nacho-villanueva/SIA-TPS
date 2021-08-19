import sys
from distutils.util import strtobool
from os.path import isfile

import arcade

from TP1.Algorithms.GlobalGreedySearch import GGS
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from TP1.heuristics import heuristic_1, get_heuristic_by_number


def main(file, test_deadlocks, heuristic):
    if not isfile(file):
        print(f"File not found: {file}")
        exit(1)
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    ggs = GGS(game, heuristic, test_deadlocks=test_deadlocks)
    solution = ggs.run()

    if solution:
        print(ggs.statistics)
        state = GameState.from_filepath(file)
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=True)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("GGS espera 3 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        heuristic_argv = get_heuristic_by_number(sys.argv[3])
        if heuristic_argv is None:
            print("Las heurísticas solo pueden ser indicadas con los valores \"1\", \"2\" o \"3\"")
        else:
            main(tablero_argv, bool(strtobool(test_deadlocks_argv)), heuristic_argv)
