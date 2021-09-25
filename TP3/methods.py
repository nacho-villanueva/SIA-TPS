import numpy as np


def tanh(x):
    return np.tanh(x)


def d_tanh(x):
    return 1 - tanh(x) ** 2


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def stair():
    def _stair(x):
        if x < 0:
            return -1
        else:
            return 1

    return np.vectorize(_stair)


def d_stair(x):
    return 0


def lineal(x):
    return x


def d_lineal(x):
    return 1


def error(expected, actual):
    return 0.5 * (expected - actual) ** 2


def d_error(expected, actual):
    return expected - actual
