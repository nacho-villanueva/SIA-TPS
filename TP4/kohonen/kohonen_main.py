import json
import sys

import numpy as np
import pandas as pd

from TP4.kohonen.heatmap import plot_matrix_u, plot_matrix
from TP4.kohonen.kohonen_config import KohonenConfig
from TP4.kohonen.kohonen import Kohonen, find_neighbours


def standarize_data(data):
    for j in range(1, data.shape[1]):
        column = data.iloc[:, j].to_numpy()
        column_mean = np.mean(column)
        column_std = np.std(column)
        for i in range(data.shape[0]):
            data.iloc[i, j] = (data.iloc[i, j] - column_mean) / column_std
    return data


def get_matrix_u(weight_matrix):
    k = weight_matrix.shape[0]
    matrix_u = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            neighbours = find_neighbours(1, k, i, j)
            neighbours_distances = np.array([])
            for n in neighbours:
                a = np.array(weight_matrix[n[0]][n[1]])
                b = np.array(weight_matrix[i][j])
                neighbours_distances = np.append(neighbours_distances, np.linalg.norm(a-b))
            matrix_u[i][j] = np.mean(neighbours_distances)
    return matrix_u


def main():
    config_file = "./config/kohonen_config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print(f"Using default config file {config_file}")

    config_file = open(config_file)
    config_dict = json.load(config_file)
    config_file.close()

    config = KohonenConfig()
    config.setup_config(config_dict)

    data = pd.read_csv(config.data_path, sep=",")
    # Estandarizamos los datos
    data = standarize_data(data)

    # Le sacamos la 1era columna, ya que no es un dato en sí
    data_clean = data.iloc[:, 1:]

    kohonen = Kohonen(data_clean)
    weights = kohonen.train()

    matrix_u = get_matrix_u(weights)
    plot_matrix_u(matrix_u)

    matrix, coords_map = kohonen.test(data)  # Testeamos con la data que SÍ tiene en la 1era columna los nombres
    plot_matrix(matrix, coords_map)


if __name__ == "__main__":
    main()
