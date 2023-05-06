import tf_utils
import tensorflow as tf


def temporalAttention(X, STE, K, d, bn, bn_decay, is_training, mask=True):
    '\n    temporal attention mechanism\n    X:      [batch_size, num_step, N, D]\n    STE:    [batch_size, num_step, N, D]\n    K:      number of attention heads\n    d:      dimension of each attention outputs\n    return: [batch_size, num_step, N, D]\n    '
    D = (K * d)
    X = tf.concat((X, STE), axis=(- 1))
    query = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    key = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    value = FC(X, units=D, activations=tf.nn.relu, bn=bn, bn_decay=bn_decay, is_training=is_training)
    query = tf.concat(tf.split(query, K, axis=(- 1)), axis=0)
    key = tf.concat(tf.split(key, K, axis=(- 1)), axis=0)
    value = tf.concat(tf.split(value, K, axis=(- 1)), axis=0)
    query = tf.transpose(query, perm=(0, 2, 1, 3))
    key = tf.transpose(key, perm=(0, 2, 3, 1))
    value = tf.transpose(value, perm=(0, 2, 1, 3))
    attention = tf.matmul(query, key)
    attention /= (d ** 0.5)
    if mask:
        batch_size = tf.shape(X)[0]
        num_step = X.get_shape()[1].value
        N = X.get_shape()[2].value
        mask = tf.ones(shape=(num_step, num_step))
        mask = tf.linalg.LinearOperatorLowerTriangular(mask).to_dense()
        mask = tf.expand_dims(tf.expand_dims(mask, axis=0), axis=0)
        mask = tf.tile(mask, multiples=((K * batch_size), N, 1, 1))
        mask = tf.cast(mask, dtype=tf.bool)
        attention = tf.compat.v2.where(condition=mask, x=attention, y=((- (2 ** 15)) + 1))
    attention = tf.nn.softmax(attention, axis=(- 1))
    X = tf.matmul(attention, value)
    X = tf.transpose(X, perm=(0, 2, 1, 3))
    X = tf.concat(tf.split(X, K, axis=0), axis=(- 1))
    X = FC(X, units=[D, D], activations=[tf.nn.relu, None], bn=bn, bn_decay=bn_decay, is_training=is_training)
    return X
