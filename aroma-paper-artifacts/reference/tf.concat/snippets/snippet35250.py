import tf_utils
import tensorflow as tf


def STEmbedding(SE, TE, T, D, bn, bn_decay, is_training):
    '\n    spatio-temporal embedding\n    SE:     [N, D]\n    TE:     [batch_size, P + Q, 2] (dayofweek, timeofday)\n    T:      num of time steps in one day\n    D:      output dims\n    retrun: [batch_size, P + Q, N, D]\n    '
    SE = tf.expand_dims(tf.expand_dims(SE, axis=0), axis=0)
    SE = FC(SE, units=[D, D], activations=[tf.nn.relu, None], bn=bn, bn_decay=bn_decay, is_training=is_training)
    dayofweek = tf.one_hot(TE[(..., 0)], depth=7)
    timeofday = tf.one_hot(TE[(..., 1)], depth=T)
    TE = tf.concat((dayofweek, timeofday), axis=(- 1))
    TE = tf.expand_dims(TE, axis=2)
    TE = FC(TE, units=[D, D], activations=[tf.nn.relu, None], bn=bn, bn_decay=bn_decay, is_training=is_training)
    return tf.add(SE, TE)
