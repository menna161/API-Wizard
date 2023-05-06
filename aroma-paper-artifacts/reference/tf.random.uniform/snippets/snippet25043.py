import code
import random
import imageio
import tensorflow as tf
import tensorflow_addons as tfa
import matplotlib.pyplot as plt
from ccn.cfg import get_config
from ccn.ml_utils import gaussian_k
from ccn.experimental_aug import transform_batch
import os


@staticmethod
def blur(imgs, DIFFICULTY):
    'Apply blur via a Gaussian convolutional kernel\n    '
    STDDEVS = [0.01, 0.3, 0.6, 0.8, 1.0, 1.3, 1.6, 1.8, 2.0, 2.3, 2.6, 2.8, 3.0, 3.3, 3.6, 3.8]
    img_shape = imgs[0].shape
    c = img_shape[2]
    stddev = tf.gather(STDDEVS, DIFFICULTY)
    stddev = tf.random.uniform([], 0, stddev)
    gauss_kernel = gaussian_k(7, 7, 3, 3, stddev)
    gauss_kernel = gauss_kernel[(:, :, tf.newaxis, tf.newaxis)]
    out_channels = []
    for c_ in range(c):
        in_channel = tf.expand_dims(imgs[(..., c_)], (- 1))
        out_channel = tf.nn.conv2d(in_channel, gauss_kernel, strides=1, padding='SAME')
        out_channel = out_channel[(..., 0)]
        out_channels.append(out_channel)
    imgs = tf.stack(out_channels, axis=(- 1))
    return imgs
