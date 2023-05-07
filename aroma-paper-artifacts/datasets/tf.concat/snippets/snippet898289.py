import cv2
import numpy as np
import tensorflow as tf
from logging import exception
import math
import scipy.stats as st
import os
import urllib
import scipy
from scipy import io
from enum import Enum
from easydict import EasyDict as edict


@staticmethod
def create_using_dotP(I_features, T_features, sigma=float(1.0), b=float(1.0)):
    cs_flow = CSFlow(sigma, b)
    with tf.name_scope('CS'):
        (T_features, I_features) = cs_flow.center_by_T(T_features, I_features)
        with tf.name_scope('TFeatures'):
            T_features = CSFlow.l2_normalize_channelwise(T_features)
        with tf.name_scope('IFeatures'):
            I_features = CSFlow.l2_normalize_channelwise(I_features)
            cosine_dist_l = []
            (N, _, _, _) = T_features.shape.as_list()
            for i in range(N):
                T_features_i = tf.expand_dims(T_features[(i, :, :, :)], 0)
                I_features_i = tf.expand_dims(I_features[(i, :, :, :)], 0)
                patches_i = cs_flow.patch_decomposition(T_features_i)
                cosine_dist_i = tf.nn.conv2d(I_features_i, patches_i, strides=[1, 1, 1, 1], padding='VALID', use_cudnn_on_gpu=True, name='cosine_dist')
                cosine_dist_l.append(cosine_dist_i)
            cs_flow.cosine_dist = tf.concat(cosine_dist_l, axis=0)
            cosine_dist_zero_to_one = ((- (cs_flow.cosine_dist - 1)) / 2)
            cs_flow.raw_distances = cosine_dist_zero_to_one
            relative_dist = cs_flow.calc_relative_distances()
            cs_flow.__calculate_CS(relative_dist)
            return cs_flow
