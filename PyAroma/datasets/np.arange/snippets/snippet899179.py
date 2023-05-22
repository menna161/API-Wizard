from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf


def scatter_by_anchor_indices(anchor_indices, data, index_shift):
    'Shift data such that it is indexed relative to anchor_indices.\n\n  For each row of the data array, we flip it horizontally and then shift it\n  so that the output at (anchor_index + index_shift) is the leftmost column\n  of the input. Namely:\n\n  output[i][j] = data[i][anchor_indices[i] - j + index_shift]\n\n  Args:\n    anchor_indices: [batch_size] int Tensor or np array\n    data: [batch_size, num_columns]: float Tensor or np array\n    index_shift: int\n  Returns:\n    [batch_size, num_columns] Tensor\n  '
    anchor_indices = tf.convert_to_tensor(anchor_indices)
    data = tf.convert_to_tensor(data)
    num_data_columns = data.shape[(- 1)].value
    indices = np.arange(num_data_columns)[(np.newaxis, ...)]
    shifted_indices = ((anchor_indices[(..., tf.newaxis)] - indices) + index_shift)
    valid_indices = (shifted_indices >= 0)
    batch_size = tf.shape(data)[0]
    batch_indices = tf.tile(tf.range(batch_size)[(..., tf.newaxis)], [1, num_data_columns])
    shifted_indices += (batch_indices * num_data_columns)
    shifted_indices = tf.reshape(shifted_indices, [(- 1)])
    num_elements = (tf.shape(data)[0] * tf.shape(data)[1])
    row_indices = tf.range(num_elements)
    stacked_indices = tf.stack([row_indices, shifted_indices], axis=1)
    lower_batch_boundaries = tf.reshape((batch_indices * num_data_columns), [(- 1)])
    upper_batch_boundaries = tf.reshape(((batch_indices + 1) * num_data_columns), [(- 1)])
    valid_indices = tf.logical_and((shifted_indices >= lower_batch_boundaries), (shifted_indices < upper_batch_boundaries))
    stacked_indices = tf.boolean_mask(stacked_indices, valid_indices)
    dense_shape = tf.cast(tf.tile(num_elements[(..., tf.newaxis)], [2]), tf.int64)
    scattering_matrix = tf.SparseTensor(indices=tf.cast(stacked_indices, tf.int64), values=tf.ones_like(stacked_indices[(:, 0)], dtype=data.dtype), dense_shape=dense_shape)
    flattened_data = tf.reshape(data, [(- 1)])[(..., tf.newaxis)]
    flattened_output = tf.sparse_tensor_dense_matmul(scattering_matrix, flattened_data, adjoint_a=False, adjoint_b=False, name=None)
    return tf.reshape(tf.transpose(flattened_output, [0, 1]), [(- 1), num_data_columns])
