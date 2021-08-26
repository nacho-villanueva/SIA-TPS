from TP2.items.item import Item


class Helmet(Item):
    def __init__(self, strength, agility, intelligence, endurance, vitality):
        super().__init__("Helmet", strength, agility, intelligence, endurance, vitality)
