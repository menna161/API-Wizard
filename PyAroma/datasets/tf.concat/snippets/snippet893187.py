import tensorflow as tf
import numpy as np
import functions.kernel.conv_kernel as conv_kernel


def upsampling3d(input_layer, scope, scale=2, interpolator='trilinear', padding_mode='SYMMETRIC', padding_constant=None, trainable=False, padding='valid', output_shape_3d=None):
    "\n    Key features:\n        - It can perform upsampling with any kernel. (nearest neighbor and trilinear are implemented)\n        - It has the padding_mode 'CONSTANT', 'REFLECT', 'SYMMETRIC'\n\n    Limitation\n        - It is limited to integer value of strides.\n        - 'valid' mode is implemented, to_do: 'same'\n\n    :param input_layer:\n    :param scope:\n    :param scale:\n    :param interpolator: 'trilinear': we use tf.nn.conv3d_transpose separately for each feature map.\n                         'nearest_neighbor': we use tf.keras.layers.UpSampling3D\n    :param padding_mode : 'CONSTANT', 'REFLECT', 'SYMMETRIC'\n    :param padding_constant\n    :param trainable\n    :param padding onle 'valid' mode is implemented\n    :param output_shape_3d: it can be defined in the trilinear mode. if not the default is scale*input_layer.size()+1\n\n    :return:\n    "
    if (padding.upper() != 'VALID'):
        print('upsampling3d is only implemented for "VALID" mode, TODO: "SAME"')
    pad_size = 1
    if (interpolator == 'nearest_neighbor'):
        with tf.variable_scope(scope):
            upsample_layer = tf.keras.layers.UpSampling3D(size=(2, 2, 2), data_format='channels_last', trainable=trainable)
            net = upsample_layer.__call__(tf.pad(input_layer, ([0, 0], [pad_size, pad_size], [pad_size, pad_size], [pad_size, pad_size], [0, 0]), mode=padding_mode, constant_values=padding_constant))
        return net[(:, (2 * pad_size):(((- 2) * pad_size) + 1), (2 * pad_size):(((- 2) * pad_size) + 1), (2 * pad_size):(((- 2) * pad_size) + 1), :)]
    if (interpolator == 'trilinear'):
        with tf.variable_scope(scope):
            conv_kernel_trilinear = conv_kernel.bilinear_up_kernel(dim=3)
            conv_kernel_trilinear = np.expand_dims(conv_kernel_trilinear, (- 1))
            conv_kernel_trilinear = np.expand_dims(conv_kernel_trilinear, (- 1))
            kernel_initializer = tf.constant_initializer(conv_kernel_trilinear)
            output_shape = input_layer[(:, :, :, :, 0, tf.newaxis)].get_shape().as_list()
            if (output_shape_3d is None):
                output_shape[1] = ((scale * (output_shape[1] + (2 * pad_size))) + 1)
                output_shape[2] = ((scale * (output_shape[2] + (2 * pad_size))) + 1)
                output_shape[3] = ((scale * (output_shape[3] + (2 * pad_size))) + 1)
            else:
                output_shape[1] = (output_shape_3d[0] + (4 * pad_size))
                output_shape[2] = (output_shape_3d[1] + (4 * pad_size))
                output_shape[3] = (output_shape_3d[2] + (4 * pad_size))
            output_shape_tf = tf.stack([tf.shape(input_layer)[0], output_shape[1], output_shape[2], output_shape[3], output_shape[4]])
            filter_transposed = tf.get_variable('kernel_transposed_3d', shape=(3, 3, 3, 1, 1), dtype=tf.float32, initializer=kernel_initializer, trainable=trainable)
            net = tf.concat([tf.nn.conv3d_transpose(tf.pad(input_layer, ([0, 0], [pad_size, pad_size], [pad_size, pad_size], [pad_size, pad_size], [0, 0]), mode=padding_mode, constant_values=padding_constant)[(:, :, :, :, i, tf.newaxis)], filter=filter_transposed, strides=(1, scale, scale, scale, 1), padding=padding.upper(), output_shape=output_shape_tf) for i in range(int(input_layer.get_shape()[4]))], axis=(- 1))
        return net[(:, (2 * pad_size):((- 2) * pad_size), (2 * pad_size):((- 2) * pad_size), (2 * pad_size):((- 2) * pad_size), :)]
