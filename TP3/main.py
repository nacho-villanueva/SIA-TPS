import os
import json
import sys

import numpy as np
import pandas as pd

from TP3.config import Config
from TP3.constants import *
from TP3.function import Function
from TP3.methods import sigmoid, d_sigmoid, d_error, error
from TP3.perceptron import Perceptron
from TP3.perceptron_visualization import plot_perceptron
from TP3.simple_perceptron import SimplePerceptron


def main():
    config_file = "./config/ejercicio_3_imagenes_v2.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print(f"Using default config file {config_file}")

    file = open(config_file)
    config_dict = json.load(file)
    file.close()

    config = Config()
    config.setup_config(config_dict)

    # Vemos cuál perceptron vamos a usar
    if config.algorithm == "simple":

        if config.activation == "non-linear" or config.activation == "linear":
            # Ejercicio 2) : función
            x = pd.read_csv(config.training_set_path, sep=";", header=None)
            y = pd.read_csv(config.output_data_path, sep=";", header=None).loc[:, 0]
        else:
            # Escalón
            # Ejercicio 1) : XOR & Y
            training_set = pd.read_csv(config.training_set_path, sep=";")
            x = training_set.drop("y", axis=1)
            y = training_set.loc[:, "y"]

        perceptron = SimplePerceptron(
            act_func=get_activation_function(config.activation),
            w0=config.w0,
            learning_rate=config.learning_rate
        )

        perceptron.train(x, y, limit=config.epochs)
        # plot_perceptron(perceptron, training_set) # No funca todavia

        print(perceptron.calculate_error(x, y))

        if config.save_perceptron:
            if not os.path.isdir(os.path.dirname(config.save_perceptron_path)):
                os.makedirs(os.path.dirname(config.save_perceptron_path))
            save_perceptron_file = open(config.save_perceptron_path, "w")
            save_perceptron_file.write(f"{perceptron}")
            save_perceptron_file.close()

    elif config.algorithm == "multi-layer":
        f = open(config.training_set_path)
        X = np.empty((config.width * config.height, 0))

        line = f.readline()
        while line:
            image = []
            for i in range(config.height):
                line = line.replace("\n", "").split(" ")
                line = [int(char) for char in line]
                image += line
                line = f.readline()
            image = np.array(image).reshape(-1, 1)
            X = np.append(X, image, 1)

        Y = np.diag(np.ones(10))

        nn = Perceptron(config.layers, Function(sigmoid, d_sigmoid), Function(error, d_error))
        nn.train(X, Y, epochs=config.epochs, batch_size=10, learning_rate=config.learning_rate)

        X_test = np.copy(X)
        X_test = np.vectorize(lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.image_noise, config.image_noise]) else v)(X_test)
        prediction = nn.feedforward(X_test, softmax=True)

        for i, p in enumerate(prediction):
            print(f"{i} is {np.argmax(p)} with {np.max(p) * 100:.2f}% certainty")


if __name__ == "__main__":
    main()
