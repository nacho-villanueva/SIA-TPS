from time import time

from TP2.genetic_algorithm import GeneticAlgorithm


def time_stop(stop_time):
    def _time_stop(genetic: GeneticAlgorithm):
        return time() - genetic.start_time > stop_time

    return _time_stop


def generation_stop(stop_generation):
    def _generation_stop(genetic: GeneticAlgorithm):
        return genetic.generation > stop_generation

    return _generation_stop


def fitness_stop(max_fitness):
    def _fitness_stop(genetic: GeneticAlgorithm):
        return genetic.max_fitness_character.fitness > max_fitness

    return _fitness_stop


def structure_stop(percentage: float, generations_amount: int):
    def _structure_stop(genetic: GeneticAlgorithm):
        if len(genetic.generations) < generations_amount:
            return False
        last_generations = genetic.generations[-generations_amount-1:]
        return all(gen.similarity >= percentage for gen in last_generations)

    return _structure_stop


def content_stop():  # TODO: IMPLEMENTAR
    pass


def joint_stop(stop_functions: list):
    def _joint_stop(genetic: GeneticAlgorithm):
        should_stop = False
        for stop in stop_functions:
            should_stop = should_stop or stop(genetic)
        return should_stop

    return _joint_stop
