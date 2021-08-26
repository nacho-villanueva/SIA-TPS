from TP2.items.item import Item


class Boots(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality):
        super().__init__("Boots", strength, agility, intelligence, endurance, vitality)
