import tensorflow as tf


@staticmethod
def _make_conv_block(out_channels, kernel_size, strides, padding, use_bn=True):
    if use_bn:
        return tf.keras.Sequential([tf.keras.layers.Conv2D(filters=out_channels, kernel_size=kernel_size, strides=strides, padding=padding), tf.keras.layers.BatchNormalization(), tf.keras.layers.ReLU()])
    else:
        return tf.keras.Sequential([tf.keras.layers.Conv2D(filters=out_channels, kernel_size=kernel_size, strides=strides, padding=padding), tf.keras.layers.ReLU()])
