import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_math_ops


def tf_batch_gather(params, indices, axis, name=None):
    '\n    Extension of the batch_gather function in tensorflow\n    (see https://github.com/tensorflow/tensorflow/blob/r1.13/tensorflow/python/ops/array_ops.py\n    or https://www.tensorflow.org/api_docs/python/tf/batch_gather)\n    Gather slices from `params` according to `indices` with leading batch dims.\n    This operation assumes that the leading dimensions of `indices` are dense,\n    and the gathers on the axis corresponding to the last dimension of `indices`.\n    More concretely it computes:\n    `result[i1, ..., in, j1, ..., jm, k1, ...., kl] = params[i1, ..., in, indices[i1, ..., in, j1, ..., jm], k1, ..., kl]`\n    Therefore `params` should be a Tensor of shape [A1, ..., AN, C0, B1, ..., BM],\n    `indices` should be a Tensor of shape [A1, ..., AN, C1, ..., CK] and `result` will be\n    a Tensor of size `[A1, ..., AN, C1, ..., CK, B1, ..., BM]`.\n    In the case in which indices is a 1D tensor, this operation is equivalent to\n    `tf.gather`.\n    See also `tf.gather` and `tf.gather_nd`.\n    Args:\n      params: A `Tensor`. The tensor from which to gather values.\n      indices: A `Tensor`. Must be one of the following types: int32, int64. Index\n          tensor. Must be in range `[0, params.shape[axis]`, where `axis` is the\n          last dimension of `indices` itself.\n      axis: A `Tensor`. Must be one of the following types: int32, int64. The axis\n            in `params` to gather `indices` from.\n      name: A name for the operation (optional).\n    Returns:\n      A Tensor. Has the same type as `params`.\n    Raises:\n      ValueError: if `indices` has an unknown shape.\n    '
    with ops.name_scope(name):
        indices = ops.convert_to_tensor(indices, name='indices')
        params = ops.convert_to_tensor(params, name='params')
        indices_shape = tf.shape(indices)
        params_shape = tf.shape(params)
        ndims = indices.shape.ndims
        if (ndims is None):
            raise ValueError('batch_gather does not allow indices with unknown shape.')
        batch_indices = indices
        indices_dtype = indices.dtype.base_dtype
        accum_dim_value = tf.ones((), dtype=indices_dtype)
        casted_params_shape = gen_math_ops.cast(params_shape, indices_dtype)
        for dim in range(axis, 0, (- 1)):
            dim_value = casted_params_shape[(dim - 1)]
            accum_dim_value *= casted_params_shape[dim]
            start = tf.zeros((), dtype=indices_dtype)
            step = tf.ones((), dtype=indices_dtype)
            dim_indices = gen_math_ops._range(start, dim_value, step)
            dim_indices *= accum_dim_value
            dim_shape = tf.stack(((([1] * (dim - 1)) + [dim_value]) + ([1] * (ndims - dim))), axis=0)
            batch_indices += tf.reshape(dim_indices, dim_shape)
        flat_inner_shape_indices = gen_math_ops.prod(indices_shape[:(axis + 1)], [0], False)
        flat_indices = tf.reshape(batch_indices, tf.concat([[flat_inner_shape_indices], indices_shape[(axis + 1):]], axis=0))
        outer_shape = params_shape[(axis + 1):]
        flat_inner_shape_params = gen_math_ops.prod(params_shape[:(axis + 1)], [0], False)
        flat_params = tf.reshape(params, tf.concat([[flat_inner_shape_params], outer_shape], axis=0))
        flat_result = tf.gather(flat_params, flat_indices)
        result = tf.reshape(flat_result, tf.concat([indices_shape, outer_shape], axis=0))
        final_shape = indices.get_shape()[:axis].merge_with(params.get_shape()[:axis])
        final_shape = final_shape.concatenate(indices.get_shape()[axis:])
        final_shape = final_shape.concatenate(params.get_shape()[(axis + 1):])
        result.set_shape(final_shape)
        return result
