import numpy as np
import pandas as pd
import random

class PerceptronSimple():
    def __init__(self,w=None,act_func=lambda h,w0:h,learning_rate=0.5,w0=0) -> None:
        self.w = np.zeros(2) if w is None else w
        self.w0 = w0
        self.learning_rate = learning_rate
        self.act_fun = act_func
    def fire(self, xi):
        return self.act_fun(np.sum(self.w * xi),self.w0)

    def update(self,xi,zeta,O):
        self.w = self.w + self.learning_rate*(zeta-O)*xi

    def __repr__(self) -> str:
        return f"{{w:{self.w}}}"

    def calculate_error(self,x,y):
        error = 0
        for i in range(len(x)):
            O = self.fire(x.iloc[i])
            error += (y.iloc[i] - O) ** 2
        return error / 2

    def run(self,x:pd.DataFrame,y:pd.DataFrame,COTA=100):
        i = 0
        p = x.shape[0]
        self.w = np.zeros(len(x.columns))
        error = 1
        errormin = p * 2
        while error > 0 and i < COTA:
            ix = random.randint(0,p-1)
            O = self.fire(x.iloc[ix])
            self.update(x.iloc[ix],y.iloc[ix],O)
            error = self.calculate_error(x, y)
            if error < errormin:
                errormin = error
                wmin = self.w
            i = i + 1
        return self