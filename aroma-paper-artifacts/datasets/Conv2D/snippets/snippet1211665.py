import numpy as np
import tensorflow as tf


def __init__(self):
    self.conv1 = tf.keras.layers.Conv2D(32, [3, 3], activation='relu')
    self.mpool1 = tf.keras.layers.MaxPool2D([2, 2], 2)
    self.conv2 = tf.keras.layers.Conv2D(64, [3, 3], activation='relu')
    self.mpool2 = tf.keras.layers.MaxPool2D([2, 2], 2)
    self.conv3 = tf.keras.layers.Conv2D(128, [3, 3], activation='relu')
    self.fconv = tf.keras.layers.Conv2D(1, [1, 1])
