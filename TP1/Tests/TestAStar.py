import sys
from distutils.util import strtobool
from os.path import isfile

import arcade

from TP1.Algorithms.AStar import AStar
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from TP1.heuristics import heuristic_1, heuristic_2, heuristic_non_admisible, get_heuristic_by_number


def main(file, test_deadlocks, heuristic):
    if not isfile(file):
        print(f"File not found: {file}")
        exit(1)
    state = GameState.from_filepath(file)
    sokoban = Sokoban(state)
    algorithm = AStar(sokoban, heuristic, test_deadlocks=test_deadlocks)
    solution = algorithm.run()

    print(f"Solution found = {len(solution) > 0}")
    print(algorithm.statistics)
    state = GameState.from_filepath(file)
    shower_app = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25)
    arcade.run()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("A* espera 3 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        heuristic_argv = get_heuristic_by_number(sys.argv[3])
        if heuristic_argv is None:
            print("Las heurísticas solo pueden ser indicadas con los valores \"1\", \"2\" o \"3\"")
        else:
            main(tablero_argv, bool(strtobool(test_deadlocks_argv)), heuristic_argv)
