import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2


def _mean_image_subtraction(image, means=(_R_MEAN, _G_MEAN, _B_MEAN)):
    if (image.get_shape().ndims != 3):
        raise ValueError('Input must be of size [height, width, C>0]')
    num_channels = image.get_shape().as_list()[(- 1)]
    if (len(means) != num_channels):
        raise ValueError('len(means) must match the number of channels')
    channels = tf.split(axis=2, num_or_size_splits=num_channels, value=image)
    for i in range(num_channels):
        channels[i] -= means[i]
    return tf.concat(axis=2, values=channels)
