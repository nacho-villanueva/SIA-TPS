
class Item:
    def __init__(self, item_type: str, strength, agility, intelligence, endurance, vitality):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.endurance = endurance
        self.vitality = vitality
        self.item_type = item_type

    def __str__(self):
        return "[" + self.item_type + ", Fu=" + str(self.strength) + ", Ag=" + str(self.agility) + \
            ", Ex=" + str(self.intelligence) + ", Re=" + str(self.endurance) + ", Vi=" + str(self.vitality) + "]"

    def __repr__(self):
        return "[" + self.item_type + ", Fu=" + str(self.strength) + ", Ag=" + str(self.agility) + \
               ", Ex=" + str(self.intelligence) + ", Re=" + str(self.endurance) + ", Vi=" + str(self.vitality) + "]"
