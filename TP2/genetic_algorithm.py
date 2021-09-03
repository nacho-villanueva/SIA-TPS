import itertools
import math
import random
from enum import Enum
from time import time
from typing import Callable, Any

import matplotlib.pyplot as plt
import numpy as np

from TP2.character import Character
from TP2.generation import Generation
from TP2.realtime_graph import RealTimeGraphDrawer


class FillType(Enum):
    FILL_ALL = "fill_all"
    FILL_PARENT = "fill_parent"

SelectFunction = Callable[[list[Character], int, 'GeneticAlgorithm'], list[Character]]
CrossoverFunction = Callable[[Character, Character], list[Character]]
MutateFunction = Callable[[Character], None]
StopFunction = Callable[[Any], bool]


class GeneticAlgorithm:
    def __init__(self, select_a: SelectFunction, crossover: CrossoverFunction, mutate: MutateFunction,
                 stop: StopFunction, repopulate_a: SelectFunction, initial_population: list[Character],

                 fill_type=FillType.FILL_ALL, k=50,

                 select_b: SelectFunction = None, select_coefficient=1.0,
                 repopulate_b: SelectFunction = None, repopulate_coefficient=1.0):
        self.stop = stop
        self.mutate = mutate
        self.select_a = select_a
        self.select_b = select_b
        self.repopulate_a = repopulate_a
        self.repopulate_b = repopulate_b
        self.crossover = crossover

        self.select_coefficient = select_coefficient
        self.repopulate_coefficient = repopulate_coefficient

        self.fill_type = fill_type
        self.population_size = len(initial_population)
        self.K = k

        self.start_time = time()
        self.generation = 0

        self.population = initial_population
        self.max_fitness_character = self.population[0]
        self.find_max_fitness()

        self.generations = [Generation(0, self.calculate_similarity(), self.max_fitness_character.fitness)]

    def run(self):
        graph = RealTimeGraphDrawer()
        while not self.stop(self):
            # print(f"Generation {self.generation} - Max Fit: {self.max_fitness_character}")

            parents = self.select_parents()
            children = self.breed(parents)
            self.population = self.repopulate(children)

            self.generation += 1

            previous_best_character = self.max_fitness_character
            self.find_max_fitness()  # Updates max_fitness_character
            if previous_best_character.fitness < self.max_fitness_character.fitness:
                print(f"New best character found in generation {self.generation}: [{self.max_fitness_character}]")

            self.generations.append(
                Generation(self.generation, self.calculate_similarity(), self.max_fitness_character.fitness))

            # Uncomment to see how the calculate_similarity() works
            # print(f"Generation {self.generation} similarity = {self.generations[-1].similarity}%")

            min_fit, max_fit, avg_fit, diversity = self.get_graph_data()
            graph.push_and_draw(min_fit, max_fit, avg_fit, diversity)

        print(f"Best {self.max_fitness_character.role} found: [{self.max_fitness_character}]")

        plt.show()

    def select_parents(self):
        parents = self.select_a(self.population, math.ceil(self.K * self.select_coefficient),self)
        if self.select_coefficient < 1:
            parents += self.select_b(self.population, math.floor(self.K * (1 - self.select_coefficient)),self)

        if self.K % 2 == 1:
            parents.append(random.choice(self.population))

        np.random.shuffle(parents)
        return parents

    def breed(self, parents):
        children = []
        # Crossover Parents
        for father, mother in pairwise(parents):
            children += self.crossover(father, mother)

        # Mutate Children
        for c in children:
            self.mutate(c)

        return children

    def fill_all(self, children):
        all_population = self.population + children
        new_population = self.repopulate_a(all_population,
                                           math.ceil(self.population_size * self.repopulate_coefficient),self)
        if self.repopulate_coefficient < 1:
            new_population += self.select_b(self.population,
                                            math.floor(self.population_size * (1 - self.repopulate_coefficient)),self)
        return new_population

    def fill_parent(self, children):
        if self.K > self.population_size:
            new_population = self.repopulate_a(children, math.ceil(self.population_size * self.repopulate_coefficient),self)
            if self.repopulate_coefficient < 1:
                new_population += self.select_b(self.population,
                                                math.floor(self.population_size * (1 - self.repopulate_coefficient)),self)
            return new_population

        elif self.K == self.population_size:
            return children

        elif self.K < self.population_size:
            new_population = children
            new_population += self.repopulate_a(self.population, math.ceil(
                (self.population_size - self.K) * self.repopulate_coefficient),self)
            if self.repopulate_coefficient < 1:
                new_population += self.select_b(self.population, math.floor(
                    (self.population_size - self.K) * (1 - self.repopulate_coefficient)),self)
            return new_population

    def repopulate(self, children):
        if self.fill_type == FillType.FILL_ALL:
            return self.fill_all(children)
        elif self.fill_type == FillType.FILL_PARENT:
            return self.fill_parent(children)

    def find_max_fitness(self):
        max_fit = self.population[0]
        for p in self.population:
            if max_fit.fitness < p.fitness:
                max_fit = p
        self.max_fitness_character = max_fit

    def get_graph_data(self):
        min_fit = self.population[0].fitness
        max_fit = self.population[0].fitness
        locuses = [i for i in Character.Allele]
        diversity = [set() for _ in locuses]
        sum_fit = 0
        for p in self.population:
            if min_fit > p.fitness:
                min_fit = p.fitness
            if max_fit < p.fitness:
                max_fit = p.fitness
            sum_fit += p.fitness
            for i in range(len(locuses)):
                diversity[i].add(p.get_allele(locuses[i]))
        diversity = np.average(list(map(lambda x: len(x), diversity)))
        return min_fit, max_fit, sum_fit  / len(self.population), diversity

    # Returns a number [0, 100] representing the percentage of similarity in the population
    # A value of 100 means that the whole population is the same
    # A value of 0 means that the whole population is different
    def calculate_similarity(self):
        without_duplicates = list(dict.fromkeys(self.population))
        return 100.0 - (len(without_duplicates) * 100.0 / len(self.population))


def pairwise(iterable):
    # Iterate by pairs
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
