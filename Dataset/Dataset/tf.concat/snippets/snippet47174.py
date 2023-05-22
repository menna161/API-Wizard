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


def _build_program_interpreter(self, tensors):
    max_objects = tensors['max_objects']
    (yt, xt, ys, xs) = tf.split(tensors['normalized_box'], 4, axis=(- 1))
    transform_constraints = snt.AffineWarpConstraints.no_shear_2d()
    warper = snt.AffineGridWarper((self.image_height, self.image_width), self.object_shape, transform_constraints)
    _boxes = tf.concat([xs, ((2 * (xt + (xs / 2))) - 1), ys, ((2 * (yt + (ys / 2))) - 1)], axis=(- 1))
    _boxes = tf.reshape(_boxes, ((self.batch_size * max_objects), 4))
    grid_coords = warper(_boxes)
    grid_coords = tf.reshape(grid_coords, (self.batch_size, max_objects, *self.object_shape, 2))
    glimpse = tf.contrib.resampler.resampler(tensors['inp'], grid_coords)
    object_encoder_in = tf.reshape(glimpse, ((self.batch_size * max_objects), *self.object_shape, self.image_depth))
    attr = self.object_encoder(object_encoder_in, (1, 1, (2 * self.A)), self.is_training)
    attr = tf.reshape(attr, (self.batch_size, max_objects, (2 * self.A)))
    (attr_mean, attr_log_std) = tf.split(attr, [self.A, self.A], axis=(- 1))
    attr_std = tf.exp(attr_log_std)
    if (not self.noisy):
        attr_std = tf.zeros_like(attr_std)
    (attr, attr_kl) = normal_vae(attr_mean, attr_std, self.attr_prior_mean, self.attr_prior_std)
    object_decoder_in = tf.reshape(attr, ((self.batch_size * max_objects), 1, 1, self.A))
    object_logits = self.object_decoder(object_decoder_in, (self.object_shape + (self.image_depth,)), self.is_training)
    objects = tf.nn.sigmoid(tf.clip_by_value(object_logits, (- 10.0), 10.0))
    objects = tf.reshape(objects, (self.batch_size, max_objects, *self.object_shape, self.image_depth))
    alpha = (tensors['obj'][(:, :, :, None, None)] * tf.ones_like(objects[(:, :, :, :, :1)]))
    importance = tf.ones_like(objects[(:, :, :, :, :1)])
    objects = tf.concat([objects, alpha, importance], axis=(- 1))
    scales = tf.concat([ys, xs], axis=(- 1))
    scales = tf.reshape(scales, (self.batch_size, max_objects, 2))
    offsets = tf.concat([yt, xt], axis=(- 1))
    offsets = tf.reshape(offsets, (self.batch_size, max_objects, 2))
    output = render_sprites.render_sprites(objects, tensors['n_objects'], scales, offsets, tensors['background'])
    return dict(output=output, glimpse=tf.reshape(glimpse, (self.batch_size, max_objects, *self.object_shape, self.image_depth)), attr=tf.reshape(attr, (self.batch_size, max_objects, self.A)), attr_kl=tf.reshape(attr_kl, (self.batch_size, max_objects, self.A)), objects=tf.reshape(objects, (self.batch_size, max_objects, *self.object_shape, self.image_depth)))
