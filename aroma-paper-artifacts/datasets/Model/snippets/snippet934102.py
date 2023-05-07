import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from keras import optimizers


def apModel(X, apw_h, apw_o):
    h = tf.nn.relu(tf.matmul(X, apw_h))
    return tf.matmul(h, apw_o)
