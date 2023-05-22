from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow as tf
from thumt.layers.nn import linear


def additive_attention(queries, keys, values, bias, hidden_size, concat=False, keep_prob=None, dtype=None, scope=None):
    " Additive attention mechanism. This layer is implemented using a\n        one layer feed forward neural network\n\n    :param queries: A tensor with shape [batch, heads, length_q, depth_k]\n    :param keys: A tensor with shape [batch, heads, length_kv, depth_k]\n    :param values: A tensor with shape [batch, heads, length_kv, depth_v]\n    :param bias: A tensor\n    :param hidden_size: An integer\n    :param concat: A boolean value. If ``concat'' is set to True, then\n        the computation of attention mechanism is following $tanh(W[q, k])$.\n        When ``concat'' is set to False, the computation is following\n        $tanh(Wq + Vk)$\n    :param keep_prob: a scalar in [0, 1]\n    :param dtype: An optional instance of tf.DType\n    :param scope: An optional string, the scope of this layer\n\n    :returns: A dict with the following keys:\n        weights: A tensor with shape [batch, length_q]\n        outputs: A tensor with shape [batch, length_q, depth_v]\n    "
    with tf.variable_scope(scope, default_name='additive_attention', values=[queries, keys, values, bias], dtype=dtype):
        length_q = tf.shape(queries)[2]
        length_kv = tf.shape(keys)[2]
        q = tf.tile(tf.expand_dims(queries, 3), [1, 1, 1, length_kv, 1])
        k = tf.tile(tf.expand_dims(keys, 2), [1, 1, length_q, 1, 1])
        if concat:
            combined = tf.tanh(linear(tf.concat([q, k], axis=(- 1)), hidden_size, True, True, name='qk_transform'))
        else:
            q = linear(queries, hidden_size, True, True, name='q_transform')
            k = linear(keys, hidden_size, True, True, name='key_transform')
            combined = tf.tanh((q + k))
        logits = tf.squeeze(linear(combined, 1, True, True, name='logits'), axis=(- 1))
        if (bias is not None):
            logits += bias
        weights = tf.nn.softmax(logits, name='attention_weights')
        if (keep_prob or (keep_prob < 1.0)):
            weights = tf.nn.dropout(weights, keep_prob)
        outputs = tf.matmul(weights, values)
        return {'weights': weights, 'outputs': outputs}
