import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


def test_with_scheduler(self):
    (w, b) = self.gen_random_weights()
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(input_shape=(3,), units=5, weights=[w, b]))
    decay = tf.keras.optimizers.schedules.ExponentialDecay(0.001, decay_steps=100000, decay_rate=0.96)
    decay = tf.keras.optimizers.schedules.serialize(decay)
    model.compile(optimizer=AdaBound(learning_rate=decay, final_lr=0.1, decay=0.5, weight_decay=decay), loss='mse')
    x = np.random.standard_normal((1, 3))
    y = (np.dot(x, w) + b)
    model.train_on_batch(x, y)
