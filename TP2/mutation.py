import random

from TP2.character import Character

MUTATION_PROBABILITY = 0.5  # TODO: MUTATION PROBABILTY AGREGAR A CONFIG


def gene_mutation():
    def _gene_mutation(character: Character):
        if random.uniform(0, 1) < MUTATION_PROBABILITY:
            locus = random.randint(0, 5)
            character.mutate_allele(locus)

    return _gene_mutation


def limited_multiple_gene_mutation(m):  # TODO: IMPLEMENTAR
    def _limited_multiple_gene_mutation(character: Character):
        loci = random.sample([0, 1, 2, 3, 4, 5], m)
        for locus in loci:
            if random.uniform(0, 1) < MUTATION_PROBABILITY:
                character.mutate_allele(locus)

    return _limited_multiple_gene_mutation


def uniform_multiple_gene_mutation():  # TODO: IMPLEMENTAR
    def _uniform_multiple_gene_mutation(character: Character):
        for locus in range(0, 6):
            if random.uniform(0, 1) < MUTATION_PROBABILITY:
                character.mutate_allele(locus)

    return _uniform_multiple_gene_mutation


def complete_mutation():  # TODO: IMPLEMENTAR
    def _complete_mutation(character: Character):
        if random.uniform(0, 1) < MUTATION_PROBABILITY:
            for locus in range(0, 6):
                character.mutate_allele(locus)

    return _complete_mutation
