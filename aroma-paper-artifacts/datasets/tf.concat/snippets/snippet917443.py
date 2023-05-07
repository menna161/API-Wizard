from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import argparse
import json
import glob
import random
import collections
import math
import time
from lxml import etree
from random import shuffle


def _parse_function(filename):
    image_string = tf.read_file(filename)
    raw_input = tf.image.decode_image(image_string)
    raw_input = tf.image.convert_image_dtype(raw_input, dtype=tf.float32)
    assertion = tf.assert_equal(tf.shape(raw_input)[2], 3, message='image does not have 3 channels')
    with tf.control_dependencies([assertion]):
        raw_input = tf.identity(raw_input)
        raw_input.set_shape([None, None, 3])
        images = []
        input = raw_input
        if (a.mode == 'eval'):
            shape = tf.shape(input)
            black = tf.zeros([shape[0], (shape[1] * a.nbTargets), shape[2]], dtype=tf.float32)
            input = tf.concat([input, black], axis=1)
        width = tf.shape(input)[1]
        imageWidth = (width // (a.nbTargets + 1))
        for imageId in range((a.nbTargets + 1)):
            beginning = (imageId * imageWidth)
            end = ((imageId + 1) * imageWidth)
            images.append(input[(:, beginning:end, :)])
    if (a.which_direction == 'AtoB'):
        (inputs, targets) = [images[0], images[1:]]
    elif (a.which_direction == 'BtoA'):
        (inputs, targets) = [images[(- 1)], images[:(- 1)]]
    else:
        raise Exception('invalid direction')
    if a.correctGamma:
        inputs = tf.pow(inputs, 2.2)
    if a.useLog:
        inputs = logTensor(inputs)
    inputs = preprocess(inputs)
    targetsTmp = []
    for target in targets:
        targetsTmp.append(preprocess(target))
    targets = targetsTmp

    def transform(image):
        r = image
        r = tf.image.resize_images(r, [a.scale_size, a.scale_size], method=tf.image.ResizeMethod.AREA)
        return r
    with tf.name_scope('input_images'):
        input_images = transform(inputs)
    with tf.name_scope('target_images'):
        target_images = []
        for target in targets:
            target_images.append(transform(target))
    return (filename, input_images, target_images)
