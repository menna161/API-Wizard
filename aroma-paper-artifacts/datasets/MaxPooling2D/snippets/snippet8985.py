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


def __init__(self, folder_path=None):
    train_data = []
    train_labels = []
    if (not os.path.exists(f'{folder_path}cifar-10-batches-bin')):
        urllib.request.urlretrieve('https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz', 'cifar-data.tar.gz')
        os.popen(f'tar -xzf cifar-data.tar.gz').read()
    for i in range(5):
        (r, s) = load_batch(((f'{folder_path}cifar-10-batches-bin/data_batch_' + str((i + 1))) + '.bin'))
        train_data.extend(r)
        train_labels.extend(s)
    train_data = np.array(train_data, dtype=np.float32)
    train_labels = np.array(train_labels)
    (self.test_data, self.test_labels) = load_batch(f'{folder_path}cifar-10-batches-bin/test_batch.bin')
    VALIDATION_SIZE = 5000
    self.validation_data = train_data[(:VALIDATION_SIZE, :, :, :)]
    self.validation_labels = train_labels[:VALIDATION_SIZE]
    self.train_data = train_data[(VALIDATION_SIZE:, :, :, :)]
    self.train_labels = train_labels[VALIDATION_SIZE:]
