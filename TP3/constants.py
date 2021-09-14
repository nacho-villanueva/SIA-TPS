from TP3.simple_perceptron import PerceptronSimple


def get_algorithm(config_dict):
    algorithm = config_dict["algorithm"]
    w0 = config_dict["w0"] if "w0" in config_dict else 0
    learning_rate = config_dict["learning_rate"] if "learning_rate" in config_dict else 0.5
    if algorithm == "simple_stair_perceptron":
        perceptron = PerceptronSimple(learning_rate=learning_rate,w0=w0)

        def stair(h, w0):
            if h > w0:
                return 1
            else:
                return -1

        perceptron.act_fun = stair
        return perceptron.run
    if algorithm == "simple_lineal_perceptron":
        perceptron = PerceptronSimple(learning_rate=learning_rate,w0=w0)
        perceptron.act_fun = lambda h, w0: h
        return perceptron.run
