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


def parse_record_sup(raw_record, is_training, num_channels, dtype, use_random_crop=True, image_size=224, autoaugment_type=None, with_drawing_bbox=False, dct_method='', preprocessing_type='imagenet', return_logits=False, num_classes=1001, return_filename=False):
    features = parse_example_proto(raw_record, ret_dict=True)
    results = {}
    sup_image = preprocess_image(image_buffer=features['image/encoded'], is_training=is_training, num_channels=num_channels, dtype=dtype, use_random_crop=use_random_crop, image_size=image_size, autoaugment_type=autoaugment_type, dct_method=dct_method, preprocessing_type=preprocessing_type)
    results['image'] = sup_image
    if return_logits:
        label = tf.one_hot(tf.cast(features['image/class/label'], dtype=tf.int32), num_classes)
        logit = tf.reshape(features['image/logit'].values, [num_classes])
        label = tf.concat([label, logit], axis=0)
    else:
        label = tf.cast(features['image/class/label'], dtype=tf.int32)
    results['label'] = label
    return results
