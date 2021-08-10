from TP1.Sokoban import Sokoban, Movement
from TP1.algorithms.algorithm import Algorithm

class IDDFS(Algorithm):
    def __init__(self, sokoban: Sokoban, max_depth=500):
        super().__init__(sokoban)
        self.repeated_states = set()
        self.max_depth = max_depth
        self.best_solution = "lurulrdrdru"
        self.i = 0

    def _DLS(self, limit, movements):
        current_state = self.sokoban.state.save_state()

        if current_state in self.repeated_states:
            return False, []

        self.repeated_states.add(current_state)

        if limit <= 0:
            return False, []

        if self.sokoban.is_game_won():
            return True, []

        if self.sokoban.is_game_over():
            return False, []

        possible_movements = self.sokoban.get_possible_movements()

        for m in possible_movements:
            self.sokoban.move(m)

            solution = self._DLS(limit-1, movements + [m])
            if solution[0]:
                solution[1].append(m)
                return True, solution[1]
            self.sokoban.state.load_state(current_state)
        return False, []

    def run(self):
        self.repeated_states = set()
        solution = self._DLS(15, [])
        if solution[0]:
            solution[1].reverse()
            return solution[1]

        # for i in range(10, self.max_depth):
        #     if i % 10 == 0:
        #         print(f"Depth: {i}")
        #     self.repeated_states = set()
        #     solution = self._DLS(i)
        #     if solution[0]:
        #         solution[1].reverse()
        #         return solution[1]
        print("Max depth reached.")
        return []

