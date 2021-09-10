import numpy as np
import pandas as pd
import random

class PerceptronSimpleEscalon():
    def __init__(self,w=None,learning_rate=0.5,w0=0) -> None:
        self.w = np.zeros(2) if w is None else w
        self.w0 = w0
        self.learning_rate = learning_rate
    def fire(self, xi):
        if np.sum(self.w * xi) > self.w0:
            return 1
        else:
            return -1
    def update(self,xi,zeta,O):
        self.w = self.w + self.learning_rate*(zeta-O)*xi

    def __repr__(self) -> str:
        return f"{{w:{self.w}}}"

    def calculate_error(self,x,y):
        error = 0
        for i in range(len(x)):
            O = self.fire(x.iloc[i])
            error += abs(y.iloc[i] - O)
        return error


    @staticmethod
    def run(x:pd.DataFrame,y:pd.DataFrame,COTA=100):
        i = 0
        p = x.shape[0]
        perceptron = PerceptronSimpleEscalon(np.zeros(len(x.columns)))
        error = 1
        errormin = p * 2
        while error > 0 and i < COTA:
            ix = random.randint(0,p-1)
            O = perceptron.fire(x.iloc[ix])
            perceptron.update(x.iloc[ix],y.iloc[ix],O)
            error = perceptron.calculate_error(x, y)
            if error < errormin:
                errormin = error
                wmin = perceptron.w
            i = i + 1
        return perceptron