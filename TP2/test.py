import random
import numpy as np
from time import time

amount = 10000000

test_random = []

start_time = time()
for i in range(amount):
    test_random.append(random.random())
random_array_time = time() - start_time

start_time = time()
random.shuffle(test_random)
random_time = time() - start_time

test_numpy = []

start_time = time()
for i in range(amount):
    test_numpy.append(np.random.random())
numpy_array_time = time() - start_time


start_time = time()
np.random.shuffle(test_numpy)
numpy_time = time() - start_time

print(f"Numpy: {numpy_array_time} - {numpy_time}")
print(f"Random: {random_array_time} - {random_time}")
