from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
import os
import arcade
import sys
from functools import reduce


class SokobanApplication(arcade.Window):
    def __init__(self, sokoban, window_height=600, window_width=600, window_title="SIA Sokoban", draw_interval=1,
                 resizable=True):
        super().__init__(window_width, window_height, window_title, resizable=resizable)

        self.sokoban = sokoban
        self.window_height = window_height
        self.window_width = window_width
        self.window_title = window_title
        self.draw_interval = draw_interval

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.sokoban.move(Movement.UP)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.sokoban.move(Movement.DOWN)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.sokoban.move(Movement.LEFT)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.sokoban.move(Movement.RIGHT)
        elif key == arcade.key.Q:
            self.close()


def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)

    sokoban_app = SokobanApplication(sokoban=sokoban)
    arcade.run()


if __name__ == "__main__":
    config_file = "./config.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.txt)")
    main(config_file)
