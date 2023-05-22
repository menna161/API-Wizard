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


def _call(self, inp, inp_features, is_training, is_posterior=True, prop_state=None):
    print(((('\n' + ('-' * 10)) + ' ConvGridObjectLayer({}, is_posterior={}) '.format(self.name, is_posterior)) + ('-' * 10)))
    self.maybe_build_subnet('box_network', builder=cfg.build_conv_lateral, key='box')
    self.maybe_build_subnet('attr_network', builder=cfg.build_conv_lateral, key='attr')
    self.maybe_build_subnet('z_network', builder=cfg.build_conv_lateral, key='z')
    self.maybe_build_subnet('obj_network', builder=cfg.build_conv_lateral, key='obj')
    self.maybe_build_subnet('object_encoder')
    (_, H, W, n_channels) = tf_shape(inp_features)
    if (self.B != 1):
        raise Exception('NotImplemented')
    if (not self.initialized):
        (self.batch_size, self.image_height, self.image_width, self.image_depth) = tf_shape(inp)
        self.H = H
        self.W = W
        self.HWB = (H * W)
        self.batch_size = tf.shape(inp)[0]
        self.is_training = is_training
        self.float_is_training = tf.to_float(is_training)
    is_posterior_tf = tf.ones_like(inp_features[(..., :2)])
    if is_posterior:
        is_posterior_tf = (is_posterior_tf * [1, 0])
    else:
        is_posterior_tf = (is_posterior_tf * [0, 1])
    objects = AttrDict()
    base_features = tf.concat([inp_features, is_posterior_tf], axis=(- 1))
    layer_inp = base_features
    n_features = self.n_passthrough_features
    output_size = 8
    network_output = self.box_network(layer_inp, (output_size + n_features), self.is_training)
    (rep_input, features) = tf.split(network_output, (output_size, n_features), axis=(- 1))
    _objects = self._build_box(rep_input, self.is_training)
    objects.update(_objects)
    if is_posterior:
        (yt, xt, ys, xs) = tf.split(objects['normalized_box'], 4, axis=(- 1))
        (yt, xt, ys, xs) = coords_to_image_space(yt, xt, ys, xs, (self.image_height, self.image_width), self.anchor_box, top_left=False)
        transform_constraints = snt.AffineWarpConstraints.no_shear_2d()
        warper = snt.AffineGridWarper((self.image_height, self.image_width), self.object_shape, transform_constraints)
        _boxes = tf.concat([xs, ((2 * xt) - 1), ys, ((2 * yt) - 1)], axis=(- 1))
        _boxes = tf.reshape(_boxes, (((self.batch_size * H) * W), 4))
        grid_coords = warper(_boxes)
        grid_coords = tf.reshape(grid_coords, (self.batch_size, H, W, *self.object_shape, 2))
        if self.edge_resampler:
            glimpse = resampler_edge.resampler_edge(inp, grid_coords)
        else:
            glimpse = tf.contrib.resampler.resampler(inp, grid_coords)
    else:
        glimpse = tf.zeros((self.batch_size, H, W, *self.object_shape, self.image_depth))
    encoded_glimpse = apply_object_wise(self.object_encoder, glimpse, n_trailing_dims=3, output_size=self.A, is_training=self.is_training)
    if (not is_posterior):
        encoded_glimpse = tf.zeros_like(encoded_glimpse)
    layer_inp = tf.concat([base_features, features, encoded_glimpse, objects['local_box']], axis=(- 1))
    network_output = self.attr_network(layer_inp, ((2 * self.A) + n_features), self.is_training)
    (attr_mean, attr_log_std, features) = tf.split(network_output, (self.A, self.A, n_features), axis=(- 1))
    attr_std = self.std_nonlinearity(attr_log_std)
    attr = Normal(loc=attr_mean, scale=attr_std).sample()
    objects.update(attr_mean=attr_mean, attr_std=attr_std, attr=attr, glimpse=glimpse)
    layer_inp = tf.concat([base_features, features, objects['local_box'], objects['attr']], axis=(- 1))
    n_features = self.n_passthrough_features
    network_output = self.z_network(layer_inp, (2 + n_features), self.is_training)
    (z_mean, z_log_std, features) = tf.split(network_output, (1, 1, n_features), axis=(- 1))
    z_std = self.std_nonlinearity(z_log_std)
    z_mean = ((self.training_wheels * tf.stop_gradient(z_mean)) + ((1 - self.training_wheels) * z_mean))
    z_std = ((self.training_wheels * tf.stop_gradient(z_std)) + ((1 - self.training_wheels) * z_std))
    z_logit = Normal(loc=z_mean, scale=z_std).sample()
    z = self.z_nonlinearity(z_logit)
    objects.update(z_logit_mean=z_mean, z_logit_std=z_std, z_logit=z_logit, z=z)
    layer_inp = tf.concat([base_features, features, objects['local_box'], objects['attr'], objects['z']], axis=(- 1))
    rep_input = self.obj_network(layer_inp, 1, self.is_training)
    _objects = self._build_obj(rep_input, self.is_training)
    objects.update(_objects)
    if (prop_state is not None):
        objects.prop_state = tf.tile(prop_state[(0:1, None, None, :)], (self.batch_size, H, W, 1))
        objects.prior_prop_state = tf.tile(prop_state[(0:1, None, None, :)], (self.batch_size, H, W, 1))
    if self.flatten:
        _objects = AttrDict()
        for (k, v) in objects.items():
            (_, _, _, *trailing_dims) = tf_shape(v)
            _objects[k] = tf.reshape(v, (self.batch_size, self.HWB, *trailing_dims))
        objects = _objects
    flat_objects = tf.reshape(objects.obj, (self.batch_size, (- 1)))
    objects.pred_n_objects = tf.reduce_sum(flat_objects, axis=1)
    objects.pred_n_objects_hard = tf.reduce_sum(tf.round(flat_objects), axis=1)
    return objects
