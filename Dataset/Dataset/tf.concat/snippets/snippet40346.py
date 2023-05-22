import os
import sys
from tf_sampling import farthest_point_sample, gather_point
from tf_grouping import query_ball_point, group_point, knn_point
from tf_interpolate import three_nn, three_interpolate
import tensorflow as tf
import numpy as np
import tf_util


def sample_and_group(npoint, radius, nsample, xyz, points, knn=False, use_xyz=True):
    '\n    Input:\n        npoint: int32\n        radius: float32\n        nsample: int32\n        xyz: (batch_size, ndataset, 3) TF tensor\n        points: (batch_size, ndataset, channel) TF tensor, if None will just use xyz as points\n        knn: bool, if True use kNN instead of radius search\n        use_xyz: bool, if True concat XYZ with local point features, otherwise just use point features\n    Output:\n        new_xyz: (batch_size, npoint, 3) TF tensor\n        new_points: (batch_size, npoint, nsample, 3+channel) TF tensor\n        idx: (batch_size, npoint, nsample) TF tensor, indices of local points as in ndataset points\n        grouped_xyz: (batch_size, npoint, nsample, 3) TF tensor, normalized point XYZs\n            (subtracted by seed point XYZ) in local regions\n    '
    new_xyz = gather_point(xyz, farthest_point_sample(npoint, xyz))
    if knn:
        (_, idx) = knn_point(nsample, xyz, new_xyz)
    else:
        (idx, pts_cnt) = query_ball_point(radius, nsample, xyz, new_xyz)
    grouped_xyz = group_point(xyz, idx)
    grouped_xyz -= tf.tile(tf.expand_dims(new_xyz, 2), [1, 1, nsample, 1])
    if (points is not None):
        grouped_points = group_point(points, idx)
        if use_xyz:
            new_points = tf.concat([grouped_xyz, grouped_points], axis=(- 1))
        else:
            new_points = grouped_points
    else:
        new_points = grouped_xyz
    return (new_xyz, new_points, idx, grouped_xyz)
