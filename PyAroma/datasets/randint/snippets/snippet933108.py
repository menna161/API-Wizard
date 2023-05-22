from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def read_face(data, batch_size):
    rand_select = np.random.randint(0, 13233, [batch_size])
    batch = data[rand_select]
    return (batch, 0)
