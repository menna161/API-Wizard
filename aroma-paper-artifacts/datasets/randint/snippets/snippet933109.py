from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def random_batch_(path, batch_size, shape, c_nums):
    folder_names = os.listdir(path)
    rand_select = np.random.randint(0, folder_names.__len__())
    if (not (c_nums == folder_names.__len__())):
        print('Error: c_nums must match the number of the folders')
        return
    y = np.zeros([1, c_nums])
    y[(0, rand_select)] = 1
    path = ((path + folder_names[rand_select]) + '//')
    data = sio.loadmat((path + 'dataset.mat'))['data']
    rand_select = np.random.randint(0, np.size(data, 0), [batch_size])
    batch = data[rand_select]
    return (batch, y)
