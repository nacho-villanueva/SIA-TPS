from TP3.perceptronSimple import PerceptronSimple

def get_algorithm(algorithm):
    if algorithm == "perceptron_simple_escalon":
        perceptron = PerceptronSimple()
        def escalon(h,w0):
            if h > w0:
                return 1
            else:
                return -1
        perceptron.act_fun = escalon
        return perceptron.run
    if algorithm == "perceptron_simple_lineal":
        perceptron = PerceptronSimple()
        perceptron.act_fun = lambda h,w0: h
        return perceptron.run