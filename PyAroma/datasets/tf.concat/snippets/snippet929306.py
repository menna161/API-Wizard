from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import numpy as np
import tensorflow as tf
from dreamer.tools import nested
from dreamer.tools import shape


def _merge_dims(tensor, dims):
    if isinstance(tensor, (list, tuple, dict)):
        return nested.map(tensor, (lambda x: _merge_dims(x, dims)))
    tensor = tf.convert_to_tensor(tensor)
    if ((np.array(dims) - min(dims)) != np.arange(len(dims))).all():
        raise ValueError('Dimensions to merge must all follow each other.')
    (start, end) = (dims[0], dims[(- 1)])
    output = tf.reshape(tensor, tf.concat([tf.shape(tensor)[:start], [tf.reduce_prod(tf.shape(tensor)[start:(end + 1)])], tf.shape(tensor)[(end + 1):]], axis=0))
    merged = tensor.shape[start:(end + 1)].as_list()
    output.set_shape(((tensor.shape[:start].as_list() + [(None if (None in merged) else np.prod(merged))]) + tensor.shape[(end + 1):].as_list()))
    return output
