from nets.model_helper import *
import numpy as np
import math


def dropblock(x, keep_prob, block_size, gamma_scale=1.0, seed=None, name=None, data_format='channels_last', is_training=True):
    "\n  Dropblock layer. For more details, refer to https://arxiv.org/abs/1810.12890\n  :param x: A floating point tensor.\n  :param keep_prob: A scalar Tensor with the same type as x. The probability that each element is kept.\n  :param block_size: The block size to drop\n  :param gamma_scale: The multiplier to gamma.\n  :param seed:  Python integer. Used to create random seeds.\n  :param name: A name for this operation (optional)\n  :param data_format: 'channels_last' or 'channels_first'\n  :param is_training: If False, do nothing.\n  :return: A Tensor of the same shape of x.\n  "
    if (not is_training):
        return x
    if ((isinstance(keep_prob, float) and (keep_prob == 1)) or (gamma_scale == 0)):
        return x
    with tf.name_scope(name, 'dropblock', [x]) as name:
        if (not x.dtype.is_floating):
            raise ValueError(("x has to be a floating point tensor since it's going to be scaled. Got a %s tensor instead." % x.dtype))
        if (isinstance(keep_prob, float) and (not (0 < keep_prob <= 1))):
            raise ValueError(('keep_prob must be a scalar tensor or a float in the range (0, 1], got %g' % keep_prob))
        br = ((block_size - 1) // 2)
        tl = ((block_size - 1) - br)
        if (data_format == 'channels_last'):
            (_, h, w, c) = x.shape.as_list()
            sampling_mask_shape = tf.stack([1, ((h - block_size) + 1), ((w - block_size) + 1), c])
            pad_shape = [[0, 0], [tl, br], [tl, br], [0, 0]]
        elif (data_format == 'channels_first'):
            (_, c, h, w) = x.shape.as_list()
            sampling_mask_shape = tf.stack([1, c, ((h - block_size) + 1), ((w - block_size) + 1)])
            pad_shape = [[0, 0], [0, 0], [tl, br], [tl, br]]
        else:
            raise NotImplementedError
        gamma = ((((1.0 - keep_prob) * (w * h)) / (block_size ** 2)) / (((w - block_size) + 1) * ((h - block_size) + 1)))
        gamma = (gamma_scale * gamma)
        mask = _bernoulli(sampling_mask_shape, gamma, seed, tf.float32)
        mask = tf.pad(mask, pad_shape)
        xdtype_mask = tf.cast(mask, x.dtype)
        xdtype_mask = tf.layers.max_pooling2d(inputs=xdtype_mask, pool_size=block_size, strides=1, padding='SAME', data_format=data_format)
        xdtype_mask = (1 - xdtype_mask)
        fp32_mask = tf.cast(xdtype_mask, tf.float32)
        ret = tf.multiply(x, xdtype_mask)
        float32_mask_size = tf.cast(tf.size(fp32_mask), tf.float32)
        float32_mask_reduce_sum = tf.reduce_sum(fp32_mask)
        normalize_factor = tf.cast((float32_mask_size / (float32_mask_reduce_sum + 1e-08)), x.dtype)
        ret = (ret * normalize_factor)
        return ret
