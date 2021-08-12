import sys

import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS3 import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def main(file):
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    iddfs = IDDFS(game, 500, 50, 10)
    solution = iddfs.run()

    if solution:
        print(iddfs.statistics)
        state = GameState.from_filepath(file)
        asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=True)
        arcade.run()
    else:
        print("No solution found.")


if __name__ == "__main__":
    config_file = "../TestCodes/testGame6.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (../config.txt)")
    main(config_file)

# 1,1 Stats:( deepness: 78, cost: 78,expanded_nodes: 8283,frontier_nodes: 28,time_spent: 0.6580321788787842)
# 1,2 Stats:( deepness: 78, cost: 78,expanded_nodes: 11300,frontier_nodes: 26,time_spent: 0.6757955551147461)
# 10,10 tats:( deepness: 78, cost: 78,expanded_nodes: 21182,frontier_nodes: 32,time_spent: 0.8815629482269287)
# 70,10 Stats:( deepness: 78, cost: 78,expanded_nodes: 21182,frontier_nodes: 32,time_spent: 0.8960270881652832)
# 78,1 Stats:( deepness: 78, cost: 78,expanded_nodes: 8283,frontier_nodes: 28,time_spent: 0.6809995174407959)