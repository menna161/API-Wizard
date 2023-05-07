from nets.model_helper import *
import numpy as np
import math


def anti_aliased_downsample(inp, data_format='channels_first', filt_size=3, stride=2, name=None, pad_off=0):
    pading_size = int(((1.0 * (filt_size - 1)) / 2))
    if (data_format == 'channels_first'):
        pad_sizes = [[0, 0], [0, 0], [(pading_size + pad_off), (pading_size + pad_off)], [(pading_size + pad_off), (pading_size + pad_off)]]
    else:
        pad_sizes = [[0, 0], [(pading_size + pad_off), (pading_size + pad_off)], [(pading_size + pad_off), (pading_size + pad_off)], [0, 0]]
    if (filt_size == 1):
        a = np.array([1.0])
    elif (filt_size == 2):
        a = np.array([1.0, 1.0])
    elif (filt_size == 3):
        a = np.array([1.0, 2.0, 1.0])
    elif (filt_size == 4):
        a = np.array([1.0, 3.0, 3.0, 1.0])
    elif (filt_size == 5):
        a = np.array([1.0, 4.0, 6.0, 4.0, 1.0])
    elif (filt_size == 6):
        a = np.array([1.0, 5.0, 10.0, 10.0, 5.0, 1.0])
    elif (filt_size == 7):
        a = np.array([1.0, 6.0, 15.0, 20.0, 15.0, 6.0, 1.0])
    channel_axis = (1 if (data_format == 'channels_first') else 3)
    G = inp.shape[channel_axis]
    filt = tf.constant((a[(:, None)] * a[(None, :)]), inp.dtype)
    filt = (filt / tf.reduce_sum(filt))
    filt = tf.reshape(filt, [filt_size, filt_size, 1, 1])
    filt = tf.tile(filt, [1, 1, 1, G])
    if (filt_size == 1):
        if (pad_off == 0):
            return inp[(:, :, ::stride, ::stride)]
        else:
            padded = tf.pad(inp, pad_sizes, 'REFLECT')
            return padded[(:, :, ::stride, ::stride)]
    else:
        inp = tf.pad(inp, pad_sizes, 'REFLECT')
        data_format = ('NCHW' if (data_format == 'channels_first') else 'NHWC')
        strides = ([1, 1, stride, stride] if (data_format == 'NCHW') else [1, stride, stride, 1])
        with tf.variable_scope(name, 'anti_alias', [inp]) as name:
            try:
                output = tf.nn.conv2d(inp, filt, strides=strides, padding='VALID', data_format=data_format)
            except:
                tf.logging.info('Group conv by looping')
                inp = tf.split(inp, G, axis=channel_axis)
                filters = tf.split(filt, G, axis=3)
                output = tf.concat([tf.nn.conv2d(i, f, strides=strides, padding='VALID', data_format=data_format) for (i, f) in zip(inp, filters)], axis=(1 if (data_format == 'NCHW') else 3))
        return output
