from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
import arcade
from functools import reduce


class AlgorithmShowerApplication(arcade.Window):
    def __init__(self, sokoban : Sokoban, solution: list(Movement), window_height=600, window_width=600, window_title="SIA Sokoban", draw_interval=1,
                 resizable=True):
        super().__init__(window_width, window_height, window_title, resizable=resizable,update_rate=draw_interval)
        
        self.sokoban = sokoban
        self.initial_state = sokoban.state.save_state()
        self.solution = solution
        self.solution_step = 0
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
    def on_update(self, delta_time: float):
        if len(self.solution) > 0:
            if self.solution_step == len(self.solution):
                self.sokoban.state.load_state(self.initial_state)
                self.solution_step = 0
            else:
                self.sokoban.move(self.solution[self.solution_step])
                self.solution_step += 1
                
            
        return super().on_update(delta_time)

    def on_resize(self, width: float, height: float):
        self.window_width = width
        self.window_height = height
        return super().on_resize(width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()