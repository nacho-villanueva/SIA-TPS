from TP2.crossover import *
from TP2.genetic_algorithm import FillType
from TP2.mutation import *
from TP2.selection import *
from TP2.stop import *

crossover_functions = {
    "one_point": one_point_crossover,
    "two_point": two_point_crossover,
    "anular": annular_crossover,
    "uniform": uniform_crossover
}

mutation_functions = {
    "gene": gene_mutation,
    "limited_multiple_gene": limited_multiple_gene_mutation,
    "uniform_multiple_gene": uniform_multiple_gene_mutation,
    "complete": complete_mutation
}

selection_functions = {
    "elite": elite_selection,
    "roulette": roulette_selection,
    "universal": universal_selection,
    "boltzmann": boltzmann_selection,
    "deterministic_tournament": deterministic_tournament_selection,
    "stochastic_tournament": stochastic_tournament_selection,
    "ranking": ranking_selection
}

stop_conditions = {
    "time": time_stop,
    "generation": generation_stop,
    "fitness": fitness_stop,
    "structure": structure_stop,
    "content": content_stop
}

implementations = {
    "fill-all": FillType.FILL_ALL,
    "fill-parent": FillType.FILL_PARENT
}

MIN_HEIGHT = 1.3
MAX_HEIGHT = 2.0
