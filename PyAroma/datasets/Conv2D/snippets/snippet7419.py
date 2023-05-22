import tensorflow as tf
from ..layers.spectralnorm import SpectralNormalization
from ..layers.conditionalbatchnorm import ConditionalBatchNorm


def __init__(self, filters, kernel_size=3, downsample=False, pad='same', spectral_norm=False):
    super(DiscResBlock, self).__init__()
    if spectral_norm:
        self.conv1 = SpectralNormalization(tf.keras.layers.Conv2D(filters, kernel_size, padding=pad, kernel_initializer='glorot_uniform'))
        self.conv2 = SpectralNormalization(tf.keras.layers.Conv2D(filters, kernel_size, padding=pad, kernel_initializer='glorot_uniform'))
        self.shortcut_conv = SpectralNormalization(tf.keras.layers.Conv2D(filters, kernel_size=(1, 1), kernel_initializer='glorot_uniform', padding=pad))
    else:
        self.conv1 = tf.keras.layers.Conv2D(filters, kernel_size, padding=pad, kernel_initializer='glorot_uniform')
        self.conv2 = tf.keras.layers.Conv2D(filters, kernel_size, padding=pad, kernel_initializer='glorot_uniform')
        self.shortcut_conv = tf.keras.layers.Conv2D(filters, kernel_size=(1, 1), kernel_initializer='glorot_uniform', padding=pad)
    self.downsample_layer = tf.keras.layers.AvgPool2D((2, 2))
    self.downsample = downsample
