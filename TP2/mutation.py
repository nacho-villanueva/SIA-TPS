import random

from TP2.character import Character


def gene_mutation():
    def _gene_mutation(character: Character):
        locus = random.randint(0, 5)
        character.mutate_allele(locus)
    return _gene_mutation


def limited_multiple_gene_mutation():  # TODO: IMPLEMENTAR
    pass


def uniform_multiple_gene_mutation():  # TODO: IMPLEMENTAR
    pass


def complete_mutation():  # TODO: IMPLEMENTAR
    pass
