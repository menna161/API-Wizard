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


def build_math(self):
    if (self.math_input_network is None):
        self.math_input_network = cfg.build_math_input(scope='math_input_network')
        if ('math' in self.fixed_weights):
            self.math_input_network.fix_variables()
    if (self.math_network is None):
        self.math_network = cfg.build_math_network(scope='math_network')
        if ('math' in self.fixed_weights):
            self.math_network.fix_variables()
    (math_rep, mask) = self.build_math_representation()
    if (self.max_possible_objects is not None):
        (math_rep, _, mask) = apply_mask_and_group_at_front(math_rep, mask)
        n_pad = (self.max_possible_objects - tf.shape(math_rep)[1])
        mask = tf.cast(mask, tf.float32)
        batch_size = tf.shape(math_rep)[0]
        A = math_rep.shape[2]
        math_rep = tf.pad(math_rep, [(0, 0), (0, n_pad), (0, 0)])
        math_rep = tf.reshape(math_rep, (batch_size, self.max_possible_objects, A))
        mask = tf.pad(mask, [(0, 0), (0, n_pad)])
        mask = tf.reshape(mask, (batch_size, self.max_possible_objects, 1))
    mask_shape = tf.concat([tf.shape(math_rep)[:(- 1)], [1]], axis=0)
    mask = tf.reshape(mask, mask_shape)
    math_rep = tf.concat([mask, math_rep], axis=(- 1))
    logits = self.math_network(math_rep, cfg.n_classes, self.is_training)
    self._tensors['prediction'] = tf.nn.softmax(logits)
    recorded_tensors = self.recorded_tensors
    if (self.math_weight is not None):
        self.record_tensors(raw_loss_math=tf.nn.softmax_cross_entropy_with_logits_v2(labels=self._tensors['targets'], logits=logits))
        self.losses['math'] = (self.math_weight * recorded_tensors['raw_loss_math'])
    self.record_tensors(math_accuracy=tf.equal(tf.argmax(logits, axis=1), tf.argmax(self._tensors['targets'], axis=1)), math_1norm=tf.abs((tf.argmax(logits, axis=1) - tf.argmax(self._tensors['targets'], axis=1))), math_correct_prob=tf.reduce_sum((tf.nn.softmax(logits) * self._tensors['targets']), axis=1))
