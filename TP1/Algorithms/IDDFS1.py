from time import time

from TP1.Sokoban import Sokoban, Movement
from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics


class IDDFS(Algorithm):
    def __init__(self, sokoban: Sokoban, max_depth=500, test_deadlocks=True):
        super().__init__(sokoban)
        self.repeated_states = {}
        self.frontier_states = [(0, sokoban.state.save_state())]

        self.max_depth = max_depth
        self.statistics = Statistics(0, 0, 0, 0, 0)
        self.start_time = time()
        self.test_deadlocks = test_deadlocks

    def _DLS(self, depth, limit, movements):
        current_state = self.sokoban.state.save_state()

        if depth >= limit:
            self.statistics.frontier_nodes += 1
            self.frontier_states.append((depth, current_state))
            return False, []

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
                self.statistics.frontier_nodes += 1
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

    def run(self, minimum_depth=1, step_size=1):
        for i in range(minimum_depth, self.max_depth, step_size):
            if i % (10 * step_size) == 0:
                print(f"Depth: {i}")
            frontier = self.frontier_states.copy()
            for s in frontier:
                self.sokoban.state.load_state(s[1])
                solution = self._DLS(s[0], i, [])
                if solution[0]:
                    self.statistics.deepness = self.statistics.cost = len(solution[1])
                    solution[1].reverse()
                    self.statistics.time_spent = time() - self.start_time
                    return solution[1]
                self.frontier_states.remove(s)
        print("Max depth reached.")
        return []
