import random

import numpy as np
import pandas as pd

from TP4.kohonen_config import KohonenConfig


# Returns all neighbours that are a distance <= R from position [i][j]
# Uses euclidean distance
def find_neighbours(R: float, k: int, i: int, j: int) -> list[tuple[int, int]]:
    to_return = []  # Array of tuples
    for ii in range(i - int(R), i + int(R) + 1):
        for jj in range(j - int(R), j + int(R) + 1):
            if 0 <= ii < k and 0 <= jj < k:
                if ii != i or jj != j:
                    # Chequeamos la distancia euclídea
                    a = np.array((ii, jj))
                    b = np.array((i, j))
                    if np.linalg.norm(a-b) <= R:
                        to_return.append((ii, jj))
    return to_return


class Kohonen:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        config = KohonenConfig()

        self.R = config.R
        self.R_updates = config.R_updates
        self.initial_R = self.R
        self.k = config.k
        self.learning_rate = config.learning_rate

        # Inicializamos todos los pesos W
        self.W = np.empty((self.k, self.k), dtype=np.ndarray)  # Matriz, cada elemento será un vector de pesos w
        for i in range(self.k):
            for j in range(self.k):
                initial_w = np.zeros(data.shape[1])
                for k in range(data.shape[1]):
                    random_row = data.loc[random.randint(0, data.shape[0] - 1)]
                    initial_w[k] = random_row.iloc[k]
                self.W[i][j] = initial_w

    def train(self):
        total_iterations = 500 * self.data.shape[1]  # TODO: parametrizar?
        for iteration in range(total_iterations):
            # Seleccionar un registro de entre todas las entradas
            random_registry_index = random.randint(0, self.data.shape[0] - 1)
            X = self.data.loc[random_registry_index].to_numpy()

            # Hayamos el w que se parezca mas a X. O sea que la distancia entre w y X sea mínima
            min_i, min_j = self.get_nearest_weight(X)

            # Buscamos las neuronas vecinas a la ganadora
            neighbours = find_neighbours(self.R, self.k, min_i, min_j)
            # Actualizamos el peso de las neuronas vecinas
            for n in neighbours:
                self.W[n[0]][n[1]] = self.W[n[0]][n[1]] + (self.learning_rate * (X - self.W[n[0]][n[1]]))

            # Actualizamos el learning_rate
            # El +2 es para que empiece en 0+2
            self.learning_rate = 1 / (iteration + 2)

            # Actualizamos R si corresponde
            # Si el R inicial era 2 y hay 10 iteraciones, entonces el R se actualizará así: 2, 1.9, 1.8 ... 1.0
            if self.R_updates and self.R > 1:
                self.R = self.R - (1/total_iterations) * (self.initial_R - 1)
        return self.W

    def get_nearest_weight(self, X):
        min_i, min_j = 0, 0
        min_distance = np.inf
        for i in range(self.k):
            for j in range(self.k):
                distance = np.linalg.norm(X - self.W[i][j])
                if distance < min_distance:
                    min_i = i
                    min_j = j
                    min_distance = distance
        return min_i, min_j

    def test(self, data):
        # Matriz que va a tener un contador de cuantas veces se activó cada neurona
        count_matrix = np.zeros((self.k, self.k))

        # Mapa de la forma:  { (0,0)->["Croacia", "Suecia"] , (0,1)->[...] , ... , (k,k)->[...] }
        coords_map = {}
        for i in range(self.k):
            for j in range(self.k):
                coords_map[(i, j)] = []

        for i in range(data.shape[0]):  # Por cada fila
            X = data.iloc[i, 1:].to_numpy()
            min_i, min_j = self.get_nearest_weight(X)
            # La neurona que se activó es la que está en [min_i][min_j]
            count_matrix[min_i][min_j] += 1
            coords_map[(min_i, min_j)].append(data.iloc[i, 0])  # Añado el nombre del país

        return count_matrix, coords_map
