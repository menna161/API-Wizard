import tensorflow as tf
import math
import constants as const
import numpy as np
import imageio
from pydoc import locate
from tensorflow.python.ops import control_flow_ops


def augment(images, preprocess_func, resize=None, horizontal_flip=False, vertical_flip=False, rotate=0, noise_probability=0, color_aug_probability=0, crop_probability=0, crop_min_percent=0.6, crop_max_percent=1.0, mixup=0):
    max_offest = (const.max_frame_size - const.frame_width)
    rand = tf.random_uniform([2], minval=0, maxval=max_offest, dtype=tf.int32)
    height_offset = tf.cast(rand[0], dtype=tf.int32)
    width_offest = tf.cast(rand[1], dtype=tf.int32)
    images = tf.image.crop_to_bounding_box(images, height_offset, width_offest, const.frame_height, const.frame_width)
    if (preprocess_func == 'inception_v1'):
        print('Inception Format Augmentation')
        images = inception_preprocess(images)
    elif (preprocess_func == 'densenet'):
        print('DenseNet Format Augmentation')
        images = denseNet_preprocess(images)
    elif (preprocess_func == 'vgg'):
        print('VGG Format Augmentation')
        images = vgg_preprocess(images)
    with tf.name_scope('augmentation'):
        shp = tf.shape(images)
        (batch_size, height, width) = (shp[0], shp[1], shp[2])
        width = tf.cast(width, tf.float32)
        height = tf.cast(height, tf.float32)
        transforms = []
        identity = tf.constant([1, 0, 0, 0, 1, 0, 0, 0], dtype=tf.float32)
        if horizontal_flip:
            coin = tf.less(tf.random_uniform([batch_size], 0, 1.0), 0.5)
            flip_transform = tf.convert_to_tensor([(- 1.0), 0.0, width, 0.0, 1.0, 0.0, 0.0, 0.0], dtype=tf.float32)
            transforms.append(tf.where(coin, tf.tile(tf.expand_dims(flip_transform, 0), [batch_size, 1]), tf.tile(tf.expand_dims(identity, 0), [batch_size, 1])))
        if transforms:
            images = tf.contrib.image.transform(images, tf.contrib.image.compose_transforms(*transforms), interpolation='BILINEAR')

        def cshift(values):
            return tf.concat([values[((- 1):, ...)], values[(:(- 1), ...)]], 0)
    return images
