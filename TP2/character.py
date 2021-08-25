from enum import Enum


class CharacterRole(Enum):
    WARRIOR = (0.6, 0.6)    # Guerrero
    ARCHER = (0.9, 0.1)     # Arquero
    TANK = (0.6, 0.6)       # Defensor
    ASSASSIN = (0.6, 0.6)   # Infiltrado

    def __init__(self, attack_coefficient, defense_coefficient):
        self.attack_coefficient = attack_coefficient
        self.defense_coefficient = defense_coefficient


class Character:

    def __init__(self, role: CharacterRole, height: float, gear: list, lastname: str):
        self.role = role
        self.height = height
        self.gear = gear
        self.lastname = lastname

        self.strength = 0       # Fuerza # TODO: IMPLEMENTAR CALCULATE_STRENGTH()
        self.endurance = 0      # Resistencia # TODO: IMPLEMENTAR CALCULATE_ENDURANCE()
        self.agility = 0        # Agilidad # TODO: IMPLEMENTAR CALCULATE_AGILITY()
        self.vitality = 0       # Vida # TODO: IMPLEMENTAR CALCULATE_VITALITY()
        self.intelligence = 0   # Pericia # TODO: IMPLEMENTAR CALCULATE_INTELLIGENCE()

        self.attack = self.calculate_attack()
        self.defense = self.calculate_defense()

        self.fitness = self.calculate_fitness()

    def calculate_chromosome(self):  # TODO: IMPLEMENTAR
        pass

    def calculate_fitness(self):
        return self.role.attack_coefficient * self.attack + self.role.defense_coefficient * self.defense

    def calculate_attack(self):
        return 0.7 - (3 * self.height - 5) ** 4 + (3 * self.height - 5) ** 2 + (self.height / 4.0)

    def calculate_defense(self):
        return 1.9 + (2.5 * self.height - 4.16) ** 4 - (2.5 * self.height - 4.16) ** 2 - (3 * self.height / 10.0)
