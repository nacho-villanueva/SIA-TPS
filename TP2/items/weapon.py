from TP2.items.item import Item


class Weapon(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality):
        super().__init__("Weapon", strength, agility, intelligence, endurance, vitality)
