import numpy as np


def find_matching(confusion_matrix):
    '\n    returns the perfect matching\n    '
    (_, n) = confusion_matrix.shape
    path = []
    for i in range(n):
        max_val = (- 10000000000.0)
        max_ind = (- 1)
        for j in range(n):
            if (j in path):
                pass
            else:
                temp = confusion_matrix[(i, j)]
                if (temp > max_val):
                    max_val = temp
                    max_ind = j
        path.append(max_ind)
    return path
