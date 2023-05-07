import sys
import numpy as np
from keras import Sequential
from keras.layers import LSTM as KERAS_LSTM, Dense, Dropout, Conv2D, Flatten, BatchNormalization, Activation, MaxPooling2D
from . import Model


def make_default_model(self):
    '\n        Makes a CNN keras model with the default hyper parameters.\n        '
    self.model.add(Conv2D(8, (13, 13), input_shape=(self.input_shape[0], self.input_shape[1], 1)))
    self.model.add(BatchNormalization(axis=(- 1)))
    self.model.add(Activation('relu'))
    self.model.add(Conv2D(8, (13, 13)))
    self.model.add(BatchNormalization(axis=(- 1)))
    self.model.add(Activation('relu'))
    self.model.add(MaxPooling2D(pool_size=(2, 1)))
    self.model.add(Conv2D(8, (13, 13)))
    self.model.add(BatchNormalization(axis=(- 1)))
    self.model.add(Activation('relu'))
    self.model.add(Conv2D(8, (2, 2)))
    self.model.add(BatchNormalization(axis=(- 1)))
    self.model.add(Activation('relu'))
    self.model.add(MaxPooling2D(pool_size=(2, 1)))
    self.model.add(Flatten())
    self.model.add(Dense(64))
    self.model.add(BatchNormalization())
    self.model.add(Activation('relu'))
    self.model.add(Dropout(0.2))
