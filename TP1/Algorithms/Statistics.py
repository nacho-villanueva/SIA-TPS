class Statistics:
    def __init__(self, deepness, cost, expanded_nodes, frontier_nodes, time_spent):
        # Agregar aca todos los statistics de la corrida del algoritmo
        self.deepness = deepness
        self.cost = cost
        self.expanded_nodes = expanded_nodes
        self.frontier_nodes = frontier_nodes
        self.time_spent = time_spent

    def __repr__(self) -> str:
        return f" Stats:( deepness: {self.deepness}, cost: {self.cost},expanded_nodes: {self.expanded_nodes},frontier_nodes: {self.frontier_nodes},time_spent: {self.time_spent})"
