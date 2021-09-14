import numpy as np
from matplotlib import pyplot as plt

from TP3.simple_perceptron import SimplePerceptron


def plot_perceptron(perceptron: SimplePerceptron, training_set):
    x1 = training_set.x1
    x2 = training_set.x2
    color = ["r" if j > 0 else "b" for j in training_set.y]

    x = np.linspace(-4, 4, 100)

    slope = -(perceptron.w0 / perceptron.w[1]) / (perceptron.w0 / perceptron.w[0])
    intercept = -perceptron.w0 / perceptron.w[1]

    print(perceptron.w[1], perceptron.w[0], perceptron.w0)

    y = slope * x + intercept

    fig, ax = plt.subplots(1, 1)
    ax.scatter(x1, x2, marker='o', color=color)
    ax.plot(x, y)

    plt.tight_layout()
    plt.show()
