import math
import random
from enum import Enum

from TP2.config import Config
from TP2.datasets import DatasetLibrary
from TP2.items.armour import Armour
from TP2.items.boots import Boots
from TP2.items.gloves import Gloves
from TP2.items.helmet import Helmet
from TP2.items.weapon import Weapon


class CharacterRole(Enum):
    WARRIOR = (0.6, 0.6)  # Guerrero
    ARCHER = (0.9, 0.1)  # Arquero
    TANK = (0.3, 0.8)  # Defensor
    ASSASSIN = (0.8, 0.3)  # Infiltrado

    def __init__(self, attack_coefficient, defense_coefficient):
        self.attack_coefficient = attack_coefficient
        self.defense_coefficient = defense_coefficient

    def __str__(self):
        if self == CharacterRole.TANK:
            return "Tank"
        elif self == CharacterRole.WARRIOR:
            return "Warrior"
        elif self == CharacterRole.ARCHER:
            return "Archer"
        elif self == CharacterRole.ASSASSIN:
            return "Assassin"

    @staticmethod
    def get_role_by_role_name(name):
        if name == "archer":
            return CharacterRole.ARCHER
        elif name == "warrior":
            return CharacterRole.WARRIOR
        elif name == "tank":
            return CharacterRole.TANK
        elif name == "assassin":
            return CharacterRole.ASSASSIN


class Gear:
    def __init__(self, weapon: Weapon, armour: Armour, helmet: Helmet, gloves: Gloves, boots: Boots):
        self.boots = boots
        self.gloves = gloves
        self.helmet = helmet
        self.armour = armour
        self.weapon = weapon

    def __iter__(self):
        return [self.weapon, self.armour, self.helmet, self.gloves, self.boots].__iter__()

    def __eq__(self, other):
        if isinstance(other, Gear):
            is_equal = other.weapon.item_id == self.weapon.item_id
            is_equal = is_equal and other.gloves.item_id == self.gloves.item_id
            is_equal = is_equal and other.helmet.item_id == self.helmet.item_id
            is_equal = is_equal and other.armour.item_id == self.armour.item_id
            is_equal = is_equal and other.boots.item_id == self.boots.item_id
            return is_equal

    def __hash__(self):
        return hash((self.weapon.item_id, self.armour.item_id, self.gloves.item_id, self.helmet.item_id, self.boots.item_id))


