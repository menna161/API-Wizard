from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def random_face_batch(path, batch_size):
    filenames_young = os.listdir((path + '0//'))
    filenames_cats = os.listdir((path + '1//'))
    rand_gender = np.random.randint(0, 2)
    batch = np.zeros([batch_size, 64, 64, 3])
    Y = np.zeros([1, 2])
    if (rand_gender == 0):
        rand_samples = np.random.randint(0, filenames_young.__len__(), [batch_size])
        c = 0
        for i in rand_samples:
            img = np.array(Image.open(((path + '0//') + filenames_young[i])))
            center_h = (img.shape[0] // 2)
            center_w = (img.shape[1] // 2)
            batch[(c, :, :, :)] = misc.imresize(img, [64, 64])
            c += 1
        Y[(0, 0)] = 1
    else:
        rand_samples = np.random.randint(0, filenames_cats.__len__(), [batch_size])
        c = 0
        for i in rand_samples:
            img = np.array(Image.open(((path + '1//') + filenames_cats[i])))
            batch[(c, :, :, :)] = misc.imresize(img, [64, 64])
            c += 1
        Y[(0, 1)] = 1
    return (batch, Y)
