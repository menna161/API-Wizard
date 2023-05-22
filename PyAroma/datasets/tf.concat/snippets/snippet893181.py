import tensorflow as tf
import numpy as np


def bending_energy(dvf, voxel_size=None):
    '\n    Bending Energy in TensorFlow:\n    :param dvf: with shape of (batch_size, dim0, dim1, dim2, 3)\n    :param voxel_size: physical voxel spacing in mm\n    :return: 3D bending energy\n    '
    if (voxel_size is None):
        voxel_size = [1, 1, 1]
    (indices_x, indices_y, indices_z) = tf.meshgrid(tf.range(0, dvf.get_shape()[1]), tf.range(0, dvf.get_shape()[2]), tf.range(0, dvf.get_shape()[3]), indexing='ij')
    dvf_tensor = tf.concat(([(tf.expand_dims(indices_x, (- 1)) * voxel_size[0]), (tf.expand_dims(indices_y, (- 1)) * voxel_size[1]), tf.expand_dims(indices_z, (- 1))] * voxel_size[2]), axis=(- 1))
    dvf_tensor = tf.expand_dims(dvf_tensor, axis=0)
    dvf_tensor = tf.tile(dvf_tensor, [tf.shape(dvf)[0], 1, 1, 1, 1])
    dvf_tensor = tf.to_float(dvf_tensor)
    dvf_tensor = tf.add(dvf_tensor, dvf)
    dvf_grad_dim0 = (diff(dvf_tensor, axis=1) / voxel_size[0])
    dvf_grad_dim1 = (diff(dvf_tensor, axis=2) / voxel_size[1])
    dvf_grad_dim2 = (diff(dvf_tensor, axis=3) / voxel_size[2])
    dvf_grad_dim0_dim0 = (diff(dvf_grad_dim0, axis=1) / voxel_size[0])
    dvf_grad_dim0_dim1 = (diff(dvf_grad_dim0, axis=2) / voxel_size[1])
    dvf_grad_dim0_dim2 = (diff(dvf_grad_dim0, axis=3) / voxel_size[2])
    dvf_grad_dim1_dim1 = (diff(dvf_grad_dim1, axis=2) / voxel_size[1])
    dvf_grad_dim1_dim2 = (diff(dvf_grad_dim1, axis=3) / voxel_size[2])
    dvf_grad_dim2_dim2 = (diff(dvf_grad_dim2, axis=3) / voxel_size[2])
    dvf_grad_dim0_dim0 = tf.pad(dvf_grad_dim0_dim0, ([0, 0], [0, 2], [0, 0], [0, 0], [0, 0]))
    dvf_grad_dim0_dim1 = tf.pad(dvf_grad_dim0_dim1, ([0, 0], [0, 1], [0, 1], [0, 0], [0, 0]))
    dvf_grad_dim0_dim2 = tf.pad(dvf_grad_dim0_dim2, ([0, 0], [0, 1], [0, 0], [0, 1], [0, 0]))
    dvf_grad_dim1_dim1 = tf.pad(dvf_grad_dim1_dim1, ([0, 0], [0, 0], [0, 2], [0, 0], [0, 0]))
    dvf_grad_dim1_dim2 = tf.pad(dvf_grad_dim1_dim2, ([0, 0], [0, 0], [0, 1], [0, 1], [0, 0]))
    dvf_grad_dim2_dim2 = tf.pad(dvf_grad_dim2_dim2, ([0, 0], [0, 0], [0, 0], [0, 2], [0, 0]))
    smoothness = tf.reduce_mean((((((tf.square(dvf_grad_dim0_dim0) + (2 * tf.square(dvf_grad_dim0_dim1))) + (2 * tf.square(dvf_grad_dim0_dim2))) + tf.square(dvf_grad_dim1_dim1)) + (2 * tf.square(dvf_grad_dim1_dim2))) + tf.square(dvf_grad_dim2_dim2)))
    return smoothness
