import tf_utils
import tensorflow as tf


def spatialAttention(X, STE, K, d, bn, bn_decay, is_training):
    '\n    spatial attention mechanism\n    X:      [batch_size, num_step, N, D]\n    STE:    [batch_size, num_step, N, D]\n    K:      number of attention heads\n    d:      dimension of each attention outputs\n    return: [batch_size, num_step, N, D]\n    '
    D = (K * d)
    X = tf.concat((X, STE), axis=(- 1))
    query = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    key = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    value = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    query = tf.concat(tf.split(query, K, axis=(- 1)), axis=0)
    key = tf.concat(tf.split(key, K, axis=(- 1)), axis=0)
    value = tf.concat(tf.split(value, K, axis=(- 1)), axis=0)
    attention = tf.matmul(query, key, transpose_b=True)
    attention /= (d ** 0.5)
    attention = tf.nn.softmax(attention, axis=(- 1))
    X = tf.matmul(attention, value)
    X = tf.concat(tf.split(X, K, axis=0), axis=(- 1))
    X = FC(X, units=[D, D], activations=[tf.nn.relu, None], bn=bn, bn_decay=bn_decay, is_training=is_training)
    return X
