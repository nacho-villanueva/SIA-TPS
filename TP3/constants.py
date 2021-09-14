from TP3.simple_perceptron import PerceptronSimple


def get_algorithm(algorithm):
    if algorithm == "simple_stair_perceptron":
        perceptron = PerceptronSimple()

        def stair(h, w0):
            if h > w0:
                return 1
            else:
                return -1

        perceptron.act_fun = stair
        return perceptron.run
    if algorithm == "simple_lineal_perceptron":
        perceptron = PerceptronSimple()
        perceptron.act_fun = lambda h, w0: h
        return perceptron.run
