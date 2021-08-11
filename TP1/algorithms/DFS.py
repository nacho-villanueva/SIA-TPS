from TP1.algorithms.algorithm import Algorithm
from TP1.algorithms.statistics import Statistics
from time import time


class DFS(Algorithm):
    def __init__(self, sokoban):
        super(DFS, self).__init__(sokoban)
        self.passed_nodes = set()
        self.movements_made = []
        self.solution_found = False
        self.current_node = None   # es una tupla de la forma ( (1,2), ((3,3),(4,4)) )
        self.statistics = Statistics(0, 0, 0, 0, 0)
        # Frontera, cada nodo tiene la forma (self.current_node, last_movement, deepness)
        self.fr = []

    def run(self):
        root_node = self.sokoban.state.save_state()
        self.current_node = root_node
        self.fr.append((self.current_node, None, 0))

        t0 = time()
        while not self.solution_found and len(self.fr) > 0:
            self.statistics.deepness += 1
            self.current_node = self.fr.pop()
            self.passed_nodes.add(self.current_node[0])
            self.sokoban.state.load_state(self.current_node[0])

            possible_movements = self.sokoban.get_possible_movements()

            new_node_inserted = False
            last_valid_movement = None
            for movement in possible_movements:
                # Lleno la frontera Fr con los hijos
                self.sokoban.move(movement)
                node_to_insert = self.sokoban.state.save_state()
                if node_to_insert not in self.passed_nodes and not self.sokoban.is_game_over():
                    new_node_inserted = True
                    self.fr.append((node_to_insert, movement, self.statistics.deepness))
                    last_valid_movement = movement
                    if self.sokoban.is_game_won():
                        self.solution_found = True
                        break
                self.sokoban.state.load_state(self.current_node[0])

            if new_node_inserted:
                self.movements_made.append(last_valid_movement)
                # Si tengo al menos un hijo, significa que me expandí
                self.statistics.expanded_nodes += 1
            else:
                aux = self.fr.pop()
                for i in range(aux[2], self.statistics.deepness):
                    self.movements_made.pop()
                self.movements_made.append(aux[1])
                self.statistics.deepness = aux[2]
                self.fr.append(aux)

        t1 = time()

        print(f"Solution found = {self.solution_found}")
        self.statistics.time_spent = t1 - t0
        self.sokoban.state.load_state(root_node)
        return self.movements_made
