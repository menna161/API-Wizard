import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2


def batch_mean_image_subtraction(images, means=(_R_MEAN, _G_MEAN, _B_MEAN)):
    if (images.get_shape().ndims != 4):
        raise ValueError('Input must be of size [batch, height, width, C>0')
    num_channels = images.get_shape().as_list()[(- 1)]
    if (len(means) != num_channels):
        raise ValueError('len(means) must match the number of channels')
    channels = tf.split(images, num_channels, axis=3)
    for i in range(num_channels):
        channels[i] -= means[i]
    return tf.concat(channels, axis=3)
