import tf_utils
import tensorflow as tf


def transformAttention(X, STE_P, STE_Q, K, d, bn, bn_decay, is_training):
    '\n    transform attention mechanism\n    X:      [batch_size, P, N, D]\n    STE_P:  [batch_size, P, N, D]\n    STE_Q:  [batch_size, Q, N, D]\n    K:      number of attention heads\n    d:      dimension of each attention outputs\n    return: [batch_size, Q, N, D]\n    '
    D = (K * d)
    query = FC(STE_Q, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    key = FC(STE_P, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    value = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    query = tf.concat(tf.split(query, K, axis=(- 1)), axis=0)
    key = tf.concat(tf.split(key, K, axis=(- 1)), axis=0)
    value = tf.concat(tf.split(value, K, axis=(- 1)), axis=0)
    query = tf.transpose(query, perm=(0, 2, 1, 3))
    key = tf.transpose(key, perm=(0, 2, 3, 1))
    value = tf.transpose(value, perm=(0, 2, 1, 3))
    attention = tf.matmul(query, key)
    attention /= (d ** 0.5)
    attention = tf.nn.softmax(attention, axis=(- 1))
    X = tf.matmul(attention, value)
    X = tf.transpose(X, perm=(0, 2, 1, 3))
    X = tf.concat(tf.split(X, K, axis=0), axis=(- 1))
    X = FC(X, units=[D, D], activations=[tf.nn.relu, None], bn=bn, bn_decay=bn_decay, is_training=is_training)
    return X
