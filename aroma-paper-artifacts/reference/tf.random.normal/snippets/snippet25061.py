import math
import code
import tensorflow as tf
import matplotlib.pyplot as plt
import os


def clipped_random():
    rand = tf.random.normal([1], dtype=tf.float32)
    rand = (tf.clip_by_value(rand, (- 2.0), 2.0) / 2.0)
    return rand
