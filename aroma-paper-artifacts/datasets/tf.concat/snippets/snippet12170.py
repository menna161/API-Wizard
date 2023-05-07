import numpy as np
import tensorflow as tf
from .utils import *
from itertools import product


def mclahe(x, kernel_size=None, n_bins=128, clip_limit=0.01, adaptive_hist_range=False, use_gpu=True):
    '\n    Contrast limited adaptive histogram equalization implemented in tensorflow\n    :param x: numpy array to which clahe is applied\n    :param kernel_size: tuple of kernel sizes, 1/8 of dimension lengths of x if None\n    :param n_bins: number of bins to be used in the histogram\n    :param clip_limit: relative intensity limit to be ignored in the histogram equalization\n    :param adaptive_hist_range: flag, if true individual range for histogram computation of each block is used\n    :param use_gpu: Flag, if true gpu is used for computations if available\n    :return: numpy array to which clahe was applied, scaled on interval [0, 1]\n    '
    if (kernel_size is None):
        kernel_size = tuple(((s // 8) for s in x.shape))
    kernel_size = np.array(kernel_size)
    assert (len(kernel_size) == len(x.shape))
    dim = len(x.shape)
    x_min = np.min(x)
    x_max = np.max(x)
    x = ((x - x_min) / (x_max - x_min))
    x_shape = np.array(x.shape)
    padding_x_length = ((kernel_size - 1) - ((x_shape - 1) % kernel_size))
    padding_x = np.column_stack((((padding_x_length + 1) // 2), (padding_x_length // 2)))
    padding_hist = (np.column_stack(((kernel_size // 2), ((kernel_size + 1) // 2))) + padding_x)
    x_hist_padded = np.pad(x, padding_hist, 'symmetric')
    with tf.variable_scope('clahe') as scope:
        tf_x_hist_padded_init = tf.placeholder(tf.float32, shape=x_hist_padded.shape)
        tf_x_hist_padded = tf.Variable(tf_x_hist_padded_init)
        tf_x_padded = tf.slice(tf_x_hist_padded, (kernel_size // 2), (x_shape + padding_x_length))
        n_blocks = np.ceil((np.array(x.shape) / kernel_size)).astype(np.int32)
        new_shape = np.reshape(np.column_stack((n_blocks, kernel_size)), ((2 * dim),))
        perm = (tuple(((2 * i) for i in range(dim))) + tuple((((2 * i) + 1) for i in range(dim))))
        tf_x_block = tf.transpose(tf.reshape(tf_x_padded, new_shape), perm=perm)
        shape_x_block = np.concatenate((n_blocks, kernel_size))
        n_blocks_hist = (n_blocks + np.ones(dim, dtype=np.int32))
        new_shape = np.reshape(np.column_stack((n_blocks_hist, kernel_size)), ((2 * dim),))
        perm = (tuple(((2 * i) for i in range(dim))) + tuple((((2 * i) + 1) for i in range(dim))))
        tf_x_hist = tf.transpose(tf.reshape(tf_x_hist_padded, new_shape), perm=perm)
        if adaptive_hist_range:
            hist_ex_shape = np.concatenate((n_blocks_hist, ([1] * dim)))
            tf_x_hist_ex_init = tf.placeholder(tf.float32, shape=n_blocks_hist)
            tf_x_hist_min = tf.Variable(tf_x_hist_ex_init, dtype=tf.float32)
            tf_x_hist_max = tf.reduce_max(tf_x_hist, np.arange((- dim), 0))
            tf_x_hist_norm = tf.Variable(tf_x_hist_ex_init, dtype=tf.float32)
            tf_get_hist_min = tf.assign(tf_x_hist_min, tf.reduce_min(tf_x_hist, np.arange((- dim), 0)))
            tf_get_hist_norm = tf.assign(tf_x_hist_norm, tf.where(tf.equal(tf_x_hist_min, tf_x_hist_max), tf.ones_like(tf_x_hist_min), (tf_x_hist_max - tf_x_hist_min)))
            tf_x_hist_scaled = ((tf_x_hist - tf.reshape(tf_x_hist_min, hist_ex_shape)) / tf.reshape(tf_x_hist_norm, hist_ex_shape))
        else:
            tf_x_hist_scaled = tf_x_hist
        tf_hist = tf.cast(tf_batch_histogram(tf_x_hist_scaled, [0.0, 1.0], dim, nbins=n_bins), tf.float32)
        tf_n_to_high = tf.reduce_sum(tf.nn.relu((tf_hist - (np.prod(kernel_size) * clip_limit))), (- 1), keepdims=True)
        tf_hist_clipped = (tf.minimum(tf_hist, (np.prod(kernel_size) * clip_limit)) + (tf_n_to_high / n_bins))
        tf_cdf = tf.cumsum(tf_hist_clipped, (- 1))
        tf_cdf_slice_size = tf.constant(np.concatenate((n_blocks_hist, [1])), tf.int32)
        tf_cdf_min = tf.slice(tf_cdf, tf.constant(([0] * (dim + 1)), dtype=tf.int32), tf_cdf_slice_size)
        tf_cdf_max = tf.slice(tf_cdf, tf.constant((([0] * dim) + [(n_bins - 1)]), dtype=tf.int32), tf_cdf_slice_size)
        tf_cdf_norm = tf.where(tf.equal(tf_cdf_min, tf_cdf_max), tf.ones_like(tf_cdf_max), (tf_cdf_max - tf_cdf_min))
        tf_mapping = ((tf_cdf - tf_cdf_min) / tf_cdf_norm)
        map_shape = np.concatenate((n_blocks_hist, [n_bins]))
        tf_map_init = tf.placeholder(tf.float32, shape=map_shape)
        tf_map = tf.Variable(tf_map_init, dtype=tf.float32)
        tf_get_map = tf.assign(tf_map, tf_mapping)
        tf_x_block_init = tf.placeholder(tf.float32, shape=shape_x_block)
        tf_slice_begin = tf.placeholder(tf.int32, shape=(dim,))
        tf_map_slice_begin = tf.concat([tf_slice_begin, [0]], 0)
        tf_map_slice_size = tf.constant(np.concatenate((n_blocks, [n_bins])), dtype=tf.int32)
        tf_map_slice = tf.slice(tf_map, tf_map_slice_begin, tf_map_slice_size)
        if adaptive_hist_range:
            tf_hist_norm_slice_shape = np.concatenate((n_blocks, ([1] * dim)))
            tf_x_hist_min_sub = tf.slice(tf_x_hist_min, tf_slice_begin, n_blocks)
            tf_x_hist_norm_sub = tf.slice(tf_x_hist_norm, tf_slice_begin, n_blocks)
            tf_x_block_scaled = ((tf_x_block - tf.reshape(tf_x_hist_min_sub, tf_hist_norm_slice_shape)) / tf.reshape(tf_x_hist_norm_sub, tf_hist_norm_slice_shape))
            tf_bin = tf.histogram_fixed_width_bins(tf_x_block_scaled, [0.0, 1.0], nbins=n_bins)
        else:
            tf_bin = tf.Variable(tf.cast(tf_x_block_init, tf.int32), dtype=tf.int32)
            tf_get_bin = tf.assign(tf_bin, tf.histogram_fixed_width_bins(tf_x_block, [0.0, 1.0], nbins=n_bins))
        tf_mapped_sub = tf_batch_gather(tf_map_slice, tf_bin, dim)
        tf_coeff = tf.placeholder(tf.float32)
        tf_res_sub = tf.Variable(tf_x_block_init, dtype=tf.float32)
        tf_apply_map = tf.assign(tf_res_sub, tf_mapped_sub)
        tf_apply_coeff = tf.assign(tf_res_sub, (tf_coeff * tf_res_sub))
        tf_res = tf.Variable(tf_x_block_init, dtype=tf.float32)
        tf_update_res = tf.assign_add(tf_res, tf_res_sub)
        (tf_res_min, tf_res_max) = (tf.reduce_min(tf_res), tf.reduce_max(tf_res))
        tf_res_norm = ((tf_res - tf_res_min) / (tf_res_max - tf_res_min))
        tf_rescale = tf.assign(tf_res, tf_res_norm)
        new_shape = tuple(((axis, (axis + dim)) for axis in range(dim)))
        new_shape = tuple((j for i in new_shape for j in i))
        tf_res_transposed = tf.transpose(tf_res, new_shape)
        tf_res_reshaped = tf.reshape(tf_res_transposed, tuple(((n_blocks[axis] * kernel_size[axis]) for axis in range(dim))))
        tf_res_cropped = tf.slice(tf_res_reshaped, padding_x[(:, 0)], x.shape)
        if use_gpu:
            config = None
        else:
            config = tf.ConfigProto(device_count={'GPU': 0})
        with tf.Session(config=config) as sess:
            map_init = np.zeros(map_shape, dtype=np.float32)
            x_block_init = np.zeros(shape_x_block, dtype=np.float32)
            if adaptive_hist_range:
                x_hist_ex_init = np.zeros(n_blocks_hist, dtype=np.float32)
                tf_var_init = tf.initializers.variables([tf_x_hist_padded, tf_map, tf_res, tf_res_sub, tf_x_hist_min, tf_x_hist_norm])
                sess.run(tf_var_init, feed_dict={tf_x_hist_padded_init: x_hist_padded, tf_map_init: map_init, tf_x_block_init: x_block_init, tf_x_hist_ex_init: x_hist_ex_init})
            else:
                tf_var_init = tf.initializers.variables([tf_x_hist_padded, tf_map, tf_bin, tf_res, tf_res_sub])
                sess.run(tf_var_init, feed_dict={tf_x_hist_padded_init: x_hist_padded, tf_map_init: map_init, tf_x_block_init: x_block_init})
            if adaptive_hist_range:
                sess.run(tf_get_hist_min)
                sess.run(tf_get_hist_norm)
            sess.run(tf_get_map)
            if (not adaptive_hist_range):
                sess.run(tf_get_bin)
            inds = [list(i) for i in product([0, 1], repeat=dim)]
            for ind_map in inds:
                sess.run(tf_apply_map, feed_dict={tf_slice_begin: ind_map})
                for axis in range(dim):
                    coeff = (np.arange(kernel_size[axis], dtype=np.float32) / kernel_size[axis])
                    if ((kernel_size[axis] % 2) == 0):
                        coeff = ((0.5 / kernel_size[axis]) + coeff)
                    if (ind_map[axis] == 0):
                        coeff = (1.0 - coeff)
                    new_shape = ((([1] * (dim + axis)) + [kernel_size[axis]]) + ([1] * ((dim - 1) - axis)))
                    coeff = np.reshape(coeff, new_shape)
                    sess.run(tf_apply_coeff, feed_dict={tf_coeff: coeff})
                sess.run(tf_update_res)
            sess.run(tf_rescale)
            result = sess.run(tf_res_cropped)
    return result
