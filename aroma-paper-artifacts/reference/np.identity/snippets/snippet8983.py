import tensorflow as tf
import numpy as np
import os
import pickle
import gzip
import pickle
import urllib.request
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.contrib.keras.api.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.contrib.keras.api.keras.layers import Conv2D, MaxPooling2D
from tensorflow.contrib.keras.api.keras.models import load_model


def load_batch(fpath):
    f = open(fpath, 'rb').read()
    size = (((32 * 32) * 3) + 1)
    labels = []
    images = []
    for i in range(10000):
        arr = np.fromstring(f[(i * size):((i + 1) * size)], dtype=np.uint8)
        lab = np.identity(10)[arr[0]]
        img = arr[1:].reshape((3, 32, 32)).transpose((1, 2, 0))
        labels.append(lab)
        images.append(((img / 255) - 0.5))
    return (np.array(images), np.array(labels))
