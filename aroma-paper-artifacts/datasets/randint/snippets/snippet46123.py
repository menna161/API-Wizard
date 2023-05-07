import numpy as np
import random
import copy
import os


def find_indices_srnn(data_set, action):
    seed = 1234567890
    rng = np.random.RandomState(seed)
    subject = 5
    T1 = data_set[(subject, action, 1, 'even')].shape[0]
    T2 = data_set[(subject, action, 2, 'even')].shape[0]
    (prefix, suffix) = (50, 100)
    idx = []
    idx.append(rng.randint(16, ((T1 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T2 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T1 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T2 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T1 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T2 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T1 - prefix) - suffix)))
    idx.append(rng.randint(16, ((T2 - prefix) - suffix)))
    return idx
