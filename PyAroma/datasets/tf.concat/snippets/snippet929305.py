from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import numpy as np
import tensorflow as tf
from dreamer.tools import nested
from dreamer.tools import shape


def overshooting(cell, target, embedded, prev_action, length, amount, posterior=None, ignore_input=False):
    if (posterior is None):
        use_obs = tf.ones(tf.shape(nested.flatten(embedded)[0][(:, :, :1)])[:3], tf.bool)
        use_obs = tf.cond(tf.convert_to_tensor(ignore_input), (lambda : tf.zeros_like(use_obs, tf.bool)), (lambda : use_obs))
        ((_, posterior), _) = tf.nn.dynamic_rnn(cell, (embedded, prev_action, use_obs), length, dtype=tf.float32, swap_memory=True)
    max_length = shape.shape(nested.flatten(embedded)[0])[1]
    first_output = {'prev_action': prev_action, 'posterior': posterior, 'target': target, 'mask': tf.sequence_mask(length, max_length, tf.int32)}
    progress_fn = (lambda tensor: tf.concat([tensor[(:, 1:)], (0 * tensor[(:, :1)])], 1))
    other_outputs = tf.scan((lambda past_output, _: nested.map(progress_fn, past_output)), tf.range(amount), first_output)
    sequences = nested.map((lambda lhs, rhs: tf.concat([lhs[None], rhs], 0)), first_output, other_outputs)
    sequences = nested.map((lambda tensor: _merge_dims(tensor, [1, 2])), sequences)
    sequences = nested.map((lambda tensor: tf.transpose(tensor, ([1, 0] + list(range(2, tensor.shape.ndims))))), sequences)
    merged_length = tf.reduce_sum(sequences['mask'], 1)
    sequences = nested.map((lambda tensor: (tensor * tf.cast(_pad_dims(sequences['mask'], tensor.shape.ndims), tensor.dtype))), sequences)
    use_obs = tf.zeros(tf.shape(sequences['mask']), tf.bool)[(..., None)]
    embed_size = nested.flatten(embedded)[0].shape[2].value
    obs = tf.zeros((shape.shape(sequences['mask']) + [embed_size]))
    prev_state = nested.map((lambda tensor: tf.concat([(0 * tensor[(:, :1)]), tensor[(:, :(- 1))]], 1)), posterior)
    prev_state = nested.map((lambda tensor: _merge_dims(tensor, [0, 1])), prev_state)
    ((priors, _), _) = tf.nn.dynamic_rnn(cell, (obs, sequences['prev_action'], use_obs), merged_length, prev_state)
    (target, prior, posterior, mask) = nested.map(functools.partial(_restore_batch_dim, batch_size=shape.shape(length)[0]), (sequences['target'], priors, sequences['posterior'], sequences['mask']))
    mask = tf.cast(mask, tf.bool)
    return (target, prior, posterior, mask)
