import os
import sys
import numpy as np
import h5py


def shuffle_points(batch_data):
    ' Shuffle orders of points in each point cloud -- changes FPS behavior.\n        Use the same shuffling idx for the entire batch.\n        Input:\n            BxNxC array\n        Output:\n            BxNxC array\n    '
    idx = np.arange(batch_data.shape[1])
    np.random.shuffle(idx)
    return batch_data[(:, idx, :)]
