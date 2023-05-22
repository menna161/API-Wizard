import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


@staticmethod
def gen_keras_linear(w, b, amsgrad=False):
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(input_shape=(3,), units=5, weights=[w, b]))
    model.compile(optimizer=AdaBound(lr=0.001, final_lr=0.1, amsgrad=amsgrad, weight_decay=0.001), loss='mse')
    return model
