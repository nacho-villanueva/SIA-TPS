from collections import deque
from time import time

from line_profiler_pycharm import profile

from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics
from TP1.Sokoban import Sokoban


class IDDFS(Algorithm):

    def __init__(self, sokoban: Sokoban, max_depth=500, start_depth=10, step_size=2, test_deadlocks=True):
        super().__init__(sokoban)
        self.max_depth = max_depth
        self.start_depth = start_depth
        self.step_size = step_size

        self.repeated_states = {}
        self.frontier_nodes = deque()

        self.test_deadlocks = test_deadlocks

        self.statistics = Statistics()
        self.start_time = time()

    @profile
    def _DLS(self, depth, limit, movements):
        current_state = self.sokoban.state.save_state()

        if depth >= limit:
            self.frontier_nodes.append((depth, current_state, movements))
            return False

        self.statistics.expanded_nodes += 1

        if current_state in self.repeated_states and self.repeated_states[current_state] <= depth:
            return False

        self.repeated_states[current_state] = depth

        if self.sokoban.is_game_won():
            return movements

        if self.test_deadlocks:
            if self.sokoban.is_game_over():
                return False

        posible_movements = self.sokoban.get_possible_movements()
        for m in posible_movements:
            self.sokoban.move(m)

            solution = self._DLS(depth + 1, limit, movements + [m])
            if solution:
                return solution

            self.sokoban.state.load_state(current_state)

        return False

    def _IDDFS(self):
        self.frontier_nodes.append((0, self.sokoban.state.save_state(), []))
        current_limit = self.start_depth

        while len(self.frontier_nodes) > 0:
            current_node = self.frontier_nodes.pop(0)
            if current_limit <= current_node[0]:
                print(f"Depth Limit: {current_limit}")
                current_limit += self.step_size
                if current_limit > self.max_depth:
                    print("Max depth reached")
                    return False

            self.sokoban.state.load_state(current_node[1])
            solution = self._DLS(current_node[0], current_limit, current_node[2])
            if solution:
                self.statistics.time_spent = time() - self.start_time
                self.statistics.deepness = self.statistics.cost = len(solution)
                self.statistics.frontier_nodes = len(self.frontier_nodes) + 1
                return solution
        return False

    def run(self):
        return self._IDDFS()
