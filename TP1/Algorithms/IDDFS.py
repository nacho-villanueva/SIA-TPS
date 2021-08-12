from collections import deque
from time import time

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
        self.frontier_nodes.append((0, self.sokoban.state.save_state(), []))

        self.test_deadlocks = test_deadlocks

        self.statistics = Statistics()
        self.start_time = time()

        self.current_depth = 0

    def _DLS(self, node, limit):
        node_stack = deque()
        node_stack.append(node)

        while node_stack:
            current_node = node_stack.pop()
            self.sokoban.state.load_state(current_node[1])

            if self.sokoban.is_game_won():
                return current_node

            posible_movements = self.sokoban.get_possible_movements()
            for m in posible_movements:
                self.sokoban.move(m)
                new_state = self.sokoban.state.save_state()
                new_node = (current_node[0] + 1, new_state, current_node[2] + [m])

                if not (new_state in self.repeated_states and self.repeated_states[new_state] <= new_node[0]):
                    if not (self.test_deadlocks and self.sokoban.is_game_over()):
                        if new_node[0] > limit:
                            self.frontier_nodes.append(new_node)
                        else:
                            self.statistics.expanded_nodes += 1
                            self.repeated_states[new_state] = new_node[0]
                            node_stack.append(new_node)
                self.sokoban.state.load_state(current_node[1])
        return False

    def _IDDFS(self):
        while self.frontier_nodes:
            current_node = self.frontier_nodes.popleft()
            current_depth = current_node[0]

            if self.current_depth < current_depth:
                self.current_depth = current_depth
                print(f"Current Depth: {current_depth}")

            if current_depth > self.max_depth:
                return False

            if current_depth != 0:
                current_limit = current_depth + self.step_size
            else:
                current_limit = self.start_depth

            solution_node = self._DLS(current_node, current_limit)
            if solution_node:
                self.statistics.cost = self.statistics.deepness = solution_node[0]
                self.statistics.time_spent = time() - self.start_time
                self.statistics.frontier_nodes = len(self.frontier_nodes) + 1
                return solution_node[2]
        return False

    def run(self):
        return self._IDDFS()
