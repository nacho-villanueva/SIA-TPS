import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from TP3.function import Function
from TP3.perceptron import Perceptron


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def error(expected, actual):
    return 0.5 * (actual - expected) ** 2


def d_error(expected, actual):
    return actual - expected


layers = [2, 3, 2, 1]
training_set = pd.read_csv("data/perceptronSimpleXOR.csv", sep=";")

X = training_set.drop("y", axis=1).to_numpy().reshape(layers[0], -1)
Y = training_set.loc[:, "y"].to_numpy().reshape(layers[-1], -1)

nn = Perceptron(layers, Function(sigmoid, d_sigmoid), Function(error, d_error))

nn.train(X, Y, epochs=500, batch_size=4, learning_rate=.01)
prediction = nn.feedforward(X)
print(prediction)
# plt.scatter(X[0], X[1])
# plt.scatter(X.flatten(), prediction.flatten())
plt.show()
