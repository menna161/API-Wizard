from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def read_cifar(data, labels, batch_size):
    rand_select = np.random.randint(0, 50000, [batch_size])
    batch = data[rand_select]
    batch_labels = labels[rand_select]
    return (batch, batch_labels)
