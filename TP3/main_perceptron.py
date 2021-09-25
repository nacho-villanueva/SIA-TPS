import pandas as pd
from matplotlib import pyplot as plt

from TP3.function import Function
from TP3.methods import *
from TP3.perceptron import Perceptron

layers = [2, 1]
training_set = pd.read_csv("data/perceptronSimpleY.csv", sep=";")

X = training_set.drop("y", axis=1).to_numpy().reshape(layers[0], -1)
Y = training_set.loc[:, "y"].to_numpy().reshape(layers[-1], -1)

nn = Perceptron(layers, Function(stair(), d_stair), Function(error, d_error))

nn.train(X, Y, epochs=10000, batch_size=4, learning_rate=.01)
prediction = nn.feedforward(X)
print(prediction)
# plt.scatter(X[0], X[1])
# plt.scatter(X.flatten(), prediction.flatten())
plt.show()
