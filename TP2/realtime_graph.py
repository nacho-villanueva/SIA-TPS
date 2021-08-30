from random import random
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

class RealTimeGraphDrawer:
    def __init__(self, max_len = 100):
        self.max_len = max_len
        self.gen_step = 1
        self.curr_len = 0

        self.x = [0]
        self.min_fitness_data = []
        self.avg_fitness_data = []
        self.diversity_data = []
        
        self.fig, self.axs = plt.subplots(3,figsize=(15,15))
        self.min_fitness_ax = self.axs[0]
        self.avg_fitness_ax = self.axs[1]
        self.diversity_ax = self.axs[2]

        self.is_closed = False
        self.fig.canvas.mpl_connect('close_event',lambda _:self._handle_close())

    def _handle_close(self):
        self.is_closed = True

    def push_data(self, min_fitness, avg_fitness, diversity):
        self.min_fitness_data.append(min_fitness)
        self.avg_fitness_data.append(avg_fitness)
        self.diversity_data.append(diversity)
        if self.curr_len != 0:
            self.x.append( self.x[-1] + self.gen_step )

        self.curr_len += 1

        if self.curr_len > self.max_len:
            self.min_fitness_data.pop(0)
            self.avg_fitness_data.pop(0)
            self.diversity_data.pop(0)
            self.x.pop(0)



    def draw(self,interval=0.0000001):
        # Clear
        self.min_fitness_ax.cla()
        self.avg_fitness_ax.cla()
        self.diversity_ax.cla()

        # Plot
        self.min_fitness_ax.plot(self.x,self.min_fitness_data, color='red')
        self.avg_fitness_ax.plot(self.x,self.avg_fitness_data, color='blue')
        self.diversity_ax.plot(self.x,self.diversity_data, color='green')

        # Set ticks
        self.min_fitness_ax.set(xlim=(self.x[0], self.x[0] + self.max_len * self.gen_step))
        self.avg_fitness_ax.set(xlim=(self.x[0], self.x[0] + self.max_len * self.gen_step))
        self.diversity_ax.set(xlim=(self.x[0], self.x[0] + self.max_len * self.gen_step))

        # Titles
        self.min_fitness_ax.set_title("min fitness", fontsize=15)
        self.avg_fitness_ax.set_title("avg fitness", fontsize=15)
        self.diversity_ax.set_title("diversity", fontsize=15)
        
        # Draw and events
        plt.pause(interval)

    def push_and_draw(self,min_fitness, avg_fitness, diversity,interval=0.0001):
        self.push_data(min_fitness,avg_fitness,diversity)
        self.draw(interval)

if __name__ == "__main__":
    graph = RealTimeGraphDrawer()
    
    while not graph.is_closed:
        graph.push_data(int(random() * 10),int(random() * 10),int(random() * 10))
        graph.draw()