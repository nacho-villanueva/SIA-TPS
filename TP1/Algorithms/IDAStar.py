from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics
from queue import PriorityQueue


class IDAStar(Algorithm):
    class SavedState:
        def __init__(self, f_result ,state, prev_movs):
            self.f_result = f_result
            self.state = state
            self.prev_movs = prev_movs
        def __repr__(self):
            return f"SavedState( {self.state} )"
        def __eq__(self, other):
            if isinstance(other, IDAStar.SavedState):
                return (self.state == other.state)
            else:
                return False
        def __lt__(self,other):
            return self.f_result < other.f_result
        def __ne__(self, other):
            return (not self.__eq__(other))
        def __hash__(self):
            return hash(self.__repr__())

    def __init__(self, sokoban, f):
        super().__init__(sokoban)
        self.f = f
        self.solution = []
        self.solved = False
        self.statistics = Statistics(0,0,0,0,0)
        

    def run(self):
        # If the solution has already been found then return that
        if self.solved:
            return self.solution

        # To restore it at the end
        initial_state = self.sokoban.state.save_state()
        # So as to not repeat ourselves
        prev_states = set()
        # Start the priority queue
        frontier = PriorityQueue()
        frontier.put(IDAStar.SavedState(self.f(initial_state),initial_state,[]))
        # While not solved and items in queue
        while not self.solved and frontier.qsize() > 0:
            # Pop first unique state, add to prev_states,
            # load state and make move
            found = False
            while not found and frontier.qsize() > 0:
                start_state = frontier.get()
                if not start_state in prev_states:
                    found = True
            if not found:
                break
            prev_states.add(start_state)
            self.sokoban.state.load_state(start_state.state)
            dfs_stack = [start_state]
            dfs_prev_states = set()

            # TODO: check if < or <=
            while not self.solved and len(dfs_stack) > 0:
                dfs_found = False
                while not dfs_found and len(dfs_stack) != 0 :
                    state = dfs_stack.pop()
                    if not state in dfs_prev_states:
                        dfs_found = True
                if not dfs_found:
                    break
                if state.f_result > start_state.f_result:
                    break
                dfs_prev_states.add(state)
                self.sokoban.state.load_state(state.state)
                for move in self.sokoban.get_possible_movements():
                    self.sokoban.move(move)
                    if self.sokoban.is_game_won():
                        self.solved = True
                        self.solution =  state.prev_movs.copy()
                        self.solution.append(move)
                        break
                    elif not self.sokoban.is_game_over():
                        prev_movs = state.prev_movs.copy()
                        prev_movs.append(move)
                        state_to_save = self.sokoban.state.save_state()
                        dfs_stack.append(IDAStar.SavedState(self.f(state_to_save),state_to_save,prev_movs))
                    self.sokoban.state.load_state(state.state)
            if not self.solved:
                for s in dfs_stack:
                    frontier.put(s)


        self.statistics.deepness = len(self.solution)
        self.statistics.cost = self.statistics.deepness
        # Already set by this point
        # self.statistics.expanded_nodes
        self.statistics.frontier_nodes = frontier.qsize()
        # self.statistics.time_spent = t1 - t0

        # Load initial state and set solved to true
        # Solved indicates if the algorithm has been
        # not wether or not it found a solution
        self.sokoban.state.load_state(initial_state)
        self.solved = True
        self.sokoban.state.load_state(initial_state)
        return self.solution
