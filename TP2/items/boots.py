from TP2.items.item import Item


class Boots(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality, item_id):
        super().__init__("Boots", strength, agility, intelligence, endurance, vitality, item_id)

    def __eq__(self, other):
        if isinstance(other, Boots) and self.item_id == other.item_id:
            return True
        return False

    def __hash__(self):
        return super().__hash__()
