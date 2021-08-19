from distutils.util import strtobool

import arcade
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
import sys
from TP1.Algorithms.IDAStar import IDAStar
from TP1.heuristics import heuristic_1, heuristic_2, heuristic_3, get_heuristic_by_number
from TP1.heuristics2 import get_heuristic1
    

def main(initial_state, test_deadlocks, heuristic):
    if not isfile(initial_state):
        print(f"File not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)
    algorithm = IDAStar(sokoban, heuristic, test_deadlocks=test_deadlocks)
    algorithm.run()
    print(algorithm.statistics)
    shower_app = AlgorithmShowerApplication(sokoban, algorithm.run(), update_rate=0.25)
    arcade.run()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("IDA* espera 3 argumentos de entrada. Leer README para ver cómo invocarlo")
    else:
        tablero_argv = sys.argv[1]
        test_deadlocks_argv = sys.argv[2]
        heuristic_argv = get_heuristic_by_number(sys.argv[3])
        if heuristic_argv is None:
            print("Las heurísticas solo pueden ser indicadas con los valores \"1\", \"2\" o \"3\"")
        else:
            main(tablero_argv, bool(strtobool(test_deadlocks_argv)), heuristic_argv)
