

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
        self.crossover_algorithm = config_dict["crossover"]
        self.mutation_algorithm = config_dict["mutation"]
        self.implementation = config_dict["implementation"]
        self.stop_condition = config_dict["stop_condition"]
        self.real_time_graphics = config_dict["real_time_graphics"]
        self.save_graph_data =  config_dict["save_graph_data"] if "save_graph_data" in config_dict else False
        self.graph_data_directory =  config_dict["graph_data_directory"] if "graph_data_directory" in config_dict else "results"
        self.run_instances = config_dict["run_instances"] if "run_instances" in config_dict else 1
        self.precision = config_dict["float_precision"]
        self.population_size = config_dict["population_size"]
        self.K = config_dict["K"]
        self.A = config_dict["A"]
        self.selection_1 = config_dict["selection_1"]
        self.selection_2 = config_dict["selection_2"]
        self.B = config_dict["B"]
        self.replacement_1 = config_dict["replacement_1"]
        self.replacement_2 = config_dict["replacement_2"]
        self.mutation_probability = config_dict["mutation_probability"]

        self.min_height = 1.3
        self.max_height = 2.0
