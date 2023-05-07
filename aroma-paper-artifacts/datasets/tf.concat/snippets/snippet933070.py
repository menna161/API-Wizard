import tensorflow as tf


def minibatch_stddev(inputs, group_size=4):
    temp = inputs
    (b, h, w, c) = (inputs.shape[0], inputs.shape[1], inputs.shape[2], inputs.shape[3])
    inputs = tf.reshape(inputs, [group_size, (- 1), h, w, c])
    inputs = tf.sqrt((tf.reduce_mean(tf.square((inputs - tf.reduce_mean(inputs, axis=0, keep_dims=True))), axis=0) + EPSILON))
    inputs = tf.reduce_mean(inputs, axis=[1, 2, 3], keep_dims=True)
    inputs = tf.tile(inputs, multiples=[group_size, h, w, 1])
    inputs = tf.concat([temp, inputs], axis=(- 1))
    return inputs
