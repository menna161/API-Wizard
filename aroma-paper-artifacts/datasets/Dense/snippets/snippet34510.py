import sys
import numpy as np
from keras import Sequential
from keras.layers import LSTM as KERAS_LSTM, Dense, Dropout, Conv2D, Flatten, BatchNormalization, Activation, MaxPooling2D
from . import Model


def __init__(self, input_shape, num_classes, **params):
    '\n        Constructor to initialize the deep neural network model. Takes the input\n        shape and number of classes and other parameters required for the\n        abstract class `Model` as parameters.\n\n        Args:\n            input_shape (tuple): shape of the input\n            num_classes (int): number of different classes ( labels ) in the data.\n            **params: Additional parameters required by the underlying abstract\n                class `Model`.\n\n        '
    super(DNN, self).__init__(**params)
    self.input_shape = input_shape
    self.model = Sequential()
    self.make_default_model()
    self.model.add(Dense(num_classes, activation='softmax'))
    self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(self.model.summary(), file=sys.stderr)
    self.save_path = (self.save_path or (self.name + '_best_model.h5'))
