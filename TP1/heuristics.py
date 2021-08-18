from TP1.Sokoban import Sokoban
from itertools import permutations

'''
    Distancia Manhattan del jugador a la caja más cercana que no esté sobre un objetivo
    +
    Distancia de esa caja al objetivo más cercano.
'''


def heuristic_1(sokoban: Sokoban):
    to_return = 0
    to_return += get_distance_from_player_to_closest_non_ended_ice(sokoban)
    ice = sokoban.get_nearest_non_finished_ice_from_player()
    if ice is not None:
        end = sokoban.get_nearest_end_from_ice(ice)
        to_return += abs(ice[0] - end[0]) + abs(ice[1] - end[1])
    return to_return


'''
    Devuelve la suma de las distancias de los hielos al objetivo mas cercano a ellos, 
    más la distancia del jugador al bloque más cercano que no esté sobre un goal
'''


def heuristic_2(sokoban: Sokoban):
    to_return = 0
    for ice in sokoban.state.save_state()[1]:
        nearest_end = sokoban.get_nearest_end_from_ice(ice)
        to_return += abs(nearest_end[0] - ice[0]) + abs(nearest_end[1] - ice[1])
    to_return += get_distance_from_player_to_closest_non_ended_ice(sokoban)
    return to_return


def heuristic_non_admisible(sokoban: Sokoban):
    dist = sokoban.get_sum_of_distance_to_non_finished_ice_from_player() + 1
    return 1 / dist


def get_distance_from_player_to_closest_non_ended_ice(sokoban: Sokoban):
    closest_ice = sokoban.get_nearest_non_finished_ice_from_player()
    if closest_ice is None:
        # Sucede solo si el juego está ganado
        return 0
    return abs(sokoban.state.player_position.x - closest_ice[0]) + abs(sokoban.state.player_position.y - closest_ice[1])


def get_distance_from_player_to_furthest_non_ended_ice(sokoban: Sokoban):
    furthest = sokoban.get_furthest_non_finished_ice_from_player()
    if furthest is None:
        # Sucede solo si el juego está ganado
        return 0
    return abs(sokoban.state.player_position.x - furthest[0]) + abs(sokoban.state.player_position.y - furthest[1])


'''
    Devuelve la suma de las distancias de los hielos a un objetivo particular.
    La elección de este objetivo es tal que la suma devuelva el número mínimo posible.
    Cada objetivo estará mapeado a solo un hielo
'''
def heuristic_3(sokoban: Sokoban):
    minimum_permutation_value = 0
    ice_positions = sokoban.state.save_state()[1]
    permutations_of_ices = permutations(ice_positions)
    first_call = True

    for permutation in permutations_of_ices:
        to_return = 0
        exclude_ends = []
        for ice in permutation:
            nearest_end = sokoban.get_nearest_end_from_ice(ice, exclude_ends=exclude_ends)
            to_return += abs(nearest_end[0] - ice[0]) + abs(nearest_end[1] - ice[1])
            exclude_ends.append(nearest_end)
        if first_call:
            first_call = False
            minimum_permutation_value = to_return
        elif to_return < minimum_permutation_value:
            minimum_permutation_value = to_return

    return minimum_permutation_value + get_distance_from_player_to_closest_non_ended_ice(sokoban)
