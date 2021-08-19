from time import time
from sortedcontainers import SortedList

from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics


def sort_state(state):
    return state[1]  # Ordena por heurística


# f(n) = g(n) + h(n)
def f(cost, heuristic):
    return cost + heuristic


class AStar(Algorithm):
    def __init__(self, sokoban, heuristic, test_deadlocks):
        super(AStar, self).__init__(sokoban)
        self.passed_nodes = set()
        self.solution_found = False
        self.statistics = Statistics(0, 0, 0, 0, 0)
        self.fr = SortedList(key=sort_state)
        self.heuristic = heuristic
        self.winning_node = None
        self.test_deadlocks = test_deadlocks

    def run(self):
        t0 = time()

        root_node = self.sokoban.state.save_state()
        self.passed_nodes.add(root_node)
        self.fr.add((root_node, f(self.statistics.deepness, self.heuristic(self.sokoban)), None, 0, None))

        while len(self.fr) > 0:
            # El primer elemento es el de menor heuristica
            curr = self.fr.pop(index=0)
            self.sokoban.state.load_state(curr[0])


            if self.sokoban.is_game_won():
                self.statistics.deepness = curr[3]
                self.solution_found = True
                self.winning_node = curr
                break
            else:
                # curr = curr[0]
                self.statistics.expanded_nodes += 1

                for movement in self.sokoban.get_possible_movements():
                    self.sokoban.move(movement)
                    new_node = self.sokoban.state.save_state()
                    if not (self.test_deadlocks and self.sokoban.is_game_over()):
                        if new_node not in self.passed_nodes:
                            self.fr.add((new_node, f(curr[3] + 1, self.heuristic(self.sokoban)), curr, curr[3] + 1, movement))
                            self.passed_nodes.add(new_node)
                    self.sokoban.state.load_state(curr[0])

        t1 = time()
        self.statistics.time_spent = t1 - t0

        if self.solution_found:
            self.statistics.deepness = self.winning_node[3]
            self.statistics.cost = self.statistics.deepness
            self.statistics.frontier_nodes = len(self.fr)
            # Me construyo el array de movimientos para devolver
            winning_movements = []
            node_aux = self.winning_node
            while node_aux[4] is not None:
                winning_movements.append(node_aux[4])
                node_aux = node_aux[2]
            winning_movements.reverse()
            return winning_movements
        else:
            return []
