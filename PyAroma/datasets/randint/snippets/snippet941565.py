import os
import tempfile
from unittest import TestCase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound


def _embedding_data(self):
    while True:
        x = np.random.randint(0, 10, (3, 7))
        y = np.zeros(3)
        for i in range(3):
            if (5 in x[i]):
                y[i] = 1
        (yield (x, y))
