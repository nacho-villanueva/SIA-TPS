import json
import sys

import numpy as np
import pandas as pd
from TP4.europe.oja.oja import Oja
from TP4.europe.oja.oja_config import OjaConfig


def standarize_data(data):
    for j in range(1, data.shape[1]):
        column = data.iloc[:, j].to_numpy()
        column_mean = np.mean(column)
        column_std = np.std(column)
        for i in range(data.shape[0]):
            data.iloc[i, j] = (data.iloc[i, j] - column_mean) / column_std
    return data


def main():
    config_file = "../../config/kohonen_config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print(f"Using default config file {config_file}")

    config_file = open(config_file)
    config_dict = json.load(config_file)
    config_file.close()

    config = OjaConfig()
    config.setup_config(config_dict)

    data = pd.read_csv(config.data_path, sep=",")
    # Estandarizamos los datos
    data = standarize_data(data)

    # Le sacamos la 1era columna, ya que no es un dato en sí
    data_clean = data.iloc[:, 1:]

    oja = Oja(data_clean)
    weights = oja.train()
    print(weights)


if __name__ == "__main__":
    main()
