from TP2.items.item import Item


class Armour(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality, item_id):
        super().__init__("Armour", strength, agility, intelligence, endurance, vitality, item_id)

    def __eq__(self, other):
        if isinstance(other, Armour) and self.item_id == other.item_id:
            return True
        return False

    def __hash__(self):
        return super().__hash__()
