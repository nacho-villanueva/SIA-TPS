from enum import Enum
import random

import pandas as pd

from TP2.items.armour import Armour
from TP2.items.boots import Boots
from TP2.items.gloves import Gloves
from TP2.items.helmet import Helmet
from TP2.items.weapon import Weapon


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatasetLibrary(metaclass=Singleton):
    class DatasetType(Enum):
        ARMOUR = Armour
        WEAPON = Weapon
        GLOVES = Gloves
        BOOTS = Boots
        HELMET = Helmet

    def __init__(self):
        self.datasets = {}

    def load_dataset(self, dataset_type: DatasetType, dataset_path: str, separator='\t'):
        dataset_data = pd.read_csv(dataset_path, sep=separator)
        self.datasets[dataset_type] = pd.DataFrame(data=dataset_data)

    def get_random_item(self, dataset_type: DatasetType):
        dataset = self.datasets[dataset_type]
        index = random.randint(0, len(dataset) - 1)
        row = dataset.iloc[index]
        return dataset_type.value(row["Fu"], row["Ag"], row["Ex"], row["Re"], row["Vi"], int(row["id"]))

    def get_item(self, dataset_type, index: int):
        dataset = self.datasets[dataset_type]
        row = dataset.iloc[index]
        return dataset_type.value(row["Fu"], row["Ag"], row["Ex"], row["Re"], row["Vi"], int(row["id"]))
