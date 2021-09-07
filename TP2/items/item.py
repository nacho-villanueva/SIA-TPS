
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
        return f"Item: {self.item_id}"

    def __eq__(self, other):
        if isinstance(other, Item) and self.item_id == other.item_id:
            return True
        return False

    def __hash__(self):
        return hash(self.item_id)
