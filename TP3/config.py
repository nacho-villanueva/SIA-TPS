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
        perceptron = get_parameter(config_dict, "perceptron")
        self.algorithm = get_parameter(perceptron, "algorithm")
        self.activation = get_parameter(perceptron, "activation", False)

        self.learning_rate = get_parameter(config_dict, "learning_rate", False, 0.5)
        self.w0 = get_parameter(config_dict, "w0", False, 0)
        self.epochs = get_parameter(config_dict, "epochs")

        self.training_set_path = get_parameter(config_dict, "training_set_path")
        self.output_data_path = get_parameter(config_dict, "output_data_path", False)

        self.k = get_parameter(config_dict, "k", False)
        self.problem_to_solve = get_parameter(config_dict, "problem_to_solve", False)

        self.save_perceptron = get_parameter(config_dict, "save_perceptron", False, False)
        self.save_perceptron_path = get_parameter(config_dict, "save_perceptron_path", self.save_perceptron)

        self.height = get_parameter(config_dict, "picture_height", False, 7)
        self.width = get_parameter(config_dict, "picture_width", False, 5)
        self.image_noise = get_parameter(config_dict, "image_noise", False, 0)

        self.layers = get_parameter(config_dict, "layers", False, None)
        self.softmax = get_parameter(config_dict, "softmax", False, False)
        self.batch_size = get_parameter(config_dict, "batch_size", False)

        self.logging = get_parameter(config_dict, "logging_activated")
        self.logging_epoch = get_parameter(config_dict, "logging_every_N_epochs", False)

