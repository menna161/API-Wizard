from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import six
import re
import tensorflow as tf
from preprocessing import imagenet_preprocessing
from preprocessing import inception_preprocessing
from preprocessing import reid_preprocessing


def parse_example_proto(example_serialized, ret_dict=False):
    feature_map = {'image/encoded': tf.FixedLenFeature([], dtype=tf.string, default_value=''), 'image/filename': tf.FixedLenFeature([], dtype=tf.string, default_value=''), 'image/class/label': tf.FixedLenFeature([], dtype=tf.int64, default_value=(- 1)), 'image/logit': tf.VarLenFeature(dtype=tf.float32)}
    sparse_float32 = tf.VarLenFeature(dtype=tf.float32)
    feature_map.update({k: sparse_float32 for k in ['image/object/bbox/xmin', 'image/object/bbox/ymin', 'image/object/bbox/xmax', 'image/object/bbox/ymax']})
    features = tf.parse_single_example(example_serialized, feature_map)
    label = tf.cast(features['image/class/label'], dtype=tf.int32)
    xmin = tf.expand_dims(features['image/object/bbox/xmin'].values, 0)
    ymin = tf.expand_dims(features['image/object/bbox/ymin'].values, 0)
    xmax = tf.expand_dims(features['image/object/bbox/xmax'].values, 0)
    ymax = tf.expand_dims(features['image/object/bbox/ymax'].values, 0)
    bbox = tf.concat([ymin, xmin, ymax, xmax], 0)
    bbox = tf.expand_dims(bbox, 0)
    bbox = tf.transpose(bbox, [0, 2, 1])
    if ret_dict:
        return features
    else:
        return (features['image/encoded'], label, bbox, features['image/filename'], features['image/logit'].values)
