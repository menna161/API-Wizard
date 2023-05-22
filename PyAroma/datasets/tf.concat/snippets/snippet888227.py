from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import capslayer as cl
import tensorflow as tf


def _leaky_routing(logits):
    leak_shape = cl.shape(logits)
    leak = tf.zeros((leak_shape[:(- 3)] + [1, 1, 1]))
    leaky_logits = tf.concat([leak, logits], axis=(- 3))
    leaky_routing = cl.softmax(leaky_logits, axis=(- 3))
    return tf.split(leaky_routing, [1, leak_shape[(- 3)]], axis=(- 3))[1]
