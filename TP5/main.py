import json
import sys

import numpy as np
import PIL.Image as Image

from TP5.autoencoder import Autoencoder
from TP5.config import Config
from TP5.function import Function
from TP5.methods import *


def create_image(X, name):
    S = ((X + 1) / 2) * 255
    array = np.array(S, dtype=np.uint8)
    img = Image.fromarray(array, mode="L").resize((125, 125), Image.NEAREST)
    img.save(name)


def print_symbol(X):
    out_str = ""
    for i, s in enumerate(X):
        if i % 5 == 0 and i != 0:
            out_str += "\n"
        out_str += "*" if s >= 0.5 else " "
    print(out_str)


def main():
    config_file = "./configs/config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print(f"Using default config file {config_file}")

    file = open(config_file)
    config_dict = json.load(file)
    file.close()

    config = Config()
    config.setup_config(config_dict)

    # Load Dataset
    f = open(config.training_dataset)
    Y = np.empty((config.width * config.height, 0))

    line = f.readline()
    while line:
        image = []
        if line == "\n":
            line = f.readline()
            continue
        for i in range(config.height):
            line = line.replace("\n", "")
            line = [1 if char == "1" else 0 for char in line]
            image += line
            line = f.readline()
        image = np.array(image).reshape(-1, 1)
        Y = np.append(Y, image, 1)

    X = np.copy(Y)
    if config.noise > 0:
        X = np.vectorize(
            lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(X)

    ae = Autoencoder(config.layers, config.latent_layer, Function(sigmoid, d_sigmoid), Function(error, d_error))
    ae.train(X, Y, epochs=config.epochs, batch_size=config.batch_size, learning_rate=config.learning_rate)

    prediction = ae.feedforward(X)

    latent_space = ae.encode(X)

    print_symbol(X[:, 2])
    print_symbol(prediction[:, 2])


if __name__ == "__main__":
    main()
