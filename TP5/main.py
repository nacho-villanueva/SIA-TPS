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
    S = X * 255
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

    subset = (0, 15)
    Y = Y[:, subset[0]:subset[1]]

    X_train = np.copy(Y)
    Y_train = np.copy(Y)
    # if config.noise > 0:
    #     X1 = np.vectorize(lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(Y)
    #     X2 = np.vectorize(
    #         lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(Y)
    #     X3 = np.vectorize(
    #         lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(Y)
    #
    #     X_train = np.append(X1, X2, axis=1)
    #     X_train = np.append(X_train, X3, axis=1)
    #     Y_train = np.append(Y, Y, axis=1)
    #     Y_train = np.append(Y_train, Y, axis=1)
    #     # X_train = X1

    ae = Autoencoder(config.layers, config.latent_layer, Function(sigmoid, d_sigmoid), Function(error, d_error))
    ae.train(X_train, Y_train, epochs=config.epochs, batch_size=config.batch_size, learning_rate=config.learning_rate)

    X_test = np.copy(Y)
    if config.noise > 0:
        X_test = np.vectorize(
            lambda v: 1 - v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(Y)
        # X_test = Y + (np.random.randn(Y.shape[0], Y.shape[1]) * config.noise * 2 - np.full((Y.shape[0], Y.shape[1]),
        #                                                                                config.noise))

    latent_space = ae.encode(X_train)

    plt.connect('motion_notify_event', mouse_move)

    mouse_figure = plt.plot(x, y, "ro")
    plt.scatter(latent_space[0], latent_space[1])
    for i, label in enumerate(config.labels[subset[0]:subset[1]]):
        plt.annotate(label, (latent_space[0][i], latent_space[1][i]))
    plt.show(block=False)

    plt.figure()

    fila = 5

    prediction = ae.feedforward(X_test)
    image = np.ones((28 + 4, 40 + 8))
    for i, p in enumerate(prediction.T):
        pp = np.ones((8, 6))
        pp[:7, :5] = p.reshape(7, 5) < 0.5
        ix = (i % fila) * 6
        jy = (i // fila) * 8
        image[jy:jy + 8, ix:ix + 6] = pp.astype(int)

        # image = np.append(image, p.reshape(7, 5), axis=1)
        # image = np.append(image, np.zeros((7, 2)), axis=1)
    create_image(image, "output.png")

    image = np.ones((28 + 4, 40 + 8))
    for i, p in enumerate(X_test.T):
        pp = np.ones((8, 6))
        pp[:7, :5] = p.reshape(7, 5) < 0.5
        ix = (i % fila) * 6
        jy = (i // fila) * 8
        image[jy:jy + 8, ix:ix + 6] = pp.astype(int)

        # image = np.append(image, p.reshape(7, 5), axis=1)
        # image = np.append(image, np.zeros((7, 2)), axis=1)
    create_image(image, "test.png")

    latent_code = ae.encode(X_train[:, 2][np.newaxis].T)
    print(latent_code)

    new_result = ae.decode(np.array([[x], [y]])).reshape((7, 5)) > 0.5

    character_figure = plt.imshow(new_result)
    plt.show()

    # asyncio.run(run_draw())
    # print_symbol(X_train[:, 2])
    # print_symbol(prediction[:, 2])


if __name__ == "__main__":
    main()
