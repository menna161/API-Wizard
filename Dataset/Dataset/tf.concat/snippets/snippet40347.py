import os
import sys
from tf_sampling import farthest_point_sample, gather_point
from tf_grouping import query_ball_point, group_point, knn_point
from tf_interpolate import three_nn, three_interpolate
import tensorflow as tf
import numpy as np
import tf_util


def sample_and_group_all(xyz, points, use_xyz=True):
    '\n    Inputs:\n        xyz: (batch_size, ndataset, 3) TF tensor\n        points: (batch_size, ndataset, channel) TF tensor, if None will just use xyz as points\n        use_xyz: bool, if True concat XYZ with local point features, otherwise just use point features\n    Outputs:\n        new_xyz: (batch_size, 1, 3) as (0,0,0)\n        new_points: (batch_size, 1, ndataset, 3+channel) TF tensor\n    Note:\n        Equivalent to sample_and_group with npoint=1, radius=inf, use (0,0,0) as the centroid\n    '
    batch_size = xyz.get_shape()[0].value
    nsample = xyz.get_shape()[1].value
    new_xyz = tf.constant(np.tile(np.array([0, 0, 0]).reshape((1, 1, 3)), (batch_size, 1, 1)), dtype=tf.float32)
    idx = tf.constant(np.tile(np.array(range(nsample)).reshape((1, 1, nsample)), (batch_size, 1, 1)))
    grouped_xyz = tf.reshape(xyz, (batch_size, 1, nsample, 3))
    if (points is not None):
        if use_xyz:
            new_points = tf.concat([xyz, points], axis=2)
        else:
            new_points = points
        new_points = tf.expand_dims(new_points, 1)
    else:
        new_points = grouped_xyz
    return (new_xyz, new_points, idx, grouped_xyz)
