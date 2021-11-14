from typing import Tuple, List, Callable

import numpy as np

from TP5.config import Config
from TP5.function import Function

Dataset = List[Tuple[np.ndarray, np.ndarray]]
ErrorMethod = Function[np.ndarray, np.ndarray]
ActivationMethod = Function[np.ndarray, np.ndarray]


def init_weights(layers, random=True):
    # TODO: Maybe use random weights instead of zeros
    weights = []
    for i in range(len(layers) - 1):
        if random:
            weights.append(np.random.randn(layers[i + 1], layers[i]))
        else:
            weights.append(np.zeros((layers[i + 1], layers[i])))
    return weights


def init_biases(layers, random=True):
    biases = []
    for i in range(len(layers) - 1):
        if random:
            biases.append(np.random.randn(layers[i + 1], 1))
        else:
            biases.append(np.zeros((layers[i + 1], 1)))
    return biases


def init_layers(layers):
    empty = []
    for la in layers:
        empty.append(np.zeros(la))
    return empty


# Inputs    -->   [x1, x2, ..., xN] --> (1, N)
# Outputs   -->   [y1, y2, ..., yM] --> (1, M)
# Weights   -->   |w11 ... w1M|
#                 |wN1 ... wNM| --> (N, M)

class Autoencoder:
    def _format_validate_dateset(self, X, Y):
        formatted_xs = []
        formatted_ys = []
        for i, (x, y) in enumerate(zip(X, Y)):
            if x.size != self.layers[0]:
                raise Exception(
                    f"Dataset contains element with {x.size} inputs, expected {self.layers[0]}, at {i}")
            if y.size != self.layers[-1]:
                raise Exception(
                    f"Dataset contains element with {y.size} outputs, expected {self.layers[-1]}, at {i}")
            formatted_x = x.copy()
            formatted_y = y.copy()
            if x.ndim != 1 or y.ndim != 1:
                # Converts Matrix into Vectors
                formatted_x = formatted_x.flatten()[np.newaxis].transpose()
                formatted_y = formatted_y.flatten()[np.newaxis].transpose()
            formatted_xs.append(formatted_x)
            formatted_ys.append(formatted_y)
        return formatted_xs, formatted_ys

    def __init__(self, layers: List[int], latent_layer: int,
                 activation: ActivationMethod, error: ErrorMethod):

        self.layers = layers
        self.latent_layer = latent_layer

        self.layers_a = init_layers(self.layers)
        self.layers_h = init_layers(self.layers[:-1])
        self.weights = init_weights(self.layers)
        self.biases = init_biases(self.layers)

        self.activation = activation
        self.error = error
        self.dw = init_weights(self.layers, False)
        self.db = init_biases(self.layers, False)

    def feedforward(self, inputs: np.ndarray, layer=0, output=None):
        assert inputs.shape[0] == self.layers[layer], f"Input size invalid. Expected: {self.layers[layer]}. Actual: {inputs.shape[0]}"

        current_layer = np.copy(inputs, order="C")

        layers_h = []
        layers_a = [current_layer]

        for i, (w, b) in enumerate(zip(self.weights[layer:], self.biases[layer:]), layer + 1):
            layers_h.append(np.dot(w, current_layer) + b)
            current_layer = self.activation.f(layers_h[-1])
            layers_a.append(current_layer)

            if output is not None and output == i:
                return current_layer

        self.layers_a[layer:] = layers_a
        self.layers_h[layer:] = layers_h

        return current_layer

    def decode(self, inputs: np.ndarray):
        return self.feedforward(inputs, self.latent_layer)

    def encode(self, inputs: np.ndarray):
        return self.feedforward(inputs, 0, self.latent_layer)

    def backpropagate(self, y):
        delta = [0] * (len(self.layers) - 1)
        delta[-1] = self.error.df(y, self.layers_a[-1]) * self.activation.df(self.layers_h[-1])

        for i in range(len(delta) - 2, -1, -1):
            delta[i] = self.weights[i + 1].T.dot(delta[i + 1]) * (
                self.activation.df(self.layers_h[i]))

        batch_size = y.shape[1]
        db = [np.dot(d, np.ones((batch_size, 1))) / float(batch_size) for d in delta]
        dw = [np.dot(d, self.layers_a[i].T) / float(batch_size) for i, d in enumerate(delta)]
        return dw, db

    def train(self, x, y, batch_size=1, epochs=100, learning_rate=0.01):
        config = Config()
        error_file = open(f"./results/error.txt", "w")

        for e in range(epochs):
            if config.log and e % config.log_epoch == 0:
                print(f"Epoch: {e}")
            i = 0
            error = 0

            while i < y.shape[1]:
                x_batch = x[:, i:i+batch_size].reshape(self.layers[0], -1)
                y_batch = y[:, i:i+batch_size].reshape(self.layers[-1], -1)
                result = self.feedforward(x_batch)

                dw, db = self.backpropagate(y_batch)
                lr = config.learning_rate * (1 / (1 + config.learning_rate_decay * epochs))
                self.weights = [w + lr * d_weight + prev_dw * config.momentum for w, d_weight, prev_dw in zip(self.weights, dw, self.dw)]
                self.biases = [w + lr * d_bias + prev_db * config.momentum for w, d_bias, prev_db in zip(self.biases, db, self.db)]

                self.dw = dw
                self.db = db

                error += np.sum(self.error.f(y_batch, result)) / result.shape[1]
                i = i + batch_size

            if error < 1.2:
                print("GOT IT!")
                break

            error_file.write(f"{error}\n")
            error_file.flush()


