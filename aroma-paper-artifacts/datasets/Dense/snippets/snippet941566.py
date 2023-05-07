import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


def test_with_embedding(self):
    model = keras.models.Sequential()
    model.add(keras.layers.Embedding(input_dim=10, output_dim=5, mask_zero=True, input_shape=(7,)))
    model.add(keras.layers.LSTM(units=5))
    model.add(keras.layers.Dense(units=2, activation='softmax'))
    model.compile(optimizer=AdaBound(), loss='sparse_categorical_crossentropy')
    model.fit(self._embedding_data(), steps_per_epoch=1000, validation_data=self._embedding_data(), validation_steps=10, epochs=3)
