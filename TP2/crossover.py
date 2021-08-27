import random
from copy import copy

from TP2.character import Character


def one_point_crossover():
    def _one_point_crossover(father: Character, mother: Character):
        child_a = copy(father)
        child_b = copy(mother)

        point = random.randint(0, 6)

        for i in range(point):
            father_allele = father.get_allele(i)
            child_b.set_allele(i, father_allele)

            mother_allele = mother.get_allele(i)
            child_a.set_allele(i, mother_allele)
        return [child_a, child_b]

    return _one_point_crossover


def two_point_crossover():  # TODO: IMPLEMENTAR
    def _two_point_crossover(father: Character, mother: Character):
        return []
    return _two_point_crossover


def annular_crossover():  # TODO: IMPLEMENTAR
    def _annular_crossover(father: Character, mother: Character):
        return []
    return _annular_crossover


def uniform_crossover():  # TODO: IMPLEMENTAR
    def _uniform_crossover(father: Character, mother: Character):
        return []
    return _uniform_crossover
