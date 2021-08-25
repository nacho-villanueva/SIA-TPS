import json
from TP2.crossover import *
from TP2.mutation import *
from TP2.selection import *
from TP2.stop import *
from TP2.genetic_algorithm import GeneticAlgorithm, FillType

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

if __name__ == "__main__":
    file = open("config.json")
    config_dict = json.load(file)
    algorithm = GeneticAlgorithm(
        select_a=selection_functions[config_dict["selection_algorithm_1"]],
        crossover=crossover_functions[config_dict["crossover_algorithm"]],
        mutate=mutation_functions[config_dict["mutation_algorithm"]],
        stop=stop_conditions[config_dict["stop_condition"]],
        repopulate_a=selection_functions[config_dict["replacement_algorithm_1"]],
        fill_type=implementations[config_dict["implementation"]],
        population_size=config_dict["population_size"],
        select_b=selection_functions[config_dict["selection_algorithm_2"]],
        select_coefficient=config_dict["A"],
        repopulate_b=selection_functions[config_dict["replacement_algorithm_2"]],
        repopulate_coefficient=config_dict["B"]
    )
