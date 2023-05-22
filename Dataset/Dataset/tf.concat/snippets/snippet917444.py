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


def load_examples(input_dir, shuffleValue):
    test_queue = tf.constant([' '])
    if ((input_dir is None) or (not os.path.exists(input_dir))):
        raise Exception('input_dir does not exist')
    flatPathList = []
    if (a.testMode == 'xml'):
        flatPathList = readInputXML(input_dir, shuffleValue)
    elif (a.testMode == 'folder'):
        flatPathList = readInputFolder(input_dir, shuffleValue)
    elif (a.testMode == 'image'):
        flatPathList = readInputImage(input_dir)
    if (len(flatPathList) == 0):
        raise Exception('input_dir contains no image files')
    with tf.name_scope('load_images'):
        filenamesTensor = tf.constant(flatPathList)
        dataset = tf.data.Dataset.from_tensor_slices(filenamesTensor)
        dataset = dataset.map(_parse_function, num_parallel_calls=1)
        dataset = dataset.repeat()
        batched_dataset = dataset.batch(a.batch_size)
        iterator = batched_dataset.make_initializable_iterator()
        (paths_batch, inputs_batch, targets_batch) = iterator.get_next()
        if (a.scale_size > CROP_SIZE):
            xyCropping = tf.random_uniform([2], 0, (a.scale_size - CROP_SIZE), dtype=tf.int32)
            inputs_batch = inputs_batch[(:, xyCropping[0]:(xyCropping[0] + CROP_SIZE), xyCropping[1]:(xyCropping[1] + CROP_SIZE), :)]
            targets_batch = targets_batch[(:, :, xyCropping[0]:(xyCropping[0] + CROP_SIZE), xyCropping[1]:(xyCropping[1] + CROP_SIZE), :)]
        print(('targets_batch_0 : ' + str(targets_batch.get_shape())))
        inputs_batch.set_shape([None, CROP_SIZE, CROP_SIZE, inputs_batch.get_shape()[(- 1)]])
        targets_batch.set_shape([None, a.nbTargets, CROP_SIZE, CROP_SIZE, targets_batch.get_shape()[(- 1)]])
    tf.summary.text('batch paths', paths_batch)
    steps_per_epoch = int(math.floor((len(flatPathList) / a.batch_size)))
    print(('steps per epoch : ' + str(steps_per_epoch)))
    print(('inputs_batch : ' + str(inputs_batch.get_shape())))
    print(('targets_batch : ' + str(targets_batch.get_shape())))
    targets_batch_concat = targets_batch[(:, 0)]
    print(('targets_batch_concat : ' + str(targets_batch_concat.get_shape())))
    for imageId in range(1, a.nbTargets):
        targets_batch_concat = tf.concat([targets_batch_concat, targets_batch[(:, imageId)]], axis=(- 1))
    targets_batch = targets_batch_concat
    print(('targets size : ' + str(targets_batch.get_shape())))
    return Examples(iterator=iterator, paths=paths_batch, inputs=inputs_batch, targets=targets_batch, count=len(flatPathList), steps_per_epoch=steps_per_epoch)
