import numpy as np
import pandas as pd
import random

from TP3.config import Config
from TP3.function import Function

ActivationMethod = Function[float, float]


class SimplePerceptron:
    def __init__(self, w=None, act_func: ActivationMethod = Function(lambda h, w0: h, lambda h, w0: 1), learning_rate=0.5, w0=0) -> None:
        self.w = np.zeros(2) if w is None else w
        self.w0 = w0
        self.learning_rate = learning_rate
        self.act_fun = act_func

    def fire(self, xi):
        return self.act_fun.f(self.get_h(xi), self.w0)

    def update(self, xi, zeta, act_state, df_value):
        self.w = self.w + self.learning_rate * (zeta - act_state) * xi * df_value

    def __str__(self) -> str:
        return f"{{\"w\":{list(self.w)}}}"

    def calculate_error(self, x, y):
        error = float(0)
        for i in range(len(x)):
            act_state = self.fire(x.iloc[i])
            error += (y.iloc[i] - act_state) ** 2
        return error / 2

    # def calculate_error_2(self, x, y):
    #     output = []
    #     for i in range(len(x)):
    #         output.append(self.fire(x.iloc[i]))
    #     return output

    def train(self, x: pd.DataFrame, y: pd.DataFrame, limit=100):
        i = 0
        p = x.shape[0]
        self.w = np.zeros(len(x.columns))
        error = 1
        min_error = p * 2
        config = Config()
        w_min = self.w
        while error > 0 and i < limit:
            if config.logging and i % config.logging_epoch == 0:
                print(f"Epoch: {i}")
            ix = random.randint(0, p - 1)
            act_state = self.fire(x.iloc[ix])
            self.update(x.iloc[ix], y.iloc[ix], act_state, self.act_fun.df(self.get_h(x.iloc[ix]), self.w0))
            error = self.calculate_error(x, y)
            if error < min_error:
                min_error = error
                w_min = self.w
            i = i + 1
        self.w = w_min

    def get_h(self, xi):
        return float(np.sum(self.w * xi))
