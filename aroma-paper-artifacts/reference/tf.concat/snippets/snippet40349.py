import os
import sys
from tf_sampling import farthest_point_sample, gather_point
from tf_grouping import query_ball_point, group_point, knn_point
from tf_interpolate import three_nn, three_interpolate
import tensorflow as tf
import numpy as np
import tf_util


def pointnet_sa_module_msg(xyz, points, npoint, radius_list, nsample_list, mlp_list, is_training, bn_decay, scope, bn=True, use_xyz=True, use_nchw=False):
    ' PointNet Set Abstraction (SA) module with Multi-Scale Grouping (MSG)\n        Input:\n            xyz: (batch_size, ndataset, 3) TF tensor\n            points: (batch_size, ndataset, channel) TF tensor\n            npoint: int32 -- #points sampled in farthest point sampling\n            radius: list of float32 -- search radius in local region\n            nsample: list of int32 -- how many points in each local region\n            mlp: list of list of int32 -- output size for MLP on each point\n            use_xyz: bool, if True concat XYZ with local point features, otherwise just use point features\n            use_nchw: bool, if True, use NCHW data format for conv2d, which is usually faster than NHWC format\n        Return:\n            new_xyz: (batch_size, npoint, 3) TF tensor\n            new_points: (batch_size, npoint, \\sum_k{mlp[k][-1]}) TF tensor\n    '
    data_format = ('NCHW' if use_nchw else 'NHWC')
    with tf.variable_scope(scope) as sc:
        new_xyz = gather_point(xyz, farthest_point_sample(npoint, xyz))
        new_points_list = []
        for i in range(len(radius_list)):
            radius = radius_list[i]
            nsample = nsample_list[i]
            (idx, pts_cnt) = query_ball_point(radius, nsample, xyz, new_xyz)
            grouped_xyz = group_point(xyz, idx)
            grouped_xyz -= tf.tile(tf.expand_dims(new_xyz, 2), [1, 1, nsample, 1])
            if (points is not None):
                grouped_points = group_point(points, idx)
                if use_xyz:
                    grouped_points = tf.concat([grouped_points, grouped_xyz], axis=(- 1))
            else:
                grouped_points = grouped_xyz
            if use_nchw:
                grouped_points = tf.transpose(grouped_points, [0, 3, 1, 2])
            for (j, num_out_channel) in enumerate(mlp_list[i]):
                grouped_points = tf_util.conv2d(grouped_points, num_out_channel, [1, 1], padding='VALID', stride=[1, 1], bn=bn, is_training=is_training, scope=('conv%d_%d' % (i, j)), bn_decay=bn_decay)
            if use_nchw:
                grouped_points = tf.transpose(grouped_points, [0, 2, 3, 1])
            new_points = tf.reduce_max(grouped_points, axis=[2])
            new_points_list.append(new_points)
        new_points_concat = tf.concat(new_points_list, axis=(- 1))
        return (new_xyz, new_points_concat)
