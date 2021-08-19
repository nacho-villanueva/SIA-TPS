from time import time
from typing import Callable

from sortedcontainers import SortedList

from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics
from TP1.Sokoban import Sokoban, Movement


def sort_node(node):
    return node.heuristic


class GGS(Algorithm):
    class Node:
        def __init__(self, depth: int, state: tuple, movements: list[Movement], heuristic: int):
            self.depth = depth
            self.state = state
            self.movements = movements
            self.heuristic = heuristic

    def __init__(self, sokoban: Sokoban, heuristics_function: Callable, test_deadlocks=True):
        super().__init__(sokoban)
        self.heuristics_function = heuristics_function

        self.frontier_nodes = SortedList(key=sort_node)
        init_state = self.sokoban.state.save_state()
        self.frontier_nodes.add(GGS.Node(0, init_state, [], heuristics_function(self.sokoban)))

        self.repeated_states = set()

        self.test_deadlocks = test_deadlocks
        self.start_time = None
        self.statistics = Statistics()

    def run(self):
        self.start_time = time()

        current_depth = 0
        while self.frontier_nodes:
            current_node = self.frontier_nodes.pop(0)
            current_depth = max(current_depth, current_node.depth)
            self.sokoban.state.load_state(current_node.state)

            for m in self.sokoban.get_possible_movements():
                self.sokoban.move(m)
                new_state = self.sokoban.state.save_state()

                if new_state not in self.repeated_states:
                    if self.sokoban.is_game_won():
                        self.statistics.frontier_nodes = len(self.frontier_nodes) + 1
                        self.statistics.time_spent = time() - self.start_time
                        self.statistics.deepness = self.statistics.cost = current_depth + 1
                        return current_node.movements + [m]

                    if not (self.test_deadlocks and self.sokoban.is_game_over()):
                        new_node = GGS.Node(current_node.depth + 1, new_state, current_node.movements + [m],
                                            self.heuristics_function(self.sokoban))
                        self.frontier_nodes.add(new_node)
                        self.repeated_states.add(new_state)
                        self.statistics.expanded_nodes += 1
                self.sokoban.state.load_state(current_node.state)
        return [] # Nothing Found
