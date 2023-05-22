import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_math_ops


def tf_batch_histogram(values, value_range, axis, nbins=100, dtype=tf.int32, use_map=True):
    '\n    Computes histogram with fixed width considering batch dimensions\n    :param values: Numeric `Tensor` containing the values for histogram computation.\n    :param value_range: Shape [2] `Tensor` of same `dtype` as `values`. values <= value_range[0] will be mapped to\n    hist[0], values >= value_range[1] will be mapped to hist[-1].\n    :param axis: Number of batch dimensions. First axis to apply histogram computation to.\n    :param nbins: Scalar `int32 Tensor`. Number of histogram bins.\n    :param dtype: dtype for returned histogram, can be either tf.int32 or tf.int64.\n    :return: histogram with batch dimensions.\n    '
    values_shape = tf.shape(values)
    batch_dim = values_shape[:axis]
    rest_dim = values_shape[axis:]
    num_batch = tf.reduce_prod(batch_dim)
    if use_map:
        values_reshaped = tf.reshape(values, tf.concat([[num_batch], rest_dim], 0))
        hist = tf.map_fn((lambda x: tf.histogram_fixed_width(x, value_range, nbins=nbins, dtype=dtype)), values_reshaped, dtype=dtype, parallel_iterations=64)
    else:
        values_float = tf.cast(values, tf.float32)
        value_range_float = tf.cast(value_range, tf.float32)
        values_norm = ((values_float - value_range_float[0]) / (value_range_float[1] - value_range_float[0]))
        values_clip1 = tf.maximum(values_norm, (0.5 / tf.cast(nbins, tf.float32)))
        values_clip2 = tf.minimum(values_clip1, (1.0 - (0.5 / tf.cast(nbins, tf.float32))))
        values_shift = (values_clip2 + tf.reshape(tf.range(tf.cast(num_batch, tf.float32), dtype=tf.float32), tf.concat([batch_dim, tf.ones(tf.size(rest_dim), tf.int32)], 0)))
        hist = tf.histogram_fixed_width(values_shift, [0.0, tf.cast(num_batch, tf.float32)], nbins=(num_batch * nbins), dtype=dtype)
    return tf.reshape(hist, tf.concat([batch_dim, [nbins]], 0))
