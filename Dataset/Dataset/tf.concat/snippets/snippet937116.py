from __future__ import print_function
import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim
import caffe


def stage_one(images, min_size, factor, thresold, scope):
    img_shape = tf.shape(images)
    (width, height) = (tf.to_float(img_shape[2]), tf.to_float(img_shape[1]))
    min_side = tf.to_float(tf.minimum(width, height))
    with tf.device('/cpu:0'):
        prob_arr = tf.TensorArray(tf.float32, size=0, clear_after_read=True, dynamic_size=True, element_shape=[None], infer_shape=False)
        reg_arr = tf.TensorArray(tf.float32, size=0, clear_after_read=True, dynamic_size=True, element_shape=[None, 4], infer_shape=False)
        box_arr = tf.TensorArray(tf.float32, size=0, clear_after_read=True, dynamic_size=True, element_shape=[None, 4], infer_shape=False)
    stride = 2
    cell_size = 12

    def body(i, scale, prob_arr, reg_arr, box_arr):
        width_scaled = tf.to_int32((width * scale))
        height_scaled = tf.to_int32((height * scale))
        img = tf.image.resize_bilinear(images, [height_scaled, width_scaled])
        (prob, reg) = det1(img, 'NHWC')
        with tf.device('/cpu:0'):
            (prob, reg) = (prob[0], reg[0])
            scope.reuse_variables()
            mask = (prob[(:, :, 1)] > thresold)
            indexes = tf.where(mask)
            bbox = [(tf.to_float(((indexes * stride) + 1)) / scale), (tf.to_float(((indexes * stride) + cell_size)) / scale)]
            bbox = tf.concat(bbox, axis=1)
            prob = tf.boolean_mask(prob[(:, :, 1)], mask)
            reg = tf.boolean_mask(reg, mask)
            idx = tf.image.non_max_suppression(bbox, prob, 1000, 0.5)
            bbox = tf.gather(bbox, idx)
            prob = tf.gather(prob, idx)
            reg = tf.gather(reg, idx)
            prob_arr = prob_arr.write(i, prob)
            reg_arr = reg_arr.write(i, reg)
            box_arr = box_arr.write(i, bbox)
        return ((i + 1), (scale * factor), prob_arr, reg_arr, box_arr)
    (_, _, prob_arr, reg_arr, box_arr) = tf.while_loop((lambda i, scale, prob_arr, reg_arr, box_arr: ((min_side * scale) > 12.0)), body, [0, (12.0 / min_size), prob_arr, reg_arr, box_arr], back_prop=False)
    (prob, reg, bbox) = (prob_arr.concat(), reg_arr.concat(), box_arr.concat())
    idx = tf.image.non_max_suppression(bbox, prob, 1000, 0.7)
    (bbox, prob, reg) = (tf.gather(bbox, idx), tf.gather(prob, idx), tf.gather(reg, idx))
    bbox = regress_box(bbox, reg)
    bbox = square_box(bbox)
    return (bbox, prob)
