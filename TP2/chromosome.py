from enum import Enum


class CharacterChromosome:
    class Allele(Enum):
        # Defines the order of the alleles
        HEIGHT = 0
        WEAPON = 1
        HELMET = 2
        ARMOUR = 3
        GLOVES = 4
        BOOTS = 5

    def __init__(self, height, weapon, helmet, armour, gloves, boots):
        self.alleles = [None] * 6
        self.alleles[CharacterChromosome.Allele.HEIGHT.value] = height
        self.alleles[CharacterChromosome.Allele.WEAPON.value] = weapon
        self.alleles[CharacterChromosome.Allele.HELMET.value] = helmet
        self.alleles[CharacterChromosome.Allele.ARMOUR.value] = armour
        self.alleles[CharacterChromosome.Allele.GLOVES.value] = gloves
        self.alleles[CharacterChromosome.Allele.BOOTS.value] = boots
