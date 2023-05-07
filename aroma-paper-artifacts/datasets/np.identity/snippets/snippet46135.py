import numpy as np
import random
import copy
import os


def encode_onehot(labels):
    classes = set(labels)
    classes_dict = {c: np.identity(len(classes))[(i, :)] for (i, c) in enumerate(classes)}
    labels_onehot = np.array(list(map(classes_dict.get, labels)), dtype=np.int32)
    return labels_onehot
