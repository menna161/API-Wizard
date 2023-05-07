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
def static(imgs, DIFFICULTY):
    'Gaussian noise, or "static"\n    '
    STATIC_STDDEVS = [0.0, 0.03, 0.06, 0.1, 0.13, 0.16, 0.2, 0.23, 0.26, 0.3, 0.33, 0.36, 0.4, 0.43, 0.46, 0.5]
    img_shape = imgs[0].shape
    batch_size = imgs.shape[0]
    stddev = tf.gather(STATIC_STDDEVS, DIFFICULTY)
    stddev = tf.random.uniform([], 0, stddev)
    noise = tf.random.normal((batch_size, *img_shape), mean=0, stddev=stddev)
    imgs = (imgs + noise)
    return imgs
