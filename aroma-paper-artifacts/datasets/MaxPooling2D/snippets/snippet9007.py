import tensorflow as tf
import numpy as np
import os
import pickle
import gzip
import urllib.request
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.contrib.keras.api.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.contrib.keras.api.keras.layers import Conv2D, MaxPooling2D
from tensorflow.contrib.keras.api.keras.models import load_model


def __init__(self, folder_path=None):
    data_path = os.path.join(folder_path, 'mnist_data')
    if (not os.path.exists(data_path)):
        os.mkdir(data_path)
        files = ['train-images-idx3-ubyte.gz', 't10k-images-idx3-ubyte.gz', 'train-labels-idx1-ubyte.gz', 't10k-labels-idx1-ubyte.gz']
        for name in files:
            urllib.request.urlretrieve(('http://yann.lecun.com/exdb/mnist/' + name), (f'{data_path}/' + name))
    train_data = extract_data(f'{data_path}/train-images-idx3-ubyte.gz', 60000)
    train_labels = extract_labels(f'{data_path}/train-labels-idx1-ubyte.gz', 60000)
    self.test_data = extract_data(f'{data_path}/t10k-images-idx3-ubyte.gz', 10000)
    self.test_labels = extract_labels(f'{data_path}/t10k-labels-idx1-ubyte.gz', 10000)
    VALIDATION_SIZE = 5000
    self.validation_data = train_data[(:VALIDATION_SIZE, :, :, :)]
    self.validation_labels = train_labels[:VALIDATION_SIZE]
    self.train_data = train_data[(VALIDATION_SIZE:, :, :, :)]
    self.train_labels = train_labels[VALIDATION_SIZE:]
