from pprint import pprint
from typing import Optional

import numpy as np


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

        orthogonal_matrix = np.dot(self.dataset, self.dataset.T)
        print("---- Orthogonality Matrix ----")
        for row in orthogonal_matrix:
            for v in row:
                print(f"{v}", end="\t")
            print("")
        print("------------------------------")

        W = np.dot(self.dataset.T, self.dataset) / len(self.dataset[0])
        np.fill_diagonal(W, 0)
        self.weights = W

    # X --> Array of input nodes
    def predict(self, X: np.ndarray, max_iter=10000):
        prev_S = None
        S = X.copy()

        i = 0
        while (not np.array_equal(prev_S, S)) and i < max_iter:
            prev_S = S
            S = np.sign(np.dot(self.weights, S)).astype(int)
            i += 1
        return S
