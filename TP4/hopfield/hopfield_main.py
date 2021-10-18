import json
import sys
import os

import matplotlib.pyplot as plt
import numpy as np

from TP4.hopfield.hopfield_config import HopfieldConfig
from TP4.hopfield.hopfield_network import HopfieldNetwork


def print_symbol(X):
    out_str = ""
    for i, s in enumerate(X):
        if i % 5 == 0 and i != 0:
            out_str += "\n"
        out_str += "*" if s == 1 else " "
    print(out_str)


def load_symbols(file):
    f = open(file)
    lines = f.readlines()
    digits = np.empty((0, 5 * 5))
    d = []
    for line in lines:
        bits = line.replace("\n", "")
        if not bits:
            digits = np.vstack((digits, d))
            d = []
        else:
            for b in bits:
                d.append(-1 if b == "0" else 1)
    if d:
        digits = np.vstack((digits, d))
    return digits.astype(int)


def choose_symbols(symbols, chosen):
    return_symbols = np.empty((0, 5 * 5))
    for s in chosen:
        return_symbols = np.vstack((return_symbols, symbols[ord(s.upper()) - 65]))
    return return_symbols.astype(int)


def main():
    config_file = "./config/hopfield_config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print(f"Using default config file {config_file}")

    config_file = open(config_file)
    config_dict = json.load(config_file)
    config_file.close()

    config = HopfieldConfig()
    config.setup_config(config_dict)

    symbols = load_symbols(config.letters_bitmap)
    loaded_symbols = choose_symbols(symbols, config.load_symbols)

    hn = HopfieldNetwork()

    hn.train(loaded_symbols)

    test_symbols = symbols[ord(config.test_symbol.upper()) - 65]
    test_symbol = np.vectorize(lambda v: -v if np.random.choice(a=[False, True], p=[1 - config.noise, config.noise]) else v)(test_symbols)

    S, energy = hn.predict(test_symbol)

    print_symbol(test_symbol)
    print("---------")
    print_symbol(S)

    plt.plot(range(0, len(energy)), energy)
    plt.show()


if __name__ == "__main__":
    main()
