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
    print(((('\n' + ('-' * 10)) + ' GridObjectLayer(is_posterior={}) '.format(is_posterior)) + ('-' * 10)))
    self.maybe_build_subnet('box_network', builder=cfg.build_lateral, key='box')
    self.maybe_build_subnet('attr_network', builder=cfg.build_lateral, key='attr')
    self.maybe_build_subnet('z_network', builder=cfg.build_lateral, key='z')
    self.maybe_build_subnet('obj_network', builder=cfg.build_lateral, key='obj')
    self.maybe_build_subnet('object_encoder')
    (_, H, W, _) = tf_shape(inp_features)
    H = int(H)
    W = int(W)
    if (not self.initialized):
        (self.batch_size, self.image_height, self.image_width, self.image_depth) = tf_shape(inp)
        self.H = H
        self.W = W
        self.HWB = ((H * W) * self.B)
        self.is_training = is_training
        self.float_is_training = tf.to_float(is_training)
    sizes = [4, self.A, 1, 1]
    sigmoids = [True, False, False, True]
    total_sample_size = sum(sizes)
    if (self.edge_weights is None):
        self.edge_weights = tf.get_variable('edge_weights', shape=total_sample_size, dtype=tf.float32)
        if ('edge' in self.fixed_weights):
            tf.add_to_collection(FIXED_COLLECTION, self.edge_weights)
    _edge_weights = tf.split(self.edge_weights, sizes, axis=0)
    _edge_weights = [(tf.nn.sigmoid(ew) if sigmoid else ew) for (ew, sigmoid) in zip(_edge_weights, sigmoids)]
    edge_element = tf.concat(_edge_weights, axis=0)
    edge_element = tf.tile(edge_element[(None, :)], (self.batch_size, 1))
    program = np.empty((H, W, self.B), dtype=np.object)
    is_posterior_tf = tf.ones((self.batch_size, 2))
    if is_posterior:
        is_posterior_tf = (is_posterior_tf * [1, 0])
    else:
        is_posterior_tf = (is_posterior_tf * [0, 1])
    results = []
    for (h, w, b) in itertools.product(range(H), range(W), range(self.B)):
        built = dict()
        (partial_program, features) = (None, None)
        context = self._get_sequential_context(program, h, w, b, edge_element)
        base_features = tf.concat([inp_features[(:, h, w, :)], context, is_posterior_tf], axis=1)
        layer_inp = base_features
        n_features = self.n_passthrough_features
        output_size = 8
        network_output = self.box_network(layer_inp, (output_size + n_features), self.is_training)
        (rep_input, features) = tf.split(network_output, (output_size, n_features), axis=1)
        _built = self._build_box(rep_input, self.is_training, hw=(h, w))
        built.update(_built)
        partial_program = built['local_box']
        if is_posterior:
            (yt, xt, ys, xs) = tf.split(built['normalized_box'], 4, axis=(- 1))
            (yt, xt, ys, xs) = coords_to_image_space(yt, xt, ys, xs, (self.image_height, self.image_width), self.anchor_box, top_left=False)
            transform_constraints = snt.AffineWarpConstraints.no_shear_2d()
            warper = snt.AffineGridWarper((self.image_height, self.image_width), self.object_shape, transform_constraints)
            _boxes = tf.concat([xs, ((2 * xt) - 1), ys, ((2 * yt) - 1)], axis=(- 1))
            grid_coords = warper(_boxes)
            grid_coords = tf.reshape(grid_coords, (self.batch_size, 1, *self.object_shape, 2))
            if self.edge_resampler:
                glimpse = resampler_edge.resampler_edge(inp, grid_coords)
            else:
                glimpse = tf.contrib.resampler.resampler(inp, grid_coords)
            glimpse = tf.reshape(glimpse, (self.batch_size, *self.object_shape, self.image_depth))
        else:
            glimpse = tf.zeros((self.batch_size, *self.object_shape, self.image_depth))
        encoded_glimpse = self.object_encoder(glimpse, (1, 1, self.A), self.is_training)
        encoded_glimpse = tf.reshape(encoded_glimpse, (self.batch_size, self.A))
        if (not is_posterior):
            encoded_glimpse = tf.zeros_like(encoded_glimpse)
        layer_inp = tf.concat([base_features, features, encoded_glimpse, partial_program], axis=1)
        network_output = self.attr_network(layer_inp, ((2 * self.A) + n_features), self.is_training)
        (attr_mean, attr_log_std, features) = tf.split(network_output, (self.A, self.A, n_features), axis=1)
        attr_std = self.std_nonlinearity(attr_log_std)
        attr = Normal(loc=attr_mean, scale=attr_std).sample()
        built.update(attr_mean=attr_mean, attr_std=attr_std, attr=attr, glimpse=glimpse)
        partial_program = tf.concat([partial_program, built['attr']], axis=1)
        layer_inp = tf.concat([base_features, features, partial_program], axis=1)
        n_features = self.n_passthrough_features
        network_output = self.z_network(layer_inp, (2 + n_features), self.is_training)
        (z_mean, z_log_std, features) = tf.split(network_output, (1, 1, n_features), axis=1)
        z_std = self.std_nonlinearity(z_log_std)
        z_mean = ((self.training_wheels * tf.stop_gradient(z_mean)) + ((1 - self.training_wheels) * z_mean))
        z_std = ((self.training_wheels * tf.stop_gradient(z_std)) + ((1 - self.training_wheels) * z_std))
        z_logit = Normal(loc=z_mean, scale=z_std).sample()
        z = self.z_nonlinearity(z_logit)
        built.update(z_logit_mean=z_mean, z_logit_std=z_std, z_logit=z_logit, z=z)
        partial_program = tf.concat([partial_program, built['z']], axis=1)
        layer_inp = tf.concat([base_features, features, partial_program], axis=1)
        rep_input = self.obj_network(layer_inp, 1, self.is_training)
        _built = self._build_obj(rep_input, self.is_training)
        built.update(_built)
        partial_program = tf.concat([partial_program, built['obj']], axis=1)
        results.append(built)
        program[(h, w, b)] = partial_program
        assert (program[(h, w, b)].shape[1] == total_sample_size)
    objects = AttrDict()
    for k in results[0]:
        objects[k] = tf.stack([r[k] for r in results], axis=1)
    if (prop_state is not None):
        objects.prop_state = tf.tile(prop_state[(0:1, None)], (self.batch_size, self.HWB, 1))
        objects.prior_prop_state = tf.tile(prop_state[(0:1, None)], (self.batch_size, self.HWB, 1))
    objects.pred_n_objects = tf.reduce_sum(objects.obj, axis=(1, 2))
    objects.pred_n_objects_hard = tf.reduce_sum(tf.round(objects.obj), axis=(1, 2))
    return objects
