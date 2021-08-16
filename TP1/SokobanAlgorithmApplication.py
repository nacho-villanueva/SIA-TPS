from TP1.SokobanBasicDisplay import SokobanBasicApplication
from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
import arcade
from functools import reduce


class AlgorithmShowerApplication(SokobanBasicApplication):
    def __init__(
            self, sokoban: Sokoban, solution: list[Movement], window_title="SIA Sokoban",
            update_rate=1, resizable=True, move_automatically=True
    ):

        super().__init__(
            sokoban=sokoban, window_title=window_title, resizable=resizable, update_rate=update_rate
        )

        self.initial_state = sokoban.state.save_state()
        self.solution = solution
        self.solution_step = 0
        self.move_automatically = move_automatically

    def update_state(self):
        if len(self.solution) > 0:
            if self.solution_step == len(self.solution):
                self.sokoban.state.load_state(self.initial_state)
                self.solution_step = 0
            else:
                self.sokoban.move(self.solution[self.solution_step])
                self.solution_step += 1

    def on_update(self, delta_time: float):
        if self.move_automatically:
            self.update_state()

        return super().on_update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()
        if key == arcade.key.SPACE:
            self.update_state()
        if key == arcade.key.A:
            self.move_automatically = not self.move_automatically
