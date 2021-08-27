import itertools
import math
import random
from enum import Enum
from random import shuffle
from time import time
from typing import Callable, Any

import numpy as np

from TP2.character import Character


class FillType(Enum):
    FILL_ALL = "fill_all"
    FILL_PARENT = "fill_parent"


SelectFunction = Callable[[list[Character], int], list[Character]]
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
        self.max_fitness_character = None

        self.population = initial_population

    def run(self):
        while not self.stop(self):
            parents = self.select_parents()
            children = self.breed(parents)
            self.population = self.repopulate(children)

            self.generation += 1

    def select_parents(self):
        parents = self.select_a(self.population, math.ceil(self.K * self.select_coefficient))
        if self.select_coefficient < 1:
            parents += self.select_b(self.population, math.floor(self.K * (1 - self.select_coefficient)))

        if self.K % 2 == 1:
            parents.append(random.choice(self.population))

        np.random.shuffle(parents)
        return parents

    def breed(self, parents):
        children_chromosomes = []
        # Crossover Parents
        for father, mother in pairwise(parents):
            children_chromosomes += self.crossover(father, mother)

        # Mutate Children
        for cc in children_chromosomes:
            self.mutate(cc)

        children = []
        for cc in children_chromosomes:
            children.append()

        return children

    def fill_all(self, children):
        all_population = self.population + children
        new_population = self.repopulate_a(all_population,
                                           math.ceil(self.population_size * self.repopulate_coefficient))
        if self.repopulate_coefficient < 1:
            new_population += self.select_b(self.population,
                                            math.floor(self.population_size * (1 - self.repopulate_coefficient)))
        return new_population

    def fill_parent(self, children):
        if self.K > self.population_size:
            new_population = self.repopulate_a(children, math.ceil(self.population_size * self.repopulate_coefficient))
            if self.repopulate_coefficient < 1:
                new_population += self.select_b(self.population,
                                                math.floor(self.population_size * (1 - self.repopulate_coefficient)))
            return new_population

        elif self.K == self.population_size:
            return children

        elif self.K < self.population_size:
            new_population = children
            new_population += self.repopulate_a(self.population, math.ceil(
                (self.population_size - self.K) * self.repopulate_coefficient))
            if self.repopulate_coefficient < 1:
                new_population += self.select_b(self.population, math.floor(
                    (self.population_size - self.K) * (1 - self.repopulate_coefficient)))
            return new_population

    def repopulate(self, children):
        if self.fill_type == FillType.FILL_ALL:
            return self.fill_all(children)
        elif self.fill_type == FillType.FILL_PARENT:
            return self.fill_parent(children)


def pairwise(iterable):
    # Iterate by pairs
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
