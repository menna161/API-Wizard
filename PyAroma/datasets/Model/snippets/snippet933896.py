from environments.rocketlander import RocketLander
import tensorflow as tf
import numpy as np
import gym
import pybullet
import pybullet_envs
import pygal
import os
import h5py
import math
from keras import optimizers


def apModel(X, apw_h, apw_h2, apw_h3, apw_o):
    h = tf.nn.leaky_relu(tf.matmul(X, apw_h))
    h2 = tf.nn.leaky_relu(tf.matmul(h, apw_h2))
    h3 = tf.nn.leaky_relu(tf.matmul(h2, apw_h3))
    return tf.matmul(h2, apw_o)
