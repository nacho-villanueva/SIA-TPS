import numpy as np
from TP3.simple_perceptron import PerceptronSimple
from TP3.config import Config
import matplotlib.pyplot as plt
import pandas as pd
import sys
import json

def get_perceptron_hiperplane(perceptron: PerceptronSimple):
    def hiperplane(x):
        return (perceptron.w[0]*x - perceptron.w0) / (-perceptron.w[1])
    return hiperplane

def get_color(y):
    return y.map({1: "red", -1: "black"})


def draw_2d_simple_perceptron(perceptron: PerceptronSimple, dataframe: pd.DataFrame):
    plt.scatter(dataframe["x1"], dataframe["x2"],
                color=get_color(dataframe["y"]))
    hiperplane = get_perceptron_hiperplane(perceptron)
    x = np.linspace(-2,2)
    y = hiperplane(x)
    plt.plot(x,y)
    plt.show()

def main():
    config_file = "./config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.json)")

    file = open(config_file)
    config_dict = json.load(file)
    file.close()

    config = Config()
    config.setup_config(config_dict)
    
    training_set = pd.read_csv(config.training_set_path, sep=";")
    perceptron = config.algorithm(pd.DataFrame([]),pd.DataFrame([]),upper_bound=0)

    save_perceptron_file = open(config.save_perceptron_path)
    perceptron_data = json.load(save_perceptron_file)
    save_perceptron_file.close()
    perceptron.w = perceptron_data["w"]

    draw_2d_simple_perceptron(perceptron,training_set)
    
    
if __name__ == "__main__":
    main()