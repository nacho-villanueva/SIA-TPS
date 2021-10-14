import numpy as np
import pandas as pd

from TP4.europe.oja.oja_config import OjaConfig

class Oja:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        config = OjaConfig()

        self.learning_rate = config.learning_rate
        self.iter = config.iter

        self.W = np.random.rand(data.shape[1])

    def train(self):
        def iter_funct(row,iteration):
            x = row
            y = self.W.dot(x)
            self.W += (self.learning_rate/iteration) * ( y * x - y*y * self.W)
        for i in range(self.iter):
            self.data.apply(iter_funct,args=[i+1],raw=True,axis=1)
        return self.W

    def get_w(self):
        return self.W
