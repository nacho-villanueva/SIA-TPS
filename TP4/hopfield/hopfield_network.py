from pprint import pprint
from typing import Optional

import numpy as np
import PIL.Image as Image


def print_symbol(X):
    out_str = ""
    for i, s in enumerate(X):
        if i % 5 == 0 and i != 0:
            out_str += "\n"
        out_str += "*" if s == 1 else " "
    print(out_str)

def create_image(X, name):
    S = ((X + 1) / 2) * 255
    array = np.array(S, dtype=np.uint8)
    img = Image.fromarray(array, mode="L").resize((125, 125), Image.NEAREST)
    img.save(name)

class HopfieldNetwork:
    def __init__(self):
        self.dataset: Optional[np.ndarray] = None
        self.weights: Optional[np.ndarray] = None
        self.dataset_size: int = 0
        self.input_size: int = 0

    # dataset --> Columns: input nodes; Rows: dataset elements
    def train(self, dataset: np.ndarray):
        self.dataset = dataset.copy()
        self.dataset_size = self.dataset.shape[1]
        self.input_size = self.dataset.shape[0]

        for i, p in enumerate(self.dataset):
            create_image(np.resize(p, (5, 5)), f"symbol{i}.jpg")

        orthogonal_matrix = np.dot(self.dataset, self.dataset.T)
        print("---- Orthogonality Matrix ----")
        for row in orthogonal_matrix:
            for v in row:
                print(f"{v}", end="\t\t")
            print("")
        print("------------------------------")

        # W = np.zeros((len(self.dataset[0]), len(self.dataset[0])))
        # for patron in self.dataset:
        #     for i, v in enumerate(patron):
        #         for j, k in enumerate(patron):
        #             W[j, i] += v * k
        # W /= len(self.dataset[0])
        # np.fill_diagonal(W, 0)
        #
        # self.weights = W

        W1 = np.dot(self.dataset.T, self.dataset) / len(self.dataset[0])
        np.fill_diagonal(W1, 0)
        self.weights = W1

    # X --> Array of input nodes
    def predict(self, X: np.ndarray, max_iter=10):
        prev_S = None
        S = X.copy()

        energies = [self.energy(S)]

        i = 0
        while (not np.array_equal(prev_S, S)) and i < max_iter:
            create_image(np.resize(S, (5, 5)), f"output{i}.jpg")
            prev_S = S
            S = np.sign(np.dot(self.weights, S)).astype(int)
            S[S == 0] = 1
            energies.append(self.energy(S))
            i += 1

        if i >= max_iter:
            print("Ended by max iteration")
        return S, energies

    def energy(self, X):
        e = 0
        for j, row in enumerate(self.weights):
            for i, w in enumerate(row):
                e += w * X[i] * X[j]
        return -e
