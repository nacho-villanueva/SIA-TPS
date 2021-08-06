from TP1.GameState import GameState
from TP1.Sokoban import Sokoban,Movement
import os
import arcade
import sys
from functools import reduce


# Constants
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
WINDOW_TITLE = "SIA Sokoban"
DRAW_INTERVAL = 1

def ondraw(dt):
    # Iterate through the states and draw
    state = ondraw.sokoban.state
    BLOCK_WIDTH = int (WINDOW_WIDTH / state.dimensions[1])
    BLOCK_HEIGHT = int (WINDOW_HEIGHT / state.dimensions[0])
    SPACING = 10
    
    arcade.start_render()
    for i in range(state.dimensions[0]):
        for j in range(state.dimensions[1]):
            val = ' '
            if state.dynamic_state[i][j] != GameState.EMPTY:
                val = state.dynamic_state[i][j]
            else:
                val = state.static_state[i][j]

            if val == GameState.BLOCK_WALL:
                arcade.draw_rectangle_filled(
                    WINDOW_HEIGHT - BLOCK_WIDTH * j - BLOCK_WIDTH/2,
                    WINDOW_HEIGHT - BLOCK_HEIGHT * i - BLOCK_HEIGHT/2,
                    BLOCK_WIDTH - SPACING,BLOCK_HEIGHT - SPACING,
                    arcade.color.WOOD_BROWN
                    )
            elif val == GameState.ICE or val == GameState.ICE_ON_END:
                arcade.draw_rectangle_filled(
                    WINDOW_HEIGHT - BLOCK_WIDTH * j - BLOCK_WIDTH/2,
                    WINDOW_HEIGHT - BLOCK_HEIGHT * i - BLOCK_HEIGHT/2,
                    BLOCK_WIDTH - SPACING,BLOCK_HEIGHT - SPACING,
                    arcade.color.LIGHT_BLUE
                    )
            elif val == GameState.PLAYER or val == GameState.PLAYER_ON_END:
                arcade.draw_rectangle_filled(
                    WINDOW_HEIGHT - BLOCK_WIDTH * j - BLOCK_WIDTH/2,
                    WINDOW_HEIGHT - BLOCK_HEIGHT * i - BLOCK_HEIGHT/2,
                    BLOCK_WIDTH - SPACING,BLOCK_HEIGHT - SPACING,
                    arcade.color.TEA_GREEN
                    )
    
    

def get_code(config_path):
    # Check if file exists or raise and error
    if not os.path.isfile(config_path):
        raise Exception("File not found")
    
    # Open file and read all lines
    f = open(config_path,"r")
    lines = f.readlines()
    
    # Remove spaces at the end and get the longest legnth or the 
    # ammout of lines, whichever is greatest
    lines = list(map(lambda line: line.rstrip(),lines))
    max_len = reduce(lambda acc,el: len(el) if len(el) > acc else acc,lines,0)
    max_len = max_len if max_len > len(lines) else len(lines)
    
    # Append spaces at the end and empty lines to form a square
    for i in range(len(lines)):
        if len(lines[i]) < max_len:
            lines[i] = lines[i] + " " * (max_len - len(lines[i]))
        lines[i] = lines[i] + "\n"
    if max_len > len(lines):
        for _ in range( max_len - len(lines) - 1 ):
            lines.append(" " * max_len + "\n")
        lines.append(" " * max_len)
    
    # Join lines into a single string, close file and return string
    lines = "".join(line for line in lines)
    f.close()
    return lines

def main(initial_state):
    state = GameState.from_code(get_code(initial_state))
    sokoban = Sokoban(state)
    ondraw.sokoban = sokoban
    # Open window, set drawing function and start running
    arcade.open_window(WINDOW_WIDTH,WINDOW_HEIGHT,WINDOW_TITLE)
    arcade.schedule(ondraw,DRAW_INTERVAL)
    arcade.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing argument initial_state")
        print("Example: $ python main.py initial/state/path.txt")
        exit(1)
    main(sys.argv[1])