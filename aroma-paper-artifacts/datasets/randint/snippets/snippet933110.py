from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def random_batch(path, batch_size, shape, c_nums):
    folder_names = os.listdir(path)
    rand_select = np.random.randint(0, folder_names.__len__())
    if (not (c_nums == folder_names.__len__())):
        print('Error: c_nums must match the number of the folders')
        return
    y = np.zeros([1, 1])
    y[(0, 0)] = rand_select
    path = ((path + folder_names[rand_select]) + '//')
    file_names = os.listdir(path)
    rand_select = np.random.randint(0, file_names.__len__(), [batch_size])
    batch = np.zeros([batch_size, shape[0], shape[1], shape[2]])
    for i in range(batch_size):
        img = np.array(Image.open((path + file_names[rand_select[i]])).resize([shape[0], shape[1]]))[(:, :, :3)]
        if (img.shape.__len__() == 2):
            img = np.dstack((img, img, img))
        batch[(i, :, :, :)] = img
    return (batch, y)
