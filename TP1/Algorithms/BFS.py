from TP1.Algorithms.Statistics import Statistics
from TP1.Sokoban import Sokoban
from TP1.Algorithms.Algorithm import Algorithm
from time import time

class BFS(Algorithm):
    class SavedState:
        def __init__(self, state, prev_movs):
            self.state = state
            self.prev_movs = prev_movs
        def __repr__(self):
            return f"SavedState( {self.state} )"
        def __eq__(self, other):
            if isinstance(other, BFS.SavedState):
                return (self.state == other.state)
            else:
                return False
        def __ne__(self, other):
            return (not self.__eq__(other))
        def __hash__(self):
            return hash(self.__repr__())

    def __init__(self, sokoban, check_deadlock = True):
        super().__init__(sokoban)
        self.check_deadlock = check_deadlock
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
        
        # Save initial state to restore it at the end
        initial_state = self.sokoban.state.save_state()
        # To save previous states to avoid loops
        prev_states = set()
        # Create queue based on the initial state
        frontier = [BFS.SavedState(initial_state,[])] 
        
        # Loop while not solved and elements on queue
        while not self.solved and len(frontier) != 0:
            # Pop first unique state, add to prev_states,
            # load state and make move
            found = False
            while len(frontier) != 0 and not found:
                state = frontier.pop(0)
                if not state in prev_states:
                    found = True
            if not found:
                break
            prev_states.add(state)
            self.sokoban.state.load_state(state.state)
            
            # Check possible moves, try move and save state
            for move in self.sokoban.get_possible_movements():
                # Make move to test
                self.sokoban.move(move)
                # Statistics related
                self.statistics.expanded_nodes += 1
                
                # If won then solution has been found
                if self.sokoban.is_game_won():
                    self.solution = state.prev_movs.copy()
                    self.solution.append(move)
                    self.solved = True
                    break
                
                # Else if game not over add children to queue
                elif not self.check_deadlock or not self.sokoban.is_game_over():
                    prev_movs = state.prev_movs.copy()
                    prev_movs.append(move)
                    frontier.append(BFS.SavedState(self.sokoban.state.save_state(),prev_movs))

                # Restore state for next move
                self.sokoban.state.load_state(state.state)
        
        # Set statistics
        t1 = time()
        self.statistics.deepness = len(self.solution)
        self.statistics.cost = self.statistics.deepness
        # Already set by this point
        # self.statistics.expanded_nodes
        self.statistics.frontier_nodes = len(frontier)
        self.statistics.time_spent = t1 - t0

        # Load initial state and set solved to true
        # Solved indicates if the algorithm has been
        # not wether or not it found a solution
        self.sokoban.state.load_state(initial_state)
        self.solved = True
        return self.solution