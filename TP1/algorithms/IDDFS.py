from time import time

from TP1.Sokoban import Sokoban, Movement
from TP1.algorithms.algorithm import Algorithm
from TP1.algorithms.statistics import Statistics


class IDDFS(Algorithm):
    def __init__(self, sokoban: Sokoban, max_depth=500, test_deadlocks=True):
        super().__init__(sokoban)
        self.repeated_states = {}
        self.max_depth = max_depth
        self.statistics = Statistics(0, 0, 0, 0, 0)
        self.start_time = time()
        self.test_deadlocks = test_deadlocks

    def _DLS(self, depth, limit, movements):
        if depth >= limit:
            return False, []

        current_state = self.sokoban.state.save_state()
        self.statistics.expanded_nodes += 1

        if current_state in self.repeated_states and self.repeated_states[current_state] <= depth:
            self.statistics.frontier_nodes += 1
            return False, []

        self.repeated_states[current_state] = depth

        if self.sokoban.is_game_won():
            self.statistics.frontier_nodes += 1
            return True, []

        if self.test_deadlocks:
            if self.sokoban.is_game_over():
                return False, []

        possible_movements = self.sokoban.get_possible_movements()

        for m in possible_movements:
            self.sokoban.move(m)

            solution = self._DLS(depth + 1, limit, movements + [m])
            if solution[0]:
                solution[1].append(m)
                return True, solution[1]
            self.sokoban.state.load_state(current_state)
        return False, []

    def run(self, minimum_depth=1):
        for i in range(minimum_depth, self.max_depth):
            if i % 10 == 0:
                print(f"Depth: {i}")
            self.repeated_states = {}
            solution = self._DLS(0, i, [])
            if solution[0]:
                self.statistics.deepness = len(solution[1])
                solution[1].reverse()
                self.statistics.time_spent = time() - self.start_time
                return solution[1]
        print("Max depth reached.")
        return []
