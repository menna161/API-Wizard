import math
import code
import tensorflow as tf
import matplotlib.pyplot as plt
import os


def get_mat(rotation, shear, height_zoom, width_zoom, height_shift, width_shift):
    'Return a 3x3 transformmatrix which transforms indicies of original images\n  '
    rotation = ((math.pi * rotation) / 180.0)
    shear = ((math.pi * shear) / 180.0)
    c1 = tf.math.cos(rotation)
    s1 = tf.math.sin(rotation)
    rotation_matrix = tf.reshape(tf.concat([c1, s1, [0], (- s1), c1, [0], [0], [0], [1]], axis=0), [3, 3])
    c2 = tf.math.cos(shear)
    s2 = tf.math.sin(shear)
    shear_matrix = tf.reshape(tf.concat([[1], s2, [0], [0], c2, [0], [0], [0], [1]], axis=0), [3, 3])
    zoom_matrix = tf.reshape(tf.concat([([1] / height_zoom), [0], [0], [0], ([1] / width_zoom), [0], [0], [0], [1]], axis=0), [3, 3])
    shift_matrix = tf.reshape(tf.concat([[1], [0], height_shift, [0], [1], width_shift, [0], [0], [1]], axis=0), [3, 3])
    return tf.matmul(tf.matmul(rotation_matrix, shear_matrix), tf.matmul(zoom_matrix, shift_matrix))
