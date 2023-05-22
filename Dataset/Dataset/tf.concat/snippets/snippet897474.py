import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2


def mean_image_subtraction(images, means=(_R_MEAN, _G_MEAN, _B_MEAN)):
    num_channels = 3
    channels = tf.split(images, num_channels, axis=2)
    for i in range(num_channels):
        channels[i] -= means[i]
    return tf.concat(channels, axis=2)
