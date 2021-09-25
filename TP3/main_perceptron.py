import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from TP3.function import Function
from TP3.methods import *
from TP3.perceptron import Perceptron

width = 5
height = 7


layers = [width*height, 50, 50, 10]
# training_set = pd.read_csv("data/perceptronSimpleY.csv", sep=";")
#
# X = training_set.drop("y", axis=1).to_numpy().reshape(layers[0], -1)
# Y = training_set.loc[:, "y"].to_numpy().reshape(layers[-1], -1)


f = open("data/pixelMap.txt")

X = np.empty((width * height, 0))

line = f.readline()
while line:
    image = []
    for i in range(height):
        line = line.replace("\n", "").split(" ")
        line = [int(char) for char in line]
        image += line
        line = f.readline()
    image = np.array(image).reshape(-1, 1)
    X = np.append(X, image, 1)

Y = np.diag(np.ones(10))


nn = Perceptron(layers, Function(sigmoid, d_sigmoid), Function(error, d_error))

nn.train(X, Y, epochs=100000, batch_size=5, learning_rate=.1)

prediction = nn.feedforward(X)

print(np.argmax(prediction[0]))
print(np.argmax(prediction[1]))
print(np.argmax(prediction[2]))
print(np.argmax(prediction[3]))
print(np.argmax(prediction[4]))
print(np.argmax(prediction[5]))
print(np.argmax(prediction[6]))
print(np.argmax(prediction[7]))
print(np.argmax(prediction[8]))
print(np.argmax(prediction[9]))
