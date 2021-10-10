import arcade
from operator import add

# Set up the constants
import numpy as np

from TP4.hopfield.hopfield_network import HopfieldNetwork

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

RECT_WIDTH = 50
RECT_HEIGHT = 50


class MyApplication(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title="Hopfield Network")
        self.left_down = False
        self.width = width
        self.height = height
        self.cell_size = 10
        self.grid = np.full((height // self.cell_size, width // self.cell_size), -1)
        self.x = 0
        self.y = 0
        self.left_down = False
        self.dataset = np.empty((0, (height // self.cell_size) * (width // self.cell_size)))

        self.hn = HopfieldNetwork()

    def draw_grid(self):
        for i in range(self.cell_size, self.width, self.cell_size):
            arcade.draw_line(i, 0, i, self.height, (255, 0, 0))

        for j in range(self.cell_size, self.height, self.cell_size):
            arcade.draw_line(0, j, self.width, j, (255, 0, 0))

    def get_pointing_cell(self, x, y):
        return x // self.cell_size, y // self.cell_size

    def draw_cell(self, pos):
        (x, y) = pos
        arcade.draw_rectangle_filled((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size, self.cell_size,
                                     self.cell_size, (255, 255, 255))

    def draw_active_cells(self):
        for j, row in enumerate(self.grid):
            for i, v in enumerate(row):
                if v == 1:
                    self.draw_cell((i, j))

    def update(self, dt):
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.draw_grid()
        self.draw_active_cells()
        curr_cell = self.get_pointing_cell(self.x, self.y)

        self.draw_cell(curr_cell)
        self.draw_cell(map(add, curr_cell, (1, 0)))
        self.draw_cell(map(add, curr_cell, (-1, 0)))
        self.draw_cell(map(add, curr_cell, (0, 1)))
        self.draw_cell(map(add, curr_cell, (0, -1)))

    def activate_cell(self, cell):
        self.grid[cell[1], cell[0]] = 1

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.x = x
        self.y = y
        if self.left_down:
            cell = self.get_pointing_cell(x, y)
            self.activate_cell(cell)
            self.activate_cell(tuple(map(add, cell, (1, 0))))
            self.activate_cell(tuple(map(add, cell, (-1, 0))))
            self.activate_cell(tuple(map(add, cell, (0, 1))))
            self.activate_cell(tuple(map(add, cell, (0, -1))))

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.left_down = True

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.left_down = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 65293: # ENTER
            self.dataset = np.vstack((self.dataset, self.grid.flatten()))
            self.grid = np.full((self.height // self.cell_size, self.width // self.cell_size), -1)
        if symbol == 32: # SPACE
            self.hn.train(self.dataset.astype(int))
        if symbol == 112: # P
            result:np.ndarray = self.hn.predict(self.grid.flatten())
            self.grid = result.reshape((self.height // self.cell_size, self.width // self.cell_size))
        if symbol == 65307: # ESC
            self.grid = np.full((self.height // self.cell_size, self.width // self.cell_size), -1)




def main():
    window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


main()
