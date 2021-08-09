from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
import os
import arcade
import sys
from functools import reduce
from TP1.algorithms.BFS import BFS

def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)
    algo = BFS(sokoban)
    print(algo.run())


if __name__ == "__main__":
    config_file = "./config.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)
