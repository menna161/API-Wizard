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
def cutout(imgs, DIFFICULTY):
    MASK_PERCENT = [0.0, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.34, 0.36, 0.38, 0.4]
    mask_percent = tf.gather(MASK_PERCENT, DIFFICULTY)
    y_size = tf.random.uniform([], 0, mask_percent)
    x_size = tf.random.uniform([], 0, mask_percent)
    y_size = (tf.cast(((imgs.shape[1] * y_size) / 2), tf.int32) * 2)
    x_size = (tf.cast(((imgs.shape[2] * x_size) / 2), tf.int32) * 2)
    for _ in range(2):
        imgs = tfa.image.random_cutout(imgs, mask_size=[y_size, x_size])
    return imgs
