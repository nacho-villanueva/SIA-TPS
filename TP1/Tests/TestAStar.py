import sys
from os.path import isfile

import arcade

from TP1.Algorithms.AStar import AStar
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication


def get_distance_from_player_to_closest_ice(sokoban: Sokoban):
    closest_ice = sokoban.get_nearest_ice_from_player()
    return abs(sokoban.state.player_position.x - closest_ice[0]) + abs(sokoban.state.player_position.y - closest_ice[1])


'''
    Devuelve la suma de las distancias de los hielos al objetivo mas cercano a ellos, 
    más la distancia del jugador al bloque más cercano
'''
def heuristic(sokoban: Sokoban):
    to_return = 0
    for ice in sokoban.state.save_state()[1]:
        nearest_end = sokoban.get_nearest_end_from_ice(ice)
        to_return += abs(nearest_end[0] - ice[0]) + abs(nearest_end[1] - ice[1])
    to_return += get_distance_from_player_to_closest_ice(sokoban)
    return to_return


def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)
    algorithm = AStar(sokoban, heuristic, test_deadlocks=True)
    movements = algorithm.run()
    shower_app = AlgorithmShowerApplication(sokoban, movements, update_rate=0.01, move_automatically=False)
    print(algorithm.statistics)
    Sokoban.check_if_movements_lead_to_repeated_state(movements, GameState.from_filepath(initial_state))
    arcade.run()


if __name__ == "__main__":
    config_file = "../TestCodes/testGame10.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)