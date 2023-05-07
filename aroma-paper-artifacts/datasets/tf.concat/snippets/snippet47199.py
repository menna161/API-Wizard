import tensorflow as tf
import numpy as np
import collections
from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt
from matplotlib import animation
from dps import cfg
from dps.utils import Param, square_subplots
from dps.utils.tf import build_gradient_train_op, apply_mask_and_group_at_front, build_scheduled_value, FIXED_COLLECTION
from dps.tf.updater import DataManager, Evaluator, TensorRecorder, VideoUpdater as _VideoUpdater
from dps.train import Hook


def build_math_representation(self):
    attr_shape = tf.shape(self._tensors['attr'])
    attr = tf.reshape(self._tensors['attr'], ((- 1), self.A))
    math_A = (self.A if (self.math_A is None) else self.math_A)
    math_attr = self.math_input_network(attr, math_A, self.is_training)
    new_shape = tf.concat([attr_shape[:(- 1)], [math_A]], axis=0)
    math_attr = tf.reshape(math_attr, new_shape)
    self._tensors['math_attr'] = math_attr
    return (math_attr, self._tensors['obj'])
