from __future__ import annotations

import math
from enum import Enum
from time import time
from typing import Callable, Any

from TP2.character import Character


class FillType(Enum):
    FILL_ALL = "fill_all"
    FILL_PARENT = "fill_parent"


SelectFunction = Callable[[list[Character], int], list[Character]]
CrossoverFunction = Callable[[tuple[Character, Character]], list[Character]]
MutateFunction = Callable[[Character], Character]
StopFunction = Callable[[Any], bool]


class GeneticAlgorithm:
    def __init__(self, select_a: SelectFunction, crossover: CrossoverFunction, mutate: MutateFunction,
                 stop: StopFunction, repopulate_a: SelectFunction,

                 fill_type=FillType.FILL_ALL, generational_gap=0, population_size=500,

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
        self.population_size = population_size
        self.generational_gap = generational_gap

        self.start_time = time()
        self.generation = 0
        self.max_fitness_character = None

        self.population = []

    def run(self):
        while not self.stop(self):
            PARENT_COUNT = 99999999999999999999999  # TODO ?
            parents = self.select_parents(PARENT_COUNT)
            children = self.breed(parents)
            self.population = self.repopulate(children)

            self.generation += 1

    def select_parents(self, parents_count):  # TODO: ESTA BIEN?
        fathers = self.select_a(self.population, math.ceil(parents_count * self.select_coefficient))
        if self.select_coefficient < 1:
            fathers += self.select_b(self.population, math.floor(parents_count * (1 - self.select_coefficient)))

        mothers = self.select_a(self.population, math.ceil(parents_count * self.select_coefficient))
        if self.select_coefficient < 1:
            mothers += self.select_b(self.population, math.floor(parents_count * (1 - self.select_coefficient)))

        parents = [(fathers[i], mothers[i]) for i in range(parents_count)]
        return parents

    def breed(self, parents):
        children = []
        # Crossover Parents
        for p in parents:
            children += self.crossover(p)

        # Mutate Children
        for i in range(len(children)):
            children[i] = self.mutate(children[i])

        return children

    def fill_all(self, children):  # TODO: IMPLEMENTAR
        return []

    def fill_parent(self, children):  # TODO: IMPLEMENTAR
        return []

    def repopulate(self, children):
        # TODO: AGREGAR BRECHA GENERACIONAL ?
        if self.fill_type == FillType.FILL_ALL:
            return self.fill_all(children)
        elif self.fill_type == FillType.FILL_PARENT:
            return self.fill_parent(children)


# TODO: PREGUNTAR
''' 
Preguntas:
1) Como se define Padre y Madre? Se corre el metodo de seleccion 2 veces para obtener 2 listas y combinar el primero con el primero, segundo con segundo..? 
2) El K (numero de hijos) es arbitrario?
3) Como se define la cantidad de padres? Es K/2 ya que cada par de padre generan 2 hijos?
4) Hay que implementar brecha generacional? Como se eligen los que se salvan/persisten a la proxima generacion?
'''
