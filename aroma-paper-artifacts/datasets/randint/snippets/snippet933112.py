from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def random_batch_(path, batch_size, shape):
    filenames = os.listdir(path)
    rand_samples = np.random.randint(0, filenames.__len__(), [batch_size])
    batch = np.zeros([batch_size, shape[0], shape[1], shape[2]])
    c = 0
    y = np.zeros([batch_size, 2])
    for idx in rand_samples:
        if (filenames[idx][:3] == 'cat'):
            y[(c, 0)] = 1
        else:
            y[(c, 1)] = 1
        try:
            batch[(c, :, :, :)] = misc.imresize(crop(np.array(Image.open((path + filenames[idx])))), [shape[0], shape[1]])
        except:
            img = crop(np.array(Image.open((path + filenames[0]))))
            batch[(c, :, :, :)] = misc.imresize(img, [shape[0], shape[1]])
        c += 1
    return (batch, y)
