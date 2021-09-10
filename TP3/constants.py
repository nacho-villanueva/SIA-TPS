from TP3.perceptronSimpleEscalon import PerceptronSimpleEscalon

def get_algorithm(algorithm):
    if algorithm == "perceptron_simple":
        return PerceptronSimpleEscalon.run