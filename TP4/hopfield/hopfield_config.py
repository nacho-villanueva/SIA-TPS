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


class HopfieldConfig(metaclass=Singleton):
    def __init__(self):
        pass

    def setup_config(self, config_dict):
        self.load_symbols = get_parameter(config_dict, "load_symbols", True)
        self.test_symbol = get_parameter(config_dict, "test_symbol", True)
        self.noise = get_parameter(config_dict, "noise", False, 0.2)
        self.letters_bitmap = get_parameter(config_dict, "letters_bitmap", True)
