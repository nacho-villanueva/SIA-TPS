def mse(expected: float, actual: float):
    return 0.5 * ((actual - expected) ** 2)


def d_mse(expected: float, actual: float):
    return actual - expected
