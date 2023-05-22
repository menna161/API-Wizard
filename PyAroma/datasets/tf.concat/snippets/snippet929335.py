from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from dreamer.tools import nested
from dreamer.tools import shape


def open_loop(cell, embedded, prev_action, context=1, debug=False):
    use_obs = tf.ones(tf.shape(embedded[(:, :context, :1)])[:3], tf.bool)
    ((_, closed_state), last_state) = tf.nn.dynamic_rnn(cell, (embedded[(:, :context)], prev_action[(:, :context)], use_obs), dtype=tf.float32)
    use_obs = tf.zeros(tf.shape(embedded[(:, context:, :1)])[:3], tf.bool)
    ((_, open_state), _) = tf.nn.dynamic_rnn(cell, ((0 * embedded[(:, context:)]), prev_action[(:, context:)], use_obs), initial_state=last_state)
    state = nested.map((lambda x, y: tf.concat([x, y], 1)), closed_state, open_state)
    if debug:
        with tf.control_dependencies([tf.assert_equal(tf.shape(nested.flatten(state)[0])[1], tf.shape(embedded)[1])]):
            state = nested.map(tf.identity, state)
    return state
