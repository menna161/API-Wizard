import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def _call(self, _inp, output_size, is_training):
    if (self.h_cell is None):
        self.h_cell = cfg.build_math_cell(scope='regression_h_cell')
        self.w_cell = cfg.build_math_cell(scope='regression_w_cell')
        self.b_cell = cfg.build_math_cell(scope='regression_b_cell')
    edge_state = self.h_cell.zero_state(tf.shape(_inp)[0], tf.float32)
    (H, W, B) = tuple((int(i) for i in _inp.shape[1:4]))
    h_states = np.empty((H, W, B), dtype=np.object)
    w_states = np.empty((H, W, B), dtype=np.object)
    b_states = np.empty((H, W, B), dtype=np.object)
    for h in range(H):
        for w in range(W):
            for b in range(B):
                h_state = (h_states[((h - 1), w, b)] if (h > 0) else edge_state)
                w_state = (w_states[(h, (w - 1), b)] if (w > 0) else edge_state)
                b_state = (b_states[(h, w, (b - 1))] if (b > 0) else edge_state)
                inp = _inp[(:, h, w, b, :)]
                h_inp = tf.concat([inp, w_state.h, b_state.h], axis=1)
                (_, h_states[(h, w, b)]) = self.h_cell(h_inp, h_state)
                w_inp = tf.concat([inp, h_state.h, b_state.h], axis=1)
                (_, w_states[(h, w, b)]) = self.w_cell(w_inp, w_state)
                b_inp = tf.concat([inp, h_state.h, w_state.h], axis=1)
                (_, b_states[(h, w, b)]) = self.b_cell(b_inp, b_state)
    if (self.output_network is None):
        self.output_network = cfg.build_math_output(scope='math_output')
    final_layer_input = tf.concat([h_states[((- 1), (- 1), (- 1))].h, w_states[((- 1), (- 1), (- 1))].h, b_states[((- 1), (- 1), (- 1))].h], axis=1)
    return self.output_network(final_layer_input, output_size, is_training)
