import arcade
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban

class SokobanBasicApplication(arcade.Window):
    def __init__(
                self, sokoban:Sokoban, window_height=600, window_width=600, 
                window_title="SIA Sokoban", update_rate=1,
                resizable=True
        ):
        
        super().__init__(
            window_width, window_height, 
            window_title, resizable=resizable,
            update_rate=update_rate
        )

        self.sokoban = sokoban
        self.window_height = window_height
        self.window_width = window_width

    def on_draw(self):
        # Iterate through the states and draw
        state = self.sokoban.state
        BLOCK_WIDTH = int(self.window_width / state.dimensions[1])
        BLOCK_HEIGHT = int(self.window_height / state.dimensions[0])
        SPACING = 10

        arcade.start_render()
        for i in range(state.dimensions[0]):
            for j in range(state.dimensions[1]):
                dyn_val = state.get_dynamic_block((j, i))
                sta_val = state.static_state[i][j]

                if sta_val == GameState.WALL:
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH - SPACING, BLOCK_HEIGHT - SPACING,
                        arcade.color.WOOD_BROWN
                    )
                elif sta_val == GameState.END:
                    color = arcade.color.AMARANTH_PURPLE
                    if dyn_val == GameState.ICE:
                        color = arcade.color.APPLE_GREEN
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH, BLOCK_HEIGHT,
                        color
                    )

                if dyn_val == GameState.ICE:
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH - SPACING, BLOCK_HEIGHT - SPACING,
                        arcade.color.LIGHT_BLUE
                    )
                arcade.draw_circle_filled(
                    BLOCK_WIDTH * state.player_position.x + BLOCK_WIDTH / 2,
                    self.window_height - BLOCK_HEIGHT * state.player_position.y - BLOCK_HEIGHT / 2,
                    BLOCK_WIDTH / 2,
                    arcade.color.BLUE_VIOLET
                )

    def on_resize(self, width: float, height: float):
        self.window_width = width
        self.window_height = height
        return super().on_resize(width, height)
