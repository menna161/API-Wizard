import os
import pickle
import numpy as np


def hot_one_vector(y, max):
    import numpy as np
    labels_hot_vector = np.zeros((y.shape[0], max), dtype=np.int32)
    labels_hot_vector[(np.arange(y.shape[0]), y)] = 1
    return labels_hot_vector
