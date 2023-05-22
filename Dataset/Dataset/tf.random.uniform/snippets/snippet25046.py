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
def sharp_tanh(imgs, DIFFICULTY):
    TANH_AMT = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
    tanh_amt = tf.gather(TANH_AMT, DIFFICULTY)
    tanh_amt = tf.random.uniform([], 0, tanh_amt)
    imgs = (tf.nn.tanh((imgs * tanh_amt)) * 1.31)
    return imgs
