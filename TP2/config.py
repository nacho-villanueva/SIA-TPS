

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
        self.role = config_dict["role"]
        self.crossover_algorithm = config_dict["crossover_algorithm"]
        self.mutation_algorithm = config_dict["mutation_algorithm"]
        self.implementation = config_dict["implementation"]
        self.stop_condition = config_dict["stop_condition"]
        self.real_time_graphics = config_dict["real_time_graphics"]
        self.precision = config_dict["precision"]
        self.population_size = config_dict["population_size"]
        self.K = config_dict["K"]
        self.A = config_dict["A"]
        self.selection_algorithm_1 = config_dict["selection_algorithm_1"]
        self.selection_algorithm_2 = config_dict["selection_algorithm_2"]
        self.B = config_dict["B"]
        self.replacement_algorithm_1 = config_dict["replacement_algorithm_1"]
        self.replacement_algorithm_2 = config_dict["replacement_algorithm_2"]
        self.deterministic_tournaments_M = config_dict["deterministic_tournaments_M"]
        self.probabilistic_tournaments_Threshold = config_dict["probabilistic_tournaments_Threshold"]
