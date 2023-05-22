from pyodds.algo.base import Base
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from sklearn import preprocessing
import os


def _build_model(self):
    model = tf.keras.Sequential()
    for neuron_num in self.hidden_neurons:
        model.add(layers.Dense(neuron_num, activation=self.activation, kernel_regularizer=tf.keras.regularizers.l1(self.kernel_regularizer)))
        model.add(layers.Dropout(self.dropout_rate))
    model.compile(loss=self.loss_function, optimizer=self.optimizer)
    return model
