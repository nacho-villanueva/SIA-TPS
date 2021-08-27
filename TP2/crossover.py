import random
from copy import copy

from TP2.character import Character


# TODO: TRANSFERIR APELLIDO DEL MAYOR FITNESS
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


def two_point_crossover():
    def _two_point_crossover(father: Character, mother: Character):
        child_a = copy(father)
        child_b = copy(mother)

        point_1 = random.randint(0, 6)
        point_2 = random.randint(point_1, 6)
        for i in range(point_1, point_2):
            father_allele = father.get_allele(i)
            child_b.set_allele(i, father_allele)

            mother_allele = mother.get_allele(i)
            child_a.set_allele(i, mother_allele)
        return [child_a, child_b]

    return _two_point_crossover


def annular_crossover():
    def _annular_crossover(father: Character, mother: Character):
        child_a = copy(father)
        child_b = copy(mother)

        point = random.randint(0, 6)
        length = random.randint(0, 3)
        for i in range(point, min(point + length, 6)):
            father_allele = father.get_allele(i)
            child_b.set_allele(i, father_allele)

            mother_allele = mother.get_allele(i)
            child_a.set_allele(i, mother_allele)
        return [child_a, child_b]

    return _annular_crossover


def uniform_crossover():  # TODO: IMPLEMENTAR
    def _uniform_crossover(father: Character, mother: Character):
        child_a = copy(father)
        child_b = copy(mother)

        for i in range(0, 6):
            swap = random.uniform(0, 1) < 0.5
            if swap:
                father_allele = father.get_allele(i)
                child_b.set_allele(i, father_allele)

                mother_allele = mother.get_allele(i)
                child_a.set_allele(i, mother_allele)
        return [child_a, child_b]

    return _uniform_crossover
