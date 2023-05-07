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


def _build_box(self, box_params, is_training, hw=None):
    (mean, log_std) = tf.split(box_params, 2, axis=(- 1))
    std = self.std_nonlinearity(log_std)
    mean = ((self.training_wheels * tf.stop_gradient(mean)) + ((1 - self.training_wheels) * mean))
    std = ((self.training_wheels * tf.stop_gradient(std)) + ((1 - self.training_wheels) * std))
    (cell_y_mean, cell_x_mean, height_mean, width_mean) = tf.split(mean, 4, axis=(- 1))
    (cell_y_std, cell_x_std, height_std, width_std) = tf.split(std, 4, axis=(- 1))
    cell_y_logit = Normal(loc=cell_y_mean, scale=cell_y_std).sample()
    cell_x_logit = Normal(loc=cell_x_mean, scale=cell_x_std).sample()
    height_logit = Normal(loc=height_mean, scale=height_std).sample()
    width_logit = Normal(loc=width_mean, scale=width_std).sample()
    cell_y = tf.nn.sigmoid(tf.clip_by_value(cell_y_logit, (- 10), 10))
    cell_x = tf.nn.sigmoid(tf.clip_by_value(cell_x_logit, (- 10), 10))
    assert (self.max_yx > self.min_yx)
    cell_y = ((float((self.max_yx - self.min_yx)) * cell_y) + self.min_yx)
    cell_x = ((float((self.max_yx - self.min_yx)) * cell_x) + self.min_yx)
    height = tf.nn.sigmoid(tf.clip_by_value(height_logit, (- 10), 10))
    width = tf.nn.sigmoid(tf.clip_by_value(width_logit, (- 10), 10))
    assert (self.max_hw > self.min_hw)
    height = ((float((self.max_hw - self.min_hw)) * height) + self.min_hw)
    width = ((float((self.max_hw - self.min_hw)) * width) + self.min_hw)
    local_box = tf.concat([cell_y, cell_x, height, width], axis=(- 1))
    ys = height
    xs = width
    if (hw is None):
        (w, h) = tf.meshgrid(tf.range(self.W, dtype=tf.float32), tf.range(self.H, dtype=tf.float32))
        h = h[(None, :, :, None)]
        w = w[(None, :, :, None)]
    else:
        (h, w) = hw
    yt = (((self.pixels_per_cell[0] * (cell_y + h)) + self.grid_offset[0]) / self.anchor_box[0])
    xt = (((self.pixels_per_cell[1] * (cell_x + w)) + self.grid_offset[1]) / self.anchor_box[1])
    normalized_box = tf.concat([yt, xt, ys, xs], axis=(- 1))
    ys_logit = height_logit
    xs_logit = width_logit
    return dict(cell_y=cell_y, cell_x=cell_x, height=height, width=width, local_box=local_box, cell_y_logit_mean=cell_y_mean, cell_x_logit_mean=cell_x_mean, height_logit_mean=height_mean, width_logit_mean=width_mean, cell_y_logit_std=cell_y_std, cell_x_logit_std=cell_x_std, height_logit_std=height_std, width_logit_std=width_std, yt=yt, xt=xt, ys=ys, xs=xs, normalized_box=normalized_box, ys_logit=ys_logit, xs_logit=xs_logit)
