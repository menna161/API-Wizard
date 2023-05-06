import os
import sys
from tf_sampling import farthest_point_sample, gather_point
from tf_grouping import query_ball_point, group_point, knn_point
from tf_interpolate import three_nn, three_interpolate
import tensorflow as tf
import numpy as np
import tf_util


def pointnet_fp_module(xyz1, xyz2, points1, points2, mlp, is_training, bn_decay, scope, bn=True):
    ' PointNet Feature Propogation (FP) Module\n        Input:                                                                                                      \n            xyz1: (batch_size, ndataset1, 3) TF tensor                                                              \n            xyz2: (batch_size, ndataset2, 3) TF tensor, sparser than xyz1                                           \n            points1: (batch_size, ndataset1, nchannel1) TF tensor                                                   \n            points2: (batch_size, ndataset2, nchannel2) TF tensor\n            mlp: list of int32 -- output size for MLP on each point                                                 \n        Return:\n            new_points: (batch_size, ndataset1, mlp[-1]) TF tensor\n    '
    with tf.variable_scope(scope) as sc:
        (dist, idx) = three_nn(xyz1, xyz2)
        dist = tf.maximum(dist, 1e-10)
        norm = tf.reduce_sum((1.0 / dist), axis=2, keep_dims=True)
        norm = tf.tile(norm, [1, 1, 3])
        weight = ((1.0 / dist) / norm)
        interpolated_points = three_interpolate(points2, idx, weight)
        if (points1 is not None):
            new_points1 = tf.concat(axis=2, values=[interpolated_points, points1])
        else:
            new_points1 = interpolated_points
        new_points1 = tf.expand_dims(new_points1, 2)
        for (i, num_out_channel) in enumerate(mlp):
            new_points1 = tf_util.conv2d(new_points1, num_out_channel, [1, 1], padding='VALID', stride=[1, 1], bn=bn, is_training=is_training, scope=('conv_%d' % i), bn_decay=bn_decay)
        new_points1 = tf.squeeze(new_points1, [2])
        return new_points1
