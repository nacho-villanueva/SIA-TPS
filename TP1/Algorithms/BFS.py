from TP1.Algorithms.Statistics import Statistics
from TP1.Sokoban import Sokoban
from TP1.Algorithms.Algorithm import Algorithm
from time import time

class BFS(Algorithm):
    class SavedState:
        def __init__(self, state, mov, prev_movs):
            self.state = state
            self.mov = mov
            self.prev_movs = prev_movs
        def __repr__(self):
            return f"SavedState({self.state}, {self.mov} )"
        def __eq__(self, other):
            if isinstance(other, BFS.SavedState):
                return ((self.state == other.state) and (self.mov == other.mov))
            else:
                return False
        def __ne__(self, other):
            return (not self.__eq__(other))
        def __hash__(self):
            return hash(self.__repr__())

    def __init__(self, sokoban):
        super().__init__(sokoban)
        self.solution = []
        self.solved = False
        self.statistics = Statistics(0,0,0,0,0)

    def run(self):
        # Check if already solved
        if self.solved:
            return self.solution

        # Statistics related
        t0 = time()
        self.statistics.expanded_nodes = 1
        
        # Save initial state to apply afterwards
        initial_state = self.sokoban.state.save_state()
        # To save previous states to avoid loops
        prev_states = set()
        # Create queue based on the initial available movements
        state_queue = list(map(
            lambda mov: BFS.SavedState(
                self.sokoban.state.save_state(), mov, []
            ),
            self.sokoban.get_possible_movements()
        ))
        
        # Loop while not solved and elements on queue
        while not self.solved and len(state_queue) != 0:
            # Pop first unique state, add to prev_states,
            # load state and make move
            found = False
            while len(state_queue) != 0 and not found:
                state = state_queue.pop(0)
                if not state in prev_states:
                    found = True
            if not found:
                break
            prev_states.add(state)
            self.sokoban.state.load_state(state.state)
            self.sokoban.move(state.mov)
            # Statistics related
            self.statistics.expanded_nodes += 1
            
            # If won then solution has been found
            if self.sokoban.is_game_won():
                self.solution = state.prev_movs.copy()
                self.solution.append(state.mov)
                self.solved = True
            
            # Else if game not over add children to queue
            elif not self.sokoban.is_game_over():
                new_prev_movs = state.prev_movs.copy()
                new_prev_movs.append(state.mov)
                state_queue.extend(
                    map(
                        lambda mov: BFS.SavedState(
                            self.sokoban.state.save_state(),
                            mov,
                            new_prev_movs
                        ),
                        self.sokoban.get_possible_movements()
                    )
                )
        
        # Set statistics
        t1 = time()
        self.statistics.deepness = len(self.solution)
        # TODO: check what is
        # self.statistics.cost
        # Already set by this point
        # self.statistics.expanded_nodes
        self.statistics.frontier_nodes = len(state_queue)
        self.statistics.time_spent = t1 - t0

        # Load initial state and set solved to true
        # Solved indicates if the algorithm has been
        # not wether or not it found a solution
        self.sokoban.state.load_state(initial_state)
        self.solved = True
        return self.solution