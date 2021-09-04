from TP2.crossover import *
from TP2.genetic_algorithm import FillType
from TP2.mutation import *
from TP2.selection import *
from TP2.stop import *


def get_crossover_function(algorithm_config):
    if algorithm_config == "one_point":
        return one_point_crossover()
    elif algorithm_config == "two_point":
        return two_point_crossover()
    elif algorithm_config == "annular":
        return annular_crossover()
    elif algorithm_config == "uniform":
        return uniform_crossover()
    else:
        raise Exception(f"Unknown crossover method: {algorithm_config}")


def get_mutation_function(algorithm_config):
    name = algorithm_config["method"]
    if name == "gene":
        return gene_mutation()
    if name == "limited_multiple_gene":
        return limited_multiple_gene_mutation(algorithm_config["M"])
    if name == "uniform_multiple_gene":
        return uniform_multiple_gene_mutation()
    if name == "complete":
        return complete_mutation()
    else:
        raise Exception(f"Unknown mutation method: {name}")


def get_selection_function(algorithm_config):
    name = algorithm_config["method"]
    if name == "elite":
        return elite_selection()
    elif name == "roulette":
        return roulette_selection()
    elif name == "universal":
        return universal_selection()
    elif name == "boltzmann":
        return boltzmann_selection(algorithm_config["Tc"],algorithm_config["T0"],algorithm_config["K"])
    elif name == "deterministic_tournament":
        return deterministic_tournament_selection(algorithm_config["M"])
    elif name == "stochastic_tournament":
        return stochastic_tournament_selection(algorithm_config["threshold"])
    elif name == "ranking":
        return ranking_selection()
    else:
        raise Exception(f"Unknown selection method: {name}")


def get_stop_condition(condition_config):
    name = condition_config["method"]
    if name == "time":
        return time_stop(condition_config["time"])
    elif name == "generation":
        return generation_stop(condition_config["generation"])
    elif name == "fitness":
        return fitness_stop(condition_config["fitness"])
    elif name == "structure":
        return structure_stop(condition_config["relevant_percentage"], condition_config["generations_amount"])
    elif name == "content":
        return content_stop(condition_config["generations_amount"])
    else:
        raise Exception(f"Unknown stop condition: {name}")


implementations = {
    "fill-all": FillType.FILL_ALL,
    "fill-parent": FillType.FILL_PARENT
}

MIN_HEIGHT = 1.3
MAX_HEIGHT = 2.0
