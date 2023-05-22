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


def __init__(self, restore=None, session=None, use_softmax=False):
    self.num_channels = 3
    self.image_size = 32
    self.num_labels = 10
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=(32, 32, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(10))
    if use_softmax:
        model.add(Activation('softmax'))
    if restore:
        model.load_weights(restore)
    self.model = model
