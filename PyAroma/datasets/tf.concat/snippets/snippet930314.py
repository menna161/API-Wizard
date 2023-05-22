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


def parse_record(raw_record, is_training, num_channels, dtype, use_random_crop=True, image_size=224, autoaugment_type=None, with_drawing_bbox=False, dct_method='', preprocessing_type='imagenet', return_logits=False, num_classes=1001, return_filename=False):
    (image_buffer, label, bbox, filename, logit) = parse_example_proto(raw_record)
    if return_logits:
        assert (num_classes == 1001), 'Only support ImageNet for Knowledge Distillation yet'
        label = tf.one_hot(label, num_classes)
        logit = tf.reshape(logit, [num_classes])
        label = tf.concat([label, logit], axis=0)
    image = preprocess_image(image_buffer=image_buffer, is_training=is_training, num_channels=num_channels, dtype=dtype, use_random_crop=use_random_crop, image_size=image_size, bbox=bbox, autoaugment_type=autoaugment_type, with_drawing_bbox=with_drawing_bbox, dct_method=dct_method, preprocessing_type=preprocessing_type)
    if return_filename:
        return (image, label, filename)
    else:
        return (image, label)
