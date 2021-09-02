from TP2.genetic_algorithm import GeneticAlgorithm
import random

import numpy as np
from numpy.lib import math
from sortedcontainers import SortedList

from TP2.character import Character


def elite_selection():
    def _elite_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
        sorted_collection = sorted(population, reverse=True)
        selection = sorted_collection * (k // len(sorted_collection))
        selection += sorted_collection[:k % len(sorted_collection)]
        return selection

    return _elite_selection


def roulette_selection():  # TODO: IMPLEMENTAR
    def _roulette_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
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
    def _universal_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
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


def boltzmann_selection():  # TODO: Check
    def _boltzmann_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
        N = len(population)
        # First get the upper half of the equation of EXP
        # and the sum to later get the average
        new_relative = []
        sum_over_pop = 0
        # numero de generacion
        t  = genetic_algorithm.generation
        # T = Tc + (T0 - Tc) * (math.e ** ( - kconst * t))
        temperature = 100 + (1000 - 100) * (math.e ** ( - 10 * t)) # TODO: revisar estos numeros
        for i in range(N):
            exp = math.e ** (population[i].fitness / temperature)
            new_relative.append(exp)
            sum_over_pop += exp
        # Get the average and de sum of total fitnesses(aka, the sum of the 
        # upper half divided by de average)
        avg_over_pop = sum_over_pop / N
        sum_over_pop /= avg_over_pop
        # Calculate the fitness and then transform it to relative
        for i in range(N):
            new_relative[i] = (new_relative[i] / avg_over_pop) / sum_over_pop
        # Accumulate
        accumulated_relative_fitness = [0]
        for i in range(N):
            accumulated_relative_fitness.append(0)
            for j in range(i+1):
                accumulated_relative_fitness[i+1] += new_relative[j]
        # Finally, run roulette
        selected = []
        for i in range(k):
            r = random.uniform(0, 1)
            for j in range(N):
                if accumulated_relative_fitness[j] < r <= accumulated_relative_fitness[j+1]:
                    selected.append(population[j])
        return selected
    return _boltzmann_selection


def deterministic_tournament_selection(M):  # TODO: IMPLEMENTAR
    def _deterministic_tournament_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
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
    def _stochastic_tournament_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
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
    def _ranking_selection(population: list[Character], k, genetic_algorithm:GeneticAlgorithm):
        # Sort from highest to lowest
        sorted_pop = sorted(population, reverse=True)
        N = len(sorted_pop)
        # Get the new relative fitnesses
        new_relative = []
        for i  in range(N):
            new_relative.append(2 * (N - i) / ( ( N + 1 ) * N ))
        # Accumulate them with a 0 at the start
        accumulated_relative_fitness = [0]
        for i in range(N):
            accumulated_relative_fitness.append(0)
            for j in range(i+1):
                accumulated_relative_fitness[i+1] += new_relative[j]
        # Run roulette on this
        selected = []
        for i in range(k):
            r = random.uniform(0, 1)
            for j in range(N):
                if accumulated_relative_fitness[j] < r <= accumulated_relative_fitness[j+1]:
                    selected.append(sorted_pop[j])
        return selected
    return _ranking_selection
