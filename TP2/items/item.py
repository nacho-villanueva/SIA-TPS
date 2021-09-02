
class Item:
    def __init__(self, item_type: str, strength, agility, intelligence, endurance, vitality, item_id):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.endurance = endurance
        self.vitality = vitality
        self.item_type = item_type
        self.item_id = item_id

    def __str__(self):
        return "[" + self.item_type + ", Fu=" + str(self.strength) + ", Ag=" + str(self.agility) + \
            ", Ex=" + str(self.intelligence) + ", Re=" + str(self.endurance) + ", Vi=" + str(self.vitality) + "]"

    def __repr__(self):
        return "[" + self.item_type + ", Fu=" + str(self.strength) + ", Ag=" + str(self.agility) + \
               ", Ex=" + str(self.intelligence) + ", Re=" + str(self.endurance) + ", Vi=" + str(self.vitality) + "]"

    def __eq__(self, other):
        if isinstance(other, Item) and self.item_id == other.item_id:
            return True
        return False

    def __hash__(self):
        return hash(self.item_id)
