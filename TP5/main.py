import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D

from TP5.autoencoder import Autoencoder
from TP5.config import Config
from TP5.function import Function
from TP5.methods import *


def create_image(X, name):
    S = ((X + 1) / 2) * 255
    array = np.array(S, dtype=np.uint8)
    img = Image.fromarray(array, mode="L").resize((X.shape[1] * 10, X.shape[0] * 10), Image.NEAREST)
    img.save(f"./results/{name}")


def print_symbol(X):
    out_str = ""
    for i, s in enumerate(X):
        if i % 5 == 0 and i != 0:
            out_str += "\n"
        out_str += "*" if s >= 0.5 else " "
    print(out_str)


x, y = 0, 0
mouse_figure: list[Line2D]
character_figure: AxesImage
ae: Autoencoder


def mouse_move(event):
    global x, y, mouse_figure
    x, y = event.xdata, event.ydata

    if x is None:
        x = 0
    if x > 1:
        x = 1
    if x < 0:
        x = 0

    if y is None:
        y = 0
    if y > 1:
        y = 1
    if y < 0:
        y = 0

    mouse_figure[0].set_xdata(x)
    mouse_figure[0].set_ydata(y)
    plt.show()

    new_result = ae.decode(np.array([[x], [y]])).reshape((7, 5)) > 0.5
    character_figure.set_data(new_result)


def main():
    global mouse_figure, ae, character_figure
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

    plt.connect('motion_notify_event', mouse_move)

    mouse_figure = plt.plot(x, y, "ro")
    plt.scatter(latent_space[0], latent_space[1])
    for i, label in enumerate(config.labels):
        plt.annotate(label, (latent_space[0][i], latent_space[1][i]))
    plt.show(block=False)

    plt.figure()

    image = np.empty((7, 5))
    for p in prediction.T:
        image = np.append(image, p.reshape(7, 5), axis=1)
        image = np.append(image, np.zeros((7, 2)), axis=1)
    create_image(image > 0.5, "output.png")

    latent_code = ae.encode(X[:, 2][np.newaxis].T)
    print(latent_code)

    new_result = ae.decode(np.array([[x], [y]])).reshape((7, 5)) > 0.5

    character_figure = plt.imshow(new_result)
    plt.show()

    # asyncio.run(run_draw())
    # print_symbol(X[:, 2])
    # print_symbol(prediction[:, 2])


if __name__ == "__main__":
    main()
