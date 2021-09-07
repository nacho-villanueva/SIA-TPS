import random

from TP2.character import Character
from TP2.config import Config


def gene_mutation():
    def _gene_mutation(character: Character):
        if random.uniform(0, 1) < Config().mutation_probability:
            locus = random.randint(0, 5)
            character.mutate_allele(locus)

    return _gene_mutation


def limited_multiple_gene_mutation(m):
    def _limited_multiple_gene_mutation(character: Character):
        loci = random.sample([0, 1, 2, 3, 4, 5], m)
        if random.uniform(0, 1) < Config().mutation_probability:
            for locus in loci:
                character.mutate_allele(locus)

    return _limited_multiple_gene_mutation


def uniform_multiple_gene_mutation():
    def _uniform_multiple_gene_mutation(character: Character):
        for locus in range(0, 6):
            if random.uniform(0, 1) < Config().mutation_probability:
                character.mutate_allele(locus)

    return _uniform_multiple_gene_mutation


def complete_mutation():
    def _complete_mutation(character: Character):
        if random.uniform(0, 1) < Config().mutation_probability:
            for locus in range(0, 6):
                character.mutate_allele(locus)

    return _complete_mutation
