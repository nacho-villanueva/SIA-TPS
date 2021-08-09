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
                val = ' '
                if state.dynamic_state[i][j] != GameState.EMPTY:
                    val = state.dynamic_state[i][j]
                else:
                    val = state.static_state[i][j]

                if val == GameState.WALL:
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH - SPACING, BLOCK_HEIGHT - SPACING,
                        arcade.color.WOOD_BROWN
                    )
                elif val == GameState.ICE or val == GameState.ICE_ON_END:
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH - SPACING, BLOCK_HEIGHT - SPACING,
                        arcade.color.LIGHT_BLUE
                    )
                elif val == GameState.PLAYER or val == GameState.PLAYER_ON_END:
                    arcade.draw_rectangle_filled(
                        BLOCK_WIDTH * j + BLOCK_WIDTH / 2,
                        self.window_height - BLOCK_HEIGHT * i - BLOCK_HEIGHT / 2,
                        BLOCK_WIDTH - SPACING, BLOCK_HEIGHT - SPACING,
                        arcade.color.TEA_GREEN
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


def get_code(config_path):
    # Check if file exists or raise and error
    if not os.path.isfile(config_path):
        raise Exception("File not found")

    # Open file and read all lines
    f = open(config_path, "r")
    lines = f.readlines()

    # Remove spaces at the end and get the longest legnth or the 
    # ammout of lines, whichever is greatest
    lines = list(map(lambda line: line.rstrip(), lines))
    max_len = reduce(lambda acc, el: len(el) if len(el) > acc else acc, lines, 0)
    max_len = max_len if max_len > len(lines) else len(lines)

    # Append spaces at the end and empty lines to form a square
    for i in range(len(lines)):
        if len(lines[i]) < max_len:
            lines[i] = lines[i] + " " * (max_len - len(lines[i]))
        if max_len - 1 > i:
            lines[i] = lines[i] + "\n"
    if max_len > len(lines):
        for _ in range(max_len - len(lines) - 1):
            lines.append(" " * max_len + "\n")
        lines.append(" " * max_len)

    # Join lines into a single string, close file and return string
    lines = "".join(line for line in lines)
    f.close()
    return lines


def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_code(get_code(initial_state))
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
