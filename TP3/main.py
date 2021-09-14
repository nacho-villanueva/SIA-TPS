import os
import json
import sys

import pandas as pd

from TP3.config import Config
from TP3.constants import *
from TP3.perceptron_visualization import plot_perceptron
from TP3.simple_perceptron import SimplePerceptron


def main():
    config_file = "./config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.json)")

    file = open(config_file)
    config_dict = json.load(file)
    file.close()

    config = Config()
    config.setup_config(config_dict)

    training_set = pd.read_csv(config.training_set_path, sep=";")
    perceptron = SimplePerceptron(
        act_func=get_activation_function(config.activation),
        w0=config.w0,
        learning_rate=config.learning_rate
    )

    perceptron.train(training_set.drop("y", axis=1), training_set.loc[:, "y"])
    # plot_perceptron(perceptron, training_set) # No funca todavia

    print(perceptron.calculate_error(training_set.drop("y", axis=1), training_set.loc[:, "y"]))

    if config.save_perceptron:
        if not os.path.isdir(os.path.dirname(config.save_perceptron_path)):
            os.makedirs(os.path.dirname(config.save_perceptron_path))
        save_perceptron_file = open(config.save_perceptron_path, "w")
        save_perceptron_file.write(f"{perceptron}")
        save_perceptron_file.close()


if __name__ == "__main__":
    main()
