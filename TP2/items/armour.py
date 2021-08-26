from TP2.items.item import Item


class Armour(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality):
        super().__init__("Armour", strength, agility, intelligence, endurance, vitality)
