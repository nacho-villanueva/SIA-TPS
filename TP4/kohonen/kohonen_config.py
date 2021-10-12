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


class KohonenConfig(metaclass=Singleton):
    def __init__(self):
        pass

    def setup_config(self, config_dict):
        self.k = get_parameter(config_dict, "k")
        self.R = get_parameter(config_dict, "R", False, 1)
        self.R_updates = get_parameter(config_dict, "R_updates", False, False)
        self.learning_rate = get_parameter(config_dict, "learning_rate", False, 0.5)
        self.data_path = get_parameter(config_dict, "data_path")
