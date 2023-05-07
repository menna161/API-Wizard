import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def _call(self, inp, output_size, is_training):
    batch_size = tf.shape(inp)[0]
    spatial_shape = inp.shape[1:(- 1)]
    n_objects = np.prod(spatial_shape)
    obj_dim = inp.shape[(- 1)]
    inp = tf.reshape(inp, (batch_size, n_objects, obj_dim))
    if (self.f is None):
        self.f = cfg.build_relation_network_f(scope='relation_network_f')
    if (self.g is None):
        self.g = cfg.build_relation_network_g(scope='relation_network_g')
    f_inputs = []
    for i in range(n_objects):
        for j in range(n_objects):
            f_inputs.append(tf.concat([inp[(:, i, :)], inp[(:, j, :)]], axis=1))
    f_inputs = tf.concat(f_inputs, axis=0)
    f_output = self.f(f_inputs, self.f_dim, is_training)
    f_output = tf.split(f_output, (n_objects ** 2), axis=0)
    g_input = tf.concat(f_output, axis=1)
    return self.g(g_input, output_size, is_training)
