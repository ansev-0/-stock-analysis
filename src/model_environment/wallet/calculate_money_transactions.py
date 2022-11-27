import numpy as np

def calculate_money_operations(dict_operations):
    array_operations = np.array(list(dict_operations.values()))
    return np.multiply(array_operations[:, 0], array_operations[:, 1]).sum()
