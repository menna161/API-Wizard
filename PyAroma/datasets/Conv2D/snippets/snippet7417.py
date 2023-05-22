import tensorflow as tf
from ..layers.spectralnorm import SpectralNormalization
from ..layers.conditionalbatchnorm import ConditionalBatchNorm


def __init__(self, filters, n_classes, kernel_size=3, pad='same', spectral_norm=False):
    super(GenResBlock, self).__init__()
    self.cbn1 = ConditionalBatchNorm(n_classes)
    self.cbn2 = ConditionalBatchNorm(n_classes)
    if spectral_norm:
        self.deconv2a = SpectralNormalization(tf.keras.layers.Conv2DTranspose(filters, kernel_size, padding=pad))
        self.deconv2b = SpectralNormalization(tf.keras.layers.Conv2DTranspose(filters, kernel_size, padding=pad))
        self.shortcut_conv = SpectralNormalization(tf.keras.layers.Conv2DTranspose(filters, kernel_size=1, padding=pad))
    else:
        self.deconv2a = tf.keras.layers.Conv2DTranspose(filters, kernel_size, padding=pad)
        self.deconv2b = tf.keras.layers.Conv2DTranspose(filters, kernel_size, padding=pad)
        self.shortcut_conv = tf.keras.layers.Conv2DTranspose(filters, kernel_size=1, padding=pad)
    self.up_sample = tf.keras.layers.UpSampling2D(size=(2, 2))
