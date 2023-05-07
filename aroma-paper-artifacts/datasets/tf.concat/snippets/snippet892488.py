from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow as tf
from thumt.layers.nn import linear


def multihead_attention(queries, memories, bias, num_heads, key_size, value_size, output_size, keep_prob=None, output=True, state=None, dtype=None, scope=None, trainable=True):
    ' Multi-head scaled-dot-product attention with input/output\n        transformations.\n\n    :param queries: A tensor with shape [batch, length_q, depth_q]\n    :param memories: A tensor with shape [batch, length_m, depth_m]\n    :param bias: A tensor (see attention_bias)\n    :param num_heads: An integer dividing key_size and value_size\n    :param key_size: An integer\n    :param value_size: An integer\n    :param output_size: An integer\n    :param keep_prob: A floating point number in (0, 1]\n    :param output: Whether to use output transformation\n    :param state: An optional dictionary used for incremental decoding\n    :param dtype: An optional instance of tf.DType\n    :param scope: An optional string\n\n    :returns: A dict with the following keys:\n        weights: A tensor with shape [batch, heads, length_q, length_kv]\n        outputs: A tensor with shape [batch, length_q, depth_v]\n    '
    if ((key_size % num_heads) != 0):
        raise ValueError(('Key size (%d) must be divisible by the number of attention heads (%d).' % (key_size, num_heads)))
    if ((value_size % num_heads) != 0):
        raise ValueError(('Value size (%d) must be divisible by the number of attention heads (%d).' % (value_size, num_heads)))
    with tf.variable_scope(scope, default_name='multihead_attention', values=[queries, memories], dtype=dtype):
        next_state = {}
        if (memories is None):
            size = ((key_size * 2) + value_size)
            combined = linear(queries, size, True, True, scope='qkv_transform', trainable=trainable)
            (q, k, v) = tf.split(combined, [key_size, key_size, value_size], axis=(- 1))
            if (state is not None):
                k = tf.concat([state['key'], k], axis=1)
                v = tf.concat([state['value'], v], axis=1)
                next_state['key'] = k
                next_state['value'] = v
        else:
            q = linear(queries, key_size, True, True, scope='q_transform', trainable=trainable)
            combined = linear(memories, (key_size + value_size), True, scope='kv_transform', trainable=trainable)
            (k, v) = tf.split(combined, [key_size, value_size], axis=(- 1))
        q = split_heads(q, num_heads)
        k = split_heads(k, num_heads)
        v = split_heads(v, num_heads)
        key_depth_per_head = (key_size // num_heads)
        q *= (key_depth_per_head ** (- 0.5))
        results = multiplicative_attention(q, k, v, bias, keep_prob)
        weights = results['weights']
        x = combine_heads(results['outputs'])
        if output:
            outputs = linear(x, output_size, True, True, scope='output_transform', trainable=trainable)
        else:
            outputs = x
        outputs = {'weights': weights, 'outputs': outputs}
        if (state is not None):
            outputs['state'] = next_state
        return outputs
