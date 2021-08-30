from random import random
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimeGraphDrawer:
    def __init__(self, data_len = 100):
        self.min_fitness_data = [0] * data_len
        self.avg_fitness_data = [0] * data_len
        self.diversity_data = [0] * data_len
        
        self.fig, self.axs = plt.subplots(3)
        self.min_fitness_ax = self.axs[0]
        self.avg_fitness_ax = self.axs[1]
        self.diversity_ax = self.axs[2]

        self.is_closed = False
        self.fig.canvas.mpl_connect('close_event',lambda _:self._handle_close())

    def _handle_close(self):
        self.is_closed = True

    def push_data(self, min_fitness, avg_fitness, diversity):
        self.min_fitness_data.append(min_fitness)
        self.min_fitness_data.pop(0)

        self.avg_fitness_data.append(avg_fitness)
        self.avg_fitness_data.pop(0)

        self.diversity_data.append(diversity)
        self.diversity_data.pop(0)

    def draw(self,interval=0.0001):
        self.min_fitness_ax.cla()
        self.avg_fitness_ax.cla()
        self.diversity_ax.cla()

        self.min_fitness_ax.plot(self.min_fitness_data, color='red', label="min fitness")
        self.avg_fitness_ax.plot(self.avg_fitness_data, color='blue', label="min fitness")
        self.diversity_ax.plot(self.diversity_data, color='green', label="min fitness")

        self.min_fitness_ax.legend()
        self.avg_fitness_ax.legend()
        self.diversity_ax.legend()
        plt.pause(interval)

    def push_and_draw(self,min_fitness, avg_fitness, diversity,interval=0.0001):
        self.push_data(min_fitness,avg_fitness,diversity)
        self.draw(interval)

if __name__ == "__main__":
    graph = RealTimeGraphDrawer()
    
    while not graph.is_closed:
        graph.push_data(int(random() * 10),int(random() * 10),int(random() * 10))
        graph.draw()