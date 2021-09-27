import os
import json
import random
import sys

import numpy as np
import pandas as pd

from TP3.config import Config
from TP3.constants import *
from TP3.function import Function
from TP3.methods import sigmoid, d_sigmoid, d_error, error, tanh, d_tanh
from TP3.perceptron import Perceptron
from TP3.simple_perceptron import SimplePerceptron


def main():
    config_file = "./config/ejercicio_3_imagenes_v1.json"  # Si no especifica archivo, corre el ejercicio simplón
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

        if config.activation == "non-linear" or config.activation == "linear":
            k = config.k
            group_size = int(x.shape[0] / k)
            random_test_group = random.randint(0, k - 1)

            test_x = x.iloc[random_test_group * group_size: (random_test_group * group_size) + group_size]
            test_y = y.iloc[random_test_group * group_size: (random_test_group * group_size) + group_size]
            train_x = x.drop(range(random_test_group * group_size, (random_test_group * group_size) + group_size))
            train_y = y.drop(range(random_test_group * group_size, (random_test_group * group_size) + group_size))

            perceptron.train(train_x, train_y, limit=config.epochs)
            print(f"Training error = {2 * perceptron.calculate_error(train_x, train_y) / len(train_x)}")
            print(f"Testing error = {2 * perceptron.calculate_error(test_x, test_y) / len(test_x)}")
        else:
            perceptron.train(x, y, limit=config.epochs)
            print(f"Error = {2 * perceptron.calculate_error(x, y) / len(x)}")

        if config.save_perceptron:
            if not os.path.isdir(os.path.dirname(config.save_perceptron_path)):
                os.makedirs(os.path.dirname(config.save_perceptron_path))
            save_perceptron_file = open(config.save_perceptron_path, "w")
            save_perceptron_file.write(f"{perceptron}")
            save_perceptron_file.close()

    elif config.algorithm == "multi-layer":
        if config.problem_to_solve == "csv":
            training_set = pd.read_csv(config.training_set_path, sep=";")
            X = training_set.drop("y", axis=1).to_numpy().reshape(config.layers[0], -1)
            Y = training_set.loc[:, "y"].to_numpy().reshape(config.layers[-1], -1)

            nn = Perceptron(config.layers, Function(sigmoid, d_sigmoid), Function(error, d_error))
            nn.train(X, Y, epochs=config.epochs, batch_size=1, learning_rate=config.learning_rate)

        elif config.problem_to_solve == "picture" or config.problem_to_solve == "parity":
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

            if config.problem_to_solve == "picture":
                Y = np.diag(np.ones(10))
            else:
                Y = np.empty((2, 10))
                # Y[::2] = 1
                # Y[1::2] = -1
                # Y = Y.reshape(1, -1)
                Y[0, ::2] = 1
                Y[0, 1::2] = 0

                Y[1, ::2] = 0
                Y[1, 1::2] = 1

            nn = Perceptron(config.layers, Function(sigmoid, d_sigmoid), Function(error, d_error))
            nn.train(X, Y, epochs=config.epochs, batch_size=config.batch_size, learning_rate=config.learning_rate)

            X_test = np.copy(X)
            if config.problem_to_solve == "picture":
                X_test = np.vectorize(lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.image_noise, config.image_noise]) else v)(X_test)
            prediction = nn.feedforward(X_test, softmax=config.softmax)

            # from PIL import Image
            #
            # for i in range(10):
            #     image = Image.fromarray(X_test[:, i].reshape(7, 5) * 255)
            #     if image.mode != 'RGB':
            #         image = image.convert('RGB')
            #     image.save(f"results/test_image_{i}.jpg")

            for i, p in enumerate(prediction.transpose()):
                print(f"{i} is {np.argmax(p)} with {np.max(p) * 100:.2f}% certainty")


if __name__ == "__main__":
    main()
