import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from TP4.kohonen.kohonen_main import standarize_data

data = pd.read_csv("./data/europe.csv", sep=",")
data = standarize_data(data)


data = data.iloc[:, 1:]
data = data.to_numpy()
data = data.transpose()

covMatrix = np.cov(data, bias=True)                 # Hacer la covarianza de los datos estandarizados, es lo mismo que hacer directamente la correlacion
auto_vals, auto_vecs = np.linalg.eig(covMatrix)

pares_vals_vecs = [(np.abs(auto_vals[i]), auto_vecs[:, i]) for i in range(len(auto_vals))]

# Ordenamos estas parejas den orden descendiente con la función sort
pares_vals_vecs.sort(key=lambda x: x[0], reverse=True)
# A partir de los autovalores, calculamos la varianza explicada
tot = sum(auto_vals)
var_exp = [(i / tot) * 100 for i in sorted(auto_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)


print(f"First Vector: {pares_vals_vecs[0][1]}")
# Representamos en un diagrama de barras la varianza explicada por cada autovalor, y la acumulada
with plt.style.context('seaborn-pastel'):
    plt.figure(figsize=(6, 4))
    plt.bar(range(7), var_exp, alpha=0.5, align='center',
            label='Varianza individual explicada', color='g')
    plt.step(range(7), cum_var_exp, where='mid', linestyle='--', label='Varianza explicada acumulada')
    plt.ylabel('Ratio de Varianza Explicada')
    plt.xlabel('Componentes Principales')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()


Y = np.dot([sorted_pair[1] for sorted_pair in pares_vals_vecs], data)
print(Y)

