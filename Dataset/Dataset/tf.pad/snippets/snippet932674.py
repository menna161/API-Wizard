from __future__ import division
import tensorflow as tf
from ops import *
from utils import *


def residule_block(x, dim, ks=3, s=1, name='res'):
    p = int(((ks - 1) / 2))
    y = tf.pad(x, [[0, 0], [p, p], [p, p], [0, 0]], 'REFLECT')
    y = instance_norm(conv2d(y, dim, ks, s, padding='VALID', name=(name + '_c1')), (name + '_bn1'))
    y = tf.pad(tf.nn.relu(y), [[0, 0], [p, p], [p, p], [0, 0]], 'REFLECT')
    y = instance_norm(conv2d(y, dim, ks, s, padding='VALID', name=(name + '_c2')), (name + '_bn2'))
    return relu((y + x))
