import os
import sys
import tensorflow as tf
import numpy as np
import tf_util
from pointnet_util import pointnet_sa_module, pointnet_fp_module


def get_model(point_cloud, is_training, num_class, bn_decay=None):
    ' Semantic segmentation PointNet, input is BxNx5, output Bxnum_class '
    batch_size = point_cloud.get_shape()[0].value
    num_point = point_cloud.get_shape()[1].value
    end_points = {}
    l0_xyz = tf.slice(point_cloud, [0, 0, 0], [(- 1), (- 1), 3])
    l0_points = tf.slice(point_cloud, [0, 0, 3], [(- 1), (- 1), 2])
    end_points['l0_xyz'] = l0_xyz
    (l1_xyz, l1_points, l1_indices) = pointnet_sa_module(l0_xyz, l0_points, npoint=1024, radius=0.1, nsample=32, mlp=[32, 32, 64], mlp2=None, group_all=False, is_training=is_training, bn_decay=bn_decay, scope='layer1')
    (l2_xyz, l2_points, l2_indices) = pointnet_sa_module(l1_xyz, l1_points, npoint=256, radius=0.2, nsample=32, mlp=[64, 64, 128], mlp2=None, group_all=False, is_training=is_training, bn_decay=bn_decay, scope='layer2')
    (l3_xyz, l3_points, l3_indices) = pointnet_sa_module(l2_xyz, l2_points, npoint=64, radius=0.4, nsample=32, mlp=[128, 128, 256], mlp2=None, group_all=False, is_training=is_training, bn_decay=bn_decay, scope='layer3')
    (l4_xyz, l4_points, l4_indices) = pointnet_sa_module(l3_xyz, l3_points, npoint=16, radius=0.8, nsample=32, mlp=[256, 256, 512], mlp2=None, group_all=False, is_training=is_training, bn_decay=bn_decay, scope='layer4')
    l3_points = pointnet_fp_module(l3_xyz, l4_xyz, l3_points, l4_points, [256, 256], is_training, bn_decay, scope='fa_layer1')
    l2_points = pointnet_fp_module(l2_xyz, l3_xyz, l2_points, l3_points, [256, 256], is_training, bn_decay, scope='fa_layer2')
    l1_points = pointnet_fp_module(l1_xyz, l2_xyz, l1_points, l2_points, [256, 128], is_training, bn_decay, scope='fa_layer3')
    l0_points = pointnet_fp_module(l0_xyz, l1_xyz, tf.concat([l0_xyz, l0_points], axis=(- 1)), l1_points, [128, 128, 128], is_training, bn_decay, scope='fa_layer4')
    net = tf_util.conv1d(l0_points, 128, 1, padding='VALID', bn=True, is_training=is_training, scope='fc1', bn_decay=bn_decay)
    end_points['feats'] = net
    net = tf_util.dropout(net, keep_prob=0.5, is_training=is_training, scope='dp1')
    net = tf_util.conv1d(net, num_class, 1, padding='VALID', activation_fn=None, scope='fc2')
    return (net, end_points)
