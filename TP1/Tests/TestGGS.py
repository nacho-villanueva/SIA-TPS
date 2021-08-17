import sys

import arcade

from TP1.Algorithms.GlobalGreedySearch import GGS
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from TP1.heuristics import heuristic_1


def main(file):
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    ggs = GGS(game, heuristic_1)
    solution = ggs.run()

    if solution:
        print(ggs.statistics)
        state = GameState.from_filepath(file)
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=True)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    config_file = "../TestCodes/testGame1.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (../config.txt)")
    main(config_file)
