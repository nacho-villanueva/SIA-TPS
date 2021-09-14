import os
from TP3.constants import get_algorithm


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self):
        self.algorithm = None
        self.training_set_path = None
        pass

    def setup_config(self, config_dict):
        self.algorithm = get_algorithm(config_dict)
        self.training_set_path = config_dict[
            "training_set_path"] if "training_set_path" in config_dict else os.path.join("data",
                                                                                         "conjuntoDeEntrenamiento.txt")
        self.save_perceptron = config_dict["save_perceptron"] if "save_perceptron" in config_dict else False
        self.save_perceptron_path = config_dict["save_perceptron_path"] if "save_perceptron_path" in config_dict else os.path.join(
            "results","perceptron.txt")
