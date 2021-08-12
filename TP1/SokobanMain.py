from os.path import isfile
from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement
from SokobanBasicApplication import SokobanBasicApplication
import arcade
import sys


class SokobanApplication(SokobanBasicApplication):
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
