import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
import sonnet as snt
import itertools
from dps import cfg
from dps.utils import Param, AttrDict
from dps.utils.tf import build_scheduled_value, FIXED_COLLECTION, ScopedFunction, tf_shape, apply_object_wise
from auto_yolo.tf_ops import render_sprites, resampler_edge
from auto_yolo.models.core import concrete_binary_pre_sigmoid_sample, coords_to_image_space


def _get_sequential_context(self, program, h, w, b, edge_element):
    context = []
    grid_size = ((2 * self.n_lookback) + 1)
    n_grid_locs = int(((grid_size ** 2) / 2))
    for idx in range(n_grid_locs):
        _i = ((int((idx / grid_size)) + h) - self.n_lookback)
        _j = ((int((idx % grid_size)) + w) - self.n_lookback)
        for k in range(self.B):
            if ((_i < 0) or (_j < 0) or (_i >= program.shape[0]) or (_j >= program.shape[1])):
                context.append(edge_element)
            else:
                context.append(program[(_i, _j, k)])
    offset = ((- (self.B - 1)) + b)
    for k in range((self.B - 1)):
        _k = (k + offset)
        if (_k < 0):
            context.append(edge_element)
        else:
            context.append(program[(h, w, _k)])
    if context:
        return tf.concat(context, axis=1)
    else:
        return tf.zeros_like(edge_element[(:, 0:0)])
