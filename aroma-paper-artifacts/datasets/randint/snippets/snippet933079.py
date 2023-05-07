import scipy.io as sio
import numpy as np


def get_batch(data, batchsize):
    data_nums = data.shape[0]
    rand_select = np.random.randint(0, data_nums, [batchsize])
    batch = data[rand_select]
    z = np.random.normal(0, 1, [batchsize, 512])
    return (batch, z)
