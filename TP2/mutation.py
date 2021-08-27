import random

from TP2.character import Character


def gene_mutation():
    def _gene_mutation(character: Character):
        locus = random.randint(0, 5)
        character.mutate_allele(locus)
    return _gene_mutation


def limited_multiple_gene_mutation():  # TODO: IMPLEMENTAR
    def _limited_multiple_gene_mutation(character: Character):
        pass
    return _limited_multiple_gene_mutation


def uniform_multiple_gene_mutation():  # TODO: IMPLEMENTAR
    def _uniform_multiple_gene_mutation(character: Character):
        pass
    return _uniform_multiple_gene_mutation


def complete_mutation():  # TODO: IMPLEMENTAR
    def _complete_mutation(character: Character):
        pass
    return _complete_mutation
