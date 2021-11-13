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
    log_epoch: int
    log: bool
    latent_layer: int
    layers: list[int]
    height: int
    width: int
    noise: float
    training_dataset: str
    learning_rate: float
    epochs: int
    batch_size: int

    def __init__(self):
        pass

    def setup_config(self, config_dict):
        self.learning_rate = get_parameter(config_dict, "learning_rate", False, 0.01)
        self.epochs = get_parameter(config_dict, "epochs", False, 5000)
        self.batch_size = get_parameter(config_dict, "batch_size")

        self.training_dataset = get_parameter(config_dict, "training_dataset")
        self.noise = get_parameter(config_dict, "noise", False, 0)

        self.width = get_parameter(config_dict, "width")
        self.height = get_parameter(config_dict, "height")

        self.layers = get_parameter(config_dict, "layers")
        self.latent_layer = get_parameter(config_dict, "latent_layer")

        self.log = get_parameter(config_dict, "log", False, False)
        self.log_epoch = get_parameter(config_dict, "log_epoch", False, 100)
