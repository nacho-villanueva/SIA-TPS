import numpy as np


def get_activation_function(name):
    if name == "stair":
        return lambda h, w0: -1 if h < w0 else 1
    if name == "linear":
        return lambda h, w0: h
    if name == "non-linear":
        return lambda h, w0: np.tanh(h)
