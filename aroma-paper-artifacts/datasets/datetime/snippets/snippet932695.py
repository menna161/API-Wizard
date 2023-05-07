from __future__ import division
import math
import os
import datetime
import pprint
import scipy.misc
import numpy as np
import pretty_midi as pm
import copy
import config
import write_midi
import tensorflow as tf
from imageio import imread as _imread


def load_train_data(image_path, load_size=286, fine_size=256, is_testing=False):
    img_A = imread(image_path[0])
    img_B = imread(image_path[1])
    if (not is_testing):
        img_A = scipy.misc.imresize(img_A, [load_size, load_size])
        img_B = scipy.misc.imresize(img_B, [load_size, load_size])
        h1 = int(np.ceil(np.random.uniform(0.01, (load_size - fine_size))))
        w1 = int(np.ceil(np.random.uniform(0.01, (load_size - fine_size))))
        img_A = img_A[(h1:(h1 + fine_size), w1:(w1 + fine_size))]
        img_B = img_B[(h1:(h1 + fine_size), w1:(w1 + fine_size))]
        if (np.random.random() > 0.5):
            img_A = np.fliplr(img_A)
            img_B = np.fliplr(img_B)
    else:
        img_A = scipy.misc.imresize(img_A, [fine_size, fine_size])
        img_B = scipy.misc.imresize(img_B, [fine_size, fine_size])
    img_A = ((img_A / 127.5) - 1.0)
    img_B = ((img_B / 127.5) - 1.0)
    img_AB = np.concatenate((img_A, img_B), axis=2)
    return img_AB
