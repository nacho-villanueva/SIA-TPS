class Statistics:
    def __init__(self, deepness=0, cost=0, expanded_nodes=0, frontier_nodes=0, time_spent=0):
        # Agregar aca todos los statistics de la corrida del algoritmo
        self.deepness = deepness
        self.cost = cost
        self.expanded_nodes = expanded_nodes
        self.frontier_nodes = frontier_nodes
        self.time_spent = time_spent

    def __repr__(self) -> str:
        return f"Depth: {self.deepness}    Cost: {self.cost}    Expanded Nodes: {self.expanded_nodes}    Frontier Nodes: {self.frontier_nodes}    Time Spent: {self.time_spent:.5f}s"
