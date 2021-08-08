from pprint import pprint

from TP1.Position import Position


class GameState:
    """
    Class for maintaining the state of the game
    """

    # Static Blocks
    BLOCK_WALL = "#"
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

        static_state = []
        dynamic_state = []

        state = code.split("\n")
        dim = (len(state[0]), len(state))

        y = 0

        for row in state:
            x = 0
            if len(row) != dim[0]:
                raise Exception("Malformed Code. Code is not square.")

            static_row = []
            dynamic_row = []

            for b in row:
                if b == GameState.BLOCK_WALL or b == GameState.END:
                    static_row.append(b)
                    dynamic_row.append(GameState.EMPTY)
                elif b == GameState.ICE or b == GameState.PLAYER:
                    static_row.append(GameState.EMPTY)
                    dynamic_row.append(b)
                elif b == GameState.EMPTY:
                    static_row.append(GameState.EMPTY)
                    dynamic_row.append(GameState.EMPTY)
                elif b == GameState.PLAYER_ON_END:
                    static_row.append(GameState.END)
                    dynamic_row.append(GameState.PLAYER)
                elif b == GameState.ICE_ON_END:
                    static_row.append(GameState.END)
                    dynamic_row.append(GameState.ICE)
                else:
                    raise Exception(f"Malformed Code. Invalid simbol at ({x},{y}): {repr(b)}")
                x += 1

            static_state.append(static_row)
            dynamic_state.append(dynamic_row)
            y += 1
        return GameState(static_state, dynamic_state)

    def get_player_position(self):
        for y in range(len(self.dynamic_state)):
            for x in range(len(self.dynamic_state[y])):
                if self.dynamic_state[y][x] == GameState.PLAYER:
                    return Position(x, y)

    def __init__(self, static_state: list[list[str]], initial_dynamic_state: list[list[str]]):

        if len(static_state) != len(initial_dynamic_state) or len(static_state[0]) != len(initial_dynamic_state[0]):
            raise Exception("Static State and Dynamic State have different sizes")

        self.dimensions = (len(static_state[0]), len(static_state))
        self.dynamic_state = initial_dynamic_state
        self.static_state = static_state
        self.player_position = self.get_player_position()

    def get_static_block(self, pos: Position):
        if pos.x < 0 or pos.x > self.dimensions[0] or pos.y < 0 or pos.y > self.dimensions[1]:
            # If block is out of bound
            return GameState.EMPTY
        return self.static_state[pos.y][pos.x]

    def get_dynamic_block(self, pos: Position):
        if pos.x < 0 or pos.x > self.dimensions[0] or pos.y < 0 or pos.y > self.dimensions[1]:
            # If block is out of bound
            return GameState.EMPTY
        return self.dynamic_state[pos.y][pos.x]

    def update_dynamic_block(self, pos: Position, value: str):
        self.dynamic_state[pos.y][pos.x] = value

    def move_player(self, move_to: Position):
        self.update_dynamic_block(move_to, GameState.PLAYER)
        self.update_dynamic_block(self.player_position, GameState.EMPTY)
        self.player_position = move_to

    def is_out_of_bound(self, pos: Position):
        return pos.x < 0 or pos.x > self.dimensions[0] or pos.y < 0 or pos.y > self.dimensions[1]

    def save_state(self):
        return None

    def load_state(self):
        pass

    def __str__(self):
        string = ""

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                db = self.get_dynamic_block(Position(x, y))
                sb = self.get_static_block(Position(x, y))

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
        return string
