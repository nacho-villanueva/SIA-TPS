class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_parameter(config_dict: dict, name, required=True, default=None):
    if name not in config_dict:
        if not required:
            return default
        else:
            raise Exception(f"Missing Configuration Parameter: {name}")
    return config_dict[name]


class Config(metaclass=Singleton):
    def __init__(self):
        pass

    def setup_config(self, config_dict):
        self.algorithm = get_parameter(config_dict, "algorithm")
        self.activation = get_parameter(config_dict, "activation")

        self.learning_rate = get_parameter(config_dict, "learning_rate", False, 0.5)
        self.w0 = get_parameter(config_dict, "w0", False, 0)

        self.training_set_path = get_parameter(config_dict, "training_set_path")
        self.save_perceptron = get_parameter(config_dict, "save_perceptron", False, False)
        self.save_perceptron_path = get_parameter(config_dict, "save_perceptron_path", self.save_perceptron)
