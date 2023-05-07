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


def load_batch(fpath, label_key='labels'):
    f = open(fpath, 'rb')
    d = pickle.load(f, encoding='bytes')
    for (k, v) in d.items():
        del d[k]
        d[k.decode('utf8')] = v
    f.close()
    data = d['data']
    labels = d[label_key]
    data = data.reshape(data.shape[0], 3, 32, 32)
    final = np.zeros((data.shape[0], 32, 32, 3), dtype=np.float32)
    final[(:, :, :, 0)] = data[(:, 0, :, :)]
    final[(:, :, :, 1)] = data[(:, 1, :, :)]
    final[(:, :, :, 2)] = data[(:, 2, :, :)]
    final /= 255
    final -= 0.5
    labels2 = np.zeros((len(labels), 10))
    labels2[(np.arange(len(labels2)), labels)] = 1
    return (final, labels)
