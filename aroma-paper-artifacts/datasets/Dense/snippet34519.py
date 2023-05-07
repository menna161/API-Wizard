import sys
import numpy as np
from keras import Sequential
from keras.layers import LSTM as KERAS_LSTM, Dense, Dropout, Conv2D, Flatten, BatchNormalization, Activation, MaxPooling2D
from . import Model


def make_default_model(self):
    '\n        Makes the LSTM model with keras with the default hyper parameters.\n        '
    self.model.add(KERAS_LSTM(128, input_shape=(self.input_shape[0], self.input_shape[1])))
    self.model.add(Dropout(0.5))
    self.model.add(Dense(32, activation='relu'))
    self.model.add(Dense(16, activation='tanh'))
