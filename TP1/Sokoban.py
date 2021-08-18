import enum

from TP1.GameState import GameState
from TP1.Position import Position


class Movement(enum.Enum):
    LEFT = Position(-1, 0)
    UP = Position(0, -1)
    RIGHT = Position(1, 0)
    DOWN = Position(0, 1)

def manhattan_distance(pos1,pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])


class Sokoban:
    """
    Implementation of Sokoban's game logic
    """

    def __init__(self, initial_state: GameState):
        self.state = initial_state

    def is_empty_block(self, pos: Position):
        return self.state.get_dynamic_block((pos.x, pos.y)) == self.state.get_static_block((pos.x, pos.y)) == GameState.EMPTY

    def is_empty_end_block(self, pos: Position):
        return self.state.get_dynamic_block((pos.x, pos.y)) == GameState.EMPTY and self.state.get_static_block((pos.x, pos.y)) == GameState.END

    def is_walkable_block(self, pos: Position):
        return self.state.get_dynamic_block((pos.x, pos.y)) == GameState.EMPTY and (self.state.get_static_block((pos.x, pos.y)) in [GameState.EMPTY, GameState.END])

    def is_valid_movement(self, movement: Movement):
        move_to = movement.value + self.state.player_position

        if self.state.is_out_of_bound(move_to):
            return False

        if self.is_walkable_block(move_to):
            return True

        if self.state.get_dynamic_block(move_to) == GameState.ICE:
            if self.is_walkable_block(move_to + movement.value):
                return True

        return False

    def is_game_over(self):
        return self.state.is_ice_on_corner_and_not_in_end()

    def is_game_won(self):
        return self.state.is_all_ice_on_end()

    def get_possible_movements(self):
        possible_movements = []
        for m in Movement:
            if self.is_valid_movement(m):
                possible_movements.append(m)
        return possible_movements

    def move(self, movement: Movement):
        move_to = self.state.player_position + movement.value

        if self.is_valid_movement(movement):
            if self.state.get_dynamic_block(move_to) == GameState.ICE:
                new_ice_pos = move_to + movement.value
                self.state.add_dynamic_block(new_ice_pos.x, new_ice_pos.y, GameState.ICE)
                self.state.remove_dynamic_block(move_to.x, move_to.y)
            self.state.move_player(move_to)
        else:
            print("Invalid Movement. State unchanged.")

    # útil para chequear si un array de movimientos realmente lleva a una solucion sin pasar por estado repetidos
    @staticmethod
    def check_if_movements_lead_to_repeated_state(movement_array, initial_state):
        new_sokoban = Sokoban(initial_state)
        array_de_estados_sin_repetir = [new_sokoban.state.save_state()]
        for mov in movement_array:
            new_sokoban.move(mov)
            new_state = new_sokoban.state.save_state()
            if new_state not in array_de_estados_sin_repetir:
                array_de_estados_sin_repetir.append(new_sokoban.state.save_state())
            else:
                print("El array de movimientos está mal, ya que en un momento te hace ir a un estado repetido")
        print("El array de movimientos genera una secuencia correcta de estados sin repetir")

    # Devuelve el ice mas cercano al player
    def get_nearest_ice_from_player(self):
        state = self.state.save_state()
        player_position = state[0]
        nearest_ice = None
        nearest_dist = 0
        for ice_position in state[1]:
            ice_dist = manhattan_distance(ice_position,player_position)
            if nearest_ice is None or ice_dist < nearest_dist:
                nearest_ice = ice_position
                nearest_dist = ice_dist
        return nearest_ice

    # Devuelve el ice más cercano al player que NO esté sobre un END
    def get_nearest_non_finished_ice_from_player(self):
        state = self.state.save_state()
        player_position = state[0]
        nearest_ice = None
        nearest_dist = 0
        for ice_position in state[1]:
            if self.state.get_static_block(ice_position) != GameState.END:
                ice_dist = manhattan_distance(player_position,ice_position)
                if nearest_ice is None or  ice_dist < nearest_dist:
                    nearest_ice = ice_position
                    nearest_dist = ice_dist
        return nearest_ice

    def get_sum_of_distance_to_non_finished_ice_from_player(self):
        total_dist = 0
        for ice_position in self.state.dynamic_state:
            if self.state.get_static_block(ice_position) != GameState.END:
                total_dist += abs(ice_position[0] - self.state.player_position.x) + abs(ice_position[1] - self.state.player_position.y)
        return total_dist

    def get_furthest_non_finished_ice_from_player(self):
        furthest_ice = None
        furthest_dist = 0
        for ice_position in self.state.dynamic_state:
            if self.state.get_static_block(ice_position) != GameState.END:
                ice_dist = abs(ice_position[0] - self.state.player_position.x) + abs(ice_position[1] - self.state.player_position.y)
                if  ice_dist > furthest_dist:
                    furthest_ice = ice_position
                    furthest_dist = ice_dist
        return furthest_ice

    def get_nearest_end_from_ice(self, ice: tuple[int, int], exclude_ends=None):
        if exclude_ends is None:
            exclude_ends = []
        nearest_end = None
        nearest_dist = 0
        for end_position in self.state.end_positions:
            if end_position not in exclude_ends:
                end_dist = manhattan_distance(end_position,ice)
                if nearest_end is None or  end_dist < nearest_dist:
                    nearest_end = end_position
                    nearest_dist = end_dist
        return nearest_end