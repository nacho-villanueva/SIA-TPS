from TP1.Sokoban import Sokoban

'''
    Devuelve la suma de las distancias de los hielos al objetivo mas cercano a ellos, 
    más la distancia del jugador al bloque más cercano
'''
def heuristic_1(sokoban: Sokoban):
    to_return = 0
    for ice in sokoban.state.save_state()[1]:
        nearest_end = sokoban.get_nearest_end_from_ice(ice)
        to_return += abs(nearest_end[0] - ice[0]) + abs(nearest_end[1] - ice[1])
    to_return += get_distance_from_player_to_closest_ice(sokoban)
    return to_return


'''
    Función auxiliar para heuristic_1
    TODO TODO TODO TODO TODO TODO TODO : ¿vale la pena hacer a esta funcion una heuristica propia?
'''
def get_distance_from_player_to_closest_ice(sokoban: Sokoban):
    closest_ice = sokoban.get_nearest_ice_from_player()
    return abs(sokoban.state.player_position.x - closest_ice[0]) + abs(sokoban.state.player_position.y - closest_ice[1])


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


def get_distance_from_player_to_closest_non_ended_ice(sokoban: Sokoban):
    closest_ice = sokoban.get_nearest_non_finished_ice_from_player()
    if closest_ice is None:
        # Sucede solo si el juego está ganado
        return 0
    return abs(sokoban.state.player_position.x - closest_ice[0]) + abs(sokoban.state.player_position.y - closest_ice[1])