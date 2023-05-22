import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


def test_with_embedding_amsgrad(self):
    model = keras.models.Sequential()
    model.add(keras.layers.Embedding(input_dim=10, mask_zero=True, output_dim=5, input_shape=(7,)))
    model.add(keras.layers.LSTM(units=5))
    model.add(keras.layers.Dense(units=2, activation='softmax'))
    model.compile(optimizer=AdaBound(amsgrad=True, weight_decay=0.001), loss='sparse_categorical_crossentropy')
    model.fit(self._embedding_data(), steps_per_epoch=1000, validation_data=self._embedding_data(), validation_steps=10, epochs=2)
    with tempfile.TemporaryDirectory() as temp_path:
        model_path = os.path.join(temp_path, 'keras_adabound.h5')
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects={'AdaBound': AdaBound})
    model.fit(self._embedding_data(), steps_per_epoch=1000, validation_data=self._embedding_data(), validation_steps=10, epochs=1)
