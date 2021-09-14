import json
from os import sep
import sys

import pandas as pd
from TP3.config import Config


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
    perceptron = config.algorithm(training_set.drop("y", axis=1), training_set.loc[:, "y"])
    print(perceptron.calculate_error(training_set.drop("y", axis=1), training_set.loc[:, "y"]))


if __name__ == "__main__":
    main()
