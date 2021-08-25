from time import time

from TP2 import genetic_algorithm


def time_stop(stop_time):
    def _time_stop(genetic: genetic_algorithm):
        return time() - genetic.start_time < stop_time

    return _time_stop


def generation_stop(stop_generation):
    def _generation_stop(genetic: genetic_algorithm):
        return genetic.generation < stop_generation

    return _generation_stop


def fitness_stop(max_fitness):
    def _fitness_stop(genetic: genetic_algorithm):
        return genetic.max_fitness >= max_fitness

    return _fitness_stop


def structure_stop():  # TODO: IMPLEMENTAR
    pass


def content_stop():  # TODO: IMPLEMENTAR
    pass


def joint_stop(stop_functions: list):
    def _joint_stop(genetic: genetic_algorithm):
        should_stop = False
        for stop in stop_functions:
            should_stop = should_stop or stop(genetic)
        return should_stop

    return _joint_stop
