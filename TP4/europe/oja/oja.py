import time
import random

import numpy as np
import pandas as pd

from TP4.europe.oja.oja_config import OjaConfig

class Oja:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        config = OjaConfig()

        self.learning_rate = config.learning_rate
        self.iter = config.iter

        # Inicializamos todos los pesos W
        self.W = np.linspace(1,data.shape[1],data.shape[1], dtype=np.ndarray)  # Matriz, cada elemento será un vector de pesos w

    def train(self):
        starttime = time.time()
        def iter_funct(row):
            x = row.to_numpy()
            y = self.W.dot(x)
            self.W += self.learning_rate * y * ( x - y * self.W)
        for _ in range(self.iter):
            self.data.apply(iter_funct,axis=1)
        endtime = time.time()
        print(endtime - starttime)
        return self.W
    def get_w(self):
        pass
