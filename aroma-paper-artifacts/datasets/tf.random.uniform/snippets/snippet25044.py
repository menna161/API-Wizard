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
def random_scale(imgs, DIFFICULTY):
    'Randomly scales all of the values in each channel\n    '
    MULTIPLY_SCALES = [[1, 1], [0.9, 1.1], [0.85, 1.15], [0.8, 1.2], [0.75, 1.25], [0.7, 1.3], [0.65, 1.325], [0.6, 1.35], [0.55, 1.375], [0.5, 1.4], [0.48, 1.42], [0.46, 1.44], [0.44, 1.46], [0.42, 1.48], [0.4, 1.5], [0.35, 1.6]]
    channels = imgs.shape[(- 1)]
    scales = tf.gather(MULTIPLY_SCALES, DIFFICULTY)
    scales = tf.random.uniform([channels], minval=scales[0], maxval=scales[1])
    imgs = (imgs * scales)
    return imgs
