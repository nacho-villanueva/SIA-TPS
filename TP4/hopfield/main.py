import numpy as np

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


symbols = load_symbols("letters.txt")
symbols = choose_symbols(symbols, ["A", "J", "C"])

hn = HopfieldNetwork()

hn.train(symbols)

# test_digit = digits[2]
# test_digit = np.random.choice([-1, 1], 25)
test_digit = np.vectorize(lambda v: -v if np.random.choice(a=[False, True], p=[1 - 0.2, 0.2]) else v)(symbols[1])

S = hn.predict(test_digit)

print_symbol(test_digit)
print("---------")
print_symbol(S)
