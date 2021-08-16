import sys

import arcade

from TP1.Algorithms.GlobalGreedySearch import GGS
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.Algorithms.IDDFS import IDDFS
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def get_distance_from_player_to_closest_ice(sokoban: Sokoban):
    closest_ice = sokoban.get_nearest_ice_from_player()
    return abs(sokoban.state.player_position.x - closest_ice[0]) + abs(sokoban.state.player_position.y - closest_ice[1])


def heuristic(sokoban: Sokoban):
    to_return = 0
    for ice in sokoban.state.save_state()[1]:
        nearest_end = sokoban.get_nearest_end_from_ice(ice)
        to_return += abs(nearest_end[0] - ice[0]) + abs(nearest_end[1] - ice[1])
    to_return += get_distance_from_player_to_closest_ice(sokoban)
    return to_return


def main(file):
    state = GameState.from_filepath(file)
    game = Sokoban(state)
    ggs = GGS(game, heuristic)
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
