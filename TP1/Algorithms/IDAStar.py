from collections import deque
from time import time
from TP1.Sokoban import Sokoban
from sortedcontainers.sortedlist import SortedList
from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics


class IDAStar(Algorithm):

    def __init__(self, sokoban: Sokoban, heuristic , test_deadlocks=True):
        super().__init__(sokoban)
        
        self.f = lambda sokoban,cost: heuristic(sokoban) + cost

        self.repeated_states = {}
        self.frontier_nodes = SortedList(key=lambda x:x[0])
        self.frontier_nodes.add((self.f(self.sokoban,0), self.sokoban.state.save_state(), []))

        self.test_deadlocks = test_deadlocks

        self.statistics = Statistics()

        self.start_time = None
        self.solution = None

    def _DLS(self, node, limit):
        # Initiate stack
        node_stack = deque()
        node_stack.append(node)

        # While there are elements in the stack
        while node_stack:
            # Get last and load it
            current_node = node_stack.pop()
            self.sokoban.state.load_state(current_node[1])
            self.statistics.expanded_nodes += 1

            # If won return it
            if self.sokoban.is_game_won():
                return current_node
            # Else get possible movemnets and test them
            posible_movements = self.sokoban.get_possible_movements()
            for m in posible_movements:
                # move and save state
                self.sokoban.move(m)
                new_state = self.sokoban.state.save_state()
                new_node = (self.f(self.sokoban,len(current_node[2]) + 1), new_state, current_node[2] + [m])

                # If state is not repeated or, if repeated, has less cost
                if not (new_state in self.repeated_states and self.repeated_states[new_state] <= new_node[0]):
                    # If it's not in deadlock or we arent testing for deadlocks save it
                    # if over limit save it in frontier, else save it in stack
                    self.repeated_states[new_state] = new_node[0]
                    if not (self.test_deadlocks and self.sokoban.is_game_over()):
                        if new_node[0] > limit:
                            self.frontier_nodes.add(new_node)
                        else:
                            node_stack.append(new_node)
                # Reload state to make moves again
                self.sokoban.state.load_state(current_node[1])
        return False

    def _IDAStar(self):
        # While elements in frontier
        while self.frontier_nodes:
            # Get the one with least f value
            current_node = self.frontier_nodes.pop(0)

            # Run limited depth search
            solution_node = self._DLS(current_node, current_node[0])
            # If solution found set statistics and return it
            if solution_node:
                self.statistics.cost = self.statistics.deepness = len(solution_node[2])
                self.statistics.time_spent = time() - self.start_time
                self.statistics.frontier_nodes = len(self.frontier_nodes)
                return solution_node[2]
        return False

    def run(self):
        if(self.solution != None):
            return self.solution
        initial_state = self.sokoban.state.save_state()
        self.start_time = time()
        self.solution = self._IDAStar()
        self.sokoban.state.load_state(initial_state)
        return self.solution
    