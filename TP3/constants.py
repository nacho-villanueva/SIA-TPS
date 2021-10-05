import numpy as np

from TP3.function import Function


def get_activation_function(name):
    if name == "stair":
        return Function(
            lambda h, w0: -1 if h < w0 else 1,
            lambda h, w0: 1
        )
    if name == "linear":
        return Function(
            lambda h, w0: h,
            lambda h, w0: 1
        )
    if name == "non-linear":
        return Function(
            lambda h, w0: np.tanh(h),
            lambda h, w0: 1 - np.tanh(h) ** 2
        )
