import scipy.io as sio
import numpy as np


def get_batch_face(data, labels, batchsize):
    labels = labels[(0, :)]
    nums = int(data.shape[0])
    rand_select = np.random.randint(0, nums, [batchsize])
    batch = data[rand_select]
    labels = labels[rand_select]
    z = np.random.normal(0, 1, [batchsize, 100])
    return (batch, labels, z)
