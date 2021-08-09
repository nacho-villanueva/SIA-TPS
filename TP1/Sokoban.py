import enum

from TP1.GameState import GameState
from TP1.Position import Position


class Movement(enum.Enum):
    LEFT = Position(-1, 0)
    UP = Position(0, -1)
    RIGHT = Position(1, 0)
    DOWN = Position(0, 1)


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
        return self.state.is_ice_on_corner()

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
