import math
import numpy as np
import os
import SimpleITK as sitk
import time
import functions.kernel.conv_kernel as conv_kernel
import functions.tf_utils as tfu
import tensorflow as tf
import tensorflow as tf
import tensorflow as tf
import matplotlib.pyplot as plt


def downsampler_gpu(input, down_scale, kernel_name='bspline', normalize_kernel=True, a=(- 0.5), default_pixel_value=0):
    '\n    Downsampling wiht GPU by an integer scale\n    :param input: can be a 2D or 3D numpy array or sitk image\n    :param down_scale: an integer value!\n    :param kernel_name:\n    :param normalize_kernel:\n    :param a:\n    :param default_pixel_value:\n    :return: output: can be a numpy array or sitk image based on the input\n    '
    import tensorflow as tf
    if isinstance(input, sitk.Image):
        input_numpy = sitk.GetArrayFromImage(input)
        mode = 'sitk'
    else:
        input_numpy = input
        mode = 'numpy'
    if (not isinstance(down_scale, int)):
        'type is:'
        print(type(down_scale))
        raise ValueError(('down_scale should be integer. now it is {} with type of '.format(down_scale) + type(down_scale)))
    kernelDimension = len(np.shape(input_numpy))
    input_numpy = np.expand_dims(input_numpy[np.newaxis], axis=(- 1))
    if (down_scale == 2):
        kernel_size = 7
    elif (down_scale == 4):
        kernel_size = 15
    else:
        raise ValueError('kernel_size is not defined for down_scale={}'.format(str(down_scale)))
    padSize = np.floor((kernel_size / 2)).astype(np.int)
    kenelStrides = tuple(([down_scale] * kernelDimension))
    tf.reset_default_graph()
    sess = tf.Session()
    x = tf.placeholder(tf.float32, shape=np.shape(input_numpy), name='InputImage')
    x_pad = tf.pad(x, ([0, 0], [padSize, padSize], [padSize, padSize], [padSize, padSize], [0, 0]), constant_values=default_pixel_value)
    convKernelGPU = conv_kernel.convDownsampleKernel(kernel_name, kernelDimension, kernel_size, normalizeKernel=normalize_kernel, a=a)
    convKernelGPU = np.expand_dims(convKernelGPU, (- 1))
    convKernelGPU = np.expand_dims(convKernelGPU, (- 1))
    convKernelGPU = tf.constant(convKernelGPU)
    y = tf.nn.convolution(x_pad, convKernelGPU, 'VALID', strides=kenelStrides)
    sess.run(tf.global_variables_initializer())
    [output_numpy] = sess.run([y], feed_dict={x: input_numpy})
    if (kernelDimension == 2):
        output_numpy = output_numpy[(0, :, :, 0)]
    if (kernelDimension == 3):
        output_numpy = output_numpy[(0, :, :, :, 0)]
    if (mode == 'numpy'):
        output = output_numpy
    elif (mode == 'sitk'):
        output = array_to_sitk(output_numpy, origin=input.GetOrigin(), spacing=tuple(((i * down_scale) for i in input.GetSpacing())), direction=input.GetDirection())
    return output
