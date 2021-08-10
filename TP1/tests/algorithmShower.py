from TP1.sokobanBasicApplication import SokobanBasicApplication
from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
import arcade
from functools import reduce


class AlgorithmShowerApplication(SokobanBasicApplication):
    def __init__(
            self, sokoban : Sokoban, solution: list(Movement), 
            window_height=600, window_width=600, window_title="SIA Sokoban", 
            update_rate=1,resizable=True
        ):
        
        super().__init__(
            sokoban=sokoban,
            window_width=window_width, window_height=window_height, 
            window_title=window_title, resizable=resizable,update_rate=update_rate
        )
        
        self.initial_state = sokoban.state.save_state()
        self.solution = solution
        self.solution_step = 0

    def on_update(self, delta_time: float):
        if len(self.solution) > 0:
            if self.solution_step == len(self.solution):
                self.sokoban.state.load_state(self.initial_state)
                self.solution_step = 0
            else:
                self.sokoban.move(self.solution[self.solution_step])
                self.solution_step += 1
                
            
        return super().on_update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()