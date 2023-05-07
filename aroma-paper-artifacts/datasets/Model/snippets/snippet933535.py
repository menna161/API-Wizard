import numpy as np
import keras
import gym
from random import gauss
import math
from random import randint
import tensorflow as tf
from Lib.Individual import IndividualTF


def apModel(X, apw_h, apw_o):
    h = tf.nn.leaky_relu(tf.matmul(X, apw_h))
    return tf.matmul(h, apw_o)
