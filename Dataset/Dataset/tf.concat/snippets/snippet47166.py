import tensorflow as tf
from tensorflow.python.ops.rnn import dynamic_rnn
import numpy as np
import sonnet as snt
from matplotlib.colors import to_rgb
import matplotlib.patches as patches
import shutil
import os
from dps import cfg
from dps.utils import Param
from dps.utils.tf import RNNCell, tf_mean_sum, tf_shape, tf_cosine_similarity
from auto_yolo.tf_ops import render_sprites
from auto_yolo.models import yolo_air
from auto_yolo.models.core import xent_loss, AP, VariationalAutoencoder, normal_vae
import matplotlib.pyplot as plt


def tf_find_connected_components(inp, bg, threshold, colors=None, cosine_threshold=None):
    assert (len(inp.shape) == 4)
    if isinstance(colors, str):
        colors = colors.split()
    mask = (tf.reduce_sum(tf.abs((inp - bg)), axis=3) >= threshold)
    if ((colors is None) or (cosine_threshold is None)):
        output = _find_connected_componenents_body(mask)
        output['color'] = output['obj']
        return output
    objects = []
    for color in colors:
        if isinstance(color, str):
            color = tf.constant(to_rgb(color), tf.float32)
        similarity = tf_cosine_similarity(inp, color)
        color_mask = tf.logical_and((similarity >= cosine_threshold), mask)
        objects.append(_find_connected_componenents_body(color_mask))
    output = dict(normalized_box=tf.concat([o['normalized_box'] for o in objects], axis=1), obj=tf.concat([o['obj'] for o in objects], axis=1), n_objects=tf.reduce_sum(tf.stack([o['n_objects'] for o in objects], axis=1), axis=1), color=tf.concat([(float((i + 1)) * o['obj']) for (i, o) in enumerate(objects)], axis=1))
    output['max_objects'] = tf.reduce_max(output['n_objects'])
    return output
