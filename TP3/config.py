import os
from TP3.constants import get_algorithm


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self):
        pass

    def setup_config(self, config_dict):
       self.algorithm = get_algorithm(config_dict["algorithm"])
       self.training_set_path = config_dict["training_set_path"] if "training_set_path" in config_dict else os.path.join("data","conjuntoDeEntrenamiento.txt")