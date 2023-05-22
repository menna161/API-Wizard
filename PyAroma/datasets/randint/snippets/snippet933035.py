import scipy.io as sio
import numpy as np


def get_batch(data, labels, batchsize):
    rand_select = np.random.randint(0, 50000, [batchsize])
    batch = data[rand_select]
    labels = labels[(rand_select, 0)]
    z = np.random.normal(0, 1, [batchsize, 100])
    return (batch, labels, z)
