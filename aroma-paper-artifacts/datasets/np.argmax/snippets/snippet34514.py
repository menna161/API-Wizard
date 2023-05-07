import sys
import numpy as np
from keras import Sequential
from keras.layers import LSTM as KERAS_LSTM, Dense, Dropout, Conv2D, Flatten, BatchNormalization, Activation, MaxPooling2D
from . import Model


def predict_one(self, sample):
    if (not self.trained):
        sys.stderr.write('Model should be trained or loaded before doing predict\n')
        sys.exit((- 1))
    return np.argmax(self.model.predict(np.array([sample])))
