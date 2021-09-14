from TP3.simple_perceptron import SimplePerceptron


def get_activation_function(name):
    if name == "stair":
        return lambda h, w0: 1 if h < w0 else -1
    if name == "lineal":
        return lambda h, w0: h
