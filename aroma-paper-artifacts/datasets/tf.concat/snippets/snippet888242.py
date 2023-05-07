from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import capslayer as cl
import tensorflow as tf


def matmul_v1(a, b, transpose_a=False, transpose_b=False, name=None):
    name = ('matmul' if (name is None) else name)
    with tf.name_scope(name):
        rank_a = len(a.shape)
        rank_b = len(b.shape)
        if ((rank_a < 2) or (rank_b < 2)):
            raise TypeError('Rank must be greater than 2')
        perm_a = [i for i in range((rank_a - 2))]
        perm_b = [i for i in range((rank_b - 2))]
        if transpose_a:
            perm = (([(rank_a - 1)] + perm_a) + [(rank_a - 2)])
        else:
            perm = (([(rank_a - 2)] + perm_a) + [(rank_a - 1)])
        a = tf.transpose(a, perm=perm)
        if transpose_b:
            perm = (([(rank_b - 2)] + perm_b) + [(rank_b - 1)])
        else:
            perm = (([(rank_b - 1)] + perm_b) + [(rank_b - 2)])
        b = tf.transpose(b, perm=perm)
        C = []
        for i in range(a.get_shape()[0].value):
            B = []
            for j in range(b.get_shape()[0].value):
                k = tf.reduce_sum((a[i] * b[j]), axis=(- 1), keepdims=True)
                B.append(k)
            C.append(tf.expand_dims(tf.concat(B, axis=(- 1)), axis=(- 2)))
        C = tf.concat(C, axis=(- 2))
        return C
