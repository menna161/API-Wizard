import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def _call(self, inp, output_size, is_training):
    mod = (int(inp.shape[1]) % self.pixels_per_cell[0])
    bottom_padding = ((self.pixels_per_cell[0] - mod) if (mod > 0) else 0)
    padding_h = int(np.ceil((self.max_object_shape[0] / 2)))
    mod = (int(inp.shape[2]) % self.pixels_per_cell[1])
    right_padding = ((self.pixels_per_cell[1] - mod) if (mod > 0) else 0)
    padding_w = int(np.ceil((self.max_object_shape[1] / 2)))
    padding = [[0, 0], [padding_h, (bottom_padding + padding_h)], [padding_w, (right_padding + padding_w)], [0, 0]]
    inp = tf.pad(inp, padding)
    return super(NewBackbone, self)._call(inp, output_size, is_training)
