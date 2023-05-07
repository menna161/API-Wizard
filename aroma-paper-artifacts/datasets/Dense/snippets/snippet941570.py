import os
import tempfile
from unittest import TestCase
import torch
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound
from adabound import AdaBound as OfficialAdaBound


@staticmethod
def gen_keras_linear(w, b, amsgrad=False, weight_decay=0.0):
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(input_shape=(3,), units=5, weights=[w, b]))
    model.compile(optimizer=AdaBound(lr=0.001, final_lr=0.1, amsgrad=amsgrad, weight_decay=weight_decay), loss='mse')
    return model
