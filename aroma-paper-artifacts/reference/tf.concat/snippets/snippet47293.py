import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def _call(self, input_locs, input_features, reference_locs, reference_features, is_training):
    '\n        input_features: (B, n_inp, n_hidden)\n        input_locs: (B, n_inp, loc_dim)\n        reference_locs: (B, n_ref, loc_dim)\n\n        '
    assert ((reference_features is not None) == self.do_object_wise)
    if (not self.is_built):
        self.relation_func = self.build_mlp(scope='relation_func')
        if self.do_object_wise:
            self.object_wise_func = self.build_mlp(scope='object_wise_func')
        self.is_built = True
    loc_dim = tf_shape(input_locs)[(- 1)]
    n_ref = tf_shape(reference_locs)[(- 2)]
    (batch_size, n_inp, _) = tf_shape(input_features)
    input_locs = tf.broadcast_to(input_locs, (batch_size, n_inp, loc_dim))
    reference_locs = tf.broadcast_to(reference_locs, (batch_size, n_ref, loc_dim))
    adjusted_locs = (input_locs[(:, None, :, :)] - reference_locs[(:, :, None, :)])
    adjusted_features = tf.tile(input_features[(:, None)], (1, n_ref, 1, 1))
    relation_input = tf.concat([adjusted_features, adjusted_locs], axis=(- 1))
    if self.do_object_wise:
        object_wise = apply_object_wise(self.object_wise_func, reference_features, output_size=self.n_hidden, is_training=is_training)
        _object_wise = tf.tile(object_wise[(:, :, None)], (1, 1, n_inp, 1))
        relation_input = tf.concat([relation_input, _object_wise], axis=(- 1))
    else:
        object_wise = None
    V = apply_object_wise(self.relation_func, relation_input, output_size=self.n_hidden, is_training=is_training)
    attention_weights = tf.exp(((- 0.5) * tf.reduce_sum(((adjusted_locs / self.kernel_std) ** 2), axis=3)))
    attention_weights = ((attention_weights / ((2 * np.pi) ** (loc_dim / 2))) / (self.kernel_std ** loc_dim))
    result = tf.reduce_sum((V * attention_weights[(..., None)]), axis=2)
    if self.do_object_wise:
        result += object_wise
    return result
