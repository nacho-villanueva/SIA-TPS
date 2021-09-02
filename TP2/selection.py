import random

import numpy as np
from numpy.lib import math
from sortedcontainers import SortedList

from TP2.character import Character


def elite_selection():
    def _elite_selection(collection: list[Character], k):
        sorted_collection = sorted(collection, reverse=True)
        selection = sorted_collection * (k // len(sorted_collection))
        selection += sorted_collection[:k % len(sorted_collection)]
        return selection

    return _elite_selection


def roulette_selection():  # TODO: IMPLEMENTAR
    def _roulette_selection(population: list[Character], k):
        accumulated_relative_fitness = get_accumulated_relative_fitness(population)
        selected = []
        for i in range(k):
            r = random.uniform(0, 1)
            for j in range(len(accumulated_relative_fitness) - 1):
                if accumulated_relative_fitness[j] < r <= accumulated_relative_fitness[i+1]:
                    selected.append(accumulated_relative_fitness[i+1])
        return selected

    return _roulette_selection


def universal_selection():  # TODO: IMPLEMENTAR
    def _universal_selection(population: list[Character], k):
        accumulated_relative_fitness = get_accumulated_relative_fitness(population)
        selected = []
        for j in range(k):
            r = random.uniform(0, 1)
            r = (r + j) / k
            for i in range(len(accumulated_relative_fitness) - 1):
                if accumulated_relative_fitness[i] < r <= accumulated_relative_fitness[i+1]:
                    selected.append(accumulated_relative_fitness[i+1])
        return selected

    return _universal_selection


def get_accumulated_relative_fitness(population: list[Character]):
    accumulated_fitness = np.array([0])
    total_fitness = population[0].fitness
    for i in range(1, len(population)):
        total_fitness += population[i].fitness
        accumulated_fitness[i] = population[i].fitness + accumulated_fitness[i - 1]
    return accumulated_fitness / total_fitness


def boltzmann_selection():  # TODO: IMPLEMENTAR
    return []


def deterministic_tournament_selection(M):  # TODO: IMPLEMENTAR
    def _deterministic_tournament_selection(population: list[Character], k):
        selected = []
        for i in range(k):
            m_individuals = SortedList(key=sort_by_fitness)
            while len(m_individuals) < M:
                random_index = random.randint(0, len(population) - 1)
                random_individual = population[random_index]
                m_individuals.add(random_individual)  # Los M individuos son elegidos con reposición TODO: esta bien?
            selected.append(m_individuals[-1])  # Los K individuos son elegidos con reposición TODO: esta bien?
        return selected

    return _deterministic_tournament_selection


def sort_by_fitness(individual: Character):
    return individual.fitness


def stochastic_tournament_selection(threshold):  # TODO: IMPLEMENTAR
    def _stochastic_tournament_selection(population: list[Character], k):
        selected = []
        for i in range(k):
            two_individuals = SortedList(key=sort_by_fitness)
            two_individuals.add(population[random.randint(0, len(population) - 1)])
            two_individuals.add(population[random.randint(0, len(population) - 1)])
            r = random.uniform(0, 1)
            if r < threshold:
                selected.append(two_individuals[1])
            else:
                selected.append(two_individuals[0])
        return selected

    return _stochastic_tournament_selection


def ranking_selection():  # TODO: IMPLEMENTAR
    def _ranking_selection(population: list[Character], k):
        sorted_pop = sorted(population, reverse=True)
        N = len(sorted_pop)
        new_relative = []
        for i  in range(N):
            new_relative.append(2 * (N - i) / ( ( N + 1 ) * N ))
        accumulated_relative_fitness = [0]
        for i in range(N):
            accumulated_relative_fitness.append(0)
            for j in range(i+1):
                accumulated_relative_fitness[i+1] += new_relative[j]
        selected = []
        for i in range(k):
            r = random.uniform(0, 1)
            for j in range(N):
                if accumulated_relative_fitness[j] < r <= accumulated_relative_fitness[j+1]:
                    selected.append(sorted_pop[j])
        return selected
    return _ranking_selection
