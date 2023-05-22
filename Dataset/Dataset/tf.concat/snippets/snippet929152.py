from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow_probability import distributions as tfd
from dreamer import tools
from dreamer.models import base


def _transition(self, prev_state, prev_action, zero_obs):
    hidden = tf.concat([prev_state['sample'], prev_action], (- 1))
    for _ in range(self._num_layers):
        hidden = tf.layers.dense(hidden, **self._kwargs)
    (belief, rnn_state) = self._cell(hidden, prev_state['rnn_state'])
    if self._future_rnn:
        hidden = belief
    for _ in range(self._num_layers):
        hidden = tf.layers.dense(hidden, **self._kwargs)
    mean = tf.layers.dense(hidden, self._state_size, None)
    stddev = tf.layers.dense(hidden, self._state_size, tf.nn.softplus)
    stddev += self._min_stddev
    if self._mean_only:
        sample = mean
    else:
        sample = tfd.MultivariateNormalDiag(mean, stddev).sample()
    return {'mean': mean, 'stddev': stddev, 'sample': sample, 'belief': belief, 'rnn_state': rnn_state}
