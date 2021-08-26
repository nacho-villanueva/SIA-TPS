import math
from enum import Enum


class CharacterRole(Enum):
    WARRIOR = (0.6, 0.6)    # Guerrero
    ARCHER = (0.9, 0.1)     # Arquero
    TANK = (0.6, 0.6)       # Defensor
    ASSASSIN = (0.6, 0.6)   # Infiltrado

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


class Character:

    def __init__(self, role: CharacterRole, height: float, gear: list, lastname: str):
        self.role = role
        self.height = height
        self.gear = gear
        self.lastname = lastname

        self.strength = self.calculate_strength()           # Fuerza
        self.endurance = self.calculate_endurance()         # Resistencia
        self.agility = self.calculate_agility()             # Agilidad
        self.vitality = self.calculate_vitality()           # Vida
        self.intelligence = self.calculate_intelligence()   # Pericia

        self.attack = self.calculate_attack()
        self.defense = self.calculate_defense()

        self.fitness = self.calculate_fitness()

    def __str__(self):
        # TODO: no imprimí el Gear porque sino es enorme el output
        return "Role: " + str(self.role) + ", Height: " + str(self.height) + ", Last Name: " + self.lastname + \
                ", Fu: " + str(self.strength) + ", Ag: " + str(self.agility) + \
                ", Ex: " + str(self.intelligence) + ", Re: " + str(self.endurance) + ", Vi: " + str(self.vitality) + \
                ", ATK: " + str(self.attack) + ", DEF: " + str(self.defense) + ", FITNESS: " + str(self.fitness)

    def __repr__(self):
        # TODO: no imprimí el Gear porque sino es enorme el output
        return "Role: " + str(self.role) + ", Height: " + str(self.height) + ", Last Name: " + self.lastname + \
               ", Fu: " + str(self.strength) + ", Ag: " + str(self.agility) + \
               ", Ex: " + str(self.intelligence) + ", Re: " + str(self.endurance) + ", Vi: " + str(self.vitality) + \
               ", ATK: " + str(self.attack) + ", DEF: " + str(self.defense) + "FITNESS: " + str(self.fitness)

    def calculate_chromosome(self):  # TODO: IMPLEMENTAR
        pass

    def calculate_fitness(self):
        return self.role.attack_coefficient * self.attack + self.role.defense_coefficient * self.defense

    def calculate_attack(self):
        attack_modifier = 0.7 - (3 * self.height - 5) ** 4 + (3 * self.height - 5) ** 2 + (self.height / 4.0)
        return (self.agility + self.intelligence) * self.strength * attack_modifier

    def calculate_defense(self):
        defense_modifier = 1.9 + (2.5 * self.height - 4.16) ** 4 - (2.5 * self.height - 4.16) ** 2 - (3 * self.height / 10.0)
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
