import tensorflow as tf
from .. import layers


def create_pyramid_features(C3, C4, C5, feature_size=256):
    ' Creates the FPN layers on top of the backbone features.\n\tArgs\n\t\tC3           : Feature stage C3 from the backbone.\n\t\tC4           : Feature stage C4 from the backbone.\n\t\tC5           : Feature stage C5 from the backbone.\n\t\tfeature_size : The feature size to use for the resulting feature levels.\n\tReturns\n\t\tA list of feature levels [P3, P4, P5, P6, P7].\n\t'
    P5 = tf.keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C5_reduced')(C5)
    P5_upsampled = layers.UpsampleLike(name='P5_upsampled')([P5, C4])
    P5 = tf.keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P5')(P5)
    P4 = tf.keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C4_reduced')(C4)
    P4 = tf.keras.layers.Add(name='P4_merged')([P5_upsampled, P4])
    P4_upsampled = layers.UpsampleLike(name='P4_upsampled')([P4, C3])
    P4 = tf.keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P4')(P4)
    P3 = tf.keras.layers.Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='C3_reduced')(C3)
    P3 = tf.keras.layers.Add(name='P3_merged')([P4_upsampled, P3])
    P3 = tf.keras.layers.Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='P3')(P3)
    P6 = tf.keras.layers.Conv2D(feature_size, kernel_size=3, strides=2, padding='same', name='P6')(C5)
    P7 = tf.keras.layers.Activation('relu', name='C6_relu')(P6)
    P7 = tf.keras.layers.Conv2D(feature_size, kernel_size=3, strides=2, padding='same', name='P7')(P7)
    return [P3, P4, P5, P6, P7]
