import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def __init__(self, filters: int):
    super(ResidualBlock, self).__init__()
    self.first_conv = tf.keras.layers.Conv2D((filters // 4), kernel_size=1, strides=1, padding='same', **cnn_regularization)
    self.second_conv = tf.keras.layers.Conv2D((filters // 4), kernel_size=3, strides=1, padding='same', **cnn_regularization)
    self.third_conv = tf.keras.layers.Conv2D(filters, kernel_size=1, strides=1, padding='same', **cnn_regularization)
    self.batch_norms = [tf.keras.layers.BatchNormalization() for _ in range(3)]
