import matplotlib.pyplot as plt
import numpy as np

PARAMETER = 50000

# Esto será lo que se graficará:
test_accuracy_to_graph = []
train_accuracy_to_graph = []

# Obtenemos todos los datos de TRAIN
train_file = open(f"./results/accuracy_train_{PARAMETER}.csv")
all_train_accuracies = []
line = train_file.readline()
while line:
    execution_accuracies = line.replace("\n", "").split(";")
    execution_accuracies = [float(elem) for elem in execution_accuracies]
    all_train_accuracies.append(execution_accuracies)
    line = train_file.readline()
train_file.close()

if len(all_train_accuracies) == 1:  # En caso de que el archivo solo tenga 1 linea
    train_accuracy_to_graph = all_train_accuracies[0]
else:
    train_accuracy_to_graph = np.mean(all_train_accuracies, axis=0)

# Obtenemos todos los datos de TEST
test_file = open(F"./results/accuracy_test_{PARAMETER}.csv")
all_test_accuracies = []
line = test_file.readline()
while line:
    execution_accuracies = line.replace("\n", "").split(";")
    execution_accuracies = [float(elem) for elem in execution_accuracies]
    all_test_accuracies.append(execution_accuracies)
    line = test_file.readline()
test_file.close()

if len(all_test_accuracies) == 1:  # En caso de que el archivo solo tenga 1 linea
    test_accuracy_to_graph = all_test_accuracies[0]
else:
    test_accuracy_to_graph = np.mean(all_test_accuracies, axis=0)

# Graficamos
x = [i for i in range(1, len(test_accuracy_to_graph) + 1)]
# Solo graficamos cada N datos
N = 101
x = x[0::N]
test_accuracy_to_graph = test_accuracy_to_graph[0::N]
train_accuracy_to_graph = train_accuracy_to_graph[0::N]

plt.plot(x, test_accuracy_to_graph, color='r', label='TEST')
plt.plot(x, train_accuracy_to_graph, color='b', label='TRAIN')
plt.ylim([0, 1])
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()
