from collections import Set

from TP1.algorithms.algorithm import Algorithm


class BFS(Algorithm):
    def __init__(self, sokoban):
        super().__init__(sokoban)
        self.passed_nodes = Set()

    def run(self):
        pass
