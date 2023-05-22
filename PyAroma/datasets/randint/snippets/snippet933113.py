from PIL import Image
import numpy as np
import scipy.misc as misc
import scipy.io as sio
import os
import pickle


def crop(img):
    h = img.shape[0]
    w = img.shape[1]
    if (h < w):
        x = 0
        y = np.random.randint(0, ((w - h) + 1))
        length = h
    elif (h > w):
        x = np.random.randint(0, ((h - w) + 1))
        y = 0
        length = w
    else:
        x = 0
        y = 0
        length = h
    return img[(x:(x + length), y:(y + length), :)]