class Character:
    class Allele(Enum):
        # Defines the order of the alleles
        HEIGHT = 0
        WEAPON = 1
        HELMET = 2
        ARMOUR = 3
        GLOVES = 4
        BOOTS = 5

    def __init__(self, role: CharacterRole, height: float, gear: Gear, lastname: str):
        self.role = role
        self.height = height
        self.gear = gear
        self.lastname = lastname

        self.strength = self.calculate_strength()  # Fuerza
        self.endurance = self.calculate_endurance()  # Resistencia
        self.agility = self.calculate_agility()  # Agilidad
        self.vitality = self.calculate_vitality()  # Vida
        self.intelligence = self.calculate_intelligence()  # Pericia

        self.attack = self.calculate_attack()
        self.defense = self.calculate_defense()

        self.fitness = self.calculate_fitness()

    def recalculate_stats(self):
        self.strength = self.calculate_strength()
        self.endurance = self.calculate_endurance()
        self.agility = self.calculate_agility()
        self.vitality = self.calculate_vitality()
        self.intelligence = self.calculate_intelligence()

        self.attack = self.calculate_attack()
        self.defense = self.calculate_defense()

        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        return self.role.attack_coefficient * self.attack + self.role.defense_coefficient * self.defense

    def calculate_attack(self):
        attack_modifier = 0.7 - (3 * self.height - 5) ** 4 + (3 * self.height - 5) ** 2 + (self.height / 4.0)
        return (self.agility + self.intelligence) * self.strength * attack_modifier

    def calculate_defense(self):
        defense_modifier = 1.9 + (2.5 * self.height - 4.16) ** 4 - (2.5 * self.height - 4.16) ** 2 - (
                3 * self.height / 10.0)
        return (self.endurance + self.intelligence) * self.vitality * defense_modifier

    def calculate_strength(self):
        strength = 0
        for item in self.gear:
            strength += item.strength
        return 100 * math.tanh(0.01 * strength)

    def calculate_endurance(self):
        endurance = 0
        for item in self.gear:
            endurance += item.endurance
        return math.tanh(0.01 * endurance)

    def calculate_agility(self):
        agility = 0
        for item in self.gear:
            agility += item.agility
        return math.tanh(0.01 * agility)

    def calculate_vitality(self):
        vitality = 0
        for item in self.gear:
            vitality += item.vitality
        return 100 * math.tanh(0.01 * vitality)

    def calculate_intelligence(self):
        intelligence = 0
        for item in self.gear:
            intelligence += item.intelligence
        return 0.6 * math.tanh(0.01 * intelligence)

    def mutate_allele(self, locus):
        allele = Character.Allele(locus)
        dl = DatasetLibrary()
        if allele == Character.Allele.HEIGHT:
            configs = Config()
            multiplier = 10 ** configs.precision
            self.height = random.randint(configs.min_height * multiplier, configs.max_height * multiplier) / multiplier
        elif allele == Character.Allele.WEAPON:
            self.gear.weapon = dl.get_random_item(DatasetLibrary.DatasetType.WEAPON)
        elif allele == Character.Allele.ARMOUR:
            self.gear.armour = dl.get_random_item(DatasetLibrary.DatasetType.ARMOUR)
        elif allele == Character.Allele.HELMET:
            self.gear.helmet = dl.get_random_item(DatasetLibrary.DatasetType.HELMET)
        elif allele == Character.Allele.GLOVES:
            self.gear.gloves = dl.get_random_item(DatasetLibrary.DatasetType.GLOVES)
        elif allele == Character.Allele.BOOTS:
            self.gear.boots = dl.get_random_item(DatasetLibrary.DatasetType.BOOTS)
        else:
            raise Exception(f"Locus {locus} out of range")
        self.recalculate_stats()

    def set_allele(self, locus, value):
        allele = Character.Allele(locus)
        if allele == Character.Allele.HEIGHT:
            self.height = value
        elif allele == Character.Allele.WEAPON:
            self.gear.weapon = value
        elif allele == Character.Allele.ARMOUR:
            self.gear.armour = value
        elif allele == Character.Allele.HELMET:
            self.gear.helmet = value
        elif allele == Character.Allele.GLOVES:
            self.gear.gloves = value
        elif allele == Character.Allele.BOOTS:
            self.gear.boots = value
        else:
            raise Exception(f"Locus {locus} out of range")
        self.recalculate_stats()

    def get_allele(self, locus):
        allele = Character.Allele(locus)
        if allele == Character.Allele.HEIGHT:
            return self.height
        elif allele == Character.Allele.WEAPON:
            return self.gear.weapon
        elif allele == Character.Allele.ARMOUR:
            return self.gear.armour
        elif allele == Character.Allele.HELMET:
            return self.gear.helmet
        elif allele == Character.Allele.GLOVES:
            return self.gear.gloves
        elif allele == Character.Allele.BOOTS:
            return self.gear.boots
        else:
            raise Exception(f"Locus {locus} out of range")

    def __lt__(self, other):
        if not isinstance(other, Character):
            raise TypeError(f"< not supported between isntaces of 'Character' and '{type(other)}'")
        return self.fitness < other.fitness

    def __str__(self):
        return f"Name: {self.lastname}\tFitness: {self.fitness}"

    def __repr__(self):
        return "Role: " + str(self.role) + "\tHeight: " + str(self.height) + "\tLast Name: " + self.lastname + \
               "\tFu: " + str(self.strength) + "\tAg: " + str(self.agility) + \
               "\tEx: " + str(self.intelligence) + "\tRe: " + str(self.endurance) + "\tVi: " + str(self.vitality) + \
               "\tATK: " + str(self.attack) + "\tDEF: " + str(self.defense) + "\tFITNESS: " + str(self.fitness)

    def __eq__(self, other):
        if isinstance(other, Character):
            if self.fitness == other.fitness and abs(self.height - other.height) < 10**(-Config().precision) and self.gear == other.gear:
                return True
        return False

    def __hash__(self):
        return hash((self.fitness, self.height, self.gear))
