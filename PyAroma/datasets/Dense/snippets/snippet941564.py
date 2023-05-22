import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


def test_with_plateau(self):
    self.reset_seed(51966)
    (w, b) = self.gen_random_weights()
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(input_shape=(3,), units=5, weights=[w, b]))
    model.compile(optimizer=AdaBound(lr=0.001, final_lr=0.1), loss='mse')
    x = np.random.standard_normal((10000, 3))
    y = (np.dot(x, w) + b)
    model.fit(x, y, epochs=100, callbacks=[keras.callbacks.ReduceLROnPlateau(monitor='loss')], verbose=False)
    with tempfile.TemporaryDirectory() as temp_path:
        model_path = os.path.join(temp_path, 'keras_adabound.h5')
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects={'AdaBound': AdaBound})
    self.assertGreater(0.001, float(K.get_value(model.optimizer.lr)))
    self.assertEqual(0.001, model.optimizer.base_lr)
