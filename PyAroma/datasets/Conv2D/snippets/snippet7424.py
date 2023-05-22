import tensorflow as tf
from ..layers.spectralnorm import SpectralNormalization


def build(self, input):
    (_, _, _, n_channels) = input
    if self.spectral_norm:
        self.conv1x1_f = SpectralNormalization(tf.keras.layers.Conv2D(filters=(n_channels // 8), kernel_size=(1, 1), padding='same', strides=(1, 1)))
        self.conv1x1_g = SpectralNormalization(tf.keras.layers.Conv2D(filters=(n_channels // 8), kernel_size=(1, 1), padding='same', strides=(1, 1)))
        self.conv1x1_h = SpectralNormalization(tf.keras.layers.Conv2D(filters=(n_channels // 2), kernel_size=(1, 1), padding='same', strides=(1, 1)))
        self.conv1x1_attn = SpectralNormalization(tf.keras.layers.Conv2D(filters=n_channels, kernel_size=(1, 1), padding='same', strides=(1, 1)))
    else:
        self.conv1x1_f = tf.keras.layers.Conv2D(filters=(n_channels // 8), kernel_size=(1, 1), padding='same', strides=(1, 1))
        self.conv1x1_g = SpectralNormalization(tf.keras.layers.Conv2D(filters=(n_channels // 8), kernel_size=(1, 1), padding='same', strides=(1, 1)))
        self.conv1x1_h = SpectralNormalization(tf.keras.layers.Conv2D(filters=(n_channels // 2), kernel_size=(1, 1), padding='same', strides=(1, 1)))
        self.conv1x1_attn = SpectralNormalization(tf.keras.layers.Conv2D(filters=n_channels, kernel_size=(1, 1), padding='same', strides=(1, 1)))
    self.g_maxpool = tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=2)
    self.h_maxpool = tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=2)
