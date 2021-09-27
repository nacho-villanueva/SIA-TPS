import numpy as np
from matplotlib import pyplot as plt

PARAMETER = 10100

error_to_graph = []
error_file = open(f"./results/error_{PARAMETER}.csv")
all_errors = []
line = error_file.readline()
while line:
    execution_errors = line.replace("\n", "").split(";")[0:-1]
    execution_errors = [float(elem) for elem in execution_errors]
    all_errors.append(execution_errors)
    line = error_file.readline()
error_file.close()

if len(all_errors) == 1:  # En caso de que el archivo solo tenga 1 linea
    error_to_graph = all_errors[0]
else:
    error_to_graph = np.mean(all_errors, axis=0)

error_difference = [error_to_graph[i+1] - error_to_graph[i] for i in range(len(error_to_graph) - 1)]

x = [i for i in range(1, len(error_to_graph) + 1)]

# Solo graficamos cada N datos
N = 101
x = x[0::N]
# error_to_graph = error_to_graph[0::N]
error_difference = error_difference[0::N]

# plt.plot(x, error_to_graph)
plt.plot(x, error_difference)
plt.ylabel("Error")
plt.xlabel("Epochs")
plt.show()
