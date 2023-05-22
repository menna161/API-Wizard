import math
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.python.framework import ops
from utils import *


def to_binary_tf(bar_or_track_bar, threshold=0.0, track_mode=False, melody=False):
    'Return the binarize tensor of the input tensor (be careful of the channel order!)'
    if track_mode:
        if melody:
            melody_is_max = tf.equal(bar_or_track_bar, tf.reduce_max(bar_or_track_bar, axis=2, keep_dims=True))
            melody_pass_threshold = (bar_or_track_bar > threshold)
            out_tensor = tf.logical_and(melody_is_max, melody_pass_threshold)
        else:
            out_tensor = (bar_or_track_bar > threshold)
        return out_tensor
    else:
        if (len(bar_or_track_bar.get_shape()) == 4):
            melody_track = tf.slice(bar_or_track_bar, [0, 0, 0, 0], [(- 1), (- 1), (- 1), 1])
            other_tracks = tf.slice(bar_or_track_bar, [0, 0, 0, 1], [(- 1), (- 1), (- 1), (- 1)])
        elif (len(bar_or_track_bar.get_shape()) == 5):
            melody_track = tf.slice(bar_or_track_bar, [0, 0, 0, 0, 0], [(- 1), (- 1), (- 1), (- 1), 1])
            other_tracks = tf.slice(bar_or_track_bar, [0, 0, 0, 0, 1], [(- 1), (- 1), (- 1), (- 1), (- 1)])
        melody_is_max = tf.equal(melody_track, tf.reduce_max(melody_track, axis=2, keep_dims=True))
        melody_pass_threshold = (melody_track > threshold)
        out_tensor_melody = tf.logical_and(melody_is_max, melody_pass_threshold)
        out_tensor_others = (other_tracks > threshold)
        if (len(bar_or_track_bar.get_shape()) == 4):
            return tf.concat([out_tensor_melody, out_tensor_others], 3)
        elif (len(bar_or_track_bar.get_shape()) == 5):
            return tf.concat([out_tensor_melody, out_tensor_others], 4)
