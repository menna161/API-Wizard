import os
import sys
import numpy as np
import h5py


def shuffle_data(data, labels):
    ' Shuffle data and labels.\n        Input:\n          data: B,N,... numpy array\n          label: B,... numpy array\n        Return:\n          shuffled data, label and shuffle indices\n    '
    idx = np.arange(len(labels))
    np.random.shuffle(idx)
    return (data[(idx, ...)], labels[idx], idx)
