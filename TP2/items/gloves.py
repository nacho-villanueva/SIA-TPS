from TP2.items.item import Item


class Gloves(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality):
        super().__init__("Gloves", strength, agility, intelligence, endurance, vitality)
