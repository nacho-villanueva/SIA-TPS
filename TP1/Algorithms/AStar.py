from time import time
from sortedcontainers import SortedList

from TP1.Algorithms.Algorithm import Algorithm
from TP1.Algorithms.Statistics import Statistics


def sort_state(state):
    return state[4]  # Ordena por heurística


class AStar(Algorithm):
    def __init__(self, sokoban, heuristic):
        super(AStar, self).__init__(sokoban)
        self.passed_nodes = set()
        self.solution_found = False
        self.current_node = None
        self.statistics = Statistics(0, 0, 0, 0, 0)
        self.fr = SortedList(key=sort_state)
        self.heuristic = heuristic
        self.winning_node = None

    def run(self):
        if self.sokoban.is_game_won():
            # Caso especial: el juego estaba ganado desde el comienzo
            print(f"Solution found = {True}")
            self.statistics.time_spent = 0
            return []

        if self.sokoban.is_game_over():
            # Caso especial: el juego estaba perdido desde el comienzo
            print(f"Solution found = {False}")
            self.statistics.time_spent = 0
            return []

        t0 = time()

        root_node = self.sokoban.state.save_state()
        self.current_node = root_node
        self.fr.add((self.current_node, None, None, 0, self.heuristic(self.sokoban)))

        while not self.solution_found and len(self.fr) > 0:
            self.statistics.deepness += 1

            # El primer elemento es el de menor heuristica
            self.current_node = self.fr.pop(index=0)
            self.passed_nodes.add(self.current_node[0])
            self.sokoban.state.load_state(self.current_node[0])

            possible_movements = self.sokoban.get_possible_movements()

            new_node_inserted = False
            for movement in possible_movements:
                # Lleno la frontera Fr con los hijos
                self.sokoban.move(movement)
                node_to_insert = self.sokoban.state.save_state()
                if node_to_insert not in self.passed_nodes and not self.sokoban.is_game_over():
                    new_node_inserted = True
                    new_fr_element = (node_to_insert, movement, self.current_node, self.statistics.deepness, self.heuristic(self.sokoban))
                    self.fr.add(new_fr_element)
                    if self.sokoban.is_game_won():
                        self.solution_found = True
                        self.winning_node = (new_fr_element, movement)
                        break
                self.sokoban.state.load_state(self.current_node[0])

            if new_node_inserted:
                # Si tengo al menos un hijo, significa que me expandí
                self.statistics.expanded_nodes += 1

            aux = self.fr.__getitem__(index=0)
            self.statistics.deepness = aux[3]

        t1 = time()
        self.statistics.time_spent = t1 - t0

        print(f"Solution found = {self.solution_found}")

        if self.winning_node is not None:
            self.sokoban.state.load_state(root_node)
            movements_to_win = [self.winning_node[1]]
            parent = self.winning_node[0][2]
            while parent is not None and parent[1] is not None:
                movements_to_win.append(parent[1])
                parent = parent[2]
            movements_to_win.reverse()
            return movements_to_win
        else:
            return []
