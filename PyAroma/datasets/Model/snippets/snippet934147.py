import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from random import gauss


def apModel(X, apw_h, apw_o):
    h = tf.nn.leaky_relu(tf.matmul(X, apw_h))
    return tf.matmul(h, apw_o)
