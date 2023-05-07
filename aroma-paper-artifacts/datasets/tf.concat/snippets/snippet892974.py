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


def upsampler_gpu_old(input, up_scale, default_pixel_value=0, dvf_output_size=None):
    '\n    Upsampling wiht GPU by an integer scale\n    :param input: can be a 3D numpy array or sitk image\n    :param up_scale: an integer value!\n    :param default_pixel_value:\n    :return: output: can be a numpy array or sitk image based on the input\n    '
    import tensorflow as tf
    if isinstance(input, sitk.Image):
        input_numpy = sitk.GetArrayFromImage(input)
        mode = 'sitk'
    else:
        input_numpy = input
        mode = 'numpy'
    if (not isinstance(up_scale, int)):
        raise ValueError(('upscale should be integer. now it is {} with type of '.format(str(up_scale)) + type(up_scale)))
    tf.reset_default_graph()
    sess = tf.Session()
    dvf_tf = tf.placeholder(tf.float32, shape=[1, None, None, None, 3], name='DVF_Input')
    DVF_outSize = tf.placeholder(tf.int32, shape=[3], name='DVF_outSize')
    convKernelBiLinear = conv_kernel.bilinear_up_kernel(dim=3)
    convKernelBiLinear = np.expand_dims(convKernelBiLinear, (- 1))
    convKernelBiLinear = np.expand_dims(convKernelBiLinear, (- 1))
    convKernelBiLinear = tf.constant(convKernelBiLinear)
    myDVF0 = tf.expand_dims(dvf_tf[(:, :, :, :, 0)], (- 1))
    myDVF1 = tf.expand_dims(dvf_tf[(:, :, :, :, 1)], (- 1))
    myDVF2 = tf.expand_dims(dvf_tf[(:, :, :, :, 2)], (- 1))
    upSampledDVF0 = tf.nn.conv3d_transpose(myDVF0, convKernelBiLinear, output_shape=(1, DVF_outSize[0], DVF_outSize[1], DVF_outSize[2], 1), strides=(1, up_scale, up_scale, up_scale, 1))
    upSampledDVF1 = tf.nn.conv3d_transpose(myDVF1, convKernelBiLinear, output_shape=(1, DVF_outSize[0], DVF_outSize[1], DVF_outSize[2], 1), strides=(1, up_scale, up_scale, up_scale, 1))
    upSampledDVF2 = tf.nn.conv3d_transpose(myDVF2, convKernelBiLinear, output_shape=(1, DVF_outSize[0], DVF_outSize[1], DVF_outSize[2], 1), strides=(1, up_scale, up_scale, up_scale, 1))
    upSampledDVF = tf.squeeze(tf.concat([upSampledDVF0, upSampledDVF1, upSampledDVF2], (- 1)), axis=0)
    sess.run(tf.global_variables_initializer())
    [output_numpy] = sess.run([upSampledDVF], feed_dict={dvf_tf: np.expand_dims(input_numpy, axis=0), DVF_outSize: dvf_output_size})
    if (mode == 'numpy'):
        output = output_numpy
    elif (mode == 'sitk'):
        output = array_to_sitk(output_numpy.astype(np.float64), origin=input.GetOrigin(), spacing=tuple(((i / up_scale) for i in input.GetSpacing())), direction=input.GetDirection(), is_vector=True)
    return output
