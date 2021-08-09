from pprint import pprint
from typing import Union

from django.conf.locale import pl
from line_profiler_pycharm import profile

from TP1.Position import Position


class GameState:
    """
    Class for maintaining the state of the game
    """

    # Static Blocks
    WALL = "#"
    END = "."

    # Dynamic Blocks
    ICE = "$"
    PLAYER = "@"

    # Both
    EMPTY = " "

    # Only used for Parsing
    PLAYER_ON_END = "+"
    ICE_ON_END = "*"

    @staticmethod
    def from_code(code: str):

        player_position = Position(-1, -1)

        static_state = []
        dynamic_state = {}

        state = code.split("\n")
        dim = (len(state[0]), len(state))

        for y, row in enumerate(state):
            if len(row) != dim[0]:
                print(repr(row), repr(state[0]))
                raise Exception("Malformed Code. Code is not square.")

            static_row = []

            for x, b in enumerate(row):
                if b == GameState.WALL or b == GameState.END:
                    static_row.append(b)
                elif b == GameState.ICE:
                    static_row.append(GameState.EMPTY)
                    dynamic_state[(x, y)] = GameState.ICE
                elif b == GameState.PLAYER:
                    static_row.append(GameState.EMPTY)
                    player_position = Position(x, y)
                elif b == GameState.EMPTY:
                    static_row.append(GameState.EMPTY)
                elif b == GameState.PLAYER_ON_END:
                    static_row.append(GameState.END)
                    player_position = Position(x, y)
                elif b == GameState.ICE_ON_END:
                    static_row.append(GameState.END)
                    dynamic_state[(x, y)] = GameState.ICE
                else:
                    raise Exception(f"Malformed Code. Invalid simbol at ({x},{y}): {repr(b)}")

            static_state.append(static_row)

        if player_position.x == -1:
            raise Exception("Malformed Code. Player not found")
        return GameState(static_state, dynamic_state, player_position)

    def __init__(self, static_state: list[list[str]], initial_dynamic_state: dict[tuple[int, int], str], initial_player_position: Position):
        self.dimensions = (len(static_state[0]), len(static_state))
        self.dynamic_state = initial_dynamic_state
        self.static_state = static_state
        self.player_position = initial_player_position

# TODO: IMPROVE
    def get_static_block(self, pos: tuple[int, int]):
        if pos[0] < 0 or pos[0] > self.dimensions[0] or pos[1] < 0 or pos[1] > self.dimensions[1]:
            # If block is out of bound
            return GameState.EMPTY
        return self.static_state[pos[1]][pos[0]]

# TODO: IMPROVE
    def get_dynamic_block(self, pos: Union[Position, tuple[int, int]]):
        position = pos
        if type(pos) == tuple:
            position = Position(pos[0], pos[1])
        if position.x < 0 or position.x > self.dimensions[0] or position.y < 0 or position.y > self.dimensions[1]:
            # If block is out of bound
            return GameState.EMPTY
        if (position.x, position.y) not in self.dynamic_state:
            return GameState.EMPTY
        return self.dynamic_state[(position.x, position.y)]

    def add_dynamic_block(self, x: int, y: int, value: str):
        self.dynamic_state[(x, y)] = value

    def remove_dynamic_block(self, x: int, y: int):
        self.dynamic_state.pop((x, y))

    def move_player(self, move_to: Position):
        self.player_position = move_to

    def is_out_of_bound(self, pos: Position):
        return pos.x < 0 or pos.x > self.dimensions[0] or pos.y < 0 or pos.y > self.dimensions[1]

    def save_state(self):
        state = ((self.player_position.x, self.player_position.y), tuple(self.dynamic_state.keys()))
        return state

    def load_state(self, load_state):
        self.dynamic_state = {}

        for i in load_state[1]:
            self.add_dynamic_block(i[0], i[1], GameState.ICE)
        self.player_position = Position(load_state[0][0], load_state[0][1])

    # TODO: CAN BE OPTIMIZED BY USING A DICTIONARY/ARRAY OF POSITIONS INSTEAD OF A MATRIX FOR DYNAMIC_STATE
    def is_ice_on_corner(self):
        for db in self.dynamic_state:
            if self.dynamic_state[db] == GameState.ICE:
                x, y = db
                walls = [
                    self.get_static_block((x - 1, y)) == GameState.WALL,  # Left
                    self.get_static_block((x, y - 1)) == GameState.WALL,  # Top
                    self.get_static_block((x + 1, y)) == GameState.WALL,  # Right
                    self.get_static_block((x, y + 1)) == GameState.WALL  # Bottom
                ]
                is_adjacent_wall = False
                for i in range(5):
                    if walls[i % 4]:
                        if is_adjacent_wall:
                            return True
                    is_adjacent_wall = walls[i % 4]
        return False

    # TODO: ES TARDE, NO QUIERO PENSAR EN UN MEJOR NOMBRE...
    def is_all_ice_on_end(self):
        for db in self.dynamic_state:
            if self.dynamic_state[db] == GameState.ICE and self.get_static_block(db) != GameState.END:
                return False
        return True

    def __str__(self):
        string = ""

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                db = self.get_dynamic_block((x, y))
                sb = self.get_static_block((x, y))

                if sb == GameState.END:
                    if db == GameState.PLAYER:
                        string += GameState.PLAYER_ON_END
                    elif db == GameState.ICE:
                        string += GameState.ICE_ON_END
                    else:
                        string += GameState.END
                else:
                    if sb != GameState.EMPTY:
                        string += sb
                    elif db != GameState.EMPTY:
                        string += db
                    else:
                        string += GameState.EMPTY
            string += "\n"
        return string[:-1]
